import random, string, time
import os
from pymongo import MongoClient

#CONNECTION_STING="mongodb+srv://mongodb-in-k8s-svc.mongodb.svc.cluster.local/test?ssl=false&replicaSet=mongodb-in-k8s"

CONNECTION_STRING = os.getenv('MONGODB_URI','mongodb+srv://localhost:27017')
SECONDS_TO_PAUSE = float(os.getenv('SECONDS_TO_PAUSE','1.0'))
mongo = MongoClient(CONNECTION_STRING)

print(f'CONNECTION_STRING={CONNECTION_STRING}')
print(f'SECONDS_TO_PAUSE={SECONDS_TO_PAUSE}')

print(f'test connected to {mongo}')
db = mongo['mongodb-in-kubernetes']
result = db['demodata'].drop()
print(f'{result}')

def random_doc():
  doc = {}
  num_keys =  random.randint(1,10)
  for i in range(0,num_keys):
    v =  random.randint(1,256)
    value = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(v)])

    doc[f'key_{i}']=value
  return doc

def test_load(num_docs):
  results = [];
  for i in range(0,num_docs):
    result = db['demodata'].insert( random_doc() );
    results.append(result)
  size = db['demodata'].count_documents({})
  print(f'Inserted {results} documents. Collection size: {size}')
 

while True:
  test_load( random.randint(1,101) )
  time.sleep( SECONDS_TO_PAUSE )

