#!/usr/local/bin/python3
import pandas as pd
import numpy as np
import re
import json
import sys
import csv
import datetime
import argparse 
import struct
import pymysql 
import secrets
import guid
import unicodedata
import scrmapi
from threading import Thread

#Color formating
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#Threading class
#Not used here - but I might need it at some point
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return
#Command line options
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
        description=('''\
./build_relationships.py -m props_Spaces -t props_spaces -p props_properties_id_c -c id
  Examples:
  build_relationships.py -m props_Listings -t props_listings -p id -c props_properties_id_c -r props_Properties
  build_relationships.py -m Contacts -t documents -c id -p parent_id -r Documents
        '''))
parser.add_argument('-m', '--module', required=True,
                    help='SQL table name')
parser.add_argument('-r', '--relations', required=True,
                    help='Relationship Name')
parser.add_argument('-t', '--table', required=True,
                    help='SQL table name')
parser.add_argument('-p', '--parent', required=True,
                    help='A column name in DB')
parser.add_argument('-c', '--child', required=True,
                    help='B column name in DB')
parser.add_argument('-d', '--debug', required=False, action='store_true',
                    help='Debug - No changes to CRM or DB')
args = parser.parse_args()
module = (args.module) 
table = (args.table) 
parent = (args.parent) 
child = (args.child)
debug = (args.debug)
relation = (args.relations)

now = datetime.datetime.now()

if debug is True:
    print(bcolors.WARNING + str(now) + " - Supplied attributes: " + parent + " " + child + " " + "debug: " + str(debug) + bcolors.ENDC)
    print("\n")

def mysql_search(table, column, value):
    table = table.lower()
    db = pymysql.connect('localhost',secrets.mysqluser,secrets.mysqlpass,secrets.db)
    cur = db.cursor()
    try:
        sql = ("SELECT {1}, {2}, deleted FROM {0} INNER JOIN {0}_cstm ON id=id_c WHERE deleted='0'".format(table, parent, child))
        cur.execute(sql)
    except:
        sql = ("SELECT {1}, {2}, deleted FROM {0} WHERE deleted='0'".format(table, parent, child))
        cur.execute(sql)

    if debug is True:
        print("sfid: " + str(value))
        print(table, column, value)
        print(sql)
    rows = cur.fetchall()
    db.commit()
    db.close()
    return rows 

def entry_check(table, value):
    db = pymysql.connect('localhost',secrets.mysqluser,secrets.mysqlpass,secrets.db)
    table = table.lower()
    cur = db.cursor()
    if debug is True:
        print("Checking DV for sfid: " + str(value))
    try:
        sql = ("SELECT id, salesforceid_c, deleted FROM {0} INNER JOIN {0}_cstm ON id=id_c WHERE deleted='0' and id = '{1}'".format(table, value))
        cur.execute(sql)
    except:
        sql = ("SELECT id, salesforceid_c, deleted FROM {0} WHERE deleted='0' and id = '{1}'".format(table, value))
        cur.execute(sql)

    if debug is True:
        print(table, value)
        print(sql)
    cur.execute(sql)
    row_count = cur.rowcount
    print ("number of affected rows: {}".format(row_count))
    if row_count == 0:
        result = False
    elif row_count == 1:
        result = True 
    db.commit()
    db.close()
    return result 

results = mysql_search(table, parent, child)
for result in results:
    parent, child, deleted = (result)
    found = entry_check(module.lower(), parent)
    if found is True and child is not None:
        if parent is not None and parent is not "" and child is not '':
            data = {
                    "data": {
                        "type": "{0}".format(relation),
                        "id": "{0}".format(child),
                        }
                    }
            print(found)
            print("scrmapi.add_relationship("+module+", "+parent+", "+str(data)+")")
            print(str(data) + "\n\n")
            if debug is False:
                scrmapi.add_relationship(module, parent, data)
