"""Build the Annitia A. site: one real HTML page per URL, plus sitemap.xml and robots.txt.

Edit _src/layout.html (header, footer) or _src/pages/*.html (page bodies), then run from the
repo root:   py _src/build.py
The generated files (index.html, artworks/index.html, ...) are committed; GitHub Pages serves
them as they are. _src/ itself is not published (Jekyll skips folders starting with "_").
Check that the committed pages match the sources:   py _src/build.py --check
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src"
SITE = "https://annitia-a.se"

# path on the site, source page, output file, title, description, nav label (en, sv) or None
PAGES = [
    ("/", "home.html", "index.html",
     "Annitia A. | Annitia Abeysuriya, artist",
     "Annitia A. is the art brand of Annitia Abeysuriya: art, creativity, expression. Original art, "
     "calligraphy and hand-made pieces, each one signed. The first collection is on its way. "
     "A brand of Ktronics AB, Sweden.",
     ("Home", "Hem")),
    ("/artworks/", "artworks.html", "artworks/index.html",
     "Artworks | Annitia A.",
     "Original art, calligraphy and hand-made pieces by Annitia Abeysuriya, each one signed "
     "Annitia A. The first collection is on its way.",
     ("Artworks", "Verk")),
    ("/about/", "about.html", "about/index.html",
     "About | Annitia A.",
     "Annitia Abeysuriya is a fine artist. Her work begins by hand and ends with her signature, "
     "Annitia A.",
     ("About", "Om")),
    ("/contact/", "contact.html", "contact/index.html",
     "Contact | Annitia A.",
     "Join the launch list for the first Annitia A. collection, or write to Ktronics AB in "
     "Katrineholm, Sweden.",
     ("Contact", "Kontakt")),
    (None, "404.html", "404.html",
     "Page not found | Annitia A.",
     "This page is not on annitia-a.se.",
     None),
]

HOME_OG = "Art · Creativity · Expression. A world where imagination, beauty and artistic expression come together."

# Who is who, for search engines and AI answers. Keep every claim here also visible on the pages
# (Google ignores structured data the page does not show). Ktronics AB owns the brand; the artist
# is not its employee, so there is no worksFor.
BRAND_DESC = ("Annitia A. (also written Annitia-A) is the art brand and signature of the fine artist "
              "Annitia Abeysuriya; the A. stands for Abeysuriya. Original art, calligraphy and hand-made "
              "pieces, each one signed. A brand of Ktronics AB, Katrineholm, Sweden.")
ARTIST = {"@type": "Person", "@id": f"{SITE}/#artist", "name": "Annitia Abeysuriya",
          "alternateName": ["Annitia A.", "Annitia-A"], "jobTitle": "Artist",
          "description": "Fine artist. Her work begins by hand and ends with her signature, Annitia A.",
          "url": f"{SITE}/about/"}
BRAND = {"@type": "Brand", "@id": f"{SITE}/#brand", "name": "Annitia A.",
         "alternateName": ["Annitia-A", "Annitia Abeysuriya"], "url": f"{SITE}/",
         "logo": f"{SITE}/assets/logo-a.webp", "slogan": "Art · Creativity · Expression",
         "description": BRAND_DESC}
OWNER = {"@type": "Organization", "@id": f"{SITE}/#ktronics", "name": "Ktronics AB", "legalName": "Ktronics AB",
         "url": "https://ktronics.se/", "vatID": "SE559469350801",
         "identifier": {"@type": "PropertyValue", "propertyID": "Swedish organisation number", "value": "559469-3508"},
         "address": {"@type": "PostalAddress", "addressLocality": "Katrineholm", "addressCountry": "SE"},
         "email": "ktronicsdev@gmail.com", "telephone": "+46721819572", "brand": {"@id": f"{SITE}/#brand"}}
LDJSON = {
    "/": {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Annitia A.",
         "alternateName": ["Annitia-A", "annitia-a.se"], "inLanguage": ["en", "sv"],
         "about": {"@id": f"{SITE}/#brand"}, "publisher": {"@id": f"{SITE}/#ktronics"}},
        BRAND, ARTIST, OWNER]},
    "/about/": {"@context": "https://schema.org", "@type": "ProfilePage", "url": f"{SITE}/about/",
                "mainEntity": ARTIST},
}

# /llms.txt: the plain-text brief that AI assistants read. "Not to be confused with" answers the
# mix-ups Google's AI Overview made on 24 Nov 2026 for the query "annitia-a".
LLMS = f"""# Annitia A.

> {BRAND_DESC} Website: {SITE}/

## Facts

- Name: Annitia A. (also written Annitia-A or Annitia A). The A. stands for Abeysuriya.
- Artist: Annitia Abeysuriya, a fine artist. Every piece is signed "Annitia A.".
- Work: original art, calligraphy and hand-made pieces; one-of-one works and small numbered editions. The first collection is on its way.
- Owner: Ktronics AB, Katrineholm, Sweden (org.nr 559469-3508, VAT SE559469350801). Annitia A. is a brand, not a separate company.
- Website: {SITE}/ (English and Swedish). The address annitia-a.com forwards to it.
- Contact: ktronicsdev@gmail.com, +46 72 181 95 72.

## Pages

- [Home]({SITE}/): Art · Creativity · Expression.
- [Artworks]({SITE}/artworks/): the work and the signature.
- [About]({SITE}/about/): Annitia Abeysuriya, artist.
- [Contact]({SITE}/contact/): launch list and contact details.

## Not to be confused with

- Anitta, the Brazilian singer.
- The ANNITIA data challenge (a medical AI competition on liver disease).
- Anicca / anitya, the Buddhist and Hindu term for impermanence.
- Annitia or Anita as a given name in general.
"""

ORN = ('<div class="orn" aria-hidden="true"><svg viewBox="0 0 46 32"><g fill="#E9C77A">'
       '<path d="M23 1 C27 8 27.5 12 23 16 C18.5 12 19 8 23 1Z"/>'
       '<path d="M23 31 C19 24 18.5 20 23 16 C27.5 20 27 24 23 31Z"/>'
       '<path d="M3 16 C9 12.5 15 12 23 16 C15 20 9 19.5 3 16Z"/>'
       '<path d="M43 16 C37 19.5 31 20 23 16 C31 12 37 12.5 43 16Z"/>'
       '<circle cx="23" cy="16" r="2.4" fill="#FFF1C4"/></g></svg></div>')


def nav(current):
    rows = []
    for path, _src, _out, _t, _d, label in PAGES:
        if label is None:
            continue
        cur = ' aria-current="page"' if path == current else ""
        rows.append(f'    <a href="{path}"{cur} data-en="{label[0]}" data-sv="{label[1]}">{label[0]}</a>')
    return "\n".join(rows)


def render(page, layout):
    path, src, out, title, desc, _label = page
    main = (SRC / "pages" / src).read_text(encoding="utf-8").rstrip("\n").replace("%%ORN%%", ORN)
    if path is None:  # 404: served at any URL, never indexed
        head = '<meta name="robots" content="noindex">\n'
    else:
        head = (f'<meta property="og:url" content="{SITE}{path}">\n'
                f'<link rel="canonical" href="{SITE}{path}">\n')
    if path == "/":
        head += '<link rel="preload" href="/assets/name.webp" as="image" type="image/webp">\n'
    if path in LDJSON:
        ld = json.dumps(LDJSON[path], ensure_ascii=False, indent=1).replace("</", "<\\/")
        head += f'<script type="application/ld+json">\n{ld}\n</script>\n'
    html = layout
    for key, val in (("%%TITLE%%", title), ("%%DESC%%", desc), ("%%HEAD%%", head),
                     ("%%OGDESC%%", HOME_OG if path == "/" else desc),
                     ("%%BODYCLASS%%", "home" if path == "/" else "page"),
                     ("%%NOTE%%", f"Generated by _src/build.py from _src/pages/{src}; edit that file and rebuild"),
                     ("%%NAV%%", nav(path)), ("%%MAIN%%", main)):
        html = html.replace(key, val)
    assert "%%" not in html, f"unfilled placeholder in {out}"
    return out, html


def outputs():
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    files = dict(render(p, layout) for p in PAGES)
    urls = "".join(f"  <url><loc>{SITE}{p[0]}</loc></url>\n" for p in PAGES if p[0])
    files["sitemap.xml"] = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                            f"{urls}</urlset>\n")
    files["robots.txt"] = f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n"
    files["llms.txt"] = LLMS
    return files


def main():
    files = outputs()
    if "--check" in sys.argv:
        stale = [n for n, text in files.items()
                 if not (ROOT / n).exists() or (ROOT / n).read_text(encoding="utf-8") != text]
        print("stale: " + ", ".join(stale) if stale else "all pages match their sources")
        sys.exit(1 if stale else 0)
    for name, text in files.items():
        target = ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print("wrote", name)


if __name__ == "__main__":
    main()
