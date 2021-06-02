from tinydb import TinyDB, where
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb import Query

import logging
import json
import traceback
from datetime import datetime
import copy
import json_logging
import sys
import time

print (time.time())

db = TinyDB("outNorm.json",storage=CachingMiddleware(JSONStorage))

tabl = db.table("t1")

print (time.time())

with open('json.logs') as f:
    for entry in f.readlines():
        # print (time.time())
        out = json.loads(entry)
        #print (time.time())
        tabl.insert(out)
        # print (time.time())
    
print(time.time())

q = Query()
if (db.table("t1").search(q.level.exists())):
#     print(db.table("t1").search(Query().fragment({'level':'INFO','message':' Debug'})))#['level']=="INFO" and Query()['message']==" Debug"))
#     print()
    print(db.table("t1").search(q.level=="ERROR"))
#     print()
#     print(db.table("t1").search(q.level=="WARNING"))
#     print()
#     def time_filter_func(val,lowerLimit,upperLimit):
#         print(val)
#         print(lowerLimit)
#         print(upperLimit)
#         return lowerLimit <= val <= upperLimit
#     print(db.table("t1").search(Query()['userTime'].test(time_filter_func,0,1)))
# print()
# doc = db.table("t1").all()[0]
# print(doc)
#print(db.all())
# print()
# q = Query()

# print(db.search(q.level == "INFO"))


