import requests
import time
import re

# === CONFIG ===
DT_ENV_URL = "https://qgb06100.live.dynatrace.com"
DT_API_TOKEN = "<YOUR_API_TOKEN>"
JMETER_METRICS_URL = "http://localhost:9270/metrics"

# Dynatrace metrics ingest endpoint
DT_METRIC_ENDPOINT = f"{DT_ENV_URL}/api/v2/metrics/ingest"
HEADERS = {
    
    "Authorization": f"Api-Token {DT_API_TOKEN}",
    "Content-Type": "text/plain"
}

def parse_prometheus_metrics(raw_metrics):
    metrics = []
    timestamp = int(time.time() * 1000)

    for line in raw_metrics.splitlines():
        # Skip comments and empty lines
        if not line or line.startswith("#"):
            continue

        # Example line: jmeter_requests{testName="Test01",requestName="Login",status="PASS"} 42
        match = re.match(r'^(\w+)\{([^}]+)\}\s+([0-9\.\-eE]+)', line)
        if not match:
            continue

        metric_name, labels_str, value = match.groups()

        # Clean/format labels for Dynatrace
        tags = labels_str.replace('"', '')
        tags = tags.replace(",", ",")  # Dynatrace accepts simple key=value pairs

        # Create the Dynatrace metric line
        metric_line = f"custom.{metric_name},{tags} {value} {timestamp}"
        metrics.append(metric_line)

    return metrics

def push_to_dynatrace(metrics):
    payload = "\n".join(metrics)
    response = requests.post(DT_METRIC_ENDPOINT, headers=HEADERS, data=payload)
    
    if response.status_code == 202:
        print(" Metrics successfully pushed to Dynatrace.")
    else:
        print(f"Failed to push metrics. Status: {response.status_code}")
        print(response.text)

def main():
    try:
        resp = requests.get(JMETER_METRICS_URL)
        resp.raise_for_status()
        metrics = parse_prometheus_metrics(resp.text)
        if metrics:
            push_to_dynatrace(metrics)
        else:
            print("No metrics parsed from JMeter endpoint.")
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    main()