import psycopg2
from datetime import datetime


# 1. What are the most popular three articles of all time? Which articles have been accessed the most?
# Present this information as a sorted list with the most popular article at the top.
def get_mp_articles(n=3, dbname="news"):
  db = psycopg2.connect(database=dbname)
  c = db.cursor()
  c.execute ("""
    select 
      articles.title, count(log.path) as num 
    from articles 
      join log on ('/article/' || articles.slug) = log.path  
    group by articles.slug, articles.title
    order by num desc limit 3;
  """)
  mp_articles = c.fetchall()  
  db.close()
  result = []

  for row in mp_articles:
    result.append( '"{}" -- {} views'.format(row[0], str(row[1])) )

  return result 


# 2. Who are the most popular article authors of all time? 
# That is, when you sum up all of the articles each author has written, which authors get the most page views?
# Present this as a sorted list with the most popular author at the top.
def get_mp_authors(dbname="news"):
  db = psycopg2.connect(database=dbname)
  c = db.cursor()
  c.execute ("""
    select 
      authors.name, count(log.path) as num 
    from authors 
      left join articles on authors.id = articles.author
      join log on ('/article/' || articles.slug) = log.path
    group by authors.name
    order by num desc;
  """)
  mp_authors = c.fetchall()  
  db.close()
  result = []

  for row in mp_authors:
    result.append('{} -- {} views'.format(row[0], str(row[1])) )

  return result
 
 

# 3. On which days did more than 1% of requests lead to errors? 
# The log table includes a column status that indicates the HTTP status code that the news site sent to 
# the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)
def get_error_rate(dbname="news"):
  db = psycopg2.connect(database=dbname)
  c = db.cursor()
  c.execute ("""
    create view count_by_date as 
      select 
        time::date as date,
        count(*) as log_count
      from log 
      group by date;
    
    create view error_by_date as
      select 
        time::date as date,
        count(*) as error_count 
      from log 
      where status like '4%' or status like '5%' 
      group by date;
  
    create view error_rate_by_date as
      select 
        c.date, 
        1.0 * error_count/log_count as error_rate 
      from count_by_date as c join error_by_date as e on c.date = e.date;

    select 
      date,
      error_rate
    from error_rate_by_date
    where error_rate > 0.01;
  """)
  error_rate = c.fetchall()  
  db.close()
  result = []

  for row in error_rate:
    ds = datetime.strftime(row[0], "%b %d, %Y")
    result.append('{} -- {}% errors'.format(ds, str(round(row[1]*100,1)) ))
    
  return result


if __name__ == '__main__':
  mp_articles = get_mp_articles()
  print "1. What are the most popular three articles of all time?\n"
  for line in mp_articles:
    print line
  
  print "\n"
  
  mp_authors = get_mp_authors()
  print "2. Who are the most popular article authors of all time?\n"
  for line in mp_authors:
    print line

  error_rate = get_error_rate()
  print "\n"

  print "3. On which days did more than 1% of requests lead to errors? \n"
  for line in error_rate:
    print line
 