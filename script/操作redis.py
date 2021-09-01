import redis

conn = redis.Redis(host='127.0.0.1', port=6379)
# conn.set('foo', 'Bar')
#
result = conn.get('+8618782168312')
print(result)
# conn.flushall()
print(conn.keys())

