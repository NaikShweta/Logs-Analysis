# Log Analysis Project

### Project Overview
This project database contains newspaper articles, web server log for the site. The project is to build internal reporting tool by using information from the database 

### Pre-requisites:
* Python3
* Vagrant
* Virtual Box

### Setup:
1. Install Python3, Vagrant and Virtual Box.
2. Clone repository from udacity project3

### To Run:
1. Launch vagrant by vagrant up
2. Log in with winpty vagrant ssh 
3. Set up database by psql -d news -f newsdata.sql

The database has three tables:
* Authors
* Articles
* Log

To execute the program run log-analysis.py

Three view statements are included in this project
* view 1: CREATE OR REPLACE VIEW request as SELECT date(time) as date, count(*) as num FROM log GROUP BY date;
* view 2: CREATE OR REPLACE VIEW errorrequest as SELECT date(time) as date, count(*) as num FROM log WHERE status != '200 OK' GROUP BY date ORDER BY date;
* view 3: CREATE OR REPLACE VIEW pererror as SELECT request.date, (100 * errorrequest.num)/request.num::float as percentage FROM request JOIN errorrequest on request.date = errorrequest.date;


