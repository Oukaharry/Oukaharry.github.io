#!/usr/bin/env python3
"""Build the static site into the repository root for GitHub Pages."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "posts"
BASE = "https://oukaharry.github.io"
TODAY = "2026-11-12"

PERSON = {
    "@type": "Person",
    "@id": BASE + "/#person",
    "name": "Harrison Odhiambo Ouka",
    "alternateName": ["Harry Ouka", "Ouka Harry", "Harrison Ouka"],
    "jobTitle": "Software Developer",
    "url": BASE + "/",
    "email": "harryodhiambo17@gmail.com",
    "image": BASE + "/assets/og.png",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Nairobi",
        "addressCountry": "KE",
    },
    "alumniOf": {
        "@type": "CollegeOrUniversity",
        "name": "The Catholic University of Eastern Africa",
    },
    "hasCredential": {
        "@type": "EducationalOccupationalCredential",
        "credentialCategory": "degree",
        "name": "BSc Computer Science",
        "description": "2017–2021",
        "recognizedBy": {
            "@type": "CollegeOrUniversity",
            "name": "The Catholic University of Eastern Africa",
        },
    },
    "worksFor": {
        "@type": "Organization",
        "name": "blueedgefinancial.com",
        "url": "https://blueedgefinancial.com/",
    },
    "hasOccupation": [
        {
            "@type": "Occupation",
            "name": "Software Developer",
            "description": "Software Developer at blueedgefinancial.com since September 2020",
        },
        {
            "@type": "Occupation",
            "name": "Foreign Exchange Consultant",
            "description": "Freelance",
        },
    ],
    "sameAs": [
        "https://github.com/Oukaharry",
        "https://www.linkedin.com/in/harrisonouka/",
        "https://dev.to/harrisonouka",
        "https://www.mql5.com/en/users/_mrharry",
        "https://www.mql5.com/en/users/_harrison",
    ],
}

NAV = [
    ("/", "Home"),
    ("/about/", "About"),
    ("/projects/", "Projects"),
    ("/blog/", "Blog"),
    ("/contact/", "Contact"),
]

POSTS = [
    {
        "slug": "on-chart-trade-manager-mql4",
        "title": "Building an on-chart trade manager in MQL4",
        "seo_title": "On-Chart MQL4 Trade Managers · Harry Ouka, Software Developer",
        "description": "Harrison Odhiambo Ouka (Harry Ouka), a software developer, on the structure of TradeManagerEA: chart-object panels, magic numbers, partial closes, and pip sizes in MQL4.",
        "date": "2026-11-04",
        "excerpt": "How TradeManagerEA uses an on-chart panel, a magic number, and partial-close levels, and which close-price and pip-size details to check before extending it.",
        "file": "on-chart-trade-manager-mql4.html",
    },
    {
        "slug": "django-account-pairs",
        "title": "Pairing live and prop-firm accounts in Django",
        "seo_title": "Django Account Pairs · Ouka Harry, Software Developer",
        "description": "Ouka Harry (Harrison Odhiambo Ouka), software developer, on HedgePass Pro: Django models for live and prop accounts, Fernet encryption, and secrets that do not belong in git.",
        "date": "2026-11-08",
        "excerpt": "The Django models behind HedgePass Pro: live and prop account pairs, Fernet encryption of trading passwords, and what should never be committed beside them.",
        "file": "django-account-pairs.html",
    },
    {
        "slug": "c-pointers-and-the-shell",
        "title": "What C pointers and the shell are for",
        "seo_title": "C Pointers and the Shell · Harrison Odhiambo Ouka, Software Developer",
        "description": "Software developer Harrison Odhiambo Ouka on his public ALX coursework: C pointers, arrays, function pointers, and the Unix shell commands that run the programs.",
        "date": "2026-11-12",
        "excerpt": "Notes from public ALX coursework in C and the Unix shell: addresses versus values, function pointers, and the commands that actually run the binary.",
        "file": "c-pointers-and-the-shell.html",
    },
]

PROJECTS = [
    {
        "id": "trademanagerea",
        "name": "TradeManagerEA",
        "year": "2021",
        "language": "MQL4",
        "summary": "A MetaTrader 4 expert advisor with an on-chart GUI for placing trades, configurable stop-loss and take-profit levels, and partial closes.",
        "tags": ["MetaTrader 4", "Expert advisor", "MQL4"],
        "repo": "https://github.com/Oukaharry/TradeManagerEA",
    },
    {
        "id": "hedgepass-pro",
        "name": "HedgePass Pro",
        "year": "2025",
        "language": "Python · Django",
        "summary": "A Django web application for prop-firm challenge hedging and trade management, with a client dashboard, account pairs, and settings.",
        "tags": ["Django", "Python", "HTML", "CSS", "JavaScript"],
        "repo": "https://github.com/Oukaharry/hedgepass-pro",
        "demo": "https://hedgepass-pro.vercel.app",
    },
    {
        "id": "alx-c",
        "name": "alx-low_level_programming",
        "year": "2021",
        "language": "C",
        "summary": "ALX low-level programming coursework in C: variables, functions, debugging, pointers, arrays, strings, static libraries, function pointers, and variadic functions.",
        "tags": ["C", "ALX coursework"],
        "repo": "https://github.com/Oukaharry/alx-low_level_programming",
    },
    {
        "id": "alx-shell",
        "name": "alx-system_engineering-devops",
        "year": "2021–2022",
        "language": "Shell",
        "summary": "ALX systems coursework in the Unix shell: basics, permissions, redirections, and variable expansions.",
        "tags": ["Shell", "Unix", "ALX coursework"],
        "repo": "https://github.com/Oukaharry/alx-system_engineering-devops",
    },
    {
        "id": "cpointers",
        "name": "CPointers",
        "year": "2021",
        "language": "C",
        "summary": "Short C programs on sizeof, addresses, and dereferencing, kept beside the larger ALX C repository.",
        "tags": ["C", "Pointers"],
        "repo": "https://github.com/Oukaharry/CPointers",
    },
]

LOGO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="HO, initials of Harrison Odhiambo Ouka" width="36" height="36">
  <rect width="64" height="64" rx="14" fill="#0e5c4a"/>
  <path fill="#f4efe6" d="M14 16h6.2v12.2h11.2V16H38v32h-6.6V34.4H20.2V48H14V16z"/>
  <circle cx="48" cy="32" r="8.2" fill="none" stroke="#f4efe6" stroke-width="4.2"/>
</svg>"""


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def word_count(fragment: str) -> int:
    text = re.sub(r"<[^>]+>", " ", fragment)
    for src, dest in (("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&"), ("&nbsp;", " ")):
        text = text.replace(src, dest)
    return len([word for word in re.split(r"\s+", text.strip()) if word])


def pretty_date(iso: str) -> str:
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%-d %B %Y")


def load_token() -> str:
    raw = (ROOT / "config" / "search-console.txt").read_text(encoding="utf-8")
    token = ""
    for line in raw.splitlines():
        if line.startswith("GOOGLE_SITE_VERIFICATION="):
            token = line.split("=", 1)[1].strip()
    if not token or token == "PASTE_TOKEN_HERE":
        return ""
    return token


def verification_html() -> str:
    token = load_token()
    if token:
        return (
            "<!-- Google Search Console token: /config/search-console.txt -->\n"
            f'  <meta name="google-site-verification" content="{esc(token)}" />'
        )
    return """<!--
  Google Search Console verification placeholder.
  Set GOOGLE_SITE_VERIFICATION in /config/search-console.txt
  (replace PASTE_TOKEN_HERE), then run: python3 scripts/build_site.py
  The meta tag to add is:
  <meta name="google-site-verification" content="PASTE_TOKEN_HERE" />
-->"""


def person_json(*extra: dict) -> str:
    graph = [PERSON, *extra]
    payload = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(payload, ensure_ascii=False, indent=2)


def nav_html(current: str) -> str:
    items = []
    for href, label in NAV:
        current_attr = ' aria-current="page"' if href == current else ""
        items.append(f'<a href="{href}"{current_attr}>{label}</a>')
    return "\n        ".join(items)


def chrome(current: str, title: str, description: str, path: str, body: str, jsonld: str, robots: str = "index,follow,max-image-preview:large", og_type: str = "website", extra_head: str = "") -> str:
    canonical = BASE + path
    og_image = BASE + "/assets/og.png"
    og_alt = "Harrison Odhiambo Ouka, software developer in Nairobi, also known as Harry Ouka and Ouka Harry."
    canonical_tag = f'<link rel="canonical" href="{canonical}" />' if robots.startswith("index") else ""
    return f"""<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <script>
    (function () {{
      try {{
        var stored = localStorage.getItem("theme");
        var theme = stored || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
        document.documentElement.setAttribute("data-theme", theme);
      }} catch (err) {{
        document.documentElement.setAttribute("data-theme", "light");
      }}
      document.documentElement.classList.remove("no-js");
      document.documentElement.classList.add("js");
    }})();
  </script>
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <meta name="author" content="Harrison Odhiambo Ouka" />
  <meta name="robots" content="{robots}" />
  <meta name="theme-color" content="#f3efe6" />
  {canonical_tag}
  <link rel="alternate" hreflang="en" href="{canonical if robots.startswith('index') else BASE + '/'}" />
  <link rel="alternate" type="application/rss+xml" title="Harrison Odhiambo Ouka — RSS" href="{BASE}/feed.xml" />
  <link rel="alternate" type="application/atom+xml" title="Harrison Odhiambo Ouka — Atom" href="{BASE}/atom.xml" />
  <link rel="me" href="https://github.com/Oukaharry" />
  <link rel="me" href="https://www.linkedin.com/in/harrisonouka/" />
  <link rel="me" href="https://dev.to/harrisonouka" />
  <meta property="og:site_name" content="Harrison Odhiambo Ouka" />
  <meta property="og:locale" content="en_KE" />
  <meta property="og:type" content="{og_type}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(description)}" />
  <meta property="og:url" content="{canonical if robots.startswith('index') else BASE + '/'}" />
  <meta property="og:image" content="{og_image}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{esc(og_alt)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(description)}" />
  <meta name="twitter:image" content="{og_image}" />
  <meta name="twitter:image:alt" content="{esc(og_alt)}" />
  {verification_html()}
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
  <link rel="icon" href="/assets/favicon-32.png" type="image/png" sizes="32x32" />
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <link rel="stylesheet" href="/css/styles.css" />
  {extra_head}
  <script type="application/ld+json">
{jsonld}
  </script>
</head>
<body>
  <a class="skip-link" href="#content">Skip to content</a>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="/">
        {LOGO}
        <span class="brand-text">Harrison Ouka<small>Software Developer</small></span>
      </a>
      <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><span class="menu-closed">Menu</span><span class="menu-open">Close</span></button>
      <nav class="site-nav" id="site-nav" data-nav aria-label="Primary">
        {nav_html(current)}
      </nav>
      <div class="header-actions">
        <button class="theme-toggle" type="button" data-theme-toggle aria-pressed="false" aria-label="Switch to dark theme">
          <span class="when-light">Dark</span>
          <span class="when-dark">Light</span>
        </button>
      </div>
    </div>
  </header>
  <main id="content" tabindex="-1">
    {body}
  </main>
  <footer class="site-footer">
    <div class="wrap footer-inner">
      <p>Harrison Odhiambo Ouka · Harry Ouka · Ouka Harry · Software developer in Nairobi, Kenya.</p>
      <nav class="footer-nav" aria-label="Footer">
        <a href="/about/">About</a>
        <a href="/projects/">Projects</a>
        <a href="/blog/">Blog</a>
        <a href="/contact/">Contact</a>
        <a href="/feed.xml">RSS</a>
        <a href="https://github.com/Oukaharry">GitHub</a>
        <a href="https://www.linkedin.com/in/harrisonouka/">LinkedIn</a>
        <a href="https://dev.to/harrisonouka">DEV</a>
      </nav>
    </div>
  </footer>
  <script src="/js/site.js"></script>
</body>
</html>
"""


def write_page(relative: str, markup: str) -> None:
    dest = ROOT / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(markup, encoding="utf-8")


def project_card(project: dict) -> str:
    tags = "".join(f"<li>{esc(tag)}</li>" for tag in project["tags"])
    demo = ""
    if project.get("demo"):
        demo = f'<a href="{esc(project["demo"])}">Live demo</a>'
    return f"""<article class="project" id="{esc(project["id"])}">
      <p class="eyebrow">{esc(project["language"])} · {esc(project["year"])}</p>
      <h3><a href="{esc(project["repo"])}">{esc(project["name"])}</a></h3>
      <p>{esc(project["summary"])}</p>
      <ul class="tags">{tags}</ul>
      <p class="links"><a href="{esc(project["repo"])}">Source on GitHub</a>{demo}</p>
    </article>"""


def home_body() -> str:
    featured = "".join(project_card(project) for project in PROJECTS[:2])
    posts = []
    for post in sorted(POSTS, key=lambda item: item["date"], reverse=True):
        posts.append(
            f"""<li>
          <time datetime="{post["date"]}">{pretty_date(post["date"])}</time>
          <div>
            <h3><a href="/blog/{post["slug"]}/">{esc(post["title"])}</a></h3>
            <p>{esc(post["excerpt"])}</p>
          </div>
        </li>"""
        )
    return f"""<div class="wrap">
      <section class="hero" aria-labelledby="home-title">
        <div>
          <p class="kicker">Nairobi, Kenya</p>
          <p class="headline">Software Developer</p>
          <h1 id="home-title">Harrison Odhiambo Ouka</h1>
          <p class="aliases">Also known as <strong>Harry Ouka</strong> and <strong>Ouka Harry</strong>.</p>
          <p class="lede">I build algorithmic trading tools in MQL4 and MQL5, and web applications in Python and Django. This site is the public home for that work: the repositories, and notes on how they are put together.</p>
          <div class="cta">
            <a class="button" href="/projects/">View projects</a>
            <a class="button button-ghost" href="/contact/">Contact Harrison</a>
          </div>
        </div>
        <aside class="id-card">
          <dl>
            <div><dt>Full name</dt><dd>Harrison Odhiambo Ouka</dd></div>
            <div><dt>Also known as</dt><dd>Harry Ouka<br />Ouka Harry<br />Harrison Ouka</dd></div>
            <div><dt>Role</dt><dd>Software Developer</dd></div>
            <div><dt>Based in</dt><dd>Nairobi, Kenya</dd></div>
            <div><dt>Email</dt><dd><a href="mailto:harryodhiambo17@gmail.com">harryodhiambo17@gmail.com</a></dd></div>
          </dl>
        </aside>
      </section>

      <section class="section" aria-labelledby="work-heading">
        <div class="section-head">
          <h2 id="work-heading">What I build</h2>
        </div>
        <div class="split">
          <article class="panel">
            <h3>Trading tools</h3>
            <p>MetaTrader expert advisors and trade-management tools in MQL4 and MQL5. The public example is TradeManagerEA, an on-chart panel for orders, stops, targets, and partial closes.</p>
          </article>
          <article class="panel">
            <h3>Web applications</h3>
            <p>Python and Django applications that support trading workflows. HedgePass Pro is a client dashboard for prop-firm account pairs, with HTML, CSS, and JavaScript on the pages.</p>
          </article>
          <article class="panel">
            <h3>Systems coursework</h3>
            <p>C and Unix/Linux coursework from the ALX software engineering program, published in the public repositories.</p>
          </article>
        </div>
      </section>

      <section class="section" aria-labelledby="projects-heading">
        <div class="section-head">
          <h2 id="projects-heading">Selected projects</h2>
          <a href="/projects/">All projects</a>
        </div>
        <div class="cards">
          {featured}
        </div>
      </section>

      <section class="section" aria-labelledby="notes-heading">
        <div class="section-head">
          <h2 id="notes-heading">Notes</h2>
          <a href="/blog/">All notes</a>
        </div>
        <ol class="post-list">
          {"".join(posts)}
        </ol>
      </section>
    </div>"""


def about_body() -> str:
    return """<div class="wrap">
      <header class="page-intro">
        <p class="kicker">About</p>
        <h1>Harrison Odhiambo Ouka, known as Harry Ouka / Ouka Harry</h1>
        <p class="lede">I am a software developer based in Nairobi, Kenya. I build algorithmic trading systems and web applications that support trading workflows.</p>
      </header>
      <div class="prose">
        <p>The public record of that work is my GitHub account, <a href="https://github.com/Oukaharry">github.com/Oukaharry</a>, created in December 2018. The profile README is the short version of this page: MetaTrader expert advisors and trade-management tools written in MQL4 and MQL5, plus Python and Django applications.</p>
        <p>Two repositories carry the product work. <a href="https://github.com/Oukaharry/TradeManagerEA">TradeManagerEA</a> is a MetaTrader 4 expert advisor. It puts a GUI on the chart for placing trades, setting stop-loss and take-profit levels, and closing part of a position. <a href="https://github.com/Oukaharry/hedgepass-pro">HedgePass Pro</a> is a Django web application for prop-firm challenge hedging and trade management, with a client dashboard and account settings. A demo of that app is at <a href="https://hedgepass-pro.vercel.app">hedgepass-pro.vercel.app</a>.</p>
        <p>I have also completed software engineering coursework in C and Unix/Linux through the ALX program. Those repositories are public: <a href="https://github.com/Oukaharry/alx-low_level_programming">alx-low_level_programming</a>, <a href="https://github.com/Oukaharry/alx-system_engineering-devops">alx-system_engineering-devops</a>, and <a href="https://github.com/Oukaharry/CPointers">CPointers</a>. The earliest ALX repositories, from 2021, describe them as the first ones I published as an ALX student.</p>
        <p>I take freelance development work through my MQL5 profiles, <a href="https://www.mql5.com/en/users/_mrharry">_mrharry</a> and <a href="https://www.mql5.com/en/users/_harrison">_harrison</a>. The direct email is <a href="mailto:harryodhiambo17@gmail.com">harryodhiambo17@gmail.com</a>. I am also on <a href="https://www.linkedin.com/in/harrisonouka/">LinkedIn</a> and <a href="https://dev.to/harrisonouka">DEV</a>.</p>
        <p>If you searched for Ouka Harry, Harry Ouka, or Harrison Odhiambo Ouka, you are in the right place. Those are my names. The work on this site is the work in those repositories, and the notes are written from reading them.</p>
      </div>
      <section class="section" aria-labelledby="background-heading">
        <h2 id="background-heading">Education and work</h2>
        <table class="stack-table">
          <caption class="sr-only">Education and work of Harrison Odhiambo Ouka</caption>
          <thead>
            <tr><th scope="col">When</th><th scope="col">What</th></tr>
          </thead>
          <tbody>
            <tr>
              <td>2017–2021</td>
              <td>BSc Computer Science, The Catholic University of Eastern Africa</td>
            </tr>
            <tr>
              <td>September 2020–present</td>
              <td>Software Developer at <a href="https://blueedgefinancial.com/">blueedgefinancial.com</a></td>
            </tr>
            <tr>
              <td>Freelance</td>
              <td>Foreign Exchange Consultant</td>
            </tr>
          </tbody>
        </table>
      </section>
      <section class="section" aria-labelledby="stack-heading">
        <h2 id="stack-heading">Stack, as the repositories show it</h2>
        <div class="prose">
          <p>This is not a wishlist. Each row is something a public repository or the profile README actually contains.</p>
        </div>
        <table class="stack-table">
          <caption class="sr-only">Tools evidenced on the public GitHub profile and repositories of Harrison Odhiambo Ouka</caption>
          <thead>
            <tr><th scope="col">Tool</th><th scope="col">Where it shows up</th></tr>
          </thead>
          <tbody>
            <tr><td>MQL4</td><td>TradeManagerEA, a MetaTrader 4 expert advisor</td></tr>
            <tr><td>MQL5 and MetaTrader</td><td>Named in the profile README, and the MQL5 profiles used for freelance work</td></tr>
            <tr><td>Python and Django</td><td>HedgePass Pro</td></tr>
            <tr><td>HTML, CSS, JavaScript</td><td>Templates and static files in HedgePass Pro</td></tr>
            <tr><td>C</td><td>alx-low_level_programming and CPointers</td></tr>
            <tr><td>Shell</td><td>alx-system_engineering-devops</td></tr>
            <tr><td>Git</td><td>The version control used across the public repositories</td></tr>
          </tbody>
        </table>
      </section>
    </div>"""


def projects_body() -> str:
    cards = "".join(project_card(project) for project in PROJECTS)
    return f"""<div class="wrap">
      <header class="page-intro">
        <p class="kicker">Projects</p>
        <h1>Projects by Harrison Odhiambo Ouka</h1>
        <p class="lede">Software from the public GitHub account of Harry Ouka / Ouka Harry. Each card matches a repository that contains the work.</p>
      </header>
      <div class="cards" style="margin-top:1.5rem">
        {cards}
      </div>
      <section class="section prose">
        <h2>Also on GitHub</h2>
        <p>A few smaller repositories sit next to the ones above. They are starter or tutorial trees, and the descriptions below are the ones on GitHub.</p>
        <ul class="also-list">
          <li><a href="https://github.com/Oukaharry/alx-pre_course">alx-pre_course</a> — described as a first repository as an ALX student.</li>
          <li><a href="https://github.com/Oukaharry/alx-zero_day">alx-zero_day</a> — the same description, in shell.</li>
          <li><a href="https://github.com/Oukaharry/Tutorials">Tutorials</a> — C files, described as files from tutorials.</li>
        </ul>
      </section>
    </div>"""


def blog_index_body(loaded: list[dict]) -> str:
    items = []
    for post in sorted(loaded, key=lambda item: item["date"], reverse=True):
        minutes = max(1, round(post["words"] / 220))
        items.append(
            f"""<li>
          <time datetime="{post["date"]}">{pretty_date(post["date"])}</time>
          <div>
            <h2><a href="/blog/{post["slug"]}/">{esc(post["title"])}</a></h2>
            <p>{esc(post["excerpt"])} · {minutes} min read</p>
          </div>
        </li>"""
        )
    return f"""<div class="wrap">
      <header class="page-intro">
        <p class="kicker">Blog</p>
        <h1>Notes from Harrison Odhiambo Ouka</h1>
        <p class="lede">Technical notes by a software developer in Nairobi. Harry Ouka writes here about the MQL4, Django, and C work in the public repositories. Nothing on this list is a product announcement.</p>
      </header>
      <ol class="post-list" style="margin-top:1.5rem">
        {"".join(items)}
      </ol>
    </div>"""


def contact_body() -> str:
    return """<div class="wrap">
      <header class="page-intro">
        <p class="kicker">Contact</p>
        <h1>Contact Harrison Odhiambo Ouka</h1>
        <p class="lede">Harry Ouka / Ouka Harry, software developer in Nairobi. Email is the reliable way to reach me. I also list GitHub, LinkedIn, DEV, and the MQL5 profiles I use for freelance development work.</p>
      </header>
      <div class="contact-grid">
        <section class="panel" aria-labelledby="reach-heading">
          <h2 id="reach-heading">Reach me</h2>
          <ul class="contact-list">
            <li><span>Email</span><a href="mailto:harryodhiambo17@gmail.com">harryodhiambo17@gmail.com</a></li>
            <li><span>GitHub</span><a href="https://github.com/Oukaharry">github.com/Oukaharry</a></li>
            <li><span>LinkedIn</span><a href="https://www.linkedin.com/in/harrisonouka/">linkedin.com/in/harrisonouka</a></li>
            <li><span>DEV</span><a href="https://dev.to/harrisonouka">dev.to/harrisonouka</a></li>
            <li><span>MQL5</span><a href="https://www.mql5.com/en/users/_mrharry">mql5.com/en/users/_mrharry</a></li>
            <li><span>MQL5</span><a href="https://www.mql5.com/en/users/_harrison">mql5.com/en/users/_harrison</a></li>
            <li><span>Location</span>Nairobi, Kenya</li>
          </ul>
        </section>
        <section class="panel" aria-labelledby="form-heading">
          <h2 id="form-heading">Open an email</h2>
          <p class="form-note">This is a static site. The form opens your email app addressed to Harrison. It does not store the message.</p>
          <form id="contact-form">
            <label for="name">Your name
              <input id="name" name="name" type="text" autocomplete="name" required />
            </label>
            <label for="email">Your email
              <input id="email" name="email" type="email" autocomplete="email" required />
            </label>
            <label for="message">Message
              <textarea id="message" name="message" required></textarea>
            </label>
            <button class="button" type="submit">Email Harrison Odhiambo Ouka</button>
            <p id="form-status" role="status"></p>
          </form>
        </section>
      </div>
    </div>"""


def post_body(post: dict) -> str:
    minutes = max(1, round(post["words"] / 220))
    others = []
    for other in POSTS:
        if other["slug"] == post["slug"]:
            continue
        others.append(f'<li><a href="/blog/{other["slug"]}/">{esc(other["title"])}</a></li>')
    return f"""<div class="wrap">
      <article class="prose">
        <header class="page-intro">
          <p class="kicker">Notes</p>
          <h1>{esc(post["title"])}</h1>
          <p class="byline">By <a href="/about/">Harrison Odhiambo Ouka</a> · <time datetime="{post["date"]}">{pretty_date(post["date"])}</time> · {minutes} min read</p>
        </header>
        {post["html"]}
        <nav class="note" aria-label="More from the blog">
          <p>More from Harrison Odhiambo Ouka</p>
          <ul>
            {"".join(others)}
          </ul>
        </nav>
      </article>
    </div>"""


def posting_json(post: dict) -> dict:
    url = f"{BASE}/blog/{post['slug']}/"
    return {
        "@type": "BlogPosting",
        "@id": url + "#post",
        "headline": post["title"],
        "description": post["description"],
        "datePublished": post["date"],
        "dateModified": TODAY,
        "wordCount": post["words"],
        "inLanguage": "en",
        "mainEntityOfPage": url,
        "url": url,
        "image": BASE + "/assets/og.png",
        "author": {"@id": BASE + "/#person"},
        "publisher": {"@id": BASE + "/#person"},
    }


def load_posts() -> list[dict]:
    loaded = []
    for post in POSTS:
        fragment = (CONTENT / post["file"]).read_text(encoding="utf-8").strip()
        count = word_count(fragment)
        if not 600 <= count <= 1000:
            raise SystemExit(f"{post['file']} is {count} words; expected 600-1000")
        item = dict(post)
        item["html"] = fragment
        item["words"] = count
        loaded.append(item)
    return loaded


def rfc822(iso: str) -> str:
    stamp = datetime.strptime(iso, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return format_datetime(stamp)


def write_feeds(posts: list[dict]) -> None:
    items = []
    atom_entries = []
    updated = rfc822(TODAY)
    for post in sorted(posts, key=lambda item: item["date"], reverse=True):
        url = f"{BASE}/blog/{post['slug']}/"
        items.append(
            f"""    <item>
      <title>{esc(post["title"])}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{rfc822(post["date"])}</pubDate>
      <description>{esc(post["description"])}</description>
      <author>harryodhiambo17@gmail.com (Harrison Odhiambo Ouka)</author>
    </item>"""
        )
        atom_entries.append(
            f"""  <entry>
    <title>{esc(post["title"])}</title>
    <link href="{url}" rel="alternate" />
    <id>{url}</id>
    <published>{post["date"]}T00:00:00Z</published>
    <updated>{TODAY}T00:00:00Z</updated>
    <author><name>Harrison Odhiambo Ouka</name></author>
    <summary>{esc(post["description"])}</summary>
  </entry>"""
        )
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Harrison Odhiambo Ouka — Software Developer</title>
    <link>{BASE}/blog/</link>
    <description>Technical notes by Harrison Odhiambo Ouka (Harry Ouka / Ouka Harry), a software developer in Nairobi, Kenya.</description>
    <language>en</language>
    <lastBuildDate>{updated}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""
    atom = f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Harrison Odhiambo Ouka — Software Developer</title>
  <subtitle>Technical notes by Harrison Odhiambo Ouka (Harry Ouka / Ouka Harry), a software developer in Nairobi.</subtitle>
  <link href="{BASE}/atom.xml" rel="self" />
  <link href="{BASE}/blog/" rel="alternate" />
  <id>{BASE}/blog/</id>
  <updated>{TODAY}T00:00:00Z</updated>
  <author><name>Harrison Odhiambo Ouka</name><email>harryodhiambo17@gmail.com</email></author>
{chr(10).join(atom_entries)}
</feed>
"""
    (ROOT / "feed.xml").write_text(rss, encoding="utf-8")
    (ROOT / "atom.xml").write_text(atom, encoding="utf-8")


def write_sitemap(urls: list[str]) -> None:
    body = "\n".join(
        f"""  <url>
    <loc>{BASE}{path}</loc>
    <lastmod>{TODAY}</lastmod>
  </url>"""
        for path in urls
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
"""
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://oukaharry.github.io/sitemap.xml\n",
        encoding="utf-8",
    )


def write_manifest() -> None:
    manifest = {
        "name": "Harrison Odhiambo Ouka",
        "short_name": "Harry Ouka",
        "description": "Software developer in Nairobi, Kenya. Also known as Ouka Harry.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#f3efe6",
        "theme_color": "#0e5c4a",
        "lang": "en",
        "icons": [
            {"src": "/assets/favicon-32.png", "sizes": "32x32", "type": "image/png"},
            {"src": "/assets/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
        ],
    }
    (ROOT / "site.webmanifest").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    posts = load_posts()
    pages = {
        "index.html": chrome(
            "/",
            "Harrison Odhiambo Ouka (Harry Ouka) · Software Developer",
            "Harrison Odhiambo Ouka, also known as Harry Ouka and Ouka Harry, is a software developer in Nairobi, Kenya. He builds MQL4/MQL5 trading tools and Python/Django web applications.",
            "/",
            home_body(),
            person_json(),
        ),
        "about/index.html": chrome(
            "/about/",
            "About Harrison Odhiambo Ouka · Software Developer",
            "About Harrison Odhiambo Ouka (Harry Ouka / Ouka Harry), a software developer in Nairobi. BSc Computer Science; software developer at blueedgefinancial.com since 2020.",
            "/about/",
            about_body(),
            person_json(),
        ),
        "projects/index.html": chrome(
            "/projects/",
            "Projects by Ouka Harry · Software Developer",
            "Software projects by Harrison Odhiambo Ouka (Harry Ouka): TradeManagerEA for MetaTrader 4, the Django app HedgePass Pro, and ALX C and shell coursework.",
            "/projects/",
            projects_body(),
            person_json(),
        ),
        "blog/index.html": chrome(
            "/blog/",
            "Blog · Harry Ouka, Software Developer",
            "Technical notes by software developer Harrison Odhiambo Ouka (Ouka Harry) on MQL4 trade managers, Django account models, and C pointers.",
            "/blog/",
            blog_index_body(posts),
            person_json({
                "@type": "Blog",
                "@id": BASE + "/blog/#blog",
                "name": "Notes by Harrison Odhiambo Ouka",
                "description": "Technical notes by software developer Harrison Odhiambo Ouka.",
                "url": BASE + "/blog/",
                "author": {"@id": BASE + "/#person"},
                "blogPost": [{"@id": f"{BASE}/blog/{post['slug']}/#post"} for post in posts],
            }),
        ),
        "contact/index.html": chrome(
            "/contact/",
            "Contact Harry Ouka · Software Developer",
            "Contact software developer Harrison Odhiambo Ouka (Harry Ouka / Ouka Harry) in Nairobi at harryodhiambo17@gmail.com.",
            "/contact/",
            contact_body(),
            person_json(),
        ),
        "404.html": chrome(
            "",
            "Page not found · Harrison Odhiambo Ouka, Software Developer",
            "This page is not on the site of Harrison Odhiambo Ouka, a software developer in Nairobi also known as Harry Ouka and Ouka Harry.",
            "/404.html",
            """<div class="wrap">
      <header class="page-intro">
        <p class="kicker">404</p>
        <h1>This page is not on the site</h1>
        <p class="lede">The address does not match a page for Harrison Odhiambo Ouka. Try the projects or the notes.</p>
        <div class="cta">
          <a class="button" href="/">Home</a>
          <a class="button button-ghost" href="/projects/">Projects</a>
          <a class="button button-ghost" href="/blog/">Blog</a>
        </div>
      </header>
    </div>""",
            person_json(),
            robots="noindex",
        ),
    }
    for post in posts:
        url = f"/blog/{post['slug']}/"
        extra = (
            f'<meta property="article:published_time" content="{post["date"]}" />\n'
            f'  <meta property="article:modified_time" content="{TODAY}" />\n'
            '  <meta property="article:author" content="Harrison Odhiambo Ouka" />'
        )
        pages[f"blog/{post['slug']}/index.html"] = chrome(
            url,
            post["seo_title"],
            post["description"],
            url,
            post_body(post),
            person_json(posting_json(post)),
            og_type="article",
            extra_head=extra,
        )
    for relative, markup in pages.items():
        if "@@" in markup:
            raise SystemExit(f"unreplaced token in {relative}")
        write_page(relative, markup)
    write_feeds(posts)
    write_sitemap(["/", "/about/", "/projects/", "/blog/", "/contact/"] + [f"/blog/{post['slug']}/" for post in posts])
    write_manifest()
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    for post in posts:
        print(f"{post['words']:4} words  {post['slug']}")
    print(f"wrote {len(pages)} html pages")


if __name__ == "__main__":
    main()
