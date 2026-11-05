"""Sincroniza o ItemList do schema de /blog/index.html com os cards visíveis.

Cada <a class="card" href="slug.html"><h3>Título</h3> vira um ListItem, na
ordem em que aparece na página, e numberOfItems passa a refletir o total.
Roda localmente ou no workflow .github/workflows/site-automacao.yml.
Saída: código 0 sempre; imprime "ALTERADO" quando reescreve o arquivo.
"""
import html
import json
import re
import sys
from pathlib import Path

BASE = "https://joaovictorataide.com.br/blog/"
ARQ = Path(__file__).resolve().parent.parent / "blog" / "index.html"


def main() -> int:
    s = ARQ.read_text(encoding="utf-8")
    cards, vistos = [], set()
    for slug, titulo in re.findall(r'<a class="card" href="([^"#?]+)"[^>]*>\s*<h3>(.*?)</h3>', s, re.S):
        if slug in vistos:
            continue
        vistos.add(slug)
        nome = html.unescape(re.sub(r"<[^>]+>", "", titulo)).strip()
        cards.append((slug, nome))

    for m in re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S):
        data = json.loads(m.group(2))
        nos = data.get("@graph", [data])
        il = [n for n in nos if n.get("@type") == "ItemList"]
        if not il:
            continue
        novo = [{"@type": "ListItem", "position": i, "url": BASE + slug, "name": nome}
                for i, (slug, nome) in enumerate(cards, 1)]
        if il[0].get("itemListElement") == novo and il[0].get("numberOfItems") == len(novo):
            print(f"ItemList já sincronizado ({len(novo)} itens)")
            return 0
        il[0]["itemListElement"] = novo
        il[0]["numberOfItems"] = len(novo)
        s = s[:m.start(2)] + json.dumps(data, ensure_ascii=False) + s[m.end(2):]
        ARQ.write_text(s, encoding="utf-8")
        print(f"ALTERADO: ItemList com {len(novo)} itens")
        return 0

    print("Nenhum ItemList encontrado em blog/index.html", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
