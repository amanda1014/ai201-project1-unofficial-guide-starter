"""
query.py - Milestone 5: retrieve chunks, generate a grounded answer with Groq.
"""
import os
from dotenv import load_dotenv
from groq import Groq
from embed import get_model_and_collection, retrieve

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"
TOP_K = 8   # retrieve a few more chunks so answer-bearing chunks are included

_model, _collection = get_model_and_collection()

SYSTEM_PROMPT = """You are a Q&A assistant for UCF off-campus housing.
Answer the question using ONLY the information in the CONTEXT below, which
contains real student comments from Reddit. You may summarize and combine
what multiple students say.

Rules:
- Do NOT use outside or general knowledge.
- Do NOT invent specific facts (prices, names, policies) that are not in the context.
- If the question asks to COMPARE options but the context only covers one of
  them, or does not address the specific thing asked about, say you do not
  have enough information to make that comparison.
- If the context contains no relevant information at all, respond with exactly:
  "I don't have enough information on that."

Keep your answer concise and grounded in what students actually said."""


def ask(question, k=TOP_K):
    hits = retrieve(question, _model, _collection, k=k)
    context = "\n\n".join(
        f"[Source: {h['source']}]\n{h['text']}" for h in hits
    )
    user_prompt = f"CONTEXT:\n{context}\n\nQUESTION: {question}"
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
    )
    answer = completion.choices[0].message.content.strip()

    seen, sources = set(), []
    for h in hits:
        if h["source"] not in seen:
            seen.add(h["source"])
            sources.append(h["source"])

    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    tests = [
        "Which apartment complex is most commonly recommended for students without a car?",
        "Is Knights Circle or Accolade better for a student who wants a quiet apartment?",
        "What is the pet policy at Knights Circle?",   # out-of-scope probe
    ]
    for q in tests:
        print("=" * 70)
        print("Q:", q)
        r = ask(q)
        print("\nANSWER:", r["answer"])
        print("SOURCES:", ", ".join(r["sources"]))
        print()