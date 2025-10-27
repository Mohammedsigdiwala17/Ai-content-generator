import streamlit as st
from openai import OpenAI
import random
from datetime import datetime, timedelta

# -------------------- CONFIG --------------------
st.set_page_config(page_title="AI Content Studio", page_icon="✨", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------- UI HEADER --------------------
st.title("✨ AI Content Creation Studio Pro")
st.caption("Your all-in-one AI-powered content planner for social media, blogs & YouTube 🚀")

# -------------------- SIDEBAR --------------------
st.sidebar.header("🧠 Setup Your Content")
niche_input = st.sidebar.text_input("Enter your niche (e.g. Fitness, Finance, Travel):")

auto_niches = [
    "Fitness", "Finance", "Fashion", "Travel", "Food", "Technology", "Motivation",
    "Parenting", "Health & Wellness", "Self Improvement", "Education", "AI Tools", "Marketing"
]

if st.sidebar.button("🎯 Suggest Niche"):
    st.sidebar.info(f"Try **{random.choice(auto_niches)}** niche!")

content_type = st.sidebar.selectbox(
    "Select Content Type:",
    ["Instagram Captions", "YouTube Script", "Hashtags", "Blog Topics", "Post Ideas", "Perfect Post Timing", "30-Day Content Calendar"]
)

topic = st.sidebar.text_input("Add a topic (optional):")
description = st.sidebar.text_area("Add extra details (optional):")

st.markdown("---")

# -------------------- GENERATION --------------------
if st.button("🚀 Generate AI Content"):
    if not niche_input:
        st.warning("Please enter your niche before generating.")
    else:
        # Build prompt
        prompt = f"You are an expert social media content strategist for the {niche_input} niche.\n"
        prompt += f"Generate {content_type.lower()}."

        if topic:
            prompt += f"\nFocus on the topic: {topic}."
        if description:
            prompt += f"\nAdditional details: {description}."

        if content_type == "Perfect Post Timing":
            prompt += "\nList the best posting days and times for maximum engagement."
        elif content_type == "30-Day Content Calendar":
            prompt += "\nCreate a 30-day daily content plan with post titles, short ideas, and call-to-action for each day."

        prompt += "\nMake it engaging, creative, and useful for growing an online audience."

        with st.spinner("✨ AI is creating your content..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8
            )

        output = response.choices[0].message.content

        st.success("✅ Your AI content is ready!")
        st.text_area("📝 Generated Content", output, height=350)

        # Download option
        st.download_button("⬇️ Download Content", output, file_name=f"{niche_input}_content.txt")

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown("💡 *Tip: Add a niche, choose content type, and get instant AI-powered ideas!*")
st.markdown("Built with ❤️ using GPT-4o and Streamlit")
