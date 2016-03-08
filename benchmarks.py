# coding:utf-8

import time
import pickle

try:
    import ujson
except ImportError:
    ujson = None
try:
    import tornado.escape
except ImportError:
    tornado.escape = None
try:
    import simplejson
except ImportError:
    simplejson = None
try:
    import bson.json_util as bson
except ImportError:
    bson = None
try:
    import json
except ImportError:
    json = None

default_data = {
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}

def ttt(f, data=None, x=100*1000):
    start = time.time()
    while x:
        x -= 1
        foo = f(data)
    return time.time()-start


def profile(serial, deserial, data=None, x=100*1000):
    if not data:
        data = default_data
    squashed = serial(data)
    return (ttt(serial, data, x), ttt(deserial, squashed, x))


def test(serial, deserial, data=None):
    if not data:
        data = default_data
    assert deserial(serial(data)) == data

contenders = []

if tornado.escape:
    contenders.append(('tornado', (tornado.escape.json_encode, tornado.escape.json_decode)))
if ujson:
    contenders.append(('ujson', (ujson.encode, ujson.decode)))
if simplejson:
    contenders.append(('simplejson', (simplejson.dumps, simplejson.loads)))
if bson:
    contenders.append(('mongodb bson', (bson.dumps, bson.loads)))
if json:
    contenders.append(('stdlib json', (json.dumps, json.loads)))

for name, args in contenders:
    test(*args)
    x, y = profile(*args)
    print("%-11s serialize: %0.3f  deserialize: %0.3f  total: %0.3f" % (
        name, x, y, x+y))
