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


db = TinyDB("out.json",storage=CachingMiddleware(JSONStorage))

tabl = db.table('t1')

ls = []
with open('json.logs') as f:
    for entry in f.readlines():
        out = json.loads(entry)
        ls.append(out)
# print(ls)
print(len(ls))
print(time.time())
tabl.insert_multiple([i for i in ls])
db.storage.flush()
print(time.time())

q = Query()
print(len(tabl.all()))
print(db.table("t1").search(q.level=="ERROR"))