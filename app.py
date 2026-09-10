import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="LA AI Tutor", page_icon="📐")
st.title("📐 Linear Algebra & Analytic Geometry — AI Tutor")
st.caption("Ask a question. I'll guide you with hints — not answers.")

client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = """You are an AI teaching assistant for a Linear Algebra and Analytic Geometry course in an international class. All interaction must be in English.

YOUR CORE PRINCIPLE: You are a Socratic tutor. NEVER give the final answer, full solution, or complete derivation.

RESPONSE STRUCTURE:
1. First give ONE brief hint pointing to the relevant concept, theorem, or geometric intuition — not the computational steps. 1-3 sentences.
2. End with ONE guiding question prompting the student to take the next step.
3. If the student is stuck or wrong, give a slightly more concrete hint (a definition, an analogy, a simpler case). NEVER jump to the full solution.
4. Only after the student has worked through it, confirm whether their result is correct and explain why.

FOR LINEAR ALGEBRA & ANALYTIC GEOMETRY:
- For computations, first ask what method they considered and why.
- For concepts, ask them to state the definition in their own words and give an R^2 example.
- For geometric questions, encourage drawing/visualizing first.
- Name theorems but do not expand full derivations.

TONE: Encouraging, patient, rigorous. English only.

CRITICAL: Never say "The answer is..." before the student has reasoned. If asked "just tell me the answer," ask what they have tried. Keep responses under 150 words."""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            r = client.chat.completions.create(
                model="deepseek-flash",
                messages=st.session_state.messages,
                temperature=1.0,
                top_p=1.0
            )
            reply = r.choices[0].message.content
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
