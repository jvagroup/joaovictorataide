"""Envia URLs ao IndexNow (Bing, Yandex, Seznam, Naver e parceiros).

Uso:
  python scripts/indexnow.py --todas                 # todas as URLs do sitemap.xml
  python scripts/indexnow.py blog/x.html tributario/index.html ...   # arquivos alterados
Somente arquivos .html publicados entram; redirecionamentos (stubs com
http-equiv="refresh") são ignorados. A chave fica em /<chave>.txt na raiz.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

HOST = "joaovictorataide.com.br"
RAIZ = Path(__file__).resolve().parent.parent
CHAVE = "e81637155791eeb48733b04a8dc27654"
ENDPOINT = "https://api.indexnow.org/indexnow"


def url_de(caminho: str) -> str | None:
    p = Path(caminho)
    if p.suffix != ".html" or not (RAIZ / p).exists():
        return None
    if p.parts and p.parts[0].startswith("."):
        return None
    texto = (RAIZ / p).read_text(encoding="utf-8", errors="ignore")
    if re.search(r'http-equiv=["\']refresh', texto, re.I):
        return None
    rel = p.as_posix()
    if rel == "index.html":
        return f"https://{HOST}/"
    if rel.endswith("/index.html"):
        return f"https://{HOST}/{rel[:-len('index.html')]}"
    return f"https://{HOST}/{rel}"


def diagnostico_chave() -> None:
    """403 = o IndexNow não validou a chave. Testa se o arquivo abre para um robô."""
    for ua in ("Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)", "python-urllib"):
        try:
            r = urllib.request.urlopen(urllib.request.Request(
                f"https://{HOST}/{CHAVE}.txt", headers={"User-Agent": ua}), timeout=30)
            corpo = r.read(200).decode("utf-8", "ignore").strip()
            print(f"  chave via '{ua[:20]}': HTTP {r.status} | servidor={r.headers.get('server')} | "
                  f"cf-ray={r.headers.get('cf-ray')} | conteúdo confere={corpo == CHAVE}")
        except urllib.error.HTTPError as e:
            print(f"  chave via '{ua[:20]}': HTTP {e.code} | servidor={e.headers.get('server')} | "
                  f"cf-ray={e.headers.get('cf-ray')}")
        except Exception as e:  # noqa: BLE001
            print(f"  chave via '{ua[:20]}': erro {e}")


def main(args: list[str]) -> int:
    if not (RAIZ / f"{CHAVE}.txt").exists():
        print("Arquivo da chave não encontrado na raiz; nada enviado.")
        return 1
    if args == ["--todas"]:
        sm = (RAIZ / "sitemap.xml").read_text(encoding="utf-8")
        urls = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sm)
    else:
        urls = [u for u in (url_de(a) for a in args) if u]
    urls = sorted(set(urls))
    if not urls:
        print("Nenhuma URL publicável alterada; nada enviado.")
        return 0
    corpo = json.dumps({"host": HOST, "key": CHAVE,
                        "keyLocation": f"https://{HOST}/{CHAVE}.txt",
                        "urlList": urls[:10000]}).encode()
    req = urllib.request.Request(ENDPOINT, data=corpo, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    corpo_resp = ""
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            status = r.status
            corpo_resp = r.read(500).decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        status = e.code
        corpo_resp = e.read(500).decode("utf-8", "ignore")
    print(f"IndexNow: HTTP {status} para {len(urls)} URL(s) {corpo_resp.strip()}")
    if status == 403:
        diagnostico_chave()
    for u in urls[:50]:
        print("  ", u)
    # 200 = aceito; 202 = aceito, chave em validação. Demais códigos falham o job.
    return 0 if status in (200, 202) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
