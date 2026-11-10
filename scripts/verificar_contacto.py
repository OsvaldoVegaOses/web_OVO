from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import sys

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
cases = {
    "pac-arenillas-negras": "pac", "pac-la-florida": "pac",
    "deslindes-rios-valparaiso": "pac", "medio-humano-desaladora-arica": "medio_humano",
    "medio-humano-horcon": "medio_humano", "plan-maestro-san-felipe": "investigacion",
}
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs))

for name in ["index.html", "index2.html"] + [f"proyectos/{case}{variant}.html" for case in cases for variant in ("", "-v2")]:
    parser = Links()
    parser.feed((root / name).read_text(encoding="utf-8"))
    contact = [link for link in parser.links if link.get("data-contact-source")]
    if name.startswith("index"):
        assert len([a for a in contact if a["data-contact-source"] == "servicios"]) == 3, name
        assert {a["data-contact-service"] for a in contact if a["data-contact-source"] == "servicios"} == {"pac", "medio_humano", "investigacion"}, name
        assert len([a for a in contact if a["data-contact-source"] == "footer"]) == 5, name
    else:
        case = Path(name).stem.removesuffix("-v2")
        assert len(contact) == 1 and contact[0]["data-contact-case"] == case, name
        assert contact[0]["data-contact-service"] == cases[case], name
    for link in contact:
        url = urlsplit(link["href"])
        assert url.scheme == "mailto" and url.path == "contacto@osvaldovega.cl", name
        if link["data-contact-service"] != "general":
            assert parse_qs(url.query).get("subject", [""])[0].startswith("Consulta profesional - "), name
    print("PASS", name, len(contact), "enlaces")
print("Contacto: 14 páginas verificadas")
