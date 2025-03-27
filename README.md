## Requirements

## Setup project

### Setup environment variables
```bash
cp .env.example .env
```

Update variables in `.env` accordingly.

### Setup virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements/local.txt
```

## Run development server

```
./manage.py runserver
```

## Setup initial user

```bash
./manage.py createsuperuser
```

## Bonus - SQL answer

```sql
SELECT
	MONTH,
	driver,
	count(*) AS "Count of Trips > 1 hr"
FROM
	(
		SELECT
			r.id_ride,
			TO_CHAR(created_at, 'YYYY-MM') AS "month",
			u.first_name || ' ' || u.last_name AS driver,
			age (
				max(
					CASE
						WHEN description = 'Status changed to dropoff' THEN re.created_at
						ELSE NULL
					END
				),
				min(
					CASE
						WHEN description = 'Status changed to pickup' THEN re.created_at
						ELSE NULL
					END
				)
			)  > interval '1 hour' as more_1hour
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