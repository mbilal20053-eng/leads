"""
Lead Engine PRO - Categories Service
Provides access to all 295 unified categories, dataset-specific verticals,
formatted labels, and fast category search/filter across 215M+ leads.
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ALL_CATS_FILE = os.path.join(DATA_DIR, "categories.json")
DATASET_CATS_FILE = os.path.join(DATA_DIR, "dataset_categories.json")

def format_category_label(name):
    if not name:
        return ""
    # Clean quotes or anomalies
    s = name.strip().strip('"').strip("'")
    if not s:
        return ""
    
    words = s.replace('/', ' / ').replace('&', ' & ').split()
    capitalized = []
    for w in words:
        wl = w.lower()
        if wl in ['and', 'or', 'of', 'in', 'the', '&', '/']:
            capitalized.append(wl if wl not in ['&', '/'] else w)
        else:
            capitalized.append(w.capitalize())
    res = ' '.join(capitalized).replace(' / ', '/').replace(' & ', ' & ')
    if res and res[0].islower():
        res = res[0].upper() + res[1:]
    return res

def format_count(cnt):
    if cnt >= 1_000_000:
        return f"{cnt / 1_000_000:.2f}M"
    elif cnt >= 1_000:
        return f"{cnt / 1_000:.1f}K"
    return f"{cnt:,}"

# Load categories data
ALL_CATEGORIES = []
DATASET_CATEGORIES = {}

def init_categories():
    global ALL_CATEGORIES, DATASET_CATEGORIES
    if os.path.exists(ALL_CATS_FILE):
        try:
            with open(ALL_CATS_FILE, "r", encoding="utf-8") as f:
                raw_cats = json.load(f)
            formatted = []
            for item in raw_cats:
                raw_name = item.get("name", "").strip()
                if not raw_name:
                    continue
                cnt = int(item.get("count", 0))
                formatted.append({
                    "id": raw_name,
                    "label": format_category_label(raw_name),
                    "count": cnt,
                    "count_str": f"{cnt:,}",
                    "badge": format_count(cnt)
                })
            ALL_CATEGORIES = formatted
        except Exception as e:
            print(f"[CategoriesService] Error loading all categories: {e}")
            ALL_CATEGORIES = []
            
    if os.path.exists(DATASET_CATS_FILE):
        try:
            with open(DATASET_CATS_FILE, "r", encoding="utf-8") as f:
                raw_ds = json.load(f)
            ds_dict = {}
            for did, cat_list in raw_ds.items():
                ds_formatted = []
                for item in cat_list:
                    raw_name = item.get("name", "").strip()
                    if not raw_name:
                        continue
                    cnt = int(item.get("count", 0))
                    ds_formatted.append({
                        "id": raw_name,
                        "label": format_category_label(raw_name),
                        "count": cnt,
                        "count_str": f"{cnt:,}",
                        "badge": format_count(cnt)
                    })
                ds_dict[did] = ds_formatted
            DATASET_CATEGORIES = ds_dict
        except Exception as e:
            print(f"[CategoriesService] Error loading dataset categories: {e}")
            DATASET_CATEGORIES = {}

init_categories()

def get_all_categories():
    return ALL_CATEGORIES

def get_categories_for_dataset(dataset_id=None):
    if dataset_id and dataset_id in DATASET_CATEGORIES:
        return DATASET_CATEGORIES[dataset_id]
    return ALL_CATEGORIES

def search_categories(query="", dataset_id=None):
    cats = get_categories_for_dataset(dataset_id)
    if not query:
        return cats
    q = query.lower().strip()
    return [c for c in cats if q in c["id"].lower() or q in c["label"].lower()]
