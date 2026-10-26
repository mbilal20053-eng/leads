import urllib.request
import re

html = urllib.request.urlopen("http://127.0.0.1:5000/").read().decode("utf-8")

m_badge = re.search(r'id="nav-leads-count-badge">([^<]+)<', html)
print("Sidebar badge in HTML:", m_badge.group(1) if m_badge else "NOT FOUND")

m_css = re.search(r'app\.css\?v=([^"]+)', html)
print("CSS cachebuster:", m_css.group(1) if m_css else "NOT FOUND")

m_js = re.search(r'app\.js\?v=([^"]+)', html)
print("JS cachebuster:", m_js.group(1) if m_js else "NOT FOUND")

assert m_badge and m_badge.group(1) == "919.6M", f"Badge error: {m_badge}"
print("VERIFICATION SUCCESS: Sidebar badge is 919.6M")
