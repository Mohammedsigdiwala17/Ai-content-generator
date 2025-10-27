import streamlit as st
from openai import OpenAI
from fpdf import FPDF
import pandas as pd
import random

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="AI Content Studio Pro", page_icon="✨", layout="wide")
st.title("✨ AI Content Studio Pro")
st.caption("Your AI-powered social media & content creation assistant 🚀")

# ---------------------- OPENAI INIT ----------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("⚠️ Missing OPENAI_API_KEY. Add it in Streamlit → Settings → Secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------------- SIDEBAR ----------------------
st.sidebar.header("🧠 Content Setup")

niche_input = st.sidebar.text_input("Enter your niche (e.g., Fitness, Finance, Travel):")

auto_niches = [
    "Fitness", "Finance", "Fashion", "Travel", "Food", "Technology",
    "Motivation", "Parenting", "Health & Wellness", "Education", "AI Tools", "Marketing"
]

if st.sidebar.button("🎯 Suggest a Niche"):
    st.sidebar.info(f"Try this trending niche: **{random.choice(auto_niches)}**")

content_type = st.sidebar.selectbox(
    "Select Content Type:",
    [
        "Instagram Caption",
        "YouTube Script",
        "Hashtags",
        "Blog Topics",
        "Post Ideas",
        "Perfect Post Timing",
        "30-Day Content Calendar",
        "Product Description",
        "Ad Copy",
        "Email Campaign",
    ]
)

topic = st.sidebar.text_input("Add a topic (optional):")
description = st.sidebar.text_area("Add extra details (optional):")

tone = st.sidebar.selectbox("Choose Tone:", ["Professional", "Friendly", "Funny", "Motivational", "Luxury", "Casual"])

# ---------------------- PDF CREATOR ----------------------
def create_pdf(content, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(file_name)
    return file_name

# ---------------------- GENERATION ----------------------
st.markdown("---")
st.subheader("🪄 Generate AI Content")

if st.button("🚀 Generate Content"):
    if not niche_input:
        st.warning("Please enter a niche first.")
    else:
        prompt = f"You are a professional content strategist for the {niche_input} niche.\n"
        prompt += f"Generate {content_type.lower()} with a {tone.lower()} tone."
        if topic:
            prompt += f"\nFocus on this topic: {topic}."
        if description:
            prompt += f"\nAdditional details: {description}."

        # Extra logic for content type
        if content_type == "Perfect Post Timing":
            prompt += "\nList the best posting days and times for maximum engagement for this niche."
        elif content_type == "30-Day Content Calendar":
            prompt += "\nCreate a 30-day calendar with daily content ideas, short captions, and CTAs."
        elif content_type == "Hashtags":
            prompt += "\nGenerate 20 high-performing, SEO-optimized hashtags for Instagram in this niche."
        elif content_type == "Blog Topics":
            prompt += "\nList 10 trending blog topics with catchy titles in this niche."
        elif content_type == "Ad Copy":
            prompt += "\nGenerate 3 short, persuasive ad copies for this niche."

        prompt += "\nMake the content creative, engaging, and tailored to the Indian audience when relevant."

        with st.spinner("✨ Generating your content..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,
                )
                content = response.choices[0].message.content

                st.success("✅ Your AI content is ready!")
                st.text_area("📝 Generated Content", content, height=400, key="content_box")

                # 📄 Download Buttons
                pdf_file = create_pdf(content, f"{niche_input}_content.pdf")
                with open(pdf_file, "rb") as f:
                    st.download_button("⬇️ Download as PDF", f, file_name=pdf_file, mime="application/pdf")

                st.download_button("💾 Download as Text", content, file_name=f"{niche_input}_content.txt")

            except Exception as e:
                st.error(f"⚠️ Error generating content: {e}")

# ---------------------- CALENDAR VIEW ----------------------
st.markdown("---")
st.subheader("📅 AI Content Calendar")

if st.button("🧠 Generate 30-Day Calendar"):
    if not niche_input:
        st.warning("Please enter a niche first.")
    else:
        with st.spinner("🗓️ Creating your 30-day content calendar..."):
            prompt = f"Create a 30-day content calendar for the {niche_input} niche with 3 columns: Day, Content Idea, Caption or CTA. Keep it short and engaging."
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
            )
            calendar_text = response.choices[0].message.content

            # Try to format into table
            days = []
            ideas = []
            captions = []
            for line in calendar_text.split("\n"):
                if line.strip().startswith("Day"):
                    continue
                parts = line.split(":", 2)
                if len(parts) >= 2:
                    day = len(days) + 1
                    content = parts[0].strip()
                    caption = parts[-1].strip()
                    days.append(day)
                    ideas.append(content)
                    captions.append(caption)

            df = pd.DataFrame({"Day": days, "Content Idea": ideas, "Caption/CTA": captions})
            st.dataframe(df)

# ---------------------- ENGAGEMENT PREDICTION ----------------------
st.markdown("---")
st.subheader("📊 AI Engagement Prediction")

if st.button("🔮 Predict Engagement Potential"):
    if not niche_input:
        st.warning("Please enter a niche first.")
    else:
        with st.spinner("📈 Analyzing engagement potential..."):
            prompt = f"Based on social media analytics, predict engagement levels (Low, Medium, High) for 5 content types in the {niche_input} niche. Explain why each performs as such."
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            prediction = response.choices[0].message.content
            st.text_area("🔍 Engagement Insights", prediction, height=300)

# ---------------------- FOOTER ----------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit & GPT-4o-mini | Mohammed’s AI SaaS Project")
