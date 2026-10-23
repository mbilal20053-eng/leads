"""
Lead Engine PRO - Categories Service
Provides access to all 295 unified categories organized under 14 Major Categories,
formatted labels, hierarchy mapping, and fast category search/filter across 215M+ leads.
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

# 14 Comprehensive Major Categories taxonomy
MAJOR_CATEGORIES = [
    {
        "id": "restaurants_hospitality",
        "name": "Restaurants & Hospitality",
        "icon": "🍽️",
        "description": "Restaurants, Hotels, Cafes, Bakeries, Pizzerias, Bars & Culinary Services",
        "keywords": [
            r'\b(restaurant[a-z]*|dining|hotel[a-z]*|hospitality|cafe[a-z]*|coffee\s*shop[a-z]*|bistro[a-z]*|baker[a-z]*|pizza[a-z]*|pizzeria[a-z]*|chef[a-z]*|culinary|cater[a-z]*|food[a-z]*|beverage[a-z]*|bar\b|bars\b|pub\b|pubs\b|tavern[a-z]*|brew[a-z]*|win[a-z]*|distill[a-z]*|motel[a-z]*|resort[a-z]*|lodging|hostel[a-z]*|inn\b|inns\b|eater[a-z]*|steakhouse[a-z]*|tapas|sushi|burger[a-z]*|fast food|tourism|tourist|travel)\b'
        ]
    },
    {
        "id": "real_estate",
        "name": "Real Estate & Property",
        "icon": "🏢",
        "description": "Realtors, Real Estate, Single Family, Multi-Family, Property Management, Mortgages & Housing",
        "keywords": [
            r'\b(real estate|realt[a-z]*|property|single family|multi-family|multifamily|residential|commercial real estate|apartments|leasing|mortgage[a-z]*|escrow|home loan|land development|housing|mobile home|building restoration|buildings-pre-cut|real esate|broker)\b'
        ]
    },
    {
        "id": "healthcare_medical",
        "name": "Healthcare & Medical",
        "icon": "🏥",
        "description": "Hospitals, Doctors, Dentists, Clinics, Pharmaceuticals, Mental Health, Optometry & Therapy",
        "keywords": [
            r'\b(health[a-z]*|hospital[a-z]*|doctor[a-z]*|physician[a-z]*|clinic[a-z]*|dental|dentist[a-z]*|orthodont[a-z]*|medical[a-z]*|pharmac[a-z]*|biotech[a-z]*|mental health|therap[a-z]*|optometr[a-z]*|eyecare|chiropract[a-z]*|veterinar[a-z]*|vet\b|vets\b|animal hospital|nursing|psychol[a-z]*|psychiat[a-z]*|rehab[a-z]*|alternative medicine)\b'
        ]
    },
    {
        "id": "tech_software",
        "name": "Tech, Software & IT",
        "icon": "💻",
        "description": "Computer Software, SaaS, IT Services, Cyber Security, Artificial Intelligence & Web Design",
        "keywords": [
            r'\b(software|computer[a-z]*|information technology|internet|saas|cloud|cyber[a-z]*|network[a-z]*|telecom[a-z]*|artificial intelligence|\bai\b|machine learning|app dev|web dev|web design[a-z]*|semiconductor[a-z]*|data storage|electronics|hardware|information services|wireless|nanotechnology)\b'
        ]
    },
    {
        "id": "construction_trades",
        "name": "Construction & Trades",
        "icon": "🔨",
        "description": "Construction, Contractors, Plumbing, Roofing, Electrical, HVAC, Landscaping & Cleaning",
        "keywords": [
            r'\b(construct[a-z]*|builder[a-z]*|contractor[a-z]*|plumb[a-z]*|roof[a-z]*|electric[a-z]*|hvac|air cond[a-z]*|landscap[a-z]*|lawn|clean[a-z]*|janitor[a-z]*|paint[a-z]*|drywall|pest control|flooring|carpentr[a-z]*|locksmith|architecture|civil engineering|building materials|glass, ceramics)\b'
        ]
    },
    {
        "id": "financial_banking",
        "name": "Financial Services & Banking",
        "icon": "💳",
        "description": "Banking, Financial Advisory, Wealth Management, Insurance, Accounting & Tax",
        "keywords": [
            r'\b(financ[a-z]*|bank[a-z]*|credit[a-z]*|invest[a-z]*|wealth|venture capital|private equity|capital|insurance|underwriting|account[a-z]*|cpa\b|bookkeep[a-z]*|tax[a-z]*|audit[a-z]*|angel investors?|acquisition[a-z]*)\b'
        ]
    },
    {
        "id": "legal_government",
        "name": "Legal, Government & Public Policy",
        "icon": "⚖️",
        "description": "Law Practice, Attorneys, Legal Services, Judiciary, Government & Public Safety",
        "keywords": [
            r'\b(law\b|laws\b|lawyer[a-z]*|attorney[a-z]*|legal|litigation|judiciar[a-z]*|government[a-z]*|public policy|public safety|military|international affairs|court[a-z]*|law enforcement|legislative|dispute resolution)\b'
        ]
    },
    {
        "id": "automotive_transport",
        "name": "Automotive & Transportation",
        "icon": "🚗",
        "description": "Automotive Repair, Car Dealerships, Trucking, Logistics, Freight & Airlines",
        "keywords": [
            r'\b(auto[a-z]*|car\b|cars\b|truck[a-z]*|freight|logistics|shipping|transport[a-z]*|railroad|airline[a-z]*|aviation|maritime|marine|towing|mechanic[a-z]*|dealership[a-z]*|fleet|warehous[a-z]*|package|automotriz|shipbuilding)\b'
        ]
    },
    {
        "id": "fitness_beauty",
        "name": "Fitness, Sports & Beauty",
        "icon": "💇",
        "description": "Beauty Salons, Barbershops, Spas, Gyms & Fitness, Athletics & Personal Care",
        "keywords": [
            r'\b(salon[a-z]*|barber[a-z]*|hair[a-z]*|beauty|cosmetic[a-z]*|spa\b|spas\b|massage|skin care|nail[a-z]*|gym\b|gyms\b|fitness|crossfit|workout|athletic[a-z]*|yoga|pilates|sport[a-z]*|recreation[a-z]*)\b'
        ]
    },
    {
        "id": "creative_media",
        "name": "Creative, Media & Entertainment",
        "icon": "🎨",
        "description": "Marketing & Advertising, Graphic Design, Photography, Music, Media & Publishing",
        "keywords": [
            r'\b(market[a-z]*|advertising|pr\b|public relations|photograph[a-z]*|music[a-z]*|media|entertainment|film[a-z]*|motion picture|broadcast[a-z]*|graphic[a-z]*|design[a-z]*|art\b|arts\b|fine art|museum[a-z]*|performing arts|writing|publish[a-z]*|news|newspaper[a-z]*|print[a-z]*|producer[a-z]*|dj\b|band\b|bands\b|animation|casinos?|gambling)\b'
        ]
    },
    {
        "id": "education_nonprofit",
        "name": "Education & Non-Profit",
        "icon": "🎓",
        "description": "Higher Education, Schools, Tutoring, Non-Profit Organizations & Foundations",
        "keywords": [
            r'\b(education|higher education|school[a-z]*|university|college|academy|tutor[a-z]*|e-learning|librar[a-z]*|non-profit|nonprofit|philanthrop[a-z]*|charit[a-z]*|foundation[a-z]*|fund-raising|think tank[a-z]*|religious|church|civic|individual & family services|children|political organization|institution)\b'
        ]
    },
    {
        "id": "retail_consumer",
        "name": "Retail, Wholesale & Consumer Goods",
        "icon": "🛍️",
        "description": "Retail Stores, Wholesale, Supermarkets, Apparel, Fashion & Consumer Goods",
        "keywords": [
            r'\b(retail[a-z]*|wholesale|supermarket[a-z]*|grocer[a-z]*|apparel|fashion|clothing|luxury goods|jewelry|furniture|consumer goods|consumer electronics|shopping|store[a-z]*|department store|merchandis[a-z]*|consumer services)\b'
        ]
    },
    {
        "id": "manufacturing_industrial",
        "name": "Manufacturing, Energy & Industrial",
        "icon": "🏭",
        "description": "Industrial Manufacturing, Clean Energy, Oil & Gas, Chemicals, Mining & Agriculture",
        "keywords": [
            r'\b(manufactur[a-z]*|industrial|energy|oil|gas|petroleum|solar|renewable[a-z]*|environment[a-z]*|mining|metals|chemical[a-z]*|machiner[a-z]*|plastics|paper|textile[a-z]*|utilities|defense|aerospace|packaging|mechanical|farming|dairy|fisher[a-z]*|ranch[a-z]*|tobacco)\b'
        ]
    },
    {
        "id": "corporate_professional",
        "name": "Corporate & Professional Services",
        "icon": "👔",
        "description": "Management Consulting, B2B Executives, HR & Staffing, Business Coaching & Operations",
        "keywords": [
            r'\b(consult[a-z]*|management consulting|executive[a-z]*|staffing|recruiting|human resources|hr\b|professional training|coach[a-z]*|business supplies|commercial enterprise|corporate|entrepreneur[a-z]*|facilities services|security|outsourcing|international trade|import and export|program development|project management|research|events services|translation)\b'
        ]
    }
]

# Compiled patterns for fast matching
COMPILED_MAJOR_RULES = []
for m in MAJOR_CATEGORIES:
    regs = [re.compile(kw, re.I) for kw in m["keywords"]]
    COMPILED_MAJOR_RULES.append((m, regs))

def get_major_category(cat_name="", text=""):
    """
    Given a minor category name or business context, maps it to its parent Major Category.
    Returns: {"id": str, "name": str, "icon": str}
    """
    sample = f"{cat_name} {text}".strip()
    if not sample:
        return {
            "id": "corporate_professional",
            "name": "Corporate & Professional Services",
            "icon": "👔"
        }
        
    for m, regs in COMPILED_MAJOR_RULES:
        for reg in regs:
            if reg.search(sample):
                return {
                    "id": m["id"],
                    "name": m["name"],
                    "icon": m["icon"]
                }
                
    # Default fallback
    return {
        "id": "corporate_professional",
        "name": "Corporate & Professional Services",
        "icon": "👔"
    }

def get_major_categories_list():
    """Returns the list of 14 Major Categories with metadata."""
    return [
        {
            "id": m["id"],
            "name": m["name"],
            "icon": m["icon"],
            "description": m["description"]
        }
        for m in MAJOR_CATEGORIES
    ]

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
                lbl = format_category_label(raw_name)
                major = get_major_category(raw_name)
                formatted.append({
                    "id": raw_name,
                    "label": lbl,
                    "count": cnt,
                    "count_str": f"{cnt:,}",
                    "badge": format_count(cnt),
                    "major_id": major["id"],
                    "major_name": major["name"],
                    "major_icon": major["icon"]
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
                    lbl = format_category_label(raw_name)
                    major = get_major_category(raw_name)
                    ds_formatted.append({
                        "id": raw_name,
                        "label": lbl,
                        "count": cnt,
                        "count_str": f"{cnt:,}",
                        "badge": format_count(cnt),
                        "major_id": major["id"],
                        "major_name": major["name"],
                        "major_icon": major["icon"]
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
        specific = DATASET_CATEGORIES[dataset_id]
        specific_ids = {c["id"].lower() for c in specific}
        remaining = [c for c in ALL_CATEGORIES if c["id"].lower() not in specific_ids]
        return specific + remaining
    return ALL_CATEGORIES

def get_categories_hierarchy(dataset_id=None):
    """
    Groups all minor categories under the 14 Major Categories.
    Returns list of Major Category objects, each containing its minor categories with counts.
    """
    cats = get_categories_for_dataset(dataset_id)
    major_map = {}
    for m in MAJOR_CATEGORIES:
        major_map[m["id"]] = {
            "id": m["id"],
            "name": m["name"],
            "icon": m["icon"],
            "description": m["description"],
            "total_count": 0,
            "minor_count": 0,
            "minors": []
        }
        
    for c in cats:
        mid = c.get("major_id") or get_major_category(c["id"])["id"]
        if mid in major_map:
            major_map[mid]["minors"].append(c)
            major_map[mid]["total_count"] += c.get("count", 0)
            major_map[mid]["minor_count"] += 1
            
    # Format totals
    hierarchy = []
    for m in MAJOR_CATEGORIES:
        node = major_map[m["id"]]
        node["total_count_str"] = f"{node['total_count']:,}"
        node["badge"] = format_count(node["total_count"])
        hierarchy.append(node)
        
    return hierarchy

def search_categories(query="", dataset_id=None, major_category=None):
    cats = get_categories_for_dataset(dataset_id)
    
    # Filter by major category if requested
    if major_category and major_category.lower() not in ["all", ""]:
        norm_major = major_category.strip().lower()
        cats = [
            c for c in cats 
            if c.get("major_id", "").lower() == norm_major 
            or c.get("major_name", "").lower() == norm_major
        ]
        
    if not query:
        return cats
        
    q = query.lower().strip()
    return [
        c for c in cats 
        if q in c["id"].lower() 
        or q in c["label"].lower() 
        or q in c.get("major_name", "").lower()
    ]

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
    
    # Food, Dining & Hospitality (Minor categories under Restaurants & Hospitality)
    (re.compile(r'\b(restaurant[a-z]*|bistro[a-z]*|diner[a-z]*|grill[a-z]*|eatery|steakhouse|tapas|bbq|sushi|taco|burger[a-z]*)\b', re.I), 'Restaurants & Food'),
    (re.compile(r'\b(cafe[a-z]*|coffee[a-z]*|espresso[a-z]*|roaster[a-z]*|tea house)\b', re.I), 'Cafe & Coffee Shop'),
    (re.compile(r'\b(baker[a-z]*|pastry|cake[a-z]*|donut[a-z]*|bread|patisserie)\b', re.I), 'Bakery & Pastry'),
    (re.compile(r'\b(pizza[a-z]*|pizzeria[a-z]*|italian dining)\b', re.I), 'Pizzeria & Italian Dining'),
    (re.compile(r'\b(chef[a-z]*|culinary|cater[a-z]*|private chef)\b', re.I), 'Chef & Culinary Services'),
    (re.compile(r'\b(brewery|winery|distillery|bar\b|pub\b|tavern|lounge)\b', re.I), 'Breweries, Wineries & Bars'),
    (re.compile(r'\b(luxury hotel[a-z]*|five-star hotel|palace hotel)\b', re.I), 'Luxury Hotels & Resorts'),
    (re.compile(r'\b(hotel[a-z]*|resort[a-z]*|motel[a-z]*|inn\b|lodging|hostel|suites)\b', re.I), 'Hotels & Lodging'),
    
    # Real Estate & Property
    (re.compile(r'\b(realt[a-z]*|real estate|brokerage|realty|realtor[a-z]*)\b', re.I), 'Real Estate'),
    (re.compile(r'\b(property manag[a-z]*|leasing|apartments|property rental)\b', re.I), 'Property Management'),
    (re.compile(r'\b(mortgage[a-z]*|escrow|home loan[a-z]*|lending group)\b', re.I), 'Real Estate Loans & Mortgages'),
    (re.compile(r'\b(single family|residence|residential home)\b', re.I), 'Single Family Dwelling'),
    (re.compile(r'\b(multi-family|multifamily|condominium|condos?)\b', re.I), 'Multi-Family Dwelling'),
    
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
    """Infers the minor category."""
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

def infer_lead_categories(name="", job_title="", current_cat=""):
    """
    Returns both Minor Category and Major Category tuple:
    (major_name, minor_name, major_icon, major_id)
    """
    minor = infer_biz_category(name, job_title, current_cat)
    major = get_major_category(minor, text=f"{name} {job_title}")
    return (major["name"], minor, major["icon"], major["id"])
