# 📄 Fact Check Agent

I built this because marketing decks are full of lies — not always intentional ones, but stats that were true in 2019, figures someone copy-pasted from a competitor's blog, and numbers that got quietly rounded up until they became fiction. This tool fixes that. You drop in a PDF, it reads every claim, hits the live web to verify each one, and hands you back a clean report with exactly what's wrong and what the real number is.

---

## What It Actually Does

The app runs a three-step pipeline on any PDF you throw at it:

**Step 1 — Extract**
Claude reads your PDF and pulls out every specific, checkable claim: statistics, dates, financial figures, percentages, founding years, market sizes. Not summaries or opinions — just the concrete facts that can be right or wrong.

**Step 2 — Verify**
Each claim gets searched against live web data. The agent looks for authoritative sources — not random blogs — and checks whether the claim holds up today, not just at some point in the past.

**Step 3 — Report**
Every claim comes back labeled:
- ✅ **Verified** — matches current data
- ⚠️ **Inaccurate** — was probably true once, but the numbers have moved
- ❌ **False** — no credible evidence found, or actively contradicted

---

## The Stack

```
factcheck-agent/
│
├── app.py              # Streamlit frontend — PDF upload, results display
└── src/
    ├── extractor.py        # Claim extraction via Claude API
    ├── verifier.py         # Per-claim verification with web search
    ├── requirements.txt
└── utils/
    ├── pdf_reader.py   # Pulls raw text from uploaded PDFs
    └── search.py       # Web search wrapper (Tavily / SerpAPI)
```

The whole thing is built on:
- **Streamlit** for the frontend (simple, fast, no JavaScript required)
- **Anthropic Claude API** (`claude-sonnet-4-20250514`) for both extraction and verification reasoning
- **Tavily Search API** for live web results with actual source content
- **PyPDF2 / pdfplumber** for reading PDFs cleanly

---

## Running It Yourself

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/factcheck-agent.git
cd factcheck-agent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up your API keys**

Copy `.env.example` to `.env` and fill in:
```
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

You can get an Groq key at (https://console.groq.com/home) and a Tavily key at [tavily.com](https://tavily.com) — Tavily has a free tier that's more than enough for testing.

**4. Run it**
```bash
streamlit run app.py
```

That's it. Open `localhost:8501` in your browser and upload any PDF.

---

## How the Verification Works

This is the part I spent the most time on. It would have been easy to just search for each claim and declare it true if something comes up. That's not verification — that's just search.

Instead, the verifier does something closer to what a fact-checker would do:

1. Takes the raw claim ("OpenAI was founded in 2018")
2. Searches for authoritative sources on that specific topic
3. Passes both the claim AND the search results to Claude
4. Asks Claude to reason about whether the evidence actually supports the claim, contradicts it, or is ambiguous
5. Requires Claude to cite a specific correct fact if it marks something as inaccurate or false

The result is a `status` (Verified / Inaccurate / False), a `correct_fact` when something is wrong, and a `reason` explaining the judgment. No black boxes.

---

## Flow Diagram

```
User Uploads PDF
       │
       ▼
Extract Text (pdfplumber)
       │
       ▼
Claim Extraction Agent (Claude)
       │  → Outputs: ["claim 1", "claim 2", ...]
       ▼
For Each Claim:
  Web Search (Tavily)
       │
       ▼
  Fact Verification Agent (Claude + search results)
       │  → Outputs: {status, correct_fact, reason}
       ▼
Aggregate Results
       │
       ▼
Display Table + Download CSV
```

---

## Example Output

Here's what the app caught on a test document with three intentional errors:

| # | Claim | Status | Correct Fact |
|---|-------|--------|--------------|
| 0 | India population is 1.1 billion | ⚠️ Inaccurate | ~1.473 billion as of 2026 |
| 1 | OpenAI was founded in 2018 | ❌ False | Founded in December 2015 |
| 2 | Global AI market size in 2025 is $2 trillion | ❌ False | Estimated $254.5B–$390.9B |

---

## Deployment

The live app is deployed on **Streamlit Cloud**:

👉 **[https://your-app-name.streamlit.app](https://your-app-name.streamlit.app)**

To deploy your own fork:
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Add `GROQ_API_KEY` and `TAVILY_API_KEY` under **Settings → Secrets**
4. Deploy — it takes about 2 minutes

---

## Things Worth Knowing

**On accuracy:** The agent is only as good as the web search results it gets back. For very niche or recent claims, it might not find a source one way or another — in those cases it leans toward "cannot verify" rather than guessing.

**On PDFs:** Works best with text-based PDFs (slides, reports, articles). Scanned image PDFs without OCR will return empty results — that's a limitation of the PDF library, not the AI.

**On API credits:** If you're testing this and the deployed version returns errors, the API credits may have run out. The demo video below shows it working correctly with the trap document.

**On rate limits:** The verification runs claims sequentially rather than in parallel to avoid hammering the APIs. For a 20-claim document it takes about 60–90 seconds.

---

## Requirements

```
streamlit>=1.35.0
anthropic>=0.28.0
pdfplumber>=0.11.0
PyPDF2>=3.0.1
tavily-python>=0.3.3
python-dotenv>=1.0.0
pandas>=2.0.0
```

---


## What I'd Build Next

A few things I didn't have time for but would add:

- **Parallel verification** — run all claims simultaneously instead of one by one; would cut runtime to under 10 seconds
- **Source links in the report** — show which URL was used to verify/refute each claim
- **Confidence scores** — not just True/False/Inaccurate but a probability so borderline cases are clearer
- **Export to PDF** — right now you can download CSV; a formatted PDF report would be more shareable
- **Batch mode** — upload multiple PDFs and get a consolidated report


