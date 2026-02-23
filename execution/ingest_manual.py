#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
import uuid

try:
    from pypdf import PdfReader
except ImportError:
    print(json.dumps({"status": "error", "message": "Librería 'pypdf' no instalada. Ejecuta: pip install pypdf"}))
    sys.exit(1)

try:
    import chromadb
except ImportError:
    print(json.dumps({"status": "error", "message": "Librería 'chromadb' no instalada. Ejecuta: pip install chromadb"}))
    sys.exit(1)

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    """Divide un texto largo en fragmentos más pequeños con superposición."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

def main():
    parser = argparse.ArgumentParser(description="Ingestar un manual PDF en la memoria vectorial (ChromaDB).")
    parser.add_argument("--file", required=True, help="Ruta al archivo PDF a procesar.")
    parser.add_argument("--db-path", default=".tmp/chroma_db", help="Ruta a la base de datos ChromaDB.")
    parser.add_argument("--collection-name", default="agent_memory", help="Nombre de la colección en ChromaDB.")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(json.dumps({"status": "error", "message": f"Archivo no encontrado: {file_path}"}))
        sys.exit(1)

    # 1. Extraer texto del PDF
    try:
        reader = PdfReader(file_path)
        full_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Error leyendo PDF: {e}"}))
        sys.exit(1)

    if not full_text.strip():
        print(json.dumps({"status": "error", "message": "El PDF está vacío o no contiene texto extraíble."}))
        sys.exit(1)

    # 2. Dividir en fragmentos (Chunking)
    text_chunks = chunk_text(full_text)

    # 3. Conectar a ChromaDB
    try:
        client = chromadb.PersistentClient(path=args.db_path)
        collection = client.get_or_create_collection(name=args.collection_name)
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Error conectando a ChromaDB: {e}"}))
        sys.exit(1)

    # 4. Ingestar fragmentos en la BD
    try:
        ids = [str(uuid.uuid4()) for _ in text_chunks]
        metadatas = [{"source": file_path.name, "chunk": i} for i in range(len(text_chunks))]
        
        collection.upsert(documents=text_chunks, metadatas=metadatas, ids=ids)
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Error guardando en ChromaDB: {e}"}))
        sys.exit(1)

    print(json.dumps({"status": "success", "message": f"Se ingestaron {len(text_chunks)} fragmentos desde '{file_path.name}'.", "total_chars": len(full_text)}))

if __name__ == "__main__":
    main()