#!/usr/bin/env python3
"""Generate static SEO tags, robots.txt and sitemap.xml for this HTML site."""
import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
TITLE = "Vasudeva Hari Vury | Full Stack & AI Agent Developer"
DESCRIPTION = (
    "Explore Vasudeva Hari Vury's developer portfolio: voice AI agents, Python backend "
    "APIs, Next.js applications and Supabase-powered appointment booking workflows."
)
IMAGE = "https://raw.githubusercontent.com/vasudevahari/Portfolio/main/img.jpg"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", nargs="?", help="Exact public HTTPS homepage URL")
    parser.add_argument("--verification", help="Google Search Console HTML-tag content value")
    args = parser.parse_args()
    config_path = ROOT / "seo-config.json"
    config = json.loads(config_path.read_text()) if config_path.exists() else {}
    if args.url:
        parts = urlsplit(args.url)
        if (parts.scheme != "https" or not parts.hostname or parts.username or
                parts.password or parts.query or parts.fragment or
                any(c.isspace() for c in args.url)):
            parser.error("Use the real HTTPS homepage URL without credentials, query or fragment.")
        config["url"] = urlunsplit((parts.scheme, parts.netloc, parts.path.rstrip("/") + "/", "", ""))
    if args.verification:
        if not re.fullmatch(r"[A-Za-z0-9_-]+", args.verification):
            parser.error("Provide only the verification tag's content value, not the whole tag.")
        config["verification"] = args.verification
    url = config.get("url")
    person = {
        "@type": "Person", "name": "Vasudeva Hari Vury",
        "alternateName": "Vasudeva Hari", "description": DESCRIPTION,
        "image": IMAGE,
        "sameAs": ["https://github.com/vasudevahari",
                   "https://www.linkedin.com/in/hari-vury-61a363324"],
    }
    schema = {"@context": "https://schema.org", "@type": "ProfilePage",
              "name": TITLE, "description": DESCRIPTION, "mainEntity": person}
    tags = [f"<title>{html.escape(TITLE)}</title>"]
    def meta(key, value, attribute="name"):
        tags.append(f'<meta {attribute}="{key}" content="{html.escape(value, quote=True)}" />')
    meta("description", DESCRIPTION)
    meta("robots", "index, follow")
    for key, value in [("og:title", TITLE), ("og:description", DESCRIPTION),
                       ("og:type", "website"), ("og:site_name", "Vasudeva Hari Portfolio"),
                       ("og:locale", "en_IN"), ("og:image", IMAGE),
                       ("og:image:alt", "Portrait of Vasudeva Hari Vury")]:
        meta(key, value, "property")
    for key, value in [("twitter:card", "summary_large_image"), ("twitter:title", TITLE),
                       ("twitter:description", DESCRIPTION), ("twitter:image", IMAGE),
                       ("twitter:image:alt", "Portrait of Vasudeva Hari Vury")]:
        meta(key, value)
    robots = "User-agent: *\nAllow: /\n"
    if url:
        tags.append(f'<link rel="canonical" href="{html.escape(url, quote=True)}" />')
        meta("og:url", url, "property")
        schema["url"] = url
        person["url"] = url
        person["@id"] = url + "#person"
        robots += "\nSitemap: " + url + "sitemap.xml\n"
        sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                   f'  <url><loc>{html.escape(url)}</loc></url>\n</urlset>\n')
        (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    if config.get("verification"):
        meta("google-site-verification", config["verification"])
    tags.append('<script type="application/ld+json">\n' +
                json.dumps(schema, ensure_ascii=False, indent=2).replace("<", "\\u003c") +
                '\n</script>')
    path = ROOT / "index.html"
    source = path.read_text(encoding="utf-8")
    source, count = re.subn(r"<!-- SEO:START -->[\s\S]*?<!-- SEO:END -->",
                           lambda _: "<!-- SEO:START -->\n  " + "\n  ".join(tags) +
                           "\n  <!-- SEO:END -->", source)
    if count != 1:
        raise SystemExit("Expected exactly one SEO marker block; no HTML was written.")
    path.write_text(source, encoding="utf-8")
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print("SEO generated for " + url if url else "Base SEO generated. Supply the live URL to generate canonical and sitemap.")


if __name__ == "__main__":
    main()
