from tavily import TavilyClient
from groq import Groq
import streamlit as st

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

tavily = TavilyClient(
    api_key=st.secrets["TAVILY_API_KEY"]
)

def verify_claim(claim):

    search = tavily.search(
        query=claim,
        max_results=5
    )

    evidence = ""

    for result in search["results"]:

        evidence += result["content"] + "\n\n"

    prompt = f"""
    Claim:
    {claim}

    Evidence:
    {evidence}

    Determine whether the claim is:

    VERIFIED
    INACCURATE
    FALSE

    Return:

    Status:
    Correct Fact:
    Reason:
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