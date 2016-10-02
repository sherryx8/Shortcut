"""
    Connect to a vertica database and run queries
"""
from flask import g
<<<<<<< HEAD
import vertica_python

import re
import os

DB_NAME = 'test'
DB_USER = 'dbadmin'
DB_PASSWORD = ''
DB_HOST = 'ec2-52-90-190-153.compute-1.amazonaws.com'

conn_info = {'host': DB_HOST,
             'port': 5433,
             'user': 'dbadmin',
             'password': '',
             'database': 'test',
             # 10 minutes timeout on queries
             'read_timeout': 600,
             # default throw error on invalid UTF-8 results
             'unicode_error': 'strict',
             # SSL is disabled by default
             'ssl': False}

def make_dicts(cursor, row):
    """
        Turn query results into dictionaries keyed by column name
    """
    colnames = [col[0] for col in cursor.description]

    fmtrow = {}
    for idx, value in enumerate(row):
      fmtrow[colnames[idx]] = value

    return fmtrow
=======
from cli import *
>>>>>>> origin/master

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_db()
    return db

def select_one():
    """
        Select 1 from database
    """
    sql = "SELECT 1"
    results = query_db(sql, db = get_db(), pretty_print=True)
    return results


def select_feedback():
	sql = "SELECT * FROM feedback"
	results = query_db(sql)
	return results
	
def select_location(location):
	sql = "SELECT * FROM feedback WHERE loc = '" + location + "';"
	results = query_db(sql)
	return results
	
def select_average(location):
	sql = "SELECT AVG(stars) FROM feedback WHERE loc = '" + location + "';"
	results = query_db(sql)
	return results
	
def select_comments(location):
	sql = "SELECT * FROM feedback ORDER BY num DESC;"
	sqll = "SELECT com FROM feedback WHERE loc = '" + location + "' LIMIT 5;"
	query_db(sql)
	results = query_db(sqll)
	return results
	
def select_listlocations():
	sql = "SELECT DISTINCT loc FROM feedback;"
	results = query_db(sql)
	return results
	
def write_data(l, c, s):
	#preprocessing
	sql = "SELECT * FROM feedback ORDER BY num DESC;"
	sqll = "SELECT num FROM feedback LIMIT 1;"
	query_db(sql)
	n = query_db(sqll)[0][u'num']
	print n
	sqlll = "INSERT INTO feedback (stars, loc, com, num) VALUES ('" + s + "', '" + l + "', '" + c + "', '" + str(n+1) + "');"	
	query_db(sqlll)
	query_db("commit;")
	print "done db"
	
	# @app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
