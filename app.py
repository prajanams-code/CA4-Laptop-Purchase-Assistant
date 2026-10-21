import re
import base64
import html as _html
from functools import lru_cache

import pandas as pd
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="LapGenie - Laptop Purchase Assistant",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# THEME / CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp { font-family: 'Poppins', sans-serif; }

.stApp {
    background: linear-gradient(-45deg, #1e1b4b, #4c1d95, #be185d, #0e7490, #1e3a8a);
    background-size: 400% 400%;
    animation: bgshift 18s ease infinite;
}
@keyframes bgshift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1250px; }
header[data-testid="stHeader"] { background: transparent; }

/* text on the gradient */
.stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
[data-testid="stWidgetLabel"] p, [data-testid="stMetricValue"],
[data-testid="stMetricLabel"] p, [data-testid="stCaptionContainer"] { color: #f8fafc; }

/* sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1b4b 0%, #312e81 60%, #581c87 100%);
}
[data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color: #f1f5f9; }

/* hero */
.hero {
    background: rgba(255,255,255,0.10);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 26px;
    padding: 34px 38px;
    margin-bottom: 22px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.25);
}
.hero h1 {
    font-size: 46px; font-weight: 800; margin: 0 0 6px 0;
    background: linear-gradient(90deg, #fde68a, #f9a8d4, #a5f3fc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { font-size: 18px; color: #e2e8f0 !important; margin: 0; }
.hstats { display: flex; gap: 14px; margin-top: 20px; flex-wrap: wrap; }
.hstat {
    background: rgba(255,255,255,0.14); border-radius: 16px;
    padding: 10px 20px; color: #fff; font-weight: 600; font-size: 15px;
}
.hstat b { font-size: 22px; display: block; color: #fde68a; }

/* tabs */
.stTabs [data-baseweb="tab-list"] { gap: 10px; }
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.12); border-radius: 14px;
    padding: 10px 22px; color: #fff; font-weight: 600;
}
.stTabs [aria-selected="true"] { background: linear-gradient(90deg, #f472b6, #8b5cf6); }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

/* buttons */
.stButton > button, .stFormSubmitButton > button {
    border-radius: 999px; font-weight: 600;
    background: rgba(255,255,255,0.16); color: #fff;
    border: 1px solid rgba(255,255,255,0.4); transition: all .2s;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: linear-gradient(90deg, #f472b6, #8b5cf6);
    border-color: transparent; color: #fff; transform: translateY(-2px);
}

/* chat */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px; backdrop-filter: blur(8px); margin-bottom: 12px;
}
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] td, [data-testid="stChatMessage"] th { color: #f8fafc; }
[data-testid="stChatMessage"] table { background: rgba(0,0,0,0.25); border-radius: 10px; }

/* product card */
.pcard, .pcard * { color: #1f2937 !important; }
.pcard {
    background: #fff; border-radius: 20px; overflow: hidden; position: relative;
    box-shadow: 0 10px 30px rgba(0,0,0,0.28); margin-bottom: 18px; transition: all .25s;
    border: 1px solid rgba(255,255,255,0.5);
}
.pcard:hover { transform: translateY(-6px) scale(1.01); box-shadow: 0 18px 44px rgba(0,0,0,0.38); }
.pimg { height: 175px; background: #e2e8f0; overflow: hidden; }
.pimg img { width: 100%; height: 100%; object-fit: cover; display: block; }
.pbody { padding: 14px 16px 16px 16px; }
.pcard .pname { font-size: 17px; font-weight: 700; line-height: 1.25; }
.pcard .pbrand { font-size: 12px; color: #6b7280 !important; font-weight: 600; letter-spacing: .6px; text-transform: uppercase; }
.pcard .price { font-size: 25px; font-weight: 800; color: #7c3aed !important; margin: 4px 0 6px 0; }
.pcard .chip {
    display: inline-block; background: #eef2ff; border-radius: 999px;
    padding: 3px 10px; font-size: 12px; margin: 2px 4px 2px 0; font-weight: 600;
}
.pcard .use { background: #fdf2f8; }
.pcard .stars { color: #f59e0b !important; font-weight: 700; font-size: 14px; margin-top: 6px; }
.pcard .badge {
    position: absolute; top: 10px; left: 10px; z-index: 2;
    background: linear-gradient(90deg, #f59e0b, #ef4444);
    color: #fff !important; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 700;
}
.sbar { height: 7px; background: #fee2e2; border-radius: 99px; overflow: hidden; margin-top: 8px; }
.sfill { height: 100%; background: linear-gradient(90deg, #22c55e, #84cc16); }
.stxt { font-size: 12px; color: #4b5563 !important; margin-top: 4px; }

/* compare table */
.ctable, .ctable * { color: #1f2937 !important; }
.ctable { width: 100%; border-collapse: collapse; background: #fff; border-radius: 16px; overflow: hidden; }
.ctable th { background: linear-gradient(90deg, #7c3aed, #db2777); color: #fff !important; padding: 12px; text-align: left; }
.ctable th * { color: #fff !important; }
.ctable td { padding: 11px 12px; border-bottom: 1px solid #eef2f7; }
.ctable td.best { background: #dcfce7; font-weight: 700; }

/* reviews */
.rev, .rev * { color: #1f2937 !important; }
.rev { padding: 12px 16px; border-radius: 14px; margin-bottom: 10px; font-size: 15px; }
.rev.pos { background: #dcfce7; border-left: 6px solid #22c55e; }
.rev.neg { background: #fee2e2; border-left: 6px solid #ef4444; }
.rev.neu { background: #fef9c3; border-left: 6px solid #eab308; }

.section-title { font-size: 26px; font-weight: 700; color: #fff; margin: 14px 0 10px 0; }
.footer { text-align: center; color: #e2e8f0; margin-top: 40px; font-size: 14px; opacity: .9; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA
# ============================================================
PRODUCTS = [
    {"id": 1, "name": "Lenovo IdeaPad Slim 3", "brand": "Lenovo", "price": 45000,
     "processor": "Intel Core i3", "ram": 8, "storage": "512 GB SSD", "use_case": "Study", "rating": 4.1,
     "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80"},
    {"id": 2, "name": "HP 15s", "brand": "HP", "price": 52000,
     "processor": "Intel Core i5", "ram": 8, "storage": "512 GB SSD", "use_case": "Office", "rating": 4.2,
     "image": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=900&q=80"},
    {"id": 3, "name": "Lenovo ThinkBook 15", "brand": "Lenovo", "price": 58000,
     "processor": "Intel Core i5", "ram": 16, "storage": "512 GB SSD", "use_case": "Office", "rating": 4.3,
     "image": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?auto=format&fit=crop&w=900&q=80"},
    {"id": 4, "name": "ASUS Vivobook 15", "brand": "ASUS", "price": 65000,
     "processor": "Intel Core i5", "ram": 16, "storage": "512 GB SSD", "use_case": "Coding", "rating": 4.4,
     "image": "https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?auto=format&fit=crop&w=900&q=80"},
    {"id": 5, "name": "HP Pavilion 15", "brand": "HP", "price": 72000,
     "processor": "Intel Core i5", "ram": 16, "storage": "512 GB SSD", "use_case": "Gaming", "rating": 4.5,
     "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=900&q=80"},
    {"id": 6, "name": "ASUS TUF Gaming F15", "brand": "ASUS", "price": 78000,
     "processor": "Intel Core i7", "ram": 16, "storage": "1 TB SSD", "use_case": "Gaming", "rating": 4.6,
     "image": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=900&q=80"},
    {"id": 7, "name": "Lenovo IdeaPad Gaming 3", "brand": "Lenovo", "price": 85000,
     "processor": "AMD Ryzen 7", "ram": 16, "storage": "1 TB SSD", "use_case": "Gaming", "rating": 4.5,
     "image": "https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?auto=format&fit=crop&w=900&q=80"},
    {"id": 8, "name": "HP Envy 16", "brand": "HP", "price": 95000,
     "processor": "Intel Core i7", "ram": 32, "storage": "1 TB SSD", "use_case": "Designing", "rating": 4.7,
     "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=80"},
]
product_df = pd.DataFrame(PRODUCTS)
BY_ID = {p["id"]: p for p in PRODUCTS}

ALIASES = {
    1: ["ideapad slim", "slim 3", "slim3"],
    2: ["hp 15s", "15s"],
    3: ["thinkbook", "think book"],
    4: ["vivobook", "viva book"],
    5: ["pavilion"],
    6: ["tuf"],
    7: ["ideapad gaming", "gaming 3"],
    8: ["envy"],
}

DEFAULT_REVIEWS = [
    (1, "The laptop is excellent for students and everyday work."),
    (1, "Battery life is good and the laptop is easy to carry."),
    (2, "Good performance for office work and online meetings."),
    (2, "The display is decent but the battery could be better."),
    (3, "Very happy with the performance and keyboard."),
    (3, "Good laptop for office work and multitasking."),
    (4, "Excellent laptop for coding and programming."),
    (4, "Very good performance and smooth multitasking."),
    (5, "Good gaming performance and attractive design."),
    (5, "The laptop overheats during long gaming sessions."),
    (6, "Excellent gaming performance and fast processor."),
    (6, "Great cooling and a very responsive keyboard for gaming."),
    (7, "Very good gaming laptop with strong performance."),
    (7, "Fans get loud under heavy load, which is annoying."),
    (8, "Stunning display, perfect for design and video editing."),
    (8, "Powerful and smooth, but it is quite expensive."),
]

BRAND_COLORS = {"HP": ("#0ea5e9", "#6366f1"), "Lenovo": ("#ef4444", "#f97316"), "ASUS": ("#8b5cf6", "#ec4899")}

# ============================================================
# SESSION STATE
# ============================================================
if "reviews" not in st.session_state:
    st.session_state.reviews = list(DEFAULT_REVIEWS)
if "prefs" not in st.session_state:
    st.session_state.prefs = {}

GREETING = ("Hi there! 👋 I'm **LapGenie**, your laptop buying buddy. Tell me your **budget** and what you'll use "
            "the laptop for (study, office, coding, gaming or designing) and I'll show you the best matches "
            "with photos, ratings and review sentiment. Try the quick buttons below! ✨")
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": GREETING, "ids": []}]

# ============================================================
# SENTIMENT
# ============================================================
analyzer = SentimentIntensityAnalyzer()


@lru_cache(maxsize=2048)
def sentiment(text):
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive"
    if score <= -0.05:
        return "Negative"
    return "Neutral"


def review_stats(pid):
    labels = [sentiment(t) for p, t in st.session_state.reviews if p == pid]
    n = len(labels)
    if n == 0:
        return 0, 0
    return n, int(round(100 * labels.count("Positive") / n))


# ============================================================
# HTML HELPERS
# ============================================================
def clean(s):
    return "\n".join(line.strip() for line in s.split("\n") if line.strip())


def fallback_img(p):
    c1, c2 = BRAND_COLORS.get(p["brand"], ("#6366f1", "#ec4899"))
    name = _html.escape(p["name"])
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 250">'
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/>'
        f'<stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
        '<rect width="400" height="250" fill="url(#g)"/>'
        '<rect x="95" y="35" width="210" height="135" rx="10" fill="#0f172a"/>'
        '<rect x="105" y="45" width="190" height="115" rx="6" fill="#38bdf8" opacity=".85"/>'
        '<path d="M60 182h280l22 22H38z" fill="#e2e8f0"/>'
        f'<text x="200" y="110" font-family="Arial" font-size="22" font-weight="700" fill="#fff" text-anchor="middle">{p["brand"]}</text>'
        f'<text x="200" y="236" font-family="Arial" font-size="15" font-weight="700" fill="#fff" text-anchor="middle">{name}</text>'
        '</svg>'
    )
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def card(p, badge=None):
    n, pos = review_stats(p["id"])
    if n:
        sent = (f'<div class="sbar"><div class="sfill" style="width:{pos}%"></div></div>'
                f'<div class="stxt">😊 {pos}% positive · {n} reviews</div>')
    else:
        sent = '<div class="stxt">No reviews yet</div>'
    full = int(round(p["rating"]))
    stars = "★" * full + "☆" * (5 - full)
    badge_html = f'<div class="badge">{badge}</div>' if badge else ""
    img = p["image"]
    fb = fallback_img(p)
    name = _html.escape(p["name"])
    return clean(f"""
    <div class="pcard">
    {badge_html}
    <div class="pimg"><img src="{img}" alt="{name}" loading="lazy" onerror="this.onerror=null;this.src='{fb}'"></div>
    <div class="pbody">
    <div class="pbrand">{p['brand']}</div>
    <div class="pname">{name}</div>
    <div class="price">₹{p['price']:,}</div>
    <span class="chip">⚙️ {p['processor']}</span>
    <span class="chip">🧠 {p['ram']}GB RAM</span>
    <span class="chip">💾 {p['storage']}</span>
    <span class="chip use">🎯 {p['use_case']}</span>
    <div class="stars">{stars} {p['rating']}/5</div>
    {sent}
    </div>
    </div>
    """)


def show_cards(ids, cols_n=3, top_badge=False):
    for start in range(0, len(ids), cols_n):
        chunk = ids[start:start + cols_n]
        cols = st.columns(cols_n)
        for i, pid in enumerate(chunk):
            badge = "🏆 Top pick" if (top_badge and start == 0 and i == 0) else None
            with cols[i]:
                st.markdown(card(BY_ID[pid], badge), unsafe_allow_html=True)


# ============================================================
# NLP: ENTITY EXTRACTION
# ============================================================
USE_KEYS = {
    "Gaming": ["gaming", "game", "games", "gamer"],
    "Coding": ["coding", "programming", "developer", "programmer", "code", "software"],
    "Designing": ["design", "designing", "designer", "editing", "photoshop", "creative"],
    "Study": ["study", "student", "students", "college", "school"],
    "Office": ["office", "business", "work", "meetings"],
}


def has(text, words):
    return any(re.search(rf"\b{re.escape(w)}\b", text) for w in words)


def extract_budget(text):
    t = text.lower().replace(",", "").replace("₹", "")
    t = re.sub(r"\brs\.?\s*", "", t)
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|lac|lacs)\b", t)
    if m:
        return int(float(m.group(1)) * 100000)
    m = re.search(r"(\d+(?:\.\d+)?)\s*k\b", t)
    if m:
        return int(float(m.group(1)) * 1000)
    nums = re.findall(r"\b\d{5,6}\b", t)
    return int(nums[0]) if nums else None


def extract_ram(text):
    m = re.search(r"\b(8|16|32)\s*gb\b", text.lower())
    return int(m.group(1)) if m else None


def extract_cpu(text):
    t = text.lower()
    m = re.search(r"\bi([357])\b", t)
    if m:
        return "i" + m.group(1)
    if "ryzen" in t:
        return "ryzen"
    return None


def extract_brand(text):
    m = re.search(r"\b(hp|lenovo|asus)\b", text.lower())
    if not m:
        return None
    return {"hp": "HP", "lenovo": "Lenovo", "asus": "ASUS"}[m.group(1)]


def extract_use(text):
    t = text.lower()
    for use, words in USE_KEYS.items():
        if has(t, words):
            return use
    return None


def find_products(text):
    t = text.lower()
    hits = []
    for pid, p in BY_ID.items():
        names = [p["name"].lower()] + ALIASES[pid]
        positions = [t.find(n) for n in names if n in t]
        if positions:
            hits.append((min(positions), pid))
    hits.sort()
    return [pid for _, pid in hits]


# ============================================================
# RECOMMENDATION ENGINE
# ============================================================
def recommend(prefs, sort="rating", top=3):
    df = product_df.copy()
    notes = []
    budget = prefs.get("budget")
    if budget:
        sub = df[df["price"] <= budget]
        if sub.empty:
            notes.append(f"Nothing fits under ₹{budget:,}, so here are the cheapest options available.")
            return df.sort_values("price").head(top), notes
        df = sub

    def apply(mask_fn, label):
        nonlocal df
        sub = df[mask_fn(df)]
        if sub.empty:
            notes.append(f"No exact match for **{label}** in that budget, so I relaxed it.")
        else:
            df = sub

    if prefs.get("use_case"):
        apply(lambda d: d["use_case"] == prefs["use_case"], prefs["use_case"])
    if prefs.get("brand"):
        apply(lambda d: d["brand"] == prefs["brand"], prefs["brand"])
    if prefs.get("cpu"):
        apply(lambda d: d["processor"].str.lower().str.contains(prefs["cpu"]), prefs["cpu"].upper())
    if prefs.get("ram"):
        apply(lambda d: d["ram"] >= prefs["ram"], f"{prefs['ram']}GB+ RAM")

    if sort == "price":
        df = df.sort_values(["price", "rating"], ascending=[True, False])
    else:
        df = df.sort_values(["rating", "price"], ascending=[False, True])
    return df.head(top), notes


def prefs_summary(prefs):
    parts = []
    if prefs.get("budget"):
        parts.append(f"💰 up to ₹{prefs['budget']:,}")
    if prefs.get("use_case"):
        parts.append(f"🎯 {prefs['use_case']}")
    if prefs.get("brand"):
        parts.append(f"🏷️ {prefs['brand']}")
    if prefs.get("cpu"):
        parts.append(f"⚙️ {prefs['cpu'].upper()}")
    if prefs.get("ram"):
        parts.append(f"🧠 {prefs['ram']}GB+")
    return "  ·  ".join(parts) if parts else "anything"


def why(p, prefs):
    reasons = [f"rated **{p['rating']}/5**"]
    if prefs.get("budget"):
        reasons.append(f"₹{prefs['budget'] - p['price']:,} under your budget")
    if prefs.get("use_case") and p["use_case"] == prefs["use_case"]:
        reasons.append(f"built for **{p['use_case'].lower()}**")
    n, pos = review_stats(p["id"])
    if n:
        reasons.append(f"**{pos}%** positive reviews")
    return ", ".join(reasons)


# ============================================================
# CHATBOT BRAIN
# ============================================================
def spec_table(ids):
    names = [BY_ID[i]["name"] for i in ids]
    rows = [
        ("Price", [f"₹{BY_ID[i]['price']:,}" for i in ids]),
        ("Processor", [BY_ID[i]["processor"] for i in ids]),
        ("RAM", [f"{BY_ID[i]['ram']}GB" for i in ids]),
        ("Storage", [BY_ID[i]["storage"] for i in ids]),
        ("Best for", [BY_ID[i]["use_case"] for i in ids]),
        ("Rating", [f"{BY_ID[i]['rating']}/5" for i in ids]),
        ("Positive reviews", [f"{review_stats(i)[1]}%" for i in ids]),
    ]
    out = "| Spec | " + " | ".join(names) + " |\n|---|" + "---|" * len(ids) + "\n"
    for label, vals in rows:
        out += f"| **{label}** | " + " | ".join(vals) + " |\n"
    return out


def handle(text):
    t = text.lower().strip()
    prefs = st.session_state.prefs
    mentioned = find_products(t)

    if has(t, ["bye", "goodbye", "exit", "quit", "thanks", "thank you"]):
        return {"text": "You're welcome! 😊 Happy laptop hunting. Come back anytime!", "ids": []}

    if has(t, ["reset", "start over", "clear preferences", "new search"]):
        st.session_state.prefs = {}
        return {"text": "Fresh start! 🔄 Tell me your budget and what you'll use the laptop for.", "ids": []}

    if has(t, ["help"]) or "what can you do" in t:
        return {"text": ("Here's what I can do 🚀\n\n"
                         "- **Recommend**: *“gaming laptop under 80k”*, *“coding laptop with 16GB”*\n"
                         "- **Compare**: *“compare HP Pavilion vs ASUS TUF”*\n"
                         "- **Reviews**: *“reviews of ASUS Vivobook”*\n"
                         "- **Details**: *“tell me about HP Envy”*\n"
                         "- **Quick picks**: *“cheapest laptop”*, *“top rated laptop”*\n\n"
                         "I remember what you tell me, so you can refine step by step, "
                         "e.g. *“make it Lenovo”* or *“budget 60k”*."), "ids": []}

    # ---- compare
    if has(t, ["compare", "vs", "versus", "difference", "between"]) or len(mentioned) >= 2:
        if len(mentioned) >= 2:
            ids = mentioned[:3]
            cheaper = min(ids, key=lambda i: BY_ID[i]["price"])
            rated = max(ids, key=lambda i: BY_ID[i]["rating"])
            ram = max(ids, key=lambda i: BY_ID[i]["ram"])
            txt = (f"Here's the head-to-head ⚖️\n\n{spec_table(ids)}\n"
                   f"💰 **Cheapest:** {BY_ID[cheaper]['name']}  \n"
                   f"⭐ **Best rated:** {BY_ID[rated]['name']}  \n"
                   f"🧠 **Most RAM:** {BY_ID[ram]['name']}")
            return {"text": txt, "ids": ids}
        top, _ = recommend(prefs, top=2)
        ids = top["id"].tolist()
        return {"text": "Tell me which laptops to compare, e.g. *“compare HP Pavilion and ASUS TUF”*. "
                        "Meanwhile, here are two strong candidates you could compare:", "ids": ids}

    # ---- reviews
    if has(t, ["review", "reviews", "feedback", "opinion", "opinions", "sentiment", "rating", "ratings"]) and mentioned:
        pid = mentioned[0]
        p = BY_ID[pid]
        revs = [(tx, sentiment(tx)) for q, tx in st.session_state.reviews if q == pid]
        n, pos = review_stats(pid)
        emoji = {"Positive": "😊", "Negative": "😞", "Neutral": "😐"}
        lines = "\n".join(f"- {emoji[s]} {tx} *({s})*" for tx, s in revs) or "- No reviews yet."
        return {"text": f"What customers say about **{p['name']}** 💬\n\n{lines}\n\n"
                        f"**Overall: {pos}% positive** across {n} reviews.", "ids": [pid]}
    if has(t, ["review", "reviews", "feedback", "opinion", "opinions", "sentiment"]):
        best = max(BY_ID, key=lambda i: (review_stats(i)[1], BY_ID[i]["rating"]))
        return {"text": "Which laptop's reviews do you want? Try *“reviews of HP Pavilion”*, or open the "
                        "**⭐ Reviews** tab to read and add your own. The best-reviewed laptop right now is:",
                "ids": [best]}

    # ---- product details
    if mentioned:
        pid = mentioned[0]
        p = BY_ID[pid]
        n, pos = review_stats(pid)
        txt = (f"Here's the **{p['name']}** 💻\n\n"
               f"It's a **{p['use_case'].lower()}**-focused laptop with a **{p['processor']}**, "
               f"**{p['ram']}GB RAM** and **{p['storage']}**, priced at **₹{p['price']:,}**. "
               f"Customers rate it **{p['rating']}/5** and **{pos}%** of {n} reviews are positive.\n\n"
               f"Want me to compare it with another model, or show its reviews?")
        return {"text": txt, "ids": [pid]}

    # ---- extract entities for search
    new = {
        "budget": extract_budget(text),
        "ram": extract_ram(text),
        "cpu": extract_cpu(text),
        "brand": extract_brand(text),
        "use_case": extract_use(text),
    }
    found = {k: v for k, v in new.items() if v}

    # ---- greeting
    if has(t, ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]) \
            and not found and len(t.split()) <= 5:
        return {"text": "Hello! 👋 What's your budget, and what will you mainly use the laptop for?", "ids": []}

    cheapest = has(t, ["cheapest", "cheap", "affordable", "lowest"])
    toprated = has(t, ["top rated", "highest rated", "best rated", "best"]) and not found
    wants_search = found or cheapest or toprated or has(
        t, ["laptop", "laptops", "recommend", "suggest", "show", "need", "want", "looking", "buy", "options"])

    if wants_search:
        prefs.update(found)
        top, notes = recommend(prefs, sort="price" if cheapest else "rating")
        ids = top["id"].tolist()
        best = BY_ID[ids[0]]
        head = "💸 Most affordable picks" if cheapest else ("🏆 Top-rated picks" if toprated else "🎯 Your matches")
        txt = f"**{head}**  \nLooking for: {prefs_summary(prefs)}\n\n"
        txt += f"My top pick is the **{best['name']}** — {why(best, prefs)}.\n\n"
        if notes:
            txt += "\n".join(f"ℹ️ {n}" for n in notes) + "\n\n"
        if not prefs.get("budget"):
            txt += "💡 Tell me your **budget** (e.g. *“under 70k”*) to narrow this down."
        elif not prefs.get("use_case"):
            txt += "💡 What will you mainly use it for: study, office, coding, gaming or designing?"
        else:
            txt += "💡 Want me to **compare** any two of these, or show their **reviews**?"
        return {"text": txt, "ids": ids, "rank": True}

    return {"text": ("Hmm, I didn't quite catch that 🤔. I can help with budgets, RAM, processors, brands, "
                     "use cases, comparisons and reviews. Try *“gaming laptop under 80k”* or type **help**."),
            "ids": []}


# ============================================================
# SIDEBAR
# ============================================================
def clear_chat():
    st.session_state.messages = [{"role": "assistant", "content": GREETING, "ids": []}]
    st.session_state.prefs = {}


st.sidebar.title("🔎 Filter Laptops")
st.sidebar.caption("These filters control the 🛍️ Browse tab.")
f_budget = st.sidebar.slider("Maximum budget (₹)", 40000, 100000, 100000, 5000)
f_ram = st.sidebar.selectbox("Minimum RAM (GB)", [8, 16, 32], index=0)
f_use = st.sidebar.selectbox("Primary use", ["All", "Study", "Office", "Coding", "Gaming", "Designing"])
f_brand = st.sidebar.selectbox("Brand", ["All", "HP", "Lenovo", "ASUS"])
f_cpu = st.sidebar.selectbox("Processor", ["All", "Intel Core i3", "Intel Core i5", "Intel Core i7", "AMD Ryzen 7"])
st.sidebar.markdown("---")
st.sidebar.button("🧹 Clear chat & preferences", on_click=clear_chat, use_container_width=True)

# ============================================================
# HERO
# ============================================================
total_reviews = len(st.session_state.reviews)
avg_rating = product_df["rating"].mean()
st.markdown(clean(f"""
<div class="hero">
<h1>💻 LapGenie</h1>
<p>Your AI laptop buying assistant: tell it your budget and needs, get instant picks with photos, ratings and review sentiment.</p>
<div class="hstats">
<div class="hstat"><b>{len(PRODUCTS)}</b>Laptops</div>
<div class="hstat"><b>{avg_rating:.1f} ★</b>Avg rating</div>
<div class="hstat"><b>{total_reviews}</b>Reviews analysed</div>
<div class="hstat"><b>3</b>Brands</div>
</div>
</div>
"""), unsafe_allow_html=True)

tab_chat, tab_browse, tab_compare, tab_reviews = st.tabs(
    ["🤖 AI Assistant", "🛍️ Browse Laptops", "⚖️ Compare", "⭐ Reviews"]
)

# ============================================================
# TAB 1: CHAT
# ============================================================
with tab_chat:
    chat_box = st.container()

    CHIPS = [
        ("🎮 Gaming under ₹80k", "gaming laptop under 80k"),
        ("💼 Best for office", "laptop for office work"),
        ("👨‍💻 Coding, 16GB RAM", "coding laptop with 16gb ram"),
        ("🎨 Designing laptop", "laptop for designing"),
        ("💰 Cheapest laptop", "cheapest laptop"),
        ("⚖️ Pavilion vs TUF", "compare hp pavilion and asus tuf"),
    ]
    chip_cols = st.columns(3)
    pending = None
    for i, (label, query) in enumerate(CHIPS):
        if chip_cols[i % 3].button(label, key=f"chip_{i}", use_container_width=True):
            pending = query

    user_input = st.chat_input("Ask me anything, e.g. “I need a laptop under ₹70000 for coding”")
    text = user_input or pending

    if text:
        st.session_state.messages.append({"role": "user", "content": text, "ids": []})
        reply = handle(text)
        st.session_state.messages.append({
            "role": "assistant", "content": reply["text"],
            "ids": reply.get("ids", []), "rank": reply.get("rank", False),
        })

    with chat_box:
        for m in st.session_state.messages[-8:]:
            with st.chat_message(m["role"], avatar="🤖" if m["role"] == "assistant" else "🧑"):
                st.markdown(m["content"])
                if m.get("ids"):
                    show_cards(m["ids"], cols_n=3, top_badge=m.get("rank", False))

# ============================================================
# TAB 2: BROWSE
# ============================================================
with tab_browse:
    st.markdown('<div class="section-title">🛍️ Browse the collection</div>', unsafe_allow_html=True)
    sort_by = st.radio("Sort by", ["Rating ⭐", "Price: low to high", "Price: high to low"], horizontal=True)

    filtered = product_df[(product_df["price"] <= f_budget) & (product_df["ram"] >= f_ram)]
    if f_use != "All":
        filtered = filtered[filtered["use_case"] == f_use]
    if f_brand != "All":
        filtered = filtered[filtered["brand"] == f_brand]
    if f_cpu != "All":
        filtered = filtered[filtered["processor"] == f_cpu]

    if sort_by.startswith("Rating"):
        filtered = filtered.sort_values("rating", ascending=False)
    elif sort_by == "Price: low to high":
        filtered = filtered.sort_values("price")
    else:
        filtered = filtered.sort_values("price", ascending=False)

    if filtered.empty:
        st.warning("No laptops match these filters. Try a higher budget or reset a filter in the sidebar.")
        near = product_df.assign(d=(product_df["price"] - f_budget).abs()).sort_values("d").head(3)
        st.markdown("**Closest alternatives:**")
        show_cards(near["id"].tolist())
    else:
        st.caption(f"Showing {len(filtered)} laptop(s)")
        show_cards(filtered["id"].tolist())

# ============================================================
# TAB 3: COMPARE
# ============================================================
with tab_compare:
    st.markdown('<div class="section-title">⚖️ Side-by-side comparison</div>', unsafe_allow_html=True)
    chosen = st.multiselect(
        "Pick 2 or 3 laptops", list(BY_ID.keys()), default=[5, 6],
        format_func=lambda i: BY_ID[i]["name"], max_selections=3,
    )
    if len(chosen) < 2:
        st.info("Select at least two laptops to compare.")
    else:
        show_cards(chosen, cols_n=len(chosen))
        data = {
            "Price": [BY_ID[i]["price"] for i in chosen],
            "RAM": [BY_ID[i]["ram"] for i in chosen],
            "Rating": [BY_ID[i]["rating"] for i in chosen],
            "Positive reviews": [review_stats(i)[1] for i in chosen],
        }
        best = {
            "Price": min(data["Price"]), "RAM": max(data["RAM"]),
            "Rating": max(data["Rating"]), "Positive reviews": max(data["Positive reviews"]),
        }
        fmt = {"Price": lambda v: f"₹{v:,}", "RAM": lambda v: f"{v}GB",
               "Rating": lambda v: f"{v}/5", "Positive reviews": lambda v: f"{v}%"}
        head = "".join(f"<th>{_html.escape(BY_ID[i]['name'])}</th>" for i in chosen)
        body = ""
        for key in data:
            cells = "".join(
                f'<td class="{"best" if v == best[key] else ""}">{fmt[key](v)}</td>' for v in data[key])
            body += f"<tr><td><b>{key}</b></td>{cells}</tr>"
        for key, col in [("Processor", "processor"), ("Storage", "storage"), ("Best for", "use_case")]:
            cells = "".join(f"<td>{BY_ID[i][col]}</td>" for i in chosen)
            body += f"<tr><td><b>{key}</b></td>{cells}</tr>"
        st.markdown(clean(f'<table class="ctable"><tr><th>Spec</th>{head}</tr>{body}</table>'),
                    unsafe_allow_html=True)
        st.caption("Green cells mark the best value in each category (lowest price, highest RAM / rating / sentiment).")
        chart_df = pd.DataFrame({"Price (₹)": data["Price"]}, index=[BY_ID[i]["name"] for i in chosen])
        st.bar_chart(chart_df)

# ============================================================
# TAB 4: REVIEWS
# ============================================================
with tab_reviews:
    st.markdown('<div class="section-title">⭐ Customer reviews & sentiment</div>', unsafe_allow_html=True)
    sel = st.selectbox("Choose a laptop", list(BY_ID.keys()), format_func=lambda i: BY_ID[i]["name"], key="rev_sel")
    left, right = st.columns([1, 2])
    with left:
        st.markdown(card(BY_ID[sel]), unsafe_allow_html=True)
    with right:
        revs = [(tx, sentiment(tx)) for q, tx in st.session_state.reviews if q == sel]
        pos = sum(1 for _, s in revs if s == "Positive")
        neg = sum(1 for _, s in revs if s == "Negative")
        neu = sum(1 for _, s in revs if s == "Neutral")
        m1, m2, m3 = st.columns(3)
        m1.metric("😊 Positive", pos)
        m2.metric("😞 Negative", neg)
        m3.metric("😐 Neutral", neu)
        emoji = {"Positive": "😊", "Negative": "😞", "Neutral": "😐"}
        cls = {"Positive": "pos", "Negative": "neg", "Neutral": "neu"}
        if not revs:
            st.info("No reviews yet. Be the first to add one below!")
        for tx, s in revs:
            st.markdown(f'<div class="rev {cls[s]}">{emoji[s]} {_html.escape(tx)}<br><b>Sentiment: {s}</b></div>',
                        unsafe_allow_html=True)

        with st.form("add_review", clear_on_submit=True):
            new_review = st.text_area("✍️ Add your own review (analysed instantly with VADER)", height=80)
            submitted = st.form_submit_button("Analyse & add review")
        if submitted and new_review.strip():
            st.session_state.reviews.append((sel, new_review.strip()))
            s = sentiment(new_review.strip())
            st.success(f"Review added! Detected sentiment: {emoji[s]} {s}")
            st.rerun()

# ============================================================
# FOOTER
# ============================================================
st.markdown(clean("""
<div class="footer">
<b>AI-Powered E-Commerce Chatbot</b><br>
Laptop Purchase Assistant | CA4 Project<br>
Developed by M S Prajana
</div>
"""), unsafe_allow_html=True)
