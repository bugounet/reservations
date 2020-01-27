# Reservations
This software allows its users to book resources for a given time.

## installation
This software has been developed under python3.6. To install run the 
following commands:

```shell
virtualenv -p python3.6 env
source env/bin/activate
pip install -r requirements.txt
# Using debug mode since this doesn't come with staticfiles hosting.
export DEBUG=true 
python manage.py migrate
# load admins, basic-users and testing assets from dumped data
python manage.py loaddata fixtures/*.json
python manage.py runserver
```

## Features
- Admin access to create resources
- User can create a "booking"
- User can view his past, present and future bookings 
- User can cancel one of his upcoming/current bookings

## Database
The project's database is simple and relies on three models:

- Users
- Resources
- Bookings (binding users and resources)

The chosen database is sqlite for installation simplicity but if this had to
run under production constraints I would certainly reconsider this choice.

The following diagram sums thigs up:
![database-diagram](docs/database-modeling.png)
 
## Foreseen limitations

- This project will not scale indefinetly since the concurrence algorithm 
implemented is not the most efficient one.
- This app could benefit from a better auth system than the current django 
basic auth
- Users are restricted by limiting the queryset to their scope which means 
you'll get a 404 (resource doen't exist) when trying to deal with a booking 
that isn't yours. This would probably be better returning a 401/403 error code.
- I chose not to host my copy of boostrap css lib. This means without 
internet the page will look awful.
- Resources location hasn't been defined in BRs. I went with a simple 
CharField. In case the location has to be something really specific, there 
will certainly be a better data structure candidate for this implementation
- Same issue applies to resources "Type" field: it's a free varchar input. 
Could be modified to a restricted set of values if it was asked so.
- The database contains "cancelled" bookings which is nice to be able to 
"undo" something however, the DB could be cleaned after a given amount of 
time to ensure it still contains useful alive data.
- Also we could move dead data (past bookings and cancelled bookings) into 
separate tables to keep the "active bookings" table smaller (and therefore 
faster)
- Django's Basic FKs implementation has an existence check. If I used pgSQL 
instead I could pimp those to here again rely on DB's existing checks and 
avoid double work
- Security: This app is local only. Once in prod, make sure to drop http

## Using the app
You can connect the app admin interface using the following credentials:

| username | password    |
|----------|-------------|
| admin    | MyAdmin123! |
| alice    | MyAlice123! |
| bob    | MyBob123! |
