"""
ingest.py - Milestone 3: load, clean, and chunk the UCF housing documents.
"""

import os
import re
import glob

DOCUMENTS_DIR = "documents"
MIN_CHUNK_CHARS = 30
MAX_CHUNK_CHARS = 600
OVERLAP_CHARS = 100

USERNAME_RE = re.compile(r'^(\[deleted\]|[A-Za-z0-9_\-]+)( \(OP\))?:\s*$')
META_PREFIXES = ("SOURCE_TYPE:", "SUBREDDIT:", "TOPIC:", "DOCUMENT_ID:", "LOCATION:")
STRUCT_LABELS = {"TITLE:", "ORIGINAL_POST:", "COMMENTS:", "KEY COMMENTS:",
                 "OVERALL THEMES:", "KEY_TOPICS:", "SENTIMENT:",
                 "ADDITIONAL INSIGHTS:", "DISCUSSION_SUMMARY:"}
JUNK_EXACT = {"Upvote", "Downvote", "Reply", "Promoted", "Share", "Award",
              "MOD", "More replies", "Collapse video player"}


def load_documents(folder):
    docs = {}
    for path in glob.glob(os.path.join(folder, "*.txt")):
        with open(path, "r", encoding="utf-8") as f:
            docs[os.path.basename(path)] = f.read()
    return docs


def clean_lines(text):
    kept = []
    for line in text.split("\n"):
        s = line.strip()
        if s == "":
            kept.append("")
            continue
        if s.startswith(META_PREFIXES):
            continue
        if s in STRUCT_LABELS:
            continue
        if s in JUNK_EXACT:
            continue
        if s.isdigit():
            continue
        kept.append(line)
    return kept


def split_long_block(block):
    pieces, start = [], 0
    while start < len(block):
        end = start + MAX_CHUNK_CHARS
        pieces.append(block[start:end].strip())
        start = end - OVERLAP_CHARS
    return [p for p in pieces if len(p) >= MIN_CHUNK_CHARS]


def chunk_document(text, source):
    lines = clean_lines(text)
    groups, current = [], []
    for line in lines:
        if USERNAME_RE.match(line.strip()):
            if current:
                groups.append("\n".join(current).strip())
            current = []
        else:
            current.append(line)
    if current:
        groups.append("\n".join(current).strip())

    chunks = []
    for g in groups:
        g = re.sub(r"\n{2,}", "\n", g).strip()
        if len(g) < MIN_CHUNK_CHARS:
            continue
        if len(g) <= MAX_CHUNK_CHARS:
            chunks.append(g)
        else:
            chunks.extend(split_long_block(g))
    return [{"text": c, "source": source} for c in chunks]


def build_chunks(folder):
    all_chunks = []
    for filename, raw in load_documents(folder).items():
        all_chunks.extend(chunk_document(raw, filename))
    return all_chunks


if __name__ == "__main__":
    chunks = build_chunks(DOCUMENTS_DIR)
    print(f"\nTotal documents loaded: {len(load_documents(DOCUMENTS_DIR))}")
    print(f"Total chunks produced:  {len(chunks)}\n")
    print("----- 6 SAMPLE CHUNKS -----\n")
    step = max(1, len(chunks) // 6)
    for i in range(0, min(len(chunks), step * 6), step):
        c = chunks[i]
        print(f"[chunk {i}] source={c['source']} | {len(c['text'])} chars")
        print(c["text"])
        print("-" * 40)