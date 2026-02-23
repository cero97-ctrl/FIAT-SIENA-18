#!/usr/bin/env python3
import argparse
import json
import sys
from duckduckgo_search import DDGS

def main():
    parser = argparse.ArgumentParser(description="Buscar repuestos automotrices en línea.")
    parser.add_argument("--part", required=True, help="Nombre del repuesto (ej. 'Sensor MAP Fiat Siena 1.8').")
    parser.add_argument("--region", default="ve", help="Código de región para la búsqueda (ve, ar, br, co, mx).")
    args = parser.parse_args()

    # Construir una query optimizada para e-commerce
    # Priorizamos MercadoLibre por ser el estándar en Latam mencionado en el contexto
    site_filter = f"site:mercadolibre.com.{args.region}"
    query = f"{args.part} {site_filter}"
    
    print(f"🔍 Buscando '{args.part}' en MercadoLibre ({args.region})...", file=sys.stderr)

    results = []
    try:
        with DDGS() as ddgs:
            # Buscamos resultados
            ddgs_gen = ddgs.text(query, region=f"wt-wt", safesearch='off', max_results=8)
            if ddgs_gen:
                for r in ddgs_gen:
                    results.append({
                        "title": r.get("title"),
                        "link": r.get("href"),
                        "price_hint": r.get("body") # A veces el precio aparece en el snippet
                    })
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

    # Formatear salida
    if not results:
        # Fallback: búsqueda general si no hay resultados específicos en ML
        try:
            with DDGS() as ddgs:
                gen_results = ddgs.text(f"comprar {args.part}", max_results=5)
                if gen_results:
                    results = [{"title": r.get("title"), "link": r.get("href"), "price_hint": r.get("body")} for r in gen_results]
        except:
            pass

    if results:
        print(json.dumps({
            "status": "success",
            "part": args.part,
            "count": len(results),
            "results": results
        }, indent=2))
    else:
        print(json.dumps({
            "status": "success",
            "part": args.part,
            "count": 0,
            "results": [],
            "message": "No se encontraron resultados directos."
        }))

if __name__ == "__main__":
    main()