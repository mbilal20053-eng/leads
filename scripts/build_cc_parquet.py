import gzip
import os
import sys
import pyarrow as pa
import pyarrow.parquet as pq

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

f_cc = r"d:\leads\cc-index.paths.gz"
out_parquet = r"d:\leads\cc_web_index.parquet"

schema = pa.schema([
    ('id', pa.string()),
    ('name', pa.string()),
    ('contact_name', pa.string()),
    ('job_title', pa.string()),
    ('category', pa.string()),
    ('address', pa.string()),
    ('city', pa.string()),
    ('state', pa.string()),
    ('zip', pa.string()),
    ('country', pa.string()),
    ('phone', pa.string()),
    ('website', pa.string()),
    ('email', pa.string()),
    ('socials', pa.string()),
    ('tier', pa.string()),
    ('score', pa.int32()),
    ('opportunity', pa.string()),
    ('pitch', pa.string()),
    ('why', pa.string()),
    ('source_badge', pa.string()),
    ('source_id', pa.string()),
    ('source_color', pa.string()),
])

batch = {k.name: [] for k in schema}

with gzip.open(f_cc, 'rt', errors='ignore') as gz:
    for idx, line in enumerate(gz):
        path = line.strip()
        if not path:
            continue
        shard = os.path.basename(path).replace(".gz", "")
        batch['id'].append(f"cc_{idx}")
        batch['name'].append(f"Common Crawl Index Shard ({shard})")
        batch['contact_name'].append("Common Crawl Foundation")
        batch['job_title'].append(f"Web Domain Archive Cluster Shard {shard}")
        batch['category'].append("Web Archive & Internet Domains")
        batch['address'].append(path)
        batch['city'].append("Global Web")
        batch['state'].append("CC-MAIN-2026-43")
        batch['zip'].append("")
        batch['country'].append("Global")
        batch['phone'].append("")
        batch['website'].append(f"https://data.commoncrawl.org/{path}")
        batch['email'].append("")
        batch['socials'].append("commoncrawl.org")
        batch['tier'].append('A')
        batch['score'].append(90)
        batch['opportunity'].append("WEB ARCHIVE DOMAIN HARVESTING")
        batch['pitch'].append(f"Common Crawl index shard {shard}. Massive scale web domain discovery and URL metadata extraction.")
        batch['why'].append("Official Common Crawl October 2026 web corpus CDX index cluster.")
        batch['source_badge'].append("🕸️ Common Crawl")
        batch['source_id'].append("cc_web_index")
        batch['source_color'].append("#64748b")

tbl = pa.Table.from_pydict(batch, schema=schema)
pq.write_table(tbl, out_parquet)
print(f"Created {out_parquet} with {len(batch['id'])} collections!")
