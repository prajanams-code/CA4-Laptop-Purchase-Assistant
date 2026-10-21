
import streamlit as st
import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Laptop Purchase Assistant",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,0.18), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(14,165,233,0.15), transparent 30%),
        linear-gradient(135deg, #f8fafc 0%, #eef2ff 50%, #f0f9ff 100%);
}

/* Remove unnecessary top padding */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* HERO */
.hero {
    background: linear-gradient(135deg, #111827, #312e81, #2563eb);
    padding: 42px;
    border-radius: 28px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 20px 50px rgba(37, 99, 235, 0.25);
}

.hero h1 {
    font-size: 46px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    font-size: 18px;
    opacity: 0.92;
}

.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    padding: 7px 14px;
    border-radius: 50px;
    font-size: 13px;
    margin-bottom: 15px;
}

/* SECTION TITLES */

.section-title {
    font-size: 27px;
    font-weight: 800;
    color: #111827;
    margin-top: 30px;
    margin-bottom: 18px;
}

/* STAT CARDS */

.stat-card {
    background: rgba(255,255,255,0.85);
    border: 1px solid rgba(255,255,255,0.8);
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 8px 25px rgba(15,23,42,0.07);
    text-align: center;
}

.stat-number {
    font-size: 28px;
    font-weight: 800;
    color: #2563eb;
}

.stat-label {
    color: #64748b;
    font-size: 13px;
}

/* PRODUCT CARDS */

.product-card {
    background: rgba(255,255,255,0.95);
    border: 1px solid #e5e7eb;
    border-radius: 22px;
    padding: 14px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(15,23,42,0.08);
    transition: all 0.25s ease;
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 18px 40px rgba(37,99,235,0.15);
}

.product-title {
    font-size: 19px;
    font-weight: 800;
    color: #111827;
    margin-top: 10px;
}

.product-brand {
    color: #64748b;
    font-size: 13px;
}

.product-price {
    font-size: 25px;
    font-weight: 800;
    color: #2563eb;
    margin: 8px 0;
}

.product-info {
    background: #f8fafc;
    padding: 10px;
    border-radius: 12px;
    margin-top: 8px;
    font-size: 13px;
}

.rating {
    color: #f59e0b;
    font-weight: 700;
}

/* CHAT */

.chat-user {
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    color: white;
    padding: 13px 17px;
    border-radius: 18px 18px 5px 18px;
    margin: 8px 0;
    margin-left: 15%;
}

.chat-bot {
    background: white;
    color: #111827;
    padding: 15px 18px;
    border-radius: 18px 18px 18px 5px;
    margin: 8px 0;
    margin-right: 15%;
    border: 1px solid #e5e7eb;
    box-shadow: 0 5px 18px rgba(15,23,42,0.06);
}

/* FILTER BOX */

.filter-box {
    background: rgba(255,255,255,0.9);
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #e5e7eb;
}

/* INFO BOX */

.info-box {
    background: linear-gradient(135deg, #eef2ff, #eff6ff);
    border: 1px solid #c7d2fe;
    border-radius: 18px;
    padding: 18px;
    margin: 10px 0;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #64748b;
    padding: 30px;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# PRODUCT DATABASE
# ============================================================

products = [
    {
        "id": 1,
        "name": "Lenovo IdeaPad Slim 3",
        "brand": "Lenovo",
        "price": 45000,
        "processor": "Intel Core i3",
        "ram": 8,
        "storage": "512 GB SSD",
        "use_case": "Study",
        "rating": 4.1,
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80"
    },
    {
        "id": 2,
        "name": "HP 15s",
        "brand": "HP",
        "price": 52000,
        "processor": "Intel Core i5",
        "ram": 8,
        "storage": "512 GB SSD",
        "use_case": "Office",
        "rating": 4.2,
        "image": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=900&q=80"
    },
    {
        "id": 3,
        "name": "Lenovo ThinkBook 15",
        "brand": "Lenovo",
        "price": 58000,
        "processor": "Intel Core i5",
        "ram": 16,
        "storage": "512 GB SSD",
        "use_case": "Office",
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?auto=format&fit=crop&w=900&q=80"
    },
    {
        "id": 4,
        "name": "ASUS Vivobook 15",
        "brand": "ASUS",
        "price": 65000,
        "processor": "Intel Core i5",
        "ram": 16,
        "storage": "512 GB SSD",
        "use_case": "Coding",
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?auto=format&fit=crop&w=900&q=80"
    },
    {
        "id": 5,
        "name": "HP Pavilion 15",
        "brand": "HP",
        "price": 72000,
        "processor": "Intel Core i5",
        "ram": 16,
        "storage": "512 GB SSD",
        "use_case": "Gaming",
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=900&q=80"
    },
    {
        "id": 6,
        "name": "ASUS TUF Gaming F15",
        "brand": "ASUS",
        "price": 78000,
        "processor": "Intel Core i7",
        "ram": 16,
        "storage": "1 TB SSD",
        "use_case": "Gaming",
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=900&q=80"
    },
    {
        "id": 7,
        "name": "Lenovo IdeaPad Gaming 3",
        "brand": "Lenovo",
        "price": 85000,
        "processor": "AMD Ryzen 7",
        "ram": 16,
        "storage": "1 TB SSD",
        "use_case": "Gaming",
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?auto=format&fit=crop&w=900&q=80"
    },
    {
        "id": 8,
        "name": "HP Envy 16",
        "brand": "HP",
        "price": 95000,
        "processor": "Intel Core i7",
        "ram": 32,
        "storage": "1 TB SSD",
        "use_case": "Designing",
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80"
    }
]

product_df = pd.DataFrame(products)


# ============================================================
# REVIEWS
# ============================================================

reviews = [
    [1, "The laptop is excellent for students and everyday work."],
    [1, "Battery life is good and the laptop is easy to carry."],
    [2, "Good performance for office work and online meetings."],
    [2, "The display is decent but the battery could be better."],
    [3, "Very happy with the performance and keyboard."],
    [3, "Good laptop for office work and multitasking."],
    [4, "Excellent laptop for coding and programming."],
    [4, "Very good performance and smooth multitasking."],
    [5, "Good gaming performance and attractive design."],
    [5, "The laptop overheats during long gaming sessions."],
    [6, "Excellent gaming performance and fast processor."],
    [7, "Very good gaming laptop with strong performance."]
]

review_df = pd.DataFrame(
    reviews,
    columns=["product_id", "review"]
)


# ============================================================
# SENTIMENT ANALYSIS
# ============================================================

analyzer = SentimentIntensityAnalyzer()


def get_sentiment(text):

    score = analyzer.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "Positive"

    elif score <= -0.05:
        return "Negative"

    return "Neutral"


review_df["sentiment"] = review_df["review"].apply(get_sentiment)


# ============================================================
# INTENT RECOGNITION
# ============================================================

intents = {

    "GREETING": [
        "hi", "hello", "hey",
        "good morning", "good evening"
    ],

    "LAPTOP_SEARCH": [
        "laptop", "notebook", "computer",
        "buy", "looking"
    ],

    "BUDGET": [
        "budget", "price", "cost",
        "under", "afford", "cheap"
    ],

    "PROCESSOR": [
        "processor", "cpu",
        "i3", "i5", "i7", "ryzen"
    ],

    "RAM": [
        "ram", "memory",
        "8gb", "16gb", "32gb"
    ],

    "USE_CASE": [
        "study", "student", "college",
        "office", "work",
        "coding", "programming",
        "gaming", "design", "editing"
    ],

    "RECOMMENDATION": [
        "recommend", "suggest",
        "best", "suitable", "which laptop"
    ],

    "REVIEW_QUERY": [
        "review", "reviews",
        "rating", "feedback"
    ],

    "COMPARISON": [
        "compare", "comparison",
        "difference", "versus", "vs"
    ],

    "GOODBYE": [
        "bye", "goodbye",
        "exit", "quit",
        "thanks", "thank you"
    ]
}


def detect_intent(message):

    message = message.lower()

    for intent, keywords in intents.items():

        for keyword in keywords:

            if keyword in message:
                return intent

    return "FALLBACK"


# ============================================================
# ENTITY EXTRACTION
# ============================================================

def extract_budget(text):

    text = text.lower().replace(",", "").replace("₹", "")

    match = re.search(
        r'(\d+(?:\.\d+)?)\s*k\b',
        text
    )

    if match:
        return int(float(match.group(1)) * 1000)

    numbers = re.findall(
        r'\b\d{4,6}\b',
        text
    )

    if numbers:
        return int(numbers[0])

    return None


def extract_ram(text):

    match = re.search(
        r'\b(8|16|32)\s*(?:gb|g)\b',
        text.lower()
    )

    if match:
        return int(match.group(1))

    return None


def extract_processor(text):

    text = text.lower()

    if "i7" in text:
        return "Intel Core i7"

    if "i5" in text:
        return "Intel Core i5"

    if "i3" in text:
        return "Intel Core i3"

    if "ryzen 7" in text:
        return "AMD Ryzen 7"

    if "ryzen" in text:
        return "AMD Ryzen"

    return None


def extract_brand(text):

    text = text.lower()

    if "hp" in text:
        return "HP"

    if "lenovo" in text:
        return "Lenovo"

    if "asus" in text:
        return "ASUS"

    return None


def extract_use_case(text):

    text = text.lower()

    if any(word in text for word in ["gaming", "gamer", "games"]):
        return "Gaming"

    if any(word in text for word in ["coding", "programming", "developer"]):
        return "Coding"

    if any(word in text for word in ["design", "editing", "designer"]):
        return "Designing"

    if any(word in text for word in ["study", "student", "college"]):
        return "Study"

    if any(word in text for word in ["office", "work", "business"]):
        return "Office"

    return None


# ============================================================
# PRODUCT RECOMMENDATION ENGINE
# ============================================================

def recommend_products(
    budget=None,
    ram=None,
    use_case=None,
    brand=None,
    processor=None
):

    result = product_df.copy()

    if budget:
        result = result[
            result["price"] <= budget
        ]

    if ram:
        result = result[
            result["ram"] >= ram
        ]

    if use_case:
        result = result[
            result["use_case"].str.lower()
            == use_case.lower()
        ]

    if brand:
        result = result[
            result["brand"].str.lower()
            == brand.lower()
        ]

    if processor:
        result = result[
            result["processor"].str.lower()
            .str.contains(
                processor.lower(),
                na=False
            )
        ]

    # If no exact match, find closest options
    if result.empty:

        result = product_df.copy()

        if budget:

            result["distance"] = abs(
                result["price"] - budget
            )

            result = result.sort_values(
                "distance"
            )

        else:

            result = result.sort_values(
                "rating",
                ascending=False
            )

    else:

        result = result.sort_values(
            "rating",
            ascending=False
        )

    return result.head(3)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-badge">
🤖 AI-Powered E-Commerce Assistant
</div>

<h1>💻 Find Your Perfect Laptop</h1>

<p>
Smart laptop recommendations based on your budget,
performance requirements, preferred brand and intended use.
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown("## 🔎 Find Your Laptop")

st.sidebar.caption(
    "Use these filters to instantly explore suitable laptops."
)

budget = st.sidebar.slider(
    "💰 Maximum Budget",
    min_value=40000,
    max_value=100000,
    value=70000,
    step=5000
)

ram = st.sidebar.selectbox(
    "🧠 Minimum RAM",
    [8, 16, 32],
    index=1
)

use_case = st.sidebar.selectbox(
    "🎯 Primary Use",
    [
        "All",
        "Study",
        "Office",
        "Coding",
        "Gaming",
        "Designing"
    ]
)

brand = st.sidebar.selectbox(
    "🏷️ Preferred Brand",
    [
        "All",
        "HP",
        "Lenovo",
        "ASUS"
    ]
)

processor = st.sidebar.selectbox(
    "⚡ Processor",
    [
        "All",
        "Intel Core i3",
        "Intel Core i5",
        "Intel Core i7",
        "AMD Ryzen 7"
    ]
)


# ============================================================
# FILTER PRODUCTS
# ============================================================

filtered = product_df[
    product_df["price"] <= budget
]

filtered = filtered[
    filtered["ram"] >= ram
]

if use_case != "All":

    filtered = filtered[
        filtered["use_case"] == use_case
    ]

if brand != "All":

    filtered = filtered[
        filtered["brand"] == brand
    ]

if processor != "All":

    filtered = filtered[
        filtered["processor"] == processor
    ]


# ============================================================
# DASHBOARD STATISTICS
# ============================================================

st.markdown(
    '<div class="section-title">📊 Laptop Marketplace Overview</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        f"""
        <div class="stat-card">
        <div class="stat-number">{len(product_df)}</div>
        <div class="stat-label">Available Laptops</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        f"""
        <div class="stat-card">
        <div class="stat-number">{len(filtered)}</div>
        <div class="stat-label">Matching Results</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    avg_rating = product_df["rating"].mean()

    st.markdown(
        f"""
        <div class="stat-card">
        <div class="stat-number">⭐ {avg_rating:.1f}</div>
        <div class="stat-label">Average Rating</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:

    st.markdown(
        f"""
        <div class="stat-card">
        <div class="stat-number">₹{budget//1000}K</div>
        <div class="stat-label">Your Budget</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RECOMMENDED PRODUCTS
# ============================================================

st.markdown(
    '<div class="section-title">🛍️ Recommended Laptops</div>',
    unsafe_allow_html=True
)

if filtered.empty:

    st.warning(
        "No exact laptops match all your filters. "
        "Try increasing the budget or reducing the minimum RAM."
    )

else:

    cols = st.columns(3)

    for index, (_, product) in enumerate(
        filtered.sort_values(
            "rating",
            ascending=False
        ).head(6).iterrows()
    ):

        with cols[index % 3]:

            st.markdown(
                '<div class="product-card">',
                unsafe_allow_html=True
            )

            st.image(
                product["image"],
                use_container_width=True
            )

            st.markdown(
                f"""
                <div class="product-title">
                {product["name"]}
                </div>

                <div class="product-brand">
                {product["brand"]}
                </div>

                <div class="product-price">
                ₹{product["price"]:,}
                </div>

                <div class="product-info">
                ⚡ <b>{product["processor"]}</b><br>
                🧠 <b>{product["ram"]}GB RAM</b><br>
                💾 <b>{product["storage"]}</b><br>
                🎯 <b>{product["use_case"]}</b>
                </div>

                <br>

                <div class="rating">
                ⭐ {product["rating"]}/5
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "⭐ View Reviews",
                key=f"view_{product['id']}"
            ):

                st.session_state[
                    "selected_product"
                ] = product["id"]

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


# ============================================================
# QUICK RECOMMENDATION
# ============================================================

st.markdown(
    '<div class="section-title">⚡ Quick Recommendation</div>',
    unsafe_allow_html=True
)

recommendations = recommend_products(
    budget=budget,
    ram=ram,
    use_case=None if use_case == "All" else use_case,
    brand=None if brand == "All" else brand,
    processor=None if processor == "All" else processor
)

if not recommendations.empty:

    best = recommendations.iloc[0]

    left, right = st.columns([1, 1])

    with left:

        st.image(
            best["image"],
            use_container_width=True
        )

    with right:

        st.markdown(
            f"""
            ## 🏆 {best["name"]}

            **Brand:** {best["brand"]}

            **Price:** ₹{best["price"]:,}

            **Processor:** {best["processor"]}

            **RAM:** {best["ram"]}GB

            **Storage:** {best["storage"]}

            **Best for:** {best["use_case"]}

            **Rating:** ⭐ {best["rating"]}/5
            """
        )

        st.success(
            "This is the highest-rated suitable option "
            "based on your current preferences."
        )


# ============================================================
# REVIEWS AND SENTIMENT
# ============================================================

st.markdown(
    '<div class="section-title">⭐ Customer Reviews & Sentiment Analysis</div>',
    unsafe_allow_html=True
)

selected_product = st.selectbox(
    "Select a laptop",
    product_df["id"].tolist(),
    format_func=lambda x:
        product_df.loc[
            product_df["id"] == x,
            "name"
        ].iloc[0]
)

selected_reviews = review_df[
    review_df["product_id"] == selected_product
]

for _, review in selected_reviews.iterrows():

    if review["sentiment"] == "Positive":
        emoji = "😊"

    elif review["sentiment"] == "Negative":
        emoji = "😞"

    else:
        emoji = "😐"

    st.info(
        f'{emoji} {review["review"]}\n\n'
        f'**Sentiment: {review["sentiment"]}**'
    )

positive = sum(
    selected_reviews["sentiment"] == "Positive"
)

negative = sum(
    selected_reviews["sentiment"] == "Negative"
)

neutral = sum(
    selected_reviews["sentiment"] == "Neutral"
)

a, b, c = st.columns(3)

with a:
    st.metric("😊 Positive", positive)

with b:
    st.metric("😞 Negative", negative)

with c:
    st.metric("😐 Neutral", neutral)


# ============================================================
# PRODUCT COMPARISON
# ============================================================

st.markdown(
    '<div class="section-title">⚖️ Compare Laptops</div>',
    unsafe_allow_html=True
)

comparison_products = st.multiselect(
    "Choose up to 3 laptops",
    product_df["name"].tolist(),
    max_selections=3
)

if len(comparison_products) >= 2:

    comparison_df = product_df[
        product_df["name"].isin(comparison_products)
    ][
        [
            "name",
            "brand",
            "price",
            "processor",
            "ram",
            "storage",
            "use_case",
            "rating"
        ]
    ].copy()

    comparison_df.columns = [
        "Laptop",
        "Brand",
        "Price",
        "Processor",
        "RAM",
        "Storage",
        "Best For",
        "Rating"
    ]

    comparison_df["Price"] = comparison_df[
        "Price"
    ].apply(lambda x: f"₹{x:,}")

    comparison_df["RAM"] = comparison_df[
        "RAM"
    ].apply(lambda x: f"{x} GB")

    comparison_df["Rating"] = comparison_df[
        "Rating"
    ].apply(lambda x: f"⭐ {x}/5")

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.caption(
        "Select at least two laptops to compare them."
    )


# ============================================================
# CHATBOT
# ============================================================

st.markdown(
    '<div class="section-title">🤖 Chat With Your Laptop Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-box">
    💡 <b>Try asking:</b><br><br>
    • I need a laptop under ₹70000 for coding<br>
    • Which laptop has 16GB RAM?<br>
    • Suggest a gaming laptop<br>
    • I want an HP laptop under 80000<br>
    • Which laptop is best for students?<br>
    • Compare laptops<br>
    • Show me reviews
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CHAT MEMORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content":
            "Hello! 👋 I'm your Laptop Purchase Assistant. "
            "Tell me your budget, preferred use, RAM, brand or processor "
            "and I'll recommend suitable laptops."
        }
    ]


# Display messages

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="chat-user">
            👤 {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="chat-bot">
            🤖 {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Ask me anything about laptops..."
)


if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    intent = detect_intent(user_input)

    user_budget = extract_budget(user_input)
    user_ram = extract_ram(user_input)
    user_processor = extract_processor(user_input)
    user_brand = extract_brand(user_input)
    user_use_case = extract_use_case(user_input)


    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    if intent == "GREETING":

        response = (
            "Hello! 👋 I'm ready to help you find a laptop. "
            "Tell me your budget and what you mainly want to use it for."
        )


    # --------------------------------------------------------
    # GOODBYE
    # --------------------------------------------------------

    elif intent == "GOODBYE":

        response = (
            "Thank you for using the Laptop Purchase Assistant! "
            "Have a great day. 😊"
        )


    # --------------------------------------------------------
    # REVIEWS
    # --------------------------------------------------------

    elif intent == "REVIEW_QUERY":

        response = (
            "Sure! ⭐ You can select a laptop in the "
            "'Customer Reviews & Sentiment Analysis' section. "
            "The system displays customer feedback together with "
            "VADER sentiment classification."
        )


    # --------------------------------------------------------
    # COMPARISON
    # --------------------------------------------------------

    elif intent == "COMPARISON":

        response = (
            "Absolutely! ⚖️ Go to the 'Compare Laptops' section "
            "and select two or three laptops. The system will compare "
            "their price, processor, RAM, storage, use case and rating."
        )


    # --------------------------------------------------------
    # PRODUCT REQUIREMENTS
    # --------------------------------------------------------

    elif any([
        user_budget,
        user_ram,
        user_processor,
        user_brand,
        user_use_case
    ]):

        recommendations = recommend_products(
            budget=user_budget,
            ram=user_ram,
            use_case=user_use_case,
            brand=user_brand,
            processor=user_processor
        )

        if recommendations.empty:

            response = (
                "I couldn't find a suitable laptop with those exact "
                "requirements. Try increasing your budget or reducing "
                "the RAM requirement."
            )

        else:

            best = recommendations.iloc[0]

            response = (
                f"### 💻 My Recommendation\n\n"
                f"**{best['name']}**\n\n"
                f"💰 Price: ₹{best['price']:,}\n\n"
                f"⚡ Processor: {best['processor']}\n\n"
                f"🧠 RAM: {best['ram']}GB\n\n"
                f"💾 Storage: {best['storage']}\n\n"
                f"🎯 Best for: {best['use_case']}\n\n"
                f"⭐ Rating: {best['rating']}/5\n\n"
                f"📸 I've displayed this laptop in the "
                f"recommendation section above."
            )


    # --------------------------------------------------------
    # GENERAL RECOMMENDATION
    # --------------------------------------------------------

    elif intent == "RECOMMENDATION":

        recommendations = recommend_products(
            budget=budget,
            ram=ram
        )

        if recommendations.empty:

            response = (
                "I couldn't find a suitable recommendation. "
                "Try changing the filters."
            )

        else:

            best = recommendations.iloc[0]

            response = (
                f"🏆 **My top recommendation is {best['name']}!**\n\n"
                f"💰 ₹{best['price']:,}\n\n"
                f"⚡ {best['processor']}\n\n"
                f"🧠 {best['ram']}GB RAM\n\n"
                f"💾 {best['storage']}\n\n"
                f"🎯 Best for {best['use_case']}\n\n"
                f"⭐ {best['rating']}/5\n\n"
                f"The product image is displayed above."
            )


    # --------------------------------------------------------
    # BUDGET QUESTION
    # --------------------------------------------------------

    elif intent == "BUDGET":

        response = (
            f"💰 Your current maximum budget is "
            f"₹{budget:,}. You can change it using the "
            f"budget slider in the sidebar."
        )


    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    else:

        response = (
            "I can help you with:\n\n"
            "💰 Laptop prices and budgets\n"
            "🧠 RAM requirements\n"
            "⚡ Processors\n"
            "🏷️ Brands\n"
            "🎯 Study, office, coding, gaming and designing\n"
            "⭐ Customer reviews\n"
            "⚖️ Laptop comparisons\n"
            "🏆 Product recommendations\n\n"
            "Try asking something like: "
            "'Recommend a laptop under ₹70000 for coding with 16GB RAM.'"
        )


    # Save response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">

    <b>🤖 AI-Powered E-Commerce Chatbot</b>

    <br>

    Laptop Purchase Assistant | CA4 Project

    <br>

    Developed by <b>M S Prajana</b>

    </div>
    """,
    unsafe_allow_html=True
)
