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

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(135deg, #111827, #2563eb);
    padding: 35px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 8px;
}

.hero p {
    font-size: 18px;
    opacity: 0.92;
}

.product-card {
    background: white;
    border-radius: 18px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 0px 5px 18px rgba(0,0,0,0.08);
    border: 1px solid #e5e7eb;
}

.product-title {
    font-size: 20px;
    font-weight: 700;
    color: #111827;
}

.product-brand {
    color: #6b7280;
    font-size: 14px;
}

.product-price {
    font-size: 24px;
    font-weight: 800;
    color: #2563eb;
}

.rating {
    color: #f59e0b;
    font-weight: 600;
}

.feature-box {
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.05);
}

.chat-user {
    background: #2563eb;
    color: white;
    padding: 12px 16px;
    border-radius: 15px;
    margin: 8px 0;
}

.chat-bot {
    background: #eef2ff;
    color: #111827;
    padding: 12px 16px;
    border-radius: 15px;
    margin: 8px 0;
}

.section-title {
    font-size: 28px;
    font-weight: 750;
    margin-top: 30px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# PRODUCT DATA
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
# CUSTOMER REVIEWS
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
        "under", "afford"
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
        "best", "suitable"
    ],

    "REVIEW_QUERY": [
        "review", "reviews",
        "rating", "feedback"
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

    if "gaming" in text:
        return "Gaming"

    if "coding" in text or "programming" in text:
        return "Coding"

    if "design" in text or "editing" in text:
        return "Designing"

    if "study" in text or "student" in text:
        return "Study"

    if "office" in text or "work" in text:
        return "Office"

    return None


# ============================================================
# PRODUCT RECOMMENDATION
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

    return result.head(3)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown("""
<div class="hero">

<h1>💻 Laptop Purchase Assistant</h1>

<p>
Find the right laptop based on your budget,
performance needs and intended use.
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🔎 Find Your Laptop")

st.sidebar.write(
    "Set your preferences below."
)

budget = st.sidebar.slider(
    "Maximum Budget",
    min_value=40000,
    max_value=100000,
    value=70000,
    step=5000
)

ram = st.sidebar.selectbox(
    "Minimum RAM",
    [8, 16, 32],
    index=1
)

use_case = st.sidebar.selectbox(
    "Primary Use",
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
    "Preferred Brand",
    [
        "All",
        "HP",
        "Lenovo",
        "ASUS"
    ]
)

processor = st.sidebar.selectbox(
    "Processor Preference",
    [
        "All",
        "Intel Core i3",
        "Intel Core i5",
        "Intel Core i7",
        "AMD Ryzen 7"
    ]
)


# ============================================================
# PRODUCT FILTERING
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
# QUICK STATS
# ============================================================

st.markdown(
    '<div class="section-title">Why use the Assistant?</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown("""
    <div class="feature-box">
    <h2>💰</h2>
    <b>Budget Matching</b>
    <p>Find laptops within your budget.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown("""
    <div class="feature-box">
    <h2>⚡</h2>
    <b>Performance</b>
    <p>Compare processors and RAM.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:

    st.markdown("""
    <div class="feature-box">
    <h2>⭐</h2>
    <b>Ratings</b>
    <p>Explore product ratings.</p>
    </div>
    """, unsafe_allow_html=True)

with c4:

    st.markdown("""
    <div class="feature-box">
    <h2>🤖</h2>
    <b>AI Assistant</b>
    <p>Get personalised suggestions.</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# PRODUCT SECTION
# ============================================================

st.markdown(
    '<div class="section-title">🛍️ Recommended Laptops</div>',
    unsafe_allow_html=True
)

if filtered.empty:

    st.warning(
        "No exact products match your selected filters. "
        "Try increasing your budget or changing the filters."
    )

else:

    cols = st.columns(3)

    for index, (_, product) in enumerate(
        filtered.iterrows()
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
                f'<div class="product-title">'
                f'{product["name"]}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="product-brand">'
                f'{product["brand"]}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="product-price">'
                f'₹{product["price"]:,}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'⚙️ **{product["processor"]}**  '
                f'| 🧠 **{product["ram"]}GB RAM**'
            )

            st.markdown(
                f'💾 **{product["storage"]}**'
            )

            st.markdown(
                f'🎯 **Best for:** {product["use_case"]}'
            )

            st.markdown(
                f'<div class="rating">'
                f'⭐ {product["rating"]}/5</div>',
                unsafe_allow_html=True
            )

            if st.button(
                "View Reviews",
                key=f"review_{product['id']}"
            ):

                st.session_state[
                    "selected_product"
                ] = product["id"]

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


# ============================================================
# REVIEW SECTION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '⭐ Customer Reviews & Sentiment'
    '</div>',
    unsafe_allow_html=True
)

selected_product = st.selectbox(
    "Choose a product",
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
        f'{emoji} {review["review"]}  \n'
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
    st.metric(
        "Positive",
        positive
    )

with b:
    st.metric(
        "Negative",
        negative
    )

with c:
    st.metric(
        "Neutral",
        neutral
    )


# ============================================================
# CHATBOT
# ============================================================

st.markdown(
    '<div class="section-title">🤖 Chat with the Assistant</div>',
    unsafe_allow_html=True
)

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content":
            "Hello! 👋 Tell me your budget and what "
            "you mainly use a laptop for."
        }
    ]


for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f'<div class="chat-user">'
            f'👤 {message["content"]}'
            f'</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f'<div class="chat-bot">'
            f'🤖 {message["content"]}'
            f'</div>',
            unsafe_allow_html=True
        )


user_input = st.chat_input(
    "Example: I need a laptop under ₹70000 for coding"
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

    if intent == "GREETING":

        response = (
            "Hello! 👋 I can help you choose a laptop. "
            "Tell me your budget, preferred RAM and intended use."
        )

    elif intent == "GOODBYE":

        response = (
            "Thank you for using the Laptop Purchase Assistant! "
            "Have a great day. 😊"
        )

    elif intent == "REVIEW_QUERY":

        response = (
            "You can select a product in the "
            "Customer Reviews section above to see "
            "customer feedback and VADER sentiment analysis."
        )

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
                "I could not find a suitable laptop "
                "with those exact requirements."
            )

        else:

            best = recommendations.iloc[0]

            response = (
                f"Based on your requirements, I recommend "
                f"**{best['name']}**. 💻\n\n"
                f"💰 Price: ₹{best['price']:,}\n\n"
                f"⚙️ Processor: {best['processor']}\n\n"
                f"🧠 RAM: {best['ram']}GB\n\n"
                f"🎯 Best for: {best['use_case']}\n\n"
                f"⭐ Rating: {best['rating']}/5"
            )

    elif intent == "RECOMMENDATION":

        if filtered.empty:

            response = (
                "I couldn't find an exact match. "
                "Try changing the filters."
            )

        else:

            best = filtered.sort_values(
                "rating",
                ascending=False
            ).iloc[0]

            response = (
                f"My top recommendation is "
                f"**{best['name']}**. 💻 "
                f"It costs ₹{best['price']:,}, has "
                f"{best['ram']}GB RAM and a "
                f"{best['processor']} processor."
            )

    elif intent == "BUDGET":

        response = (
            f"Your current selected budget is "
            f"₹{budget:,}. You can adjust it using "
            f"the sidebar."
        )

    else:

        response = (
            "I can help you with laptop prices, "
            "RAM, processors, brands, use cases, "
            "reviews and recommendations."
        )

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
    <div style="text-align:center; color:#6b7280;">
    <b>AI-Powered E-Commerce Chatbot</b><br>
    Laptop Purchase Assistant | CA4 Project<br>
    Developed by M S Prajana
    </div>
    """,
    unsafe_allow_html=True
)
