# Python/Django Developer Test

This is my solution to the Python/Django Developer Test.

## Setup project

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

## Run development server

```bash
./manage.py runserver
```

## Setup initial user

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