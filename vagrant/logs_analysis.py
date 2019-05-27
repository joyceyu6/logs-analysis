#!/usr/bin/env python

import psycopg2


def get_mp_articles(n=3, dbname="news"):
    """
    Return rankings of articles based on view counts.

    Args:
    n (optional int) - sets the number of articles to return. Defaults to 3.

    dbname(optional string) - sets the name of the database to connect to.
                              Default to "news"

    Returns:
    A list of strings. Each string contains:
      - the title of the article.
      - the number of views for the article

    The list is sorted by number of views in descending order.
    """

    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute("""
      select
        title, views
      from articles
      inner join (
        select path, count(path) as views
        from log
        group by log.path
      ) as log
      on ('/article/' || articles.slug) = log.path
      order by views desc
      limit 3;
    """)
    mp_articles = c.fetchall()
    db.close()
    result = []

    for row in mp_articles:
        result.append('"{}" -- {} views'.format(row[0], str(row[1])))

    return result


def get_mp_authors(dbname="news"):
    """
    Return rankings of authors based on view counts.

    Args:
    dbname(optional string) - sets the name of the database to connect to.
                              Default to "news"

    Returns:
    A list of strings. Each string contains:
      - the name of the author.
      - the number of views for the author

    The list is sorted by number of views in descending order.
    """
    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute("""
      select
        name, sum(views) as total_views
      from authors
        left join articles on authors.id = articles.author
        inner join (
          select path, count(path) as views
          from log
          group by log.path
        ) as log on ('/article/' || articles.slug) = log.path
      group by authors.name
      order by total_views desc;
    """)
    mp_authors = c.fetchall()
    db.close()
    result = []

    for row in mp_authors:
        result.append('{} -- {} views'.format(row[0], str(row[1])))

    return result


def get_error_rate(dbname="news"):
    """
    Return dates on which the error rate of accessing articles is bigger
    than 1%

    Args:
    dbname(optional string) - sets the name of the database to connect to.
                              Default to "news"

    Returns:
    A list of strings. Each string contains:
      - the date
      - the error rate

    The list is sorted by number of views in descending order.
    """
    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute("""
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
        result.append('{:%B %d, %Y} -- {:.1%} errors'.format(row[0], row[1]))

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
