#!/usr/bin/env python3
"""internal reporting tool."""
import psycopg2


# Qurey 1
# Popular three articles of all time
query1 = ("SELECT articles.title, count(*) as num "
          "FROM articles JOIN log on log.path = CONCAT('/article/', slug) "
          "WHERE path != '/' and status = '200 OK' "
          "GROUP BY articles.title ORDER BY num desc limit 3;")

# Query 2
# Popular article authors of all time
query2 = ("SELECT authors.name, count(*) as num "
          "FROM authors JOIN articles on authors.id = articles.author "
          "JOIN log on log.path = CONCAT('/article/', slug) "
          "GROUP BY authors.name ORDER BY num desc;")


# Query 3
# Requests leading to more than 1% error
view1 = ("CREATE OR REPLACE VIEW request as "
         "SELECT date(time) as date, count(*) as num "
         "FROM log GROUP BY date;")

view2 = ("CREATE OR REPLACE VIEW errorrequest as "
         "SELECT date(time) as date, count(*) as num "
         "FROM log WHERE status != '200 OK' "
         "GROUP BY date ORDER BY date;")

view3 = ("CREATE OR REPLACE VIEW pererror as SELECT request.date, "
         "(100 * errorrequest.num)/request.num::float as percentage "
         "FROM request JOIN errorrequest on "
         "request.date = errorrequest.date;")

query3 = "SELECT date, percentage FROM pererror WHERE percentage > 1;"


def log(query):
    """Connect to PostgreSQL database and return database connection."""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(query)
    rows = c.fetchall()

    for row in rows:
        print("  {} - {} views".format(row[0], row[1]))
    print("-" * 70)
    
    db.close()


def err():
    """connect to PostgreDQL database for views."""
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()
    cursor.execute(view1)
    cursor.execute(view2)
    cursor.execute(view3)
    cursor.execute(query3)
    results = cursor.fetchall()

    for result in results:
        print("  {} - {} %error".format(result[0], result[1]))
    print("-" * 70)
    conn.close()


print("Most popular articles:")
log(query1)

print("Most popular authors:")
log(query2)

print("Days with more than 1% errors:")
err()
