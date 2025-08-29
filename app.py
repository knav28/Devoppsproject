from flask import Flask, request
from prometheus_client import start_http_server, Counter, Histogram
from waitress import serve
import time
import logging
from prometheus_client import start_http_server
start_http_server(9183)

# Setup Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP Requests',
    ['method', 'endpoint']
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 
    'HTTP Request latency',
    ['endpoint']
)

# Start Prometheus metrics HTTP server (on 9182)
# Only call this once in your environment!
# If it's already running elsewhere, skip this line
# start_http_server(9182)  ← You said it's already running, so skip it

# Flask App
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    start_time = time.time()
    REQUEST_COUNT.labels(method=request.method, endpoint='/').inc()
    app.logger.info(f"Received request: {request.method} /")

    time.sleep(0.1)  # Simulate latency
    response = "Hello from Flask with Prometheus metrics!"

    duration = time.time() - start_time
    REQUEST_LATENCY.labels(endpoint='/').observe(duration)
    return response, 200

if __name__ == "__main__":
    # Run the app on 0.0.0.0:7000
    serve(app, host="0.0.0.0", port=7000)
