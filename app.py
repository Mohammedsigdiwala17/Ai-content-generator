import streamlit as st
from openai import OpenAI
from fpdf import FPDF
import pyperclip

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="AI Content Studio Pro", page_icon="✨", layout="centered")
st.title("✨ AI Content Studio Pro")
st.caption("Your AI-powered social media & content creation assistant 🚀")

# ---------------------- INIT OPENAI ----------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("⚠️ Missing OPENAI_API_KEY. Please add it in Streamlit → Settings → Secrets.")
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
    import random
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

st.markdown("---")

# ---------------------- PDF CREATOR ----------------------
def create_pdf(content, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(file_name)
    return file_name

# ---------------------- MAIN CONTENT GENERATION ----------------------
if st.button("🚀 Generate AI Content"):
    if not niche_input:
        st.warning("Please enter a niche first.")
    else:
        prompt = f"You are a professional content strategist for the {niche_input} niche.\n"
        prompt += f"Generate {content_type.lower()} with a {tone.lower()} tone."
        if topic:
            prompt += f"\nFocus on this topic: {topic}."
        if description:
            prompt += f"\nAdditional details: {description}."

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

                # Copy button
                st.write("📋 **Copy to Clipboard:**")
                st.code("Press Ctrl+C or Command+C after selecting the text above.", language="")

                # PDF download
                pdf_file = create_pdf(content, f"{niche_input}_content.pdf")
                with open(pdf_file, "rb") as f:
                    st.download_button("⬇️ Download as PDF", f, file_name=pdf_file, mime="application/pdf")

                # Text download
                st.download_button("💾 Download as Text", content, file_name=f"{niche_input}_content.txt")

            except Exception as e:
                st.error(f"⚠️ Error generating content: {e}")

# ---------------------- FOOTER ----------------------
st.markdown("---")
st.markdown("💡 *Tip: Choose your niche, add topic, and let AI create your perfect post strategy!*")
st.caption("Built with ❤️ using Streamlit & GPT-4o")
