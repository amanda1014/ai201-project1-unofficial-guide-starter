"""
evaluate.py - run all 5 eval questions through the system for the README report.
"""
from query import ask

questions = [
    "Which apartment complex is most commonly recommended for students without a car?",
    "What concerns do students commonly mention about Northgate Lakes?",
    "Which apartment complexes are frequently described as affordable options under approximately $1,100 per month?",
    "What do students say about living at Plaza on University?",
    "Is Knights Circle or Accolade better for a student who wants a quiet apartment?",
]

for i, q in enumerate(questions, 1):
    r = ask(q)
    print("=" * 70)
    print(f"Q{i}: {q}")
    print(f"\nANSWER: {r['answer']}")
    print(f"SOURCES: {', '.join(r['sources'])}\n")