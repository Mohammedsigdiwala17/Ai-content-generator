import streamlit as st
from openai import OpenAI

# Initialize OpenAI Client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Content Creation Studio", page_icon="🎨", layout="centered")

st.title("🎨 AI Content Creation Studio")
st.markdown("Generate AI-powered content ideas, captions, scripts, and more based on your niche!")

# Sidebar - Settings
st.sidebar.header("🧠 Content Options")
niche = st.sidebar.text_input("Enter your niche (e.g., Fitness, Finance, Travel):")
content_type = st.sidebar.selectbox(
    "Select Content Type:",
    ["Instagram Caption", "Hashtags", "YouTube Script", "Post Ideas", "Blog Topics", "Perfect Post Timing"]
)
topic = st.sidebar.text_input("Enter Topic (optional):")
description = st.sidebar.text_area("Add Description (optional):")

st.markdown("---")

if st.button("✨ Generate Content"):
    if not niche:
        st.warning("Please enter a niche before generating.")
    else:
        # Create intelligent backend prompt
        base_prompt = f"""
        You are an expert social media content strategist.
        Generate {content_type.lower()} ideas for the {niche} niche.
        """

        if topic:
            base_prompt += f"\nFocus on the topic: {topic}."
        if description:
            base_prompt += f"\nHere are more details: {description}."

        base_prompt += "\nMake it engaging, authentic, and optimized for maximum reach."

        # Generate using GPT-4o
        with st.spinner("Creating your content..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": base_prompt}],
                temperature=0.8
            )

        content = response.choices[0].message.content
        st.success("✅ Content generated successfully!")
        st.text_area("Your Generated Content:", content, height=250)
        st.download_button("⬇️ Download Result", content, file_name="ai_content.txt")
