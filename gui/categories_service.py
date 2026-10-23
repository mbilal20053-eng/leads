"""
Lead Engine PRO - Categories Service
Provides access to all 295 unified categories, dataset-specific verticals,
formatted labels, and fast category search/filter across 215M+ leads.
"""
import os
import json
import re

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

# Comprehensive Category Inference Rules
BIZ_CATEGORY_RULES = [
    # Dental & Healthcare
    (re.compile(r'\b(dental|dentist|orthodont[a-z]*|teeth|tooth|oral surgery|periodont[a-z]*)\b', re.I), 'Dental Practice'),
    (re.compile(r'\b(hospital|clinic|doctor|physician|pediatric[a-z]*|surgeon|medical|health care|healthcare|wellness clinic|oncology|urgent care)\b', re.I), 'Hospital & Health Care'),
    (re.compile(r'\b(pharmacy|pharmaceutical|apotheke|rx|biotech[a-z]*)\b', re.I), 'Pharmaceuticals'),
    (re.compile(r'\b(mental health|therap[a-z]*|counsel[a-z]*|psychiat[a-z]*|psychol[a-z]*)\b', re.I), 'Mental Health Care'),
    (re.compile(r'\b(optometry|optometrist|eyecare|eye care|vision|ophthalmol[a-z]*)\b', re.I), 'Optometry & Eye Care'),
    (re.compile(r'\b(chiropractic|chiropractor|physical therapy|physiotherapy|rehab[a-z]*)\b', re.I), 'Physical Therapy & Rehabilitation'),
    (re.compile(r'\b(vet|veterinary|animal hospital|pet care|pet clinic|veterinarian)\b', re.I), 'Veterinary & Pet Services'),
    
    # Trades & Construction
    (re.compile(r'\b(plumb[a-z]*|drain[a-z]*|sewer[a-z]*|pipe[a-z]*|water heater)\b', re.I), 'Plumbing & Water Services'),
    (re.compile(r'\b(roof[a-z]*|shingle[a-z]*|gutter[a-z]*)\b', re.I), 'Roofing & Construction'),
    (re.compile(r'\b(electric[a-z]*|wiring|lighting|power solutions)\b', re.I), 'Electrical Services'),
    (re.compile(r'\b(hvac|air cond[a-z]*|heating|cooling|furnace|ventilation)\b', re.I), 'HVAC & Climate Control'),
    (re.compile(r'\b(construct[a-z]*|builder[a-z]*|contractor[a-z]*|remodel[a-z]*|renovat[a-z]*|carpenter[a-z]*|carpentry)\b', re.I), 'Construction'),
    (re.compile(r'\b(landscap[a-z]*|lawn[a-z]*|tree service|garden[a-z]*|mowing|turf)\b', re.I), 'Landscaping & Grounds Care'),
    (re.compile(r'\b(clean[a-z]*|janitor[a-z]*|maid[a-z]*|carpet clean[a-z]*|pressure wash[a-z]*)\b', re.I), 'Cleaning & Janitorial'),
    (re.compile(r'\b(locksmith|security system|alarm[a-z]*|surveillance)\b', re.I), 'Security & Locksmith Services'),
    (re.compile(r'\b(paint[a-z]*|drywall)\b', re.I), 'Painting & Wall Services'),
    (re.compile(r'\b(pest control|exterminat[a-z]*|termite[a-z]*)\b', re.I), 'Pest Control Services'),
    (re.compile(r'\b(flooring|tile[a-z]*|hardwood)\b', re.I), 'Flooring & Tiling'),
    (re.compile(r'\b(glass|glazing|window[a-z]*|doors?)\b', re.I), 'Windows & Glass Services'),
    
    # Food, Dining & Culinary
    (re.compile(r'\b(restaurant[a-z]*|bistro[a-z]*|diner[a-z]*|grill[a-z]*|eatery|steakhouse|tapas|bbq|sushi|taco|burger[a-z]*)\b', re.I), 'Restaurants & Food'),
    (re.compile(r'\b(cafe[a-z]*|coffee[a-z]*|espresso[a-z]*|roaster[a-z]*|tea house)\b', re.I), 'Cafe & Coffee Shop'),
    (re.compile(r'\b(baker[a-z]*|pastry|cake[a-z]*|donut[a-z]*|bread|patisserie)\b', re.I), 'Bakery & Pastry'),
    (re.compile(r'\b(pizza[a-z]*|pizzeria[a-z]*|italian dining)\b', re.I), 'Pizzeria & Italian Dining'),
    (re.compile(r'\b(chef[a-z]*|culinary|cater[a-z]*|private chef)\b', re.I), 'Chef & Culinary Services'),
    (re.compile(r'\b(brewery|winery|distillery|bar\b|pub\b|tavern|lounge)\b', re.I), 'Breweries, Wineries & Bars'),
    (re.compile(r'\b(hotel[a-z]*|resort[a-z]*|motel[a-z]*|inn\b|lodging|hostel|suites)\b', re.I), 'Hospitality & Hotels'),
    
    # Real Estate & Property
    (re.compile(r'\b(realt[a-z]*|real estate|brokerage|realty|realtor[a-z]*)\b', re.I), 'Real Estate'),
    (re.compile(r'\b(property manag[a-z]*|leasing|apartments|property rental)\b', re.I), 'Property Management'),
    (re.compile(r'\b(mortgage[a-z]*|escrow|home loan[a-z]*|lending group)\b', re.I), 'Real Estate Loans & Mortgages'),
    (re.compile(r'\b(single family|residence|residential home)\b', re.I), 'Single Family Dwelling'),
    (re.compile(r'\b(multi-family|condominium|condos?)\b', re.I), 'Multi-Family Dwelling'),
    
    # Tech & Software
    (re.compile(r'\b(software|saas|cloud|cyber[a-z]*|developer|artificial intelligence|\bai\b|machine learning|app dev)\b', re.I), 'Computer Software'),
    (re.compile(r'\b(\bit\b|information technology|msp\b|network solutions|managed it|systems)\b', re.I), 'Information Technology and Services'),
    (re.compile(r'\b(web design|web dev|seo\b|hosting|digital agency)\b', re.I), 'Internet & Web Services'),
    
    # Financial & Legal
    (re.compile(r'\b(bank[a-z]*|credit union|wealth[a-z]*|investment[a-z]*|capital[a-z]*|asset mgmt|fintech)\b', re.I), 'Financial Services'),
    (re.compile(r'\b(account[a-z]*|cpa\b|bookkeep[a-z]*|tax service|tax prep|auditor[a-z]*)\b', re.I), 'Accounting & Tax'),
    (re.compile(r'\b(law\b|lawyer[a-z]*|attorney[a-z]*|legal|counsel|law firm|litigation)\b', re.I), 'Law Practice'),
    (re.compile(r'\b(insurance|underwriting|assurance)\b', re.I), 'Insurance'),
    
    # Auto & Transport
    (re.compile(r'\b(auto repair|mechanic|collision|auto body|transmission|smog)\b', re.I), 'Automotive Repair & Maintenance'),
    (re.compile(r'\b(auto sales|car dealership|dealership|motors|car dealer)\b', re.I), 'Automotive Dealerships'),
    (re.compile(r'\b(tire[a-z]*|alignment|brake service)\b', re.I), 'Tire & Auto Care'),
    (re.compile(r'\b(trucking|freight|logistics|shipping|cargo|transport[a-z]*|towing|courier)\b', re.I), 'Transportation/Trucking/Railroad'),
    
    # Beauty & Fitness
    (re.compile(r'\b(salon[a-z]*|hair[a-z]*|barber[a-z]*|styling|haircut)\b', re.I), 'Beauty & Salons'),
    (re.compile(r'\b(spa\b|massage|esthetic[a-z]*|skin care|nail[a-z]*)\b', re.I), 'Spa & Personal Care'),
    (re.compile(r'\b(gym\b|fitness|crossfit|workout|athletic[a-z]*|yoga|pilates)\b', re.I), 'Health, Wellness and Fitness'),
    
    # Creative & Professional
    (re.compile(r'\b(market[a-z]*|advertising|pr\b|public relations|branding)\b', re.I), 'Marketing and Advertising'),
    (re.compile(r'\b(photograph[a-z]*|camera|portrait|videograph[a-z]*)\b', re.I), 'Photography'),
    (re.compile(r'\b(music[a-z]*|band[a-z]*|audio|recording|producer|dj\b)\b', re.I), 'Music & Entertainment'),
    (re.compile(r'\b(design[a-z]*|graphic design|ux\b|ui\b|interior design)\b', re.I), 'Design & Creative'),
    (re.compile(r'\b(coach[a-z]*|mentor[a-z]*|executive coach)\b', re.I), 'Professional Training & Coaching'),
    (re.compile(r'\b(school[a-z]*|university|college|academy|tutoring|education)\b', re.I), 'Higher Education & Tutoring')
]

def infer_biz_category(name="", job_title="", current_cat=""):
    c = (current_cat or "").strip()
    if c and c.lower() not in ["corporate enterprise", "general business", "commercial enterprise", "none", "", "all", "undefined"]:
        return format_category_label(c)
        
    text = f"{name} {job_title}".strip()
    if text:
        for reg, cat in BIZ_CATEGORY_RULES:
            if reg.search(text):
                return cat
                
    if c and c.lower() not in ["none", "", "all", "undefined"]:
        return format_category_label(c)
    return "Business & Commercial"

