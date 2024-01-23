# Courier Service

## Review
Simple Courier Service API is a web application for courier delivery management. The service is developed using FastAPI and includes basic functionality for order tracking and courier management.

## Functionality
1. **Order creating:** Create new orders, specifying order name and district name.
2. **Order info:** Check order information, specifying order id.
3. **Complete order:** Mark an order as completed, specifying order id.
4. **Add courier:** Add new courier, specifying courier name and working districts.
5. **Courier info:** Check information about courier, specifying courier id.
6. **List of couriers:** Check a list of couriers

## Technology
**FastAPI:** Using for creating API for web-applications. Base of this service.
**SQLAlchemy:** Using for working with database using ORM.
**PostgreSQL:** Using as database for this project.
**Docker and Docker Compose:** Using for containerization and working on server or not server.

## Requirements
1. Git
2. Docker and Docker Compose

## Install
~~~
git clone https://github.com/Vitality2012/courier_service.git
cd courier_service
docker compose build
docker compose up -d
~~~

## Tests
~~~
docker exec courier_service pytest
~~~

## Work
To work with courier service API you can go to http://localhost:8000/docs or 127.0.0.1:8000/docs.
If you want to use any app for working with API, just use http://localhost:8000 or 127.0.0.1:8000

## Thanks
This is my first project that take a lot of time. So thanks to everybody for your attention. 
