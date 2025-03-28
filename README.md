# Python/Django Developer Test

This is my solution to the Python/Django Developer Test.

## Setup project (Docker)

The fastest way to start the project is to use Docker. A Dockerfile and compose file is provided.

### Run the services

```bash
docker-compose up --build --force-recreate
```

Exposed ports:
- `8000` : web service
- `5432` : DB service

### Database migration

Initialize the database by connecting to a shell session on the running web container.

```bash
docker exec -it web_service bash
```

Then from the terminal session, execute Django's migrate.

```bash
./manage.py migrate
```

### Setup user

Create the initial user while in the same terminal session. 

Jump to the [Setup initial user](#setup-initial-user) section to setup

## Setup project (local install)

### Requirements

The following versions were used to complete this test:

- Python 3.12
- PostgreSQL 17

### Environment variables
```bash
cp .env.example .env
```

Update variables in `.env` accordingly.

### Virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements/local.txt
```

### Database migration

Initialize the database. Make sure the database details are correctly set in `.env`.

```bash
./manage.py migrate
```

## Setup initial user
<a name="setup-initial-user"></a>

```bash
./manage.py createsuperuser
```

Follow the prompts to create the first user.

Since the API is only accessible to users with the admin role, we need to manually set the first user's role to admin.

Let's use the Django shell to update the role.

```python
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(pk=1)
u.role = User.ROLE_ADMIN
u.save()
```

## Run development server

```bash
./manage.py runserver
```

## API Details

The following are the API available. A Postman collection is also added in the repo to
interact with the API in Postman. See `Rides.postman_collection.json`.

### Get token

A `Token` is expected to be able to get data over the API.

```
GET /api-token-auth/
Content-Type: application/x-www-form-urlencoded
```

Request body:
```
username={{username}}&password={{password}}
```

Replace `username/password` with a user with `admin` role.

Example response:

```json
{
    "token": "84cdd6809c5237b38c6320eb4902e7d7473ed9b4"
}
```

Use the token value in the succeeding requests.


### Rides list

Retrieves a list of rides.

```
GET /api/rides/
Authorization: Token {{token}}
```

Available query params:

- `start_latitude` : Input latitude to query rides based on distance.
- `start_longitude` : Input longitude to query rides based on distance.
- `status` : To filter by Ride status.
- `rider_email` : To filter by Rider email.
- `ordering`: To order based on column. Available columns for sorting, `pickup_time` and `distance`. 
Prefix with `-` (e.g. `-distance`) to sort in reverse order. Both may be provided separated by comma `,`.

### Create Ride

Create a ride given a payload.

```
POST /api/rides/
Content-Type: application/json
Authorization: Token {{token}}
```

Example request payload:

```json
{
    "id_rider": 1,
    "id_driver": 2,
    "status": "new",
    "pickup_latitude": "14.5998083",
    "pickup_longitude": "120.9628558",
    "dropoff_latitude": "14.5998083",
    "dropoff_longitude": "120.9628558",
    "pickup_time": "2025-05-22 08:00:00"
}
```

### Update Ride
```
PUT /api/rides/{{id_ride}}
Content-Type: application/json
Authorization: Token {{token}}
```

Replace `{{id_ride}}` with the Ride ID to update.

Example request payload (partial update):

```
{
    "id_rider": 1,
    "id_driver": 2,
    "status": "en-route",
    "pickup_time": "2025-03-29 05:02:28+08"
}
```

The above fields are the minimum required to be able to update a Ride. Provide all fields (see create payload)
to do a full update. 

### Delete Ride

To delete a ride.

```
DELETE /api/rides/{{id_ride}}
Content-Type: application/json
Authorization: Token {{token}}
```

Replace `{{id_ride}}` with the Ride ID to delete.

## Bonus - SQL

**Problem:** Provide a raw SQL statement which returns the count of Trips that took more than 1 hour from Pickup to Dropoff. 
This should be grouped by month and driver. 

**Solution:**

I'm utilizing a subquery to calculate the duration. If the duration is more than 1 hour,
the `more_1hour` column will be `true`.

To get the duration I used the `AGE` function to get the difference between two timestamps. The usage
of MAX and MIN is to aggregate the results to one row. Should there be any duplicated 'Status changed dropoff' or
'Status changed pickup', MAX and MIN will get a single row.

The outer query is responsible to actually count the number of trips with 1 hour.

```sql
SELECT
	MONTH,
	driver,
	COUNT(*) AS "Count of Trips > 1 hr"
FROM
	(
		SELECT
			r.id_ride,
			TO_CHAR(created_at, 'YYYY-MM') AS "month",
			u.first_name || ' ' || u.last_name AS driver,
			AGE(
				MAX(
					CASE
						WHEN description = 'Status changed to dropoff' THEN re.created_at
						ELSE NULL
					END
				),
				MIN(
					CASE
						WHEN description = 'Status changed to pickup' THEN re.created_at
						ELSE NULL
					END
				)
			) > INTERVAL '1 hour' AS more_1hour
		FROM
			core_rideevent re
			JOIN core_ride r ON r.id_ride = re.id_ride_id
			JOIN core_user u ON u.id_user = r.id_driver_id
		WHERE
			re.description IN ('Status changed to pickup', 'Status changed to dropoff')
		GROUP BY
			r.id_ride,
			MONTH,
			driver
	)
where more_1hour = true
GROUP BY
	MONTH,
	driver;
```

**Optimization points**

- Since the Ride Events table is expected to be very large. It is worth considering indexing the `description`
column to make retrieval of the target records faster.
- Adding a date range on Ride Events would also be beneficial to the speed of the query.