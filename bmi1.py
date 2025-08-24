
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

from dotenv import load_dotenv
load_dotenv(dotenv_path=r"C:\Users\Nishanth R\Desktop\APP\myenv1\.env" )

# You should set your Gemma API key in an environment variable or load from .env
gemini_key = os.getenv("g_key")

# Initialize model (Gemma API key needed)
llm = ChatGoogleGenerativeAI(model="gemma-3-27b-it", api_key=gemini_key)

# Gemma-compatible prompt template (no system role)
prompt = ChatPromptTemplate.from_messages([
    ("human", "<start_of_turn>user\nYou are a BMI calculator. I will provide weight in kgs and height in cms. "
              "You must respond with: 1) The BMI value, 2) The BMI category, "
              "3) A short explanation.\n\n{question}<end_of_turn>")
])

st.markdown(
    """
    <style>
    .bmi-icon {
        font-size: 60px;
        margin-bottom: 10px;
    }
    .bmi-card {
        background: #f8f9fa;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        padding: 2rem 1.5rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .bmi-result {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2e7d32;
    }
    .bmi-category {
        font-size: 1.2rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    .bmi-explanation {
        font-size: 1rem;
        color: #555;
        margin-top: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center;'>BMI Calculator (Gemma-3B Powered)</h1>", unsafe_allow_html=True)

st.markdown('<div class="bmi-card">'
            '<span class="bmi-icon">⚖️</span>'
            '<h2>Enter Your Details</h2>'
            '</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1, format="%.1f")
with col2:
    height = st.number_input("Height (cm)", min_value=10.0, step=0.1, format="%.1f")

if st.button("Calculate BMI", use_container_width=True):
    if weight > 0 and height > 0:
        # Convert height from cm to meters for BMI calculation
        question = f"Enter weight as {weight} kgs and height as {height} cms"
        with st.spinner("Calculating with Gemma-3B..."):
            try:
                chain = prompt | llm
                response = chain.invoke({"question": question})
                # Try to parse response for icon/color/category
                if "underweight" in response.content.lower():
                    icon = "🍃"
                    color = "#1976d2"
                elif "normal" in response.content.lower():
                    icon = "💪"
                    color = "#388e3c"
                elif "overweight" in response.content.lower():
                    icon = "🍔"
                    color = "#fbc02d"
                elif "obese" in response.content.lower() or "obesity" in response.content.lower():
                    icon = "⚠️"
                    color = "#d32f2f"
                else:
                    icon = "🤖"
                    color = "#333"
                st.markdown(f'''
                <div class="bmi-card">
                    <span class="bmi-icon" style="color:{color}">{icon}</span>
                    <div class="bmi-result">{response.content}</div>
                </div>
                ''', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("Please enter valid weight and height.")

st.markdown("---")
st.info("**What is BMI?**\n\nBMI (Body Mass Index) is a measure of body fat based on height and weight. This calculator is powered by Gemma-3B via LangChain. Please consult a healthcare professional for personalized advice.")

