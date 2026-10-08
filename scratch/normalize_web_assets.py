"""Audit, migrate and package the published static image paths (local only)."""
from __future__ import annotations

import argparse
import os
import posixpath
import re
import unicodedata
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
WEBP = ROOT / "Fotos_proyectos" / "webp"
HTMLS = [ROOT / "index.html", ROOT / "index_2.html", *sorted((ROOT / "proyectos").glob("*.html"))]
FOLDERS = {
    "Arenillas Negras": "arenillas-negras",
    "Desaladora_arica": "desaladora-arica",
    "Deslindes de río": "deslindes",
    "foto_personal": "perfil",
    "Horcon": "horcon",
    "La Florida": "la-florida",
    "San Felipe": "san-felipe",
}
ATTR_RE = re.compile(r'(?P<name>\b(?:src|srcset|href)\s*=\s*)(?P<q>["\'])(?P<value>.*?)(?P=q)', re.I | re.S)
URL_RE = re.compile(r'url\(\s*(?P<q>["\']?)(?P<value>.*?)(?P=q)\s*\)', re.I)
SAFE_COMPONENT = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.[a-z0-9]+$|^[a-z0-9]+(?:-[a-z0-9]+)*$")


def slug(stem: str) -> str:
    stem = re.sub(r"([A-Za-z])([0-9])", r"\1-\2", stem)
    stem = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode("ascii").lower()
    stem = stem.replace("renion", "reunion")
    return re.sub(r"[^a-z0-9]+", "-", stem).strip("-")


def target_name(folder: str, file: Path) -> str:
    stem = file.stem
    if folder == "foto_personal":
        return "osvaldo-vega.webp"
    if folder == "Desaladora_arica" and stem == "foto_Sector_playa":
        return "sector-playa.webp"
    if folder == "Deslindes de río" and stem.startswith("IMG_20221018_"):
        return "recorrido-territorial-" + slug(stem.removeprefix("IMG_")) + ".webp"
    if folder == "Deslindes de río" and stem == "foto recorrido_!":
        return "foto-recorrido-2.webp"
    if folder == "La Florida":
        match = re.match(r"Imagen\s*(\d+)\s+visita de reconocimiento", stem)
        if match:
            return f"visita-reconocimiento-{match.group(1)}.webp"
    return slug(stem) + ".webp"


def within(path: Path, parent: Path) -> bool:
    return path.resolve(strict=False).is_relative_to(parent.resolve())


def plan() -> dict[Path, Path]:
    assert within(WEBP, ROOT)
    folder_names = {p.name for p in WEBP.iterdir() if p.is_dir()}
    if folder_names != set(FOLDERS):
        raise RuntimeError(f"Unexpected WebP folders: {folder_names ^ set(FOLDERS)}")
    mapping: dict[Path, Path] = {}
    for old_folder, new_folder in FOLDERS.items():
        origin = WEBP / old_folder
        for file in origin.iterdir():
            if not file.is_file() or file.suffix.lower() != ".webp":
                raise RuntimeError(f"Unexpected item in WebP tree: {file}")
            target = WEBP / new_folder / target_name(old_folder, file)
            if not within(file, WEBP) or not within(target, WEBP):
                raise RuntimeError("Path escaped WebP root")
            mapping[file] = target
    target_keys = [str(p).casefold() for p in mapping.values()]
    if len(target_keys) != len(set(target_keys)):
        raise RuntimeError("Canonical filenames would collide")
    return mapping


def local_url(value: str) -> bool:
    value = value.strip()
    return bool(value) and not value.startswith(("#", "//")) and not urlsplit(value).scheme


def path_for(html: Path, value: str) -> Path:
    decoded = unquote(urlsplit(value).path)
    if "\\" in decoded or re.match(r"^[A-Za-z]:", decoded):
        raise RuntimeError(f"Invalid web URL: {html}: {value}")
    result = (ROOT / decoded.lstrip("/")) if decoded.startswith("/") else (html.parent / decoded)
    result = result.resolve(strict=False)
    if not within(result, ROOT):
        raise RuntimeError(f"URL escaped site root: {html}: {value}")
    return result


class RefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.refs: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value is None:
                continue
            if name in ("src", "href", "srcset"):
                if name == "srcset":
                    for candidate in value.split(","):
                        self.refs.append((tag, name, candidate.strip().split()[0]))
                else:
                    self.refs.append((tag, name, value))
            if name == "style":
                for match in URL_RE.finditer(value):
                    self.refs.append((tag, "url", match.group("value")))


def scan(mapping: dict[Path, Path] | None = None) -> dict:
    results = {}
    for html in HTMLS:
        parser = RefParser()
        parser.feed(html.read_bytes().decode("utf-8-sig"))
        media, missing, bad, refs = [], [], [], []
        for tag, kind, url in parser.refs:
            if not local_url(url):
                continue
            physical = path_for(html, url)
            expected = mapping.get(physical, physical) if mapping else physical
            refs.append((kind, url, physical, expected))
            if tag in ("img", "source") and kind in ("src", "srcset"):
                media.append(url)
            if not physical.is_file():
                missing.append(url)
            if kind in ("src", "srcset", "url") and ("\\" in url or any(ord(c) > 127 for c in unquote(url)) or " " in unquote(url)):
                bad.append(url)
            if kind in ("src", "srcset", "url") and "Fotos_proyectos/webp/" in unquote(url):
                tail = unquote(url).split("Fotos_proyectos/webp/", 1)[1]
                if any(not SAFE_COMPONENT.fullmatch(c) for c in tail.split("/")):
                    bad.append(url)
        results[html.relative_to(ROOT).as_posix()] = {"images": len(media), "missing": missing, "bad": sorted(set(bad)), "refs": refs}
    return results


def rewrite_url(html: Path, value: str, mapping: dict[Path, Path]) -> str:
    if not local_url(value):
        return value
    old = path_for(html, value)
    if old not in mapping:
        return value
    suffix = ("?" + urlsplit(value).query if urlsplit(value).query else "") + ("#" + urlsplit(value).fragment if urlsplit(value).fragment else "")
    return Path(os.path.relpath(mapping[old], html.parent)).as_posix() + suffix


def rewrite_html(html: Path, original: bytes, mapping: dict[Path, Path]) -> bytes:
    text = original.decode("utf-8-sig")
    bom = b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b""

    def change_attr(match: re.Match) -> str:
        value = match.group("value")
        if match.group("name").strip().lower() == "srcset":
            chunks = []
            for part in value.split(","):
                found = re.match(r"(\s*)(\S+)(.*)", part, re.S)
                chunks.append(found.group(1) + rewrite_url(html, found.group(2), mapping) + found.group(3) if found else part)
            value = ",".join(chunks)
        else:
            value = rewrite_url(html, value, mapping)
        return match.group("name") + match.group("q") + value + match.group("q")

    text = ATTR_RE.sub(change_attr, text)
    text = URL_RE.sub(lambda m: "url(" + m.group("q") + rewrite_url(html, m.group("value"), mapping) + m.group("q") + ")", text)
    return bom + text.encode("utf-8")


def migrate(mapping: dict[Path, Path]) -> None:
    originals = {p: p.read_bytes() for p in HTMLS}
    revised = {p: rewrite_html(p, data, mapping) for p, data in originals.items()}
    referenced = {physical for entry in scan(mapping).values() for _, _, physical, _ in entry["refs"]}
    if any(p.suffix.lower() in (".jpg", ".jpeg", ".png") and within(p, ROOT / "Fotos_proyectos") for p in referenced):
        raise RuntimeError("A source original is referenced; stop for manual mapping")
    if any(entry["missing"] for entry in scan(mapping).values()):
        raise RuntimeError("Pre-migration missing local references")
    for old, new in FOLDERS.items():
        target = WEBP / new
        if target.exists() and not target.samefile(WEBP / old):
            raise RuntimeError(f"Canonical folder already exists: {target}")
    moved_dirs, moved_files, written = [], [], []
    try:
        for index, (old, new) in enumerate(FOLDERS.items()):
            current = WEBP / old
            temporary = WEBP / f"__tmp_web_asset_{index}"
            if temporary.exists():
                raise RuntimeError(f"Temporary path exists: {temporary}")
            current.rename(temporary)
            moved_dirs.append((temporary, current))
            temporary.rename(WEBP / new)
            moved_dirs.append((WEBP / new, temporary))
        for index, (old, new) in enumerate(mapping.items()):
            current = WEBP / FOLDERS[old.parent.name] / old.name
            temporary = current.with_name(f"__tmp_web_file_{index}.webp")
            current.rename(temporary)
            moved_files.append((temporary, current))
            temporary.rename(new)
            moved_files.append((new, temporary))
        for html, content in revised.items():
            if content != originals[html]:
                html.write_bytes(content)
                written.append(html)
        report = scan()
        if any(entry["missing"] or entry["bad"] for entry in report.values()):
            raise RuntimeError("Post-migration reference audit failed")
    except Exception:
        for html in written:
            html.write_bytes(originals[html])
        for current, previous in reversed(moved_files):
            if current.exists():
                current.rename(previous)
        for current, previous in reversed(moved_dirs):
            if current.exists():
                current.rename(previous)
        raise
    print("RENAMED FOLDERS:", len(FOLDERS))
    print("RENAMED FILES:", sum(old.name != new.name for old, new in mapping.items()))
    print("MODIFIED HTML:", ", ".join(p.relative_to(ROOT).as_posix() for p in written))


def package() -> None:
    dest = ROOT / "web_OVO_v4.zip"
    temporary = ROOT / "web_OVO_v4.zip.tmp"
    if temporary.exists():
        raise RuntimeError(f"Temporary ZIP already exists: {temporary}")
    files = [ROOT / name for name in ("index.html", "index_2.html", "style.css", "script.js")]
    files += sorted((ROOT / "proyectos").glob("*.html"))
    files += sorted(WEBP.rglob("*.webp"))
    linked_assets = {physical for entry in scan().values() for _, _, physical, _ in entry["refs"] if within(physical, ROOT / "assets")}
    files += sorted(linked_assets)
    with ZipFile(temporary, "w", ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file, file.relative_to(ROOT).as_posix())
    with ZipFile(temporary) as archive:
        names = archive.namelist()
        if archive.testzip() is not None or len(names) != len(set(names)):
            raise RuntimeError("ZIP integrity or duplicate-entry failure")
        if any("\\" in name or not name.isascii() or "rÝo" in name or "Presentacin" in name or "Difusin" in name for name in names):
            raise RuntimeError("ZIP contains non-POSIX or corrupted path")
        name_set = set(names)
        for html in HTMLS:
            parser = RefParser()
            parser.feed(archive.read(html.relative_to(ROOT).as_posix()).decode("utf-8-sig"))
            for tag, kind, url in parser.refs:
                if local_url(url):
                    asset = path_for(html, url).relative_to(ROOT).as_posix()
                    if asset not in name_set:
                        raise RuntimeError(f"ZIP missing {asset} from {html.name}")
    os.replace(temporary, dest)
    print("ZIP PASS:", dest, "entries:", len(names), "bytes:", dest.stat().st_size)


def main() -> None:
    arg = argparse.ArgumentParser()
    arg.add_argument("mode", choices=("audit", "migrate", "verify", "package"))
    mode = arg.parse_args().mode
    if mode in ("audit", "migrate"):
        mapping = plan()
        if mode == "audit":
            print("FOLDERS:")
            for old, new in FOLDERS.items():
                print(f"  {old} -> {new}")
            print("FILES:")
            for old, new in mapping.items():
                print(f"  {old.relative_to(ROOT).as_posix()} -> {new.relative_to(ROOT).as_posix()}")
        else:
            migrate(mapping)
    results = scan()
    for html, entry in results.items():
        print(f"{html}: OK={entry['images'] - len(entry['missing'])} IMAGES={entry['images']} MISSING={len(entry['missing'])} BAD={len(entry['bad'])}")
        for item in entry["missing"]:
            print("  MISSING", item)
    print("TOTAL IMAGES:", sum(r["images"] for r in results.values()))
    print("TOTAL MISSING:", sum(len(r["missing"]) for r in results.values()))
    print("RUTAS WEB NO NORMALIZADAS:", sum(len(r["bad"]) for r in results.values()))
    if mode in ("verify", "package") and any(r["missing"] or r["bad"] for r in results.values()):
        raise RuntimeError("Local reference verification failed")
    if mode == "package":
        package()


if __name__ == "__main__":
    main()
