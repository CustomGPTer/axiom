# Builds the Axiom website into ../docs (or the folder given as the first argument).
# Run from anywhere: python3 site-src/gen.py. The stylesheet, fonts and pictures in docs/assets/ are kept as they are.
# For a new version change VERSION, SIZE and SHA256 below and add the version to releases().
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "docs")
BASE = "https://customgpter.github.io/axiom/"
REPO = "https://github.com/CustomGPTer/axiom"
APK = REPO + "/releases/latest/download/Axiom.apk"
VERSION = "1.0"
SIZE = "22.4 MB"
SHA256 = "bfba8d35b88a441f3f788168a263f7a57d46a6e899f52fad334d39c2715d7de8"
UPDATED = "19 November 2026"

ICON = ('<svg viewBox="0 0 108 108" aria-hidden="true"><rect width="108" height="108" rx="24" fill="#0f1115"/>'
        '<circle cx="54" cy="36" r="9" fill="#6c9bff"/><circle cx="35" cy="69" r="9" fill="#f3f5f8"/><circle cx="73" cy="69" r="9" fill="#f3f5f8"/></svg>')
GRID = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="6.5" height="6.5" rx="1.6"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.6"/>'
        '<rect x="4" y="13.5" width="6.5" height="6.5" rx="1.6"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.6"/></svg>')

DESC = ("Axiom is a scientific calculator for Android with a textbook display, exact answers, algebra, equation solving, "
        "graphs, statistics, matrices and a unit converter. Free, no adverts, no account. It cannot go online.")


def e(text):
    return html.escape(text, quote=True)


def page(name, title, description, body, extra_head="", main_class="doc"):
    canonical = BASE + ("" if name == "index.html" else name)
    head = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="author" content="Jonathan Jackson">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#f4f5f8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0f1115" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Axiom">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Two Axiom screens, the calculator and a graph, beside the Axiom name">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/literata-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/literata-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css?v=1">
{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
<div class="wrap">
<a class="brand" href="./" aria-label="Axiom home">{ICON}<span>Axiom</span></a>
<nav aria-label="Main"><ul><li><a href="./#features">Features</a></li><li><a href="releases.html">Releases</a></li><li><a class="more-apps" href="more-apps.html">{GRID}More apps</a></li><li><a href="privacy.html">Privacy</a></li><li><a href="terms.html">Terms</a></li><li><a href="licences.html">Licences</a></li></ul></nav>
</div>
</header>
"""
    main_open = f'<main id="main" class="{main_class}">' if main_class else '<main id="main">'
    foot = f"""</main>
<footer class="colophon">
<div class="wrap">
<div>
<p>&copy; 2026 Jonathan Jackson. Axiom is an independent app.</p>
<p>This site uses no cookies and no tracking. It is set in Literata and Atkinson Hyperlegible.</p>
</div>
<nav aria-label="Footer"><ul>
<li><a href="./">Home</a></li>
<li><a href="releases.html">Release notes</a></li>
<li><a href="more-apps.html">More apps</a></li>
<li><a href="privacy.html">Privacy policy</a></li>
<li><a href="terms.html">Terms of use</a></li>
<li><a href="licences.html">Licences</a></li>
<li><a href="{REPO}">Source code</a></li>
<li><a href="{REPO}/issues">Contact</a></li>
</ul></nav>
</div>
</footer>
</body>
</html>
"""
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(head + main_open + "\n" + body + foot)


def doc(title, lede, sections):
    """A plain document page: sections are (id, heading, html)."""
    contents = "".join(f'<li><a href="#{i}">{e(h)}</a></li>' for i, h, _ in sections)
    body = "".join(f'<h2 id="{i}">{e(h)}</h2>\n{c}\n' for i, h, c in sections)
    return (f'<div class="wrap">\n<div class="measure">\n<h1>{e(title)}</h1>\n<p class="lede">{lede}</p>\n'
            f'<nav class="contents" aria-label="On this page"><strong>On this page</strong><ul>{contents}</ul></nav>\n{body}</div>\n</div>\n')


# ---------------------------------------------------------------- home

SHOTS = [
    ("calculate", "Calculate", "Sums drawn as they are written on paper, with the exact form under the decimal."),
    ("algebra", "Algebra", "Type a sum with x in it and Axiom simplifies it."),
    ("more", "More", "Factorise, expand, differentiate, integrate and find the zeros from one button."),
    ("graph", "Graph", "Up to four curves. Find where they cross the axis, turn and meet."),
    ("equations", "Equations", "Quadratics, cubics and simultaneous equations, with the working."),
    ("statistics", "Statistics", "Type a list of values and every statistic is worked out at once."),
    ("matrix", "Matrix", "Determinant, inverse and products, with fractions kept exact."),
    ("units", "Unit converter", "Type a value once and see it in every unit."),
    ("triangle", "Triangle solver", "Any three measurements give the rest, including both answers when there are two."),
    ("theme", "Themes", "Eight themes and six accent colours."),
]

FEATURES = [
    ("Textbook display", "Fractions are stacked, roots stretch over what they cover and powers are raised. What you see is what you would write."),
    ("Exact answers", "Fractions, roots and π stay exact: sin 15° is (√6 − √2)/4 as well as 0.2588190451. One tap switches between the two."),
    ("An honest equals sign", "An exact answer is shown with =. A rounded one is shown with ≈. You always know which you are looking at."),
    ("Errors in plain English", "A mistake is underlined where it is, with a sentence that says what is wrong. No “Syntax ERROR”."),
    ("Algebra", "Simplify, expand, factorise, differentiate and integrate formulas in x, y and z."),
    ("Equations with working", "Quadratics, cubics, and two or three simultaneous equations, with the steps shown."),
    ("Graphs", "Plot up to four formulas. Drag, pinch, read a curve, and find crossings and turning points. A table of values is one tap away."),
    ("Statistics", "Mean, median, mode, quartiles, and both standard deviations of a list, with totals and averages exact."),
    ("Matrices", "Up to 4 × 4: determinant, inverse, transpose, sums and products."),
    ("Complex numbers", "Any sum with i in it is worked as a complex number, and its size and angle are shown."),
    ("Base-N", "Binary, octal, decimal and hexadecimal sums with AND, OR, XOR and NOT."),
    ("Your own functions", "Save any formula in x as f, g, h and so on, then use it like sin or log."),
    ("Memories and history", "Six memories that survive closing the app, and a searchable history with pins and no limit."),
    ("Unit converter", "Twelve kinds of unit. Every factor is the exact legal definition, so a mile is 1,609.344 metres exactly."),
    ("Shapes and triangles", "Areas and volumes of twelve shapes with answers such as 45π, and a solver for any triangle."),
    ("Constants and formulas", "Twenty-two physical constants at their 2022 recommended values, and seven sheets of formulas."),
    ("Home-screen widget", "A small calculator for everyday sums, with the same exact arithmetic."),
    ("Backup", "One file holds your history, memories, functions and settings. Keep it anywhere or move it to a new phone."),
    ("Phones and tablets", "Works upright and on its side. On a tablet the keys sit beside the working area."),
    ("Accessible", "Every key and answer is labelled for TalkBack, text follows your phone's size setting, and there is a stronger-contrast option."),
]

CHECKS = [
    ("4,000 known answers", "Every build must match 4,000 sums whose answers were worked out by a separate maths library, to 15 figures."),
    ("Every decimal twice", "A decimal is worked out a second time at double the precision and shown only when both agree to 30 figures."),
    ("Exact forms typed back", "An exact form such as (√6 − √2)/4 is typed back through the calculator and compared with the original before it is shown."),
    ("Algebra tested by numbers", "A simplified formula, derivative or integral is shown only if it agrees with what you typed at several test points."),
    ("Answers put back", "The solution of an equation is put back into the equation, and an inverse matrix is multiplied back by the original."),
    ("More known answers", "1,000 complex sums, 300 matrices, 400 sets of statistics and 1,500 base-N sums are checked the same way."),
]

FAQ = [
    ("Is Axiom really free?", "Yes. There is no paid version, no subscription, no trial and no adverts, and nothing in the app is locked."),
    ("Is Axiom on Google Play?", "No. It is downloaded from this site as an Android app file. Android asks you to allow the install the first time."),
    ("Does it need the internet?", "No. Axiom has no internet permission, so it cannot go online at all. Everything, including algebra and graphs, works on the phone."),
    ("Which phones does it run on?", "Phones and tablets with Android 12 or later."),
    ("How accurate is it?", "Whole numbers and fractions are worked exactly. Roots, π and trigonometry are kept exact and turned into a decimal only for display, to the number of figures you choose. Graph readings and the triangle solver give rounded answers."),
    ("Can it take a photo of a sum?", "No. Sums are typed. Reading sums from photos is unreliable, and a wrong reading gives a wrong answer that looks right."),
    ("How do I move to a new phone?", "In Settings, Backup, save a backup file. Install Axiom on the new phone and restore from that file."),
    ("Can I see the source code?", f'Yes. It is published in full at <a href="{REPO}">github.com/CustomGPTer/axiom</a>.'),
]


def home():
    shots = "".join(
        f'<li><figure><img src="assets/shots/{f}.webp" width="540" height="1170" alt="{e(t + ": " + c)}"{"" if i < 2 else " loading=\"lazy\""}>'
        f'<figcaption><strong>{e(t)}</strong>{e(c)}</figcaption></figure></li>' for i, (f, t, c) in enumerate(SHOTS))
    features = "".join(f"<div><dt>{e(t)}</dt><dd>{e(d)}</dd></div>\n" for t, d in FEATURES)
    checks = "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>\n" for t, d in CHECKS)
    faq = "".join(f"<div><h3>{e(q)}</h3><p>{a}</p></div>\n" for q, a in FAQ)
    body = f"""<div class="hero">
<div class="wrap hero-grid">
<div class="hero-copy">
<h1>The answer, and proof it is right.</h1>
<p class="lede">Axiom is a scientific calculator for Android. It draws sums the way you write them, keeps answers exact, and tells you plainly whether an answer is exact or rounded.</p>
<p class="lede">It also does algebra, solves equations with the working shown, draws graphs, and converts units. It is free, with no adverts and nothing to unlock, and it cannot go online.</p>
<p class="get"><a class="button" href="{APK}">Download for Android</a></p>
<p class="facts">Free, with nothing to unlock. Android 12 or later. No ads, no accounts. <a href="releases.html">Release notes</a></p>
<p class="facts">Chrome may say the file might be harmful. It shows this for app files that do not come from Google Play. Choose Download anyway.</p>
</div>
<figure class="hero-shot"><img src="assets/shots/calculate.webp" width="540" height="1170" alt="The Axiom calculator showing sin 15 as 0.2588190451, with the exact form, root 6 minus root 2 over 4, underneath"></figure>
</div>
</div>

<section id="how" aria-labelledby="how-h">
<div class="wrap">
<h2 id="how-h">How it works</h2>
<p class="intro">Most calculator apps give you a decimal and leave you to trust it. Axiom is built round three ideas.</p>
<ol class="steps">
<li><h3>Type it as you write it</h3><p>Fractions, roots and powers are drawn as they are on paper, and the answer appears as you type. One label on each key, with a second layer one press away.</p></li>
<li><h3>Exact first</h3><p>Whole numbers and fractions never touch rounded arithmetic, so 0.1 + 0.2 is 0.3. Roots and π stay exact until the last moment.</p></li>
<li><h3>Checked before it is shown</h3><p>Every decimal is worked out twice. Every exact form is typed back in and compared. Anything that fails a check is not shown.</p></li>
</ol>
</div>
</section>

<section id="screens" aria-labelledby="screens-h">
<div class="wrap">
<h2 id="screens-h">What it looks like</h2>
<p class="intro">Clean keys, a display that reads like a textbook, and a mode for each kind of work.</p>
<ul class="shots">{shots}</ul>
<figure class="wide-shot"><img src="assets/shots/landscape.webp" width="1040" height="480" alt="Axiom on its side: the sum on the left and the full keypad on the right" loading="lazy"><figcaption>On its side, the keys sit beside the sum. Tablets use the same layout.</figcaption></figure>
</div>
</section>

<section id="features" aria-labelledby="features-h">
<div class="wrap">
<h2 id="features-h">Everything is in, and all of it is free</h2>
<p class="intro">You can use Axiom as a plain calculator and never open another mode. The rest is there when you need it.</p>
<dl class="features">
{features}</dl>
</div>
</section>

<section id="checked" aria-labelledby="checked-h">
<div class="wrap">
<h2 id="checked-h">How the answers are kept right</h2>
<p class="intro">A calculator is only worth having if you can trust it. These checks run on every build and inside the app as you use it.</p>
<ul class="plain">
{checks}</ul>
</div>
</section>

<section id="permissions" aria-labelledby="permissions-h">
<div class="wrap">
<h2 id="permissions-h">What it asks of your phone</h2>
<p class="intro">Nothing. Axiom asks for no permissions at all: not the internet, not your files, not your camera.</p>
<div class="scroll">
<table>
<thead><tr><th scope="col">Access</th><th scope="col">What Axiom does with it</th><th scope="col">What it never does</th></tr></thead>
<tbody>
<tr><th scope="row">Internet</th><td>Axiom has no internet permission. Android itself stops it going online.</td><td>Send anything anywhere, show adverts or check for updates.</td></tr>
<tr><th scope="row">Files</th><td>Only the one backup file you choose to save or open, through Android's own file picker.</td><td>Look at any other file on your phone.</td></tr>
<tr><th scope="row">Clipboard</th><td>Copies an answer when you hold it.</td><td>Read what you have copied elsewhere.</td></tr>
</tbody>
</table>
</div>
<p class="after-table">The detail is in the <a href="privacy.html">privacy policy</a>.</p>
</div>
</section>

<section id="questions" aria-labelledby="questions-h">
<div class="wrap">
<h2 id="questions-h">Questions</h2>
<div class="faq">
{faq}</div>
</div>
</section>

<section id="get" aria-labelledby="get-h">
<div class="wrap"><div class="measure">
<h2 id="get-h">Getting Axiom</h2>
<p>Axiom is a personal project and is free, with no paid version. It is downloaded from this site as an Android app file and is not on Google Play. It runs on phones and tablets with Android 12 or later.</p>
<p class="get"><a class="button" href="{APK}">Download for Android</a></p>
<p>When you download, Chrome may warn that the file might be harmful. It shows this warning for app files that do not come from Google Play; choose Download anyway. If you want to be sure the file is the real one, compare it with the checksum in the <a href="releases.html#checking">release notes</a>.</p>
<p>Open the downloaded file to install it. The first time, Android asks you to allow your browser to install apps. Google Play Protect may also step in, because Axiom is an app it has not seen before: choose More details, then Install anyway. To update, install the latest version over the one you have: your history, memories and settings are kept. What changed in each version is in the <a href="releases.html">release notes</a>.</p>
<p class="note">Axiom is checked with care, but no calculator should be the only check on a result that safety or money depends on. See the <a href="terms.html">terms of use</a>.</p>
</div></div>
</section>
"""
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in FAQ]}
    app_ld = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Axiom", "url": BASE, "description": DESC,
              "applicationCategory": "UtilitiesApplication", "operatingSystem": "Android 12 or later", "softwareVersion": VERSION,
              "downloadUrl": APK, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "GBP"},
              "author": {"@type": "Person", "name": "Jonathan Jackson"}}
    site_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": "Axiom", "url": BASE, "inLanguage": "en-GB"}
    extra = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, separators=(",", ":"))}</script>\n' for x in (app_ld, site_ld, faq_ld))
    page("index.html", "Axiom: a free scientific calculator for Android, with exact answers", DESC, body, extra, main_class="")


# ---------------------------------------------------------------- releases

def releases():
    included = [
        "Calculator with a textbook display, a live answer as you type, exact fractions, roots and π, and plain-English errors that point at the mistake.",
        "Algebra with x, y and z: simplify, expand, factorise, differentiate, integrate and find zeros.",
        "Equation solvers for quadratics, cubics, and two or three simultaneous equations, with the working.",
        "Graphs of up to four formulas, with crossings, turning points and a table of values.",
        "Statistics, matrices up to 4 × 4, complex numbers, and base-N sums.",
        "Six memories, your own functions, and unlimited history with search and pins.",
        "Unit converter, areas and volumes, triangle solver, constants and formula sheets.",
        "Eight themes, six accent colours and a stronger-contrast option.",
        "A home-screen widget, backup to a single file, and layouts for phones on their side and tablets.",
    ]
    items = "".join(f"<li>{e(i)}</li>" for i in included)
    body = f"""<div class="wrap">
<div class="measure">
<h1>Release notes</h1>
<p class="lede">What was added, improved and fixed in each version of Axiom, newest first. The current version is {VERSION}.</p>
<div class="get">
<a class="button" href="{APK}">Download the latest version</a>
<p class="facts">Version {VERSION}. Android app file, {SIZE}. Android 12 or later. Free.</p>
<p class="facts">Chrome may say the file might be harmful. It shows this for app files that do not come from Google Play. Choose Download anyway. To be sure of the file, see <a href="#checking">Checking your download</a>.</p>
</div>
<nav class="contents" aria-label="Versions"><strong>Versions</strong><ul><li><a href="#v1-0">1.0&ensp;First release</a></li></ul></nav>

<article class="release" id="v1-0">
<p class="ver">Version 1.0</p>
<h2>First release</h2>
<h3>Included</h3>
<ul>{items}</ul>
<h3>Good to know</h3>
<ul>
<li>The first root or sine after opening the app can take a moment while the algebra engine loads.</li>
<li>Graph readings and triangle answers are rounded. Everything else says whether it is exact or rounded.</li>
</ul>
</article>

<h2 id="checking">Checking your download</h2>
<p>Every version is signed with the same key, so Android will only install an update that comes from the same developer. If you want to check the file yourself, its SHA-256 checksum should be:</p>
<p><code>{SHA256}</code></p>
<p>The signing certificate's SHA-256 fingerprint is <code>72a86c01732e8ee1811daa7d1bf2c5fcbe426d90fe9dab5e0d934365a0df6d30</code>.</p>
</div>
</div>
"""
    page("releases.html", "Axiom release notes", "What is in each version of the Axiom scientific calculator for Android, and how to check your download.", body)


# ---------------------------------------------------------------- privacy, terms, licences

def privacy():
    s = [
        ("short", "The short version", "<p>Axiom collects nothing. It has no internet permission, so it cannot send anything anywhere. Everything you type stays on your phone.</p>"),
        ("phone", "What stays on your phone", "<p>Your history, memories, saved functions, the sums and lists you were last working on, and your settings are kept in the app's own private storage on your phone. Other apps cannot read it.</p>"),
        ("reach", "What the app can reach", "<p>Axiom asks Android for no permissions. It cannot use the internet, your files, your camera, your microphone, your location or your contacts.</p><p>It copies an answer to the clipboard when you hold it. It does not read the clipboard.</p>"),
        ("online", "Services the app contacts", "<p>None. There are no adverts, no analytics, no crash reporting and no update checks.</p>"),
        ("backups", "Backups", "<p>A backup file is made only when you ask for one in Settings, and is saved where you choose through Android's own file picker. It holds your history, memories, functions and settings as plain text. Anyone who has the file can read it, so keep it somewhere you trust. Android's own device backup may also include the app's data if you have that turned on in your phone's settings.</p>"),
        ("deleting", "Deleting your data", "<p>History can be cleared from the History screen, and memories and functions from the letters sheet. Uninstalling Axiom removes everything it stored. Backup files you saved are yours to delete.</p>"),
        ("site", "This website", f"<p>This site is hosted by GitHub Pages. It sets no cookies and has no tracking or analytics of its own. GitHub, as the host, receives the technical details any web server receives, such as your IP address; see GitHub's privacy statement. The download button fetches the app file from GitHub.</p>"),
        ("children", "Children", "<p>Axiom is suitable for all ages and collects nothing from anyone.</p>"),
        ("rights", "Your rights", "<p>Because the developer holds no information about you, there is nothing to ask for, correct or delete. Everything is on your own phone and under your control.</p>"),
        ("changes", "Changes and contact", f'<p>If this policy changes, the date at the top changes with it. Questions can be raised at <a href="{REPO}/issues">{REPO.replace("https://", "")}/issues</a>.</p>'),
    ]
    lede = f"Last updated {UPDATED}. This policy covers the Axiom app for Android (package <code>uk.jj.axiom</code>) and this website. Axiom is made by Jonathan Jackson, an individual developer in the United Kingdom."
    page("privacy.html", "Axiom privacy policy", "Axiom collects nothing and cannot go online. What stays on your phone, and what this website does.", doc("Privacy policy", lede, s))


def terms():
    s = [
        ("who", "Who provides Axiom", "<p>Axiom is provided by Jonathan Jackson, an individual developer in the United Kingdom, free of charge.</p>"),
        ("licence", "Your licence", f'<p>You may install and use Axiom on any device you own or control, and pass the unchanged app file on to others, free of charge. Axiom\'s source code is published at <a href="{REPO}">{REPO.replace("https://", "")}</a>. The software Axiom is built on keeps its own licences, set out on the <a href="licences.html">licences page</a>.</p>'),
        ("what", "What Axiom is", "<p>Axiom is a calculator. It is checked with care: see the home page for how. It is still software, and software can be wrong.</p>"),
        ("checking", "Checking important results", "<p>Do not rely on Axiom alone for a result that safety, health, money, an exam mark or a legal duty depends on. Check such results by a second, independent method. In particular, structural, electrical, medical and financial calculations must be checked by a suitably qualified person.</p><p>Graph readings and triangle-solver answers are rounded. The constants are published recommended values and the formula sheets are a reminder, not a textbook.</p>"),
        ("exams", "Exams", "<p>Axiom does algebra and stores formulas, so it is not allowed in most exams. Check your exam board's rules.</p>"),
        ("data", "Your data and backups", "<p>Your history, memories and functions are stored only on your phone. If you uninstall the app or lose the phone without a backup file, they are gone. Keeping backups is up to you.</p>"),
        ("warranty", "No warranty", "<p>Axiom is provided as it is, without any promise that it is free of errors or fit for a particular purpose, to the fullest extent the law allows.</p>"),
        ("liability", "Liability", "<p>To the fullest extent the law allows, the developer is not liable for any loss arising from the use of Axiom or from relying on a result it gives. Nothing in these terms limits liability that cannot be limited by law, or takes away rights you have as a consumer.</p>"),
        ("law", "Law", "<p>These terms are governed by the law of England and Wales.</p>"),
        ("changes", "Changes and contact", f'<p>If these terms change, the date at the top changes with them. Questions can be raised at <a href="{REPO}/issues">{REPO.replace("https://", "")}/issues</a>.</p>'),
    ]
    lede = f"Last updated {UPDATED}. These terms apply to the Axiom app for Android. They set out how the app is offered and where responsibility lies when you use it. If you do not accept them, please do not use the app."
    page("terms.html", "Axiom terms of use", "The terms on which the Axiom scientific calculator for Android is offered.", doc("Terms of use", lede, s))


def licences():
    s = [
        ("itself", "Axiom itself", f'<p>Axiom is copyright &copy; 2026 Jonathan Jackson. It is free to install, use and pass on unchanged, as set out in the <a href="terms.html">terms of use</a>. Its source code is published in full at <a href="{REPO}">{REPO.replace("https://", "")}</a>.</p>'),
        ("symja", "The algebra engine", '<p>Roots, trigonometry, logarithms, exact forms and algebra use <a href="https://github.com/axkr/symja_android_library">Symja</a> (matheclipse-core, parser and external), copyright the Symja authors, under the GNU Lesser General Public License, version 3. Axiom uses the library unmodified. Because Axiom\'s own source is published, the library can be replaced with a version of your choosing and the app rebuilt. The licence text is at <a href="https://www.gnu.org/licenses/lgpl-3.0.html">gnu.org/licenses/lgpl-3.0.html</a>.</p>'),
        ("software", "Other software", "<ul><li>Apfloat, copyright Mikko Tommila. MIT licence.</li><li>Hipparchus, copyright the Hipparchus project. Apache License 2.0.</li><li>Guava, fastutil, Apache Commons (Lang, Text, IO, Codec, CSV), Log4j API, Jackson, LogicNG, Paguro, j2html and javap. Apache License 2.0.</li><li>JGraphT (EPL or LGPL), Kryo (BSD), Trove (LGPL), Choco Solver (BSD) and Janino (BSD).</li><li>Jetpack Compose and AndroidX, copyright The Android Open Source Project. Apache License 2.0.</li><li>Kotlin, copyright JetBrains s.r.o. and Kotlin contributors. Apache License 2.0.</li></ul>"),
        ("type", "Typefaces", '<p>The app is set in Inter, copyright 2020 The Inter Project Authors. This site is set in Literata, copyright The Literata Project Authors, and Atkinson Hyperlegible, copyright Braille Institute of America. All three are used under the SIL Open Font License, version 1.1; the licence files for the two site typefaces are in <a href="assets/fonts/">assets/fonts</a>.</p>'),
        ("data", "Constants", "<p>The physical constants are the 2022 CODATA recommended values published by the US National Institute of Standards and Technology.</p>"),
        ("marks", "Names and trademarks", "<p>Android and Google Play are trademarks of Google LLC. GitHub is a trademark of GitHub, Inc. Axiom is not connected with or endorsed by either.</p>"),
        ("texts", "Licence texts", '<p><a href="https://www.apache.org/licenses/LICENSE-2.0">Apache License 2.0</a> &middot; <a href="https://www.gnu.org/licenses/lgpl-3.0.html">LGPL 3.0</a> &middot; <a href="https://opensource.org/license/mit">MIT</a> &middot; <a href="https://openfontlicense.org">SIL Open Font License 1.1</a>. The same credits are inside the app under Settings, Open-source licences.</p>'),
    ]
    lede = f"Last updated {UPDATED}. Axiom is built on software made by other people. This page gives Axiom's own terms, credits the work it depends on and names the licence each part is used under."
    page("licences.html", "Axiom licences and credits", "The open-source software and typefaces Axiom is built on, and their licences.", doc("Licences and credits", lede, s))


def more_apps(source):
    """The list of sibling apps, taken from a sibling site's page and completed with that sibling itself."""
    s = open(source, encoding="utf-8").read()
    i = s.index('<ul class="mapps">')
    block = s[i:s.index("</ul>", i)]
    sibling = ('<li class="mapp" style="--b:#3b2f8f;--b2:#0b0a1f"><div class="mapp-cover" aria-hidden="true"><svg viewBox="0 0 108 108"><path fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" d="M30 56 48 74 80 36"/></svg></div>'
               '<div class="mapp-body"><svg class="mapp-icon" viewBox="0 0 108 108" aria-hidden="true"><rect width="108" height="108" rx="24" fill="#0a0b0f"/><path fill="none" stroke="#a99bff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" d="M30 56 48 74 80 36"/></svg>'
               '<h2>MyHabits</h2><p class="mapp-kind">A habit tracker with streaks that are fair</p><p class="mapp-say">MyHabits tracks tick, count, timed and quit habits, with fair streaks, 30-day journeys, reminders, statistics and widgets. It cannot go online.</p>'
               '<p class="mapp-go"><a class="button" href="https://github.com/CustomGPTer/myhabits/releases/latest/download/MyHabits.apk">Download MyHabits</a><a class="mapp-site" href="https://customgpter.github.io/myhabits/">MyHabits website</a></p>'
               '<p class="mapp-needs">Free, with no adverts. Android 8 or later.</p></div></li>\n')
    body = f"""<div class="wrap">
<div class="measure">
<h1>More apps</h1>
<p class="lede">Axiom has siblings. Each is an Android app made by the same developer, free, with no adverts and nothing to unlock. Each button downloads the latest app file straight from that app's own page on GitHub.</p>
</div>
{block}{sibling}</ul>
<div class="measure">
<h2>Installing one</h2>
<p>Chrome may warn that the file might be harmful. It shows this for app files that do not come from Google Play. Choose Download anyway. Open the downloaded file, allow your browser to install apps if Android asks, and if Google Play Protect steps in, choose More details, then Install anyway.</p>
<p>Each app has its own website with its release notes, privacy policy and terms, and its own place to report a problem.</p>
<p class="get"><a class="button" href="{APK}">Download Axiom for Android</a></p>
</div>
</div>
"""
    page("more-apps.html", "More apps by the maker of Axiom", "Other free Android apps by the same developer, each with no adverts and nothing to unlock.", body)


def extras():
    page("404.html", "Page not found: Axiom", "That page could not be found.",
         '<div class="wrap"><div class="measure">\n<h1>That page does not add up</h1>\n<p class="lede">The address may be mistyped, or the page may have moved.</p>\n<p><a href="/axiom/">Go to the Axiom home page</a></p>\n</div></div>\n')
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
    urls = "".join(f"<url><loc>{BASE}{p}</loc></url>\n" for p in ["", "releases.html", "more-apps.html", "privacy.html", "terms.html", "licences.html"])
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    with open(os.path.join(OUT, "assets", "favicon.svg"), "w") as f:
        f.write(ICON.replace(' aria-hidden="true"', ' xmlns="http://www.w3.org/2000/svg"'))


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    home(); releases(); privacy(); terms(); licences(); extras()
    more_apps(sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "siblings-more-apps.html"))
    print("built", OUT)
