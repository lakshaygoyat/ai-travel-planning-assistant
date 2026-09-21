from __future__ import annotations

import re
import shutil
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import EMBEDDING_MODEL, KNOWLEDGE_DIR, VECTOR_STORE_DIR


def _read_document(path: Path) -> Document:
    text = path.read_text(encoding="utf-8")
    metadata: dict[str, str] = {"file_name": path.name}
    if text.startswith("---"):
        _, front_matter, body = text.split("---", 2)
        for line in front_matter.splitlines():
            match = re.match(r"^([a-zA-Z_]+):\s*(.+)$", line.strip())
            if match:
                metadata[match.group(1)] = match.group(2).strip()
        text = body.strip()
    return Document(page_content=text, metadata=metadata)


def build_index() -> tuple[int, int]:
    paths = sorted(KNOWLEDGE_DIR.glob("*.md"))
    if len(paths) < 3:
        raise RuntimeError("At least three Markdown knowledge documents are required.")

    documents = [_read_document(path) for path in paths]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=750,
        chunk_overlap=120,
        separators=["\n## ", "\n# ", "\n\n", "\n", ". ", " "],
    )
    chunks = splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    vector_store = FAISS.from_documents(chunks, embeddings)

    if VECTOR_STORE_DIR.exists():
        shutil.rmtree(VECTOR_STORE_DIR)
    vector_store.save_local(str(VECTOR_STORE_DIR))
    return len(documents), len(chunks)


if __name__ == "__main__":
    document_count, chunk_count = build_index()
    print(
        f"Vector index created at {VECTOR_STORE_DIR} from "
        f"{document_count} documents and {chunk_count} chunks."
    )
