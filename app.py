from flask import Flask
from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Summary
from prometheus_client import Histogram
import random
import time

app = Flask(__name__)


REQUESTS = Counter('hello_worlds_total', 'Hello Worlds requested.')
def index_Counter():
    REQUESTS.inc(1) #you can pass a value to inc which will increase the counter by said value

EXCEPTIONS = Counter('hello_world_exceptions_total', 'Exceptions serving Hello World.')
def index_EXCEPTIONS():
    with EXCEPTIONS.count_exceptions():
        if random.random() < 0.2:
            raise Exception

INPROGRESS = Gauge('hello_worlds_inprogress', 'Number of Hello Worlds in progress.')
LAST = Gauge('hello_world_last_time_seconds', 'The last time a Hello World was served.')

def index_INPROGRESS():
    INPROGRESS.inc()

    LAST.set(time.time())
    INPROGRESS.dec()

LATENCY = Summary('hello_world_latency_seconds', 'Time for a request Hello World.')
def index_LATENCY():
    start = time.time()
    time.sleep(10)
    LATENCY.observe(time.time() - start)

LATENCY_Histogram = Histogram('hello_world_latency_seconds_histogram','Time for a request Hello World. (histogram)')
def index_LATENCY_Histogram():
    start_histogram = time.time()
    #fast process
    LATENCY_Histogram.observe(time.time() - start_histogram)

LATENCY_bucket = Histogram('hello_world_latency_seconds_bucket', 'Time for a request Hello World. (bucket)',
buckets=[0.0001, 0.0002, 0.0005, 0.001, 0.01, 0.1])

def index_LATENCY_Histogram_bucket():
    start_histogram = time.time()
    #fast process
    LATENCY_bucket.observe(time.time() - start_histogram)

@app.route('/')
def hello():
    return 'Hello'

@app.route('/test')
def test():
    return 'test'
        
        
@app.route('/inc')
def inc():
    index_Counter()
    return 'incremented'
    
@app.route('/exeption')
def exeption():
    index_EXCEPTIONS()
    return 'exception'

@app.route('/gauge')
def gauge():
    index_INPROGRESS()
    return 'gauge'

@app.route('/latency')
def latency():
    index_LATENCY()
    return 'latency'

@app.route('/histogram')
def histogram():
    index_LATENCY_Histogram()
    return 'histogram'

@app.route('/bucket')
def bucket():
    index_LATENCY_Histogram_bucket()
    return 'bucket'

if __name__ == "__main__":
    app.run()
start_http_server(8010)



