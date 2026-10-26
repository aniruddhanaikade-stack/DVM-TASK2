# GoOut (DVM Round 2 - Basic Track)

Django + PostgreSQL + uv.

## Run it

1. Make a postgres database called `dvm`:

   ```
   createdb dvm
   ```

   (default login is user `postgres`, password `postgres` on localhost. Change with env variables
   `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`)

2. Run these:

   ```
   uv sync
   uv run manage.py makemigrations main
   uv run manage.py migrate
   uv run manage.py seed
   uv run manage.py createsuperuser
   uv run manage.py runserver
   ```

3. Open http://127.0.0.1:8000

## What it does

- Sign up / login
- Add money with a fake payment form
- Slot events (turf, court) and ticket events (movie, concert)
- Book a slot / tickets (capacity is checked, money is cut from wallet)
- My bookings, Active tickets, Transaction history with timestamps
- Add more events in `/admin`
