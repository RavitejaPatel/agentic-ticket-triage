import os
import glob
import json
import boto3
import numpy as np
import faiss

_client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))
_EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0"


def _embed(text: str) -> np.ndarray:
    body = json.dumps({"inputText": text})
    response = _client.invoke_model(modelId=_EMBED_MODEL_ID, body=body)
    result = json.loads(response["body"].read())
    return np.array(result["embedding"], dtype="float32")


def load_kb_documents(kb_dir="kb"):
    docs = []
    for filepath in glob.glob(os.path.join(kb_dir, "*.md")):
        with open(filepath, "r") as f:
            content = f.read()
        docs.append({"source": os.path.basename(filepath), "text": content})
    return docs


def build_index(docs):
    embeddings = np.array([_embed(d["text"]) for d in docs])
    print("-----------------------------------------------------------------------------")
    print(f"Built embeddings for {len(docs)} documents. Embedding shape: {embeddings.shape}")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, docs


def search(query, index, docs, top_k=2):
    query_vec = _embed(query).reshape(1, -1)
    distances, indices = index.search(query_vec, top_k)
    return [docs[i] for i in indices[0]]


if __name__ == "__main__":
    docs = load_kb_documents()
    print(f"Loaded {docs} documents from the knowledge base.")
    index, docs = build_index(docs)
    test_query = "I was charged twice for my subscription"
    results = search(test_query, index, docs)
    print("-----------------------------------------------------------------------------")
    print(results)
    print("-----------------------------------------------------------------------------")
    for r in results:
        print(f"--- {r['source']} ---")
        print(r["text"][:200])
        print()