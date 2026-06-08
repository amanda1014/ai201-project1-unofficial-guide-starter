"""
embed.py - Milestone 4: embed chunks, store in ChromaDB, test retrieval.
"""
from ingest import build_chunks, DOCUMENTS_DIR
from sentence_transformers import SentenceTransformer
import chromadb

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "ucf_housing"
DB_PATH = "chroma_db"
TOP_K = 5


def build_collection():
    chunks = build_chunks(DOCUMENTS_DIR)
    print(f"Embedding {len(chunks)} chunks with {MODEL_NAME} ...")
    model = SentenceTransformer(MODEL_NAME)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    client = chromadb.PersistentClient(path=DB_PATH)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    pos, ids, metas = {}, [], []
    for c in chunks:
        src = c["source"]
        pos[src] = pos.get(src, 0) + 1
        ids.append(f"{src}::{pos[src]}")
        metas.append({"source": src, "position": pos[src]})

    collection.add(ids=ids, documents=texts, embeddings=embeddings, metadatas=metas)
    print(f"Stored {collection.count()} chunks in ChromaDB at '{DB_PATH}'.\n")
    return model, collection


def get_model_and_collection():
    model = SentenceTransformer(MODEL_NAME)
    client = chromadb.PersistentClient(path=DB_PATH)
    return model, client.get_collection(COLLECTION_NAME)


def retrieve(query, model, collection, k=TOP_K):
    q_emb = model.encode([query]).tolist()
    res = collection.query(query_embeddings=q_emb, n_results=k)
    hits = []
    for doc, meta, dist in zip(res["documents"][0],
                               res["metadatas"][0],
                               res["distances"][0]):
        hits.append({"text": doc, "source": meta["source"], "distance": dist})
    return hits


if __name__ == "__main__":
    model, collection = build_collection()

    test_questions = [
        "Which apartment complex is most commonly recommended for students without a car?",
        "What concerns do students commonly mention about Northgate Lakes?",
        "Which apartment complexes are frequently described as affordable options under approximately $1,100 per month?",
        "What do students say about living at Plaza on University?",
        "Is Knights Circle or Accolade better for a student who wants a quiet apartment?",
    ]
    for q in test_questions:
        print("=" * 70)
        print(f"QUERY: {q}\n")
        for h in retrieve(q, model, collection):
            preview = h["text"][:200].replace("\n", " ")
            print(f"[dist {h['distance']:.3f}] {h['source']}")
            print(f"   {preview}...\n")