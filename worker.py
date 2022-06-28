import os
import redis
from configs.config import global_config as config
from rq import Worker, Queue, Connection

listen = ['default']
url = f'{config["worker_protocol"]}://{config["worker_host"]}:' \
      f'{config["worker_port"]}'
redis_url = os.getenv('REDISTOGO_URL', url)

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()