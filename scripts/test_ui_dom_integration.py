import urllib.request

def test_dom():
    res = urllib.request.urlopen('http://127.0.0.1:5000/')
    html = res.read().decode('utf-8')

    checks = [
        ('5-Tier Portfolio Banner', 'portfolio-tier-banner' in html),
        ('Portfolio Audit Modal', 'id="portfolioAuditModal"' in html),
        ('all_local_unified option selected', 'value="all_local_unified" selected' in html),
        ('Tier 1 Configured 919M', '919,557,675' in html),
        ('Tier 2 Physical 567M', '567,188,074' in html),
        ('Tier 3 Dedup 43.7M', '43,788,529' in html),
        ('Tier 4 Active DuckDB 14.9M', '14,935,362' in html),
        ('Tier 5 Remote 352M', '352,334,356' in html)
    ]

    for label, passed in checks:
        status = "PASS" if passed else "FAIL"
        print(f'[{status}] HTML check: {label}')

    css_res = urllib.request.urlopen('http://127.0.0.1:5000/static/app.css')
    status = "PASS" if css_res.status == 200 else "FAIL"
    print(f'[{status}] static/app.css: HTTP {css_res.status} ({len(css_res.read()):,} bytes)')

    js_res = urllib.request.urlopen('http://127.0.0.1:5000/static/app.js')
    status = "PASS" if js_res.status == 200 else "FAIL"
    print(f'[{status}] static/app.js: HTTP {js_res.status} ({len(js_res.read()):,} bytes)')

if __name__ == '__main__':
    test_dom()
