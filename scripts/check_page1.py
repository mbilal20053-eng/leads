import urllib.request, json

req = urllib.request.urlopen("http://127.0.0.1:5000/api/leads?dataset=all_global&page=1&page_size=50")
data = json.loads(req.read().decode("utf-8"))
leads = data.get("leads", [])
has_ph = sum(1 for l in leads if l.get("phone"))
has_web = sum(1 for l in leads if l.get("website"))
has_em = sum(1 for l in leads if l.get("email"))

print(f"Page 1 ({len(leads)} leads): with_phone={has_ph} ({has_ph/len(leads)*100:.1f}%), with_web={has_web} ({has_web/len(leads)*100:.1f}%), with_email={has_em} ({has_em/len(leads)*100:.1f}%)")
for i, l in enumerate(leads[:15]):
    print(f"#{i+1}: {l.get('name')} | phone: {l.get('phone')} | web: {l.get('website')}")
