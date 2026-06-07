from groq import Groq
import streamlit as st

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

def extract_claims(text):

    prompt = f"""
    Extract factual claims from this text.

    Only include:
    - statistics
    - percentages
    - dates
    - financial figures
    - technical facts

    Return ONLY valid JSON.

    Example:

    [
      "India population is 1.4 billion",
      "OpenAI was founded in 2015"
    ]

    Text:

    {text[:12000]}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content
