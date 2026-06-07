import streamlit as st
import json

from src.pdf_reader import extract_text_from_pdf
from src.claim_extractor import extract_claims
from src.web_verifier import verify_claim
from src.report_generator import build_report

st.set_page_config(
    page_title="Fact Check Agent",
    layout="wide"
)

st.title("📄 Fact Check Agent")
st.write("Upload a PDF and verify claims against live web data.")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    # Read PDF
    with st.spinner("Reading PDF..."):
        text = extract_text_from_pdf(uploaded_file)

    st.success("PDF Loaded Successfully")

    # Extract Claims
    with st.spinner("Extracting Claims..."):
        claims_json = extract_claims(text)

    # Clean LLM response
    claims_json = (
        claims_json
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    st.subheader("Extracted Claims")
    st.code(claims_json)

    try:
        claims = json.loads(claims_json)

    except Exception as e:
        st.error(f"JSON Parse Failed: {e}")
        st.text(claims_json)
        st.stop()

    if not claims:
        st.warning("No factual claims found in the document.")
        st.stop()

    st.success(f"Found {len(claims)} claims")

    # Verify Claims
    results = []

    progress_bar = st.progress(0)

    for idx, claim in enumerate(claims):

        with st.spinner(
            f"Checking claim {idx + 1} of {len(claims)}"
        ):

            verdict = verify_claim(claim)

            results.append(
                (claim, verdict)
            )

        progress_bar.progress(
            (idx + 1) / len(claims)
        )

    # Build Report
    df = build_report(results)

    st.subheader("📊 Fact Check Report")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.success("Fact Checking Completed")
