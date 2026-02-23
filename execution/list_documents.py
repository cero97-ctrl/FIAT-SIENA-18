import json
import sys
import os
from pathlib import Path

try:
    import chromadb
except ImportError:
    print(json.dumps({"status": "error", "message": "Falta chromadb"}), file=sys.stderr)
    sys.exit(1)

def main():
    # Configuración de rutas
    base_dir = Path(__file__).resolve().parent.parent
    db_path = base_dir / ".tmp" / "chroma_db"

    if not db_path.exists():
        print(json.dumps({"status": "success", "documents": []}))
        sys.exit(0)

    try:
        client = chromadb.PersistentClient(path=str(db_path))
        collection = client.get_or_create_collection(name="agent_memory")
        
        # Traemos todos los metadatos para filtrar
        results = collection.get(include=["metadatas"])
        
        files = {}
        if results['metadatas']:
            for meta in results['metadatas']:
                # Buscamos documentos PDF ingestados
                source = meta.get('source', '')
                doc_type = meta.get('type', '')
                
                # Filtramos si es un PDF o si el tipo es document_pdf
                if source and (doc_type == 'document_pdf' or source.lower().endswith('.pdf')):
                    timestamp = meta.get('timestamp', '')
                    # Usamos el nombre base (ej: manual.pdf) en lugar de la ruta completa
                    name = os.path.basename(source)
                    if name not in files:
                        files[name] = timestamp
        
        doc_list = [{"name": k, "ingested_at": v} for k, v in files.items()]
        
        print(json.dumps({"status": "success", "documents": doc_list}))
        
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()