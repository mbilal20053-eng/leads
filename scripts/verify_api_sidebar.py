import urllib.request
import json

dash = json.loads(urllib.request.urlopen("http://127.0.0.1:5000/api/dashboard_metrics").read().decode("utf-8"))
charts = json.loads(urllib.request.urlopen("http://127.0.0.1:5000/api/charts/overview").read().decode("utf-8"))

print("Dashboard total portfolio:", dash["total_portfolio"])
print("Dashboard unique local records:", dash["unique_verified_records"])
print("Dashboard duplicates removed:", dash["duplicates_removed"])
print("Charts field coverage:", charts["field_coverage"][0])
