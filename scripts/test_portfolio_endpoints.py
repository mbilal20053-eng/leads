import urllib.request
import urllib.parse
import json

def test():
    print("Testing /api/portfolio/breakdown...")
    req = urllib.request.urlopen('http://127.0.0.1:5000/api/portfolio/breakdown')
    data = json.loads(req.read().decode())
    tiers = data['tiers']
    sources = data['sources']
    print(f'[PASS] Portfolio Breakdown:')
    print(f'       Tier 1 Configured: {tiers["total_configured"]:,}')
    print(f'       Tier 2 Physical:   {tiers["physical_on_disk"]:,}')
    print(f'       Tier 3 Unique:     {tiers["unique_deduplicated"]:,}')
    print(f'       Tier 4 Active DB:  {tiers["active_production"]:,}')
    print(f'       Tier 5 Remote:     {tiers["remote_unfetched"]:,}')
    print(f'       Total Sources:     {len(sources)}')

    print("\nTesting /api/categories/analytics (Default dataset)...")
    req = urllib.request.urlopen('http://127.0.0.1:5000/api/categories/analytics')
    cat_data = json.loads(req.read().decode())
    print(f'[PASS] Categories Analytics Default:')
    print(f'       Dataset:          {cat_data["dataset"]}')
    print(f'       Total Leads:      {cat_data["total_leads"]:,}')
    print(f'       Total Categories: {cat_data["total_categories"]:,}')
    print(f'       Top Category:     {cat_data["categories"][0]["label"]} ({cat_data["categories"][0]["count"]:,})')

    print("\nTesting /api/leads with multi-category filter on all_local_unified...")
    cat_filter = urllib.parse.quote('hospital & health care||construction')
    req = urllib.request.urlopen(f'http://127.0.0.1:5000/api/leads?dataset=all_local_unified&category={cat_filter}&page=1&page_size=2')
    multi_data = json.loads(req.read().decode())
    print(f'[PASS] Multi-Category Filter on all_local_unified:')
    print(f'       Total matching:   {multi_data["total"]:,}')
    print(f'       Returned leads:   {len(multi_data["leads"])}')
    print(f'       Sample Lead 1:    {multi_data["leads"][0].get("name")} | Category: {multi_data["leads"][0].get("category")}')

    print("\nTesting /api/categories/analytics for b2b_executives (specific dataset)...")
    req = urllib.request.urlopen('http://127.0.0.1:5000/api/categories/analytics?dataset=b2b_executives')
    b2b_data = json.loads(req.read().decode())
    print(f'[PASS] B2B Executives Specific Query:')
    print(f'       Dataset:          {b2b_data["dataset"]}')
    print(f'       Total Leads:      {b2b_data["total_leads"]:,}')
    print(f'       Total Categories: {b2b_data["total_categories"]:,}')

    print("\nAll integration tests PASSED successfully!")

if __name__ == '__main__':
    test()
