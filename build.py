# Builds the vyftwee.co.za site. Fill in the values below, run
# `python build.py`. It writes the pages in site/; site/ is what is published.
# CI does not run this script: commit the generated files in site/.
REG_NUMBER = "2026/271349/07"
LEGAL_NAME = "Vyf Twee (Pty) Ltd"
EMAIL      = "info@vyftwee.co.za"    # general enquiries
EMAIL_52   = "admin@vyftwee.co.za"   # orders, complaints, warranty and privacy requests
ADDRESS    = "565 Coert Steynberg Street, Constantia Park, Pretoria, Gauteng, 0010, South Africa"
FOOTER_ADDRESS = "565 Coert Steynberg Street, Constantia Park, Pretoria, 0010"
WA_BUSINESS_NUMBER         = "27645260397"      # the business number (a person replies), no + or spaces
WA_BUSINESS_NUMBER_DISPLAY = "+27 64 526 0397"  # the same, as people read it
WA_52         = "27795255987"      # the 52 Car Parts WhatsApp number, no + or spaces
WA_52_DISPLAY = "+27 79 525 5987"  # the same, as people read it
SITE_52    = "https://www.52carparts.co.za/"    # the www address works now; the root redirect comes later
POLICY_EFFECTIVE_DATE = "12 November 2026"      # replaces {EFFECTIVE_DATE} in content/policies/*.md (version 1.0 policies)
POLICY_V11_EFFECTIVE_DATE = "14 November 2026"  # replaces {EFFECTIVE_DATE_V11} (Terms and Delivery v1.1); set to the merge date

import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SITE = ROOT / "site"

# Policy pages, in footer order: (file and URL name, footer label)
POLICIES = [
    ("terms", "Terms"),
    ("privacy", "Privacy"),
    ("refunds", "Refunds"),
    ("cancellations", "Cancellations"),
    ("delivery", "Delivery"),
]
POLICY_LINKS = "".join(f'<a href="/{name}">{label}</a>' for name, label in POLICIES)


def page(title, description, body):
    """The shared page template: head, header, body, footer."""
    return f"""<!DOCTYPE html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/styles.css">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="mark" href="/"><img src="/vyftwee-groep-logo.svg" alt="Vyf Twee Groep" width="314" height="163"></a>
    <nav aria-label="Sections"><a href="/#ventures">Ventures</a><a href="/#company">Company</a></nav>
  </div>
</header>

{body}

<footer class="foot">
  <div class="wrap">
    <nav class="policies" aria-label="Policies">{POLICY_LINKS}</nav>
    <p>© {LEGAL_NAME} · Registration number {REG_NUMBER} · {FOOTER_ADDRESS}</p>
    <p>This site uses no cookies, analytics or tracking.</p>
  </div>
</footer>
</body>
</html>
"""


# --- Minimal Markdown: only what content/policies/*.md uses -------------------
# Headings (# and ##), paragraphs, numbered lists, pipe tables, *italic*, **bold**.

def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table(rows):
    head, body = rows[0], rows[1:]
    if body and all(re.fullmatch(r":?-+:?", c) for c in body[0]):
        body = body[1:]  # the --- separator row
    out = ['<div class="table"><table>']
    if any(head):  # a header row with all empty cells is left out
        out.append("<thead><tr>" + "".join(f'<th scope="col">{inline(c)}</th>' for c in head) + "</tr></thead>")
    out.append("<tbody>")
    for row in body:
        first, rest = row[0], row[1:]
        out.append(f'<tr><th scope="row">{inline(first)}</th>' + "".join(f"<td>{inline(c)}</td>" for c in rest) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def markdown(text):
    lines = text.splitlines()
    out, para = [], []
    numbered = re.compile(r"\d+\.\s+")

    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()

    i = 0
    while i < len(lines):
        s = lines[i].strip()
        heading = re.match(r"(#{1,2})\s+(.+)", s)
        if not s:
            flush()
            i += 1
        elif heading:
            flush()
            level = len(heading[1])
            out.append(f"<h{level}>{inline(heading[2])}</h{level}>")
            i += 1
        elif s.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            out.append(table(rows))
        elif numbered.match(s):
            flush()
            items = []
            while i < len(lines) and numbered.match(lines[i].strip()):
                items.append(numbered.sub("", lines[i].strip(), count=1))
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(item)}</li>" for item in items) + "</ol>")
        else:
            para.append(s)
            i += 1
    flush()
    return "\n".join(out)


def write(path, text):
    path = SITE / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("built", path.relative_to(SITE).as_posix())


# --- Home page -----------------------------------------------------------------

HOME = f"""<main>
  <section class="hero">
    <div class="sky">
      <div class="wrap">
        <h1>We build and run digital ventures.</h1>
      </div>
      <svg class="sun" viewBox="0 0 320 240" width="320" height="240" aria-hidden="true" focusable="false">
        <g fill="#E8B44C">
          <path d="M0 160A160 160 0 0 1 320 160Z"/>
          <rect x="65" y="172" width="190" height="7" rx="3.5"/>
          <rect x="104.5" y="190" width="95" height="7" rx="3.5"/>
          <rect x="140.5" y="208" width="55" height="7" rx="3.5"/>
          <circle cx="160" cy="229.5" r="3.5"/>
        </g>
      </svg>
    </div>
    <div class="sea">
      <div class="wrap">
        <p class="lead">Vyf Twee is a South African business that turns everyday problems into simple digital services, then runs them. Each venture gets its own name and its own customers; Vyf Twee owns and operates them.</p>
        <p><a class="go" href="/52-car-parts">How 52 Car Parts works</a></p>
      </div>
    </div>
  </section>

  <section class="ventures" id="ventures">
    <div class="wrap">
      <h2>Our ventures</h2>
      <article class="venture">
        <div class="venture-name">
          <h3><a href="/52-car-parts">52 Car Parts</a></h3>
          <p class="status">Live in South Africa</p>
        </div>
        <div class="venture-text">
          <p>Car parts sourced and delivered on WhatsApp. A client sends a photo of their licence disc, suppliers quote, the client chooses, and the part is collected, delivered and paid for after inspection.</p>
          <p>52 Car Parts is a brand of Vyf Twee. The name is the same idea in numbers: <span lang="af">vyf twee</span> is Afrikaans for five two.</p>
          <p><a class="go" href="/52-car-parts">How 52 Car Parts works</a></p>
          <p><a class="go" href="{SITE_52}">Visit 52carparts.co.za</a></p>
        </div>
      </article>
      <p class="next">More ventures will follow. Each one will be listed here.</p>
    </div>
  </section>

  <section class="company" id="company">
    <div class="wrap">
      <h2>Company</h2>
      <dl>
        <dt>Legal name</dt><dd>{LEGAL_NAME}</dd>
        <dt>Registration number</dt><dd>{REG_NUMBER}</dd>
        <dt>Address</dt><dd>{ADDRESS}</dd>
        <dt>General enquiries</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
        <dt>Orders, complaints, warranty and privacy requests</dt><dd><a href="mailto:{EMAIL_52}">{EMAIL_52}</a></dd>
        <dt>WhatsApp</dt><dd><a href="https://wa.me/{WA_BUSINESS_NUMBER}">{WA_BUSINESS_NUMBER_DISPLAY}</a></dd>
        <dt>Brands</dt><dd><a href="/52-car-parts">52 Car Parts</a></dd>
      </dl>
    </div>
  </section>
</main>"""

write("index.html", page(
    "Vyf Twee | We build and run digital ventures",
    "Vyf Twee is a South African business that builds and runs digital ventures. Its first venture is 52 Car Parts.",
    HOME,
))


# --- 52 Car Parts page ------------------------------------------------------------
# Every statement here matches content/policies/*.md. No prices, times or supplier names.

POLICY_LIST = "".join(
    f'<li><a href="/{name}">{title}</a></li>'
    for name, title in [
        ("terms", "Terms and Conditions"),
        ("privacy", "Privacy Policy"),
        ("refunds", "Refund Policy"),
        ("cancellations", "Cancellation Policy"),
        ("delivery", "Delivery Policy"),
    ]
)

CAR_PARTS = f"""<main class="doc">
  <div class="wrap">
    <h1>52 Car Parts</h1>
    <p class="lead">Vehicle parts sourced for you and delivered to your door. You inspect the part first and pay only if you accept it.</p>

    <h2>What you buy</h2>
    <p>We source new, aftermarket, reconditioned and used vehicle parts from independent suppliers in Gauteng and deliver them to you by courier anywhere in South Africa.</p>
    <p>52 Car Parts is a brand of {LEGAL_NAME}. When you buy a part through 52 Car Parts, you buy it from {LEGAL_NAME}.</p>

    <h2>How it works</h2>
    <ol>
      <li>Send a photo of your vehicle's licence disc to our WhatsApp number and complete the request form.</li>
      <li>We ask our suppliers for quotes and send you a quote with the total price, including delivery.</li>
      <li>If you accept the quote, we agree a delivery date and time with you.</li>
      <li>A courier collects the part from the supplier and delivers it to you.</li>
      <li>You inspect the part. If you accept it, you pay through a secure PayFast payment link at handover. If you reject it, you pay nothing.</li>
    </ol>

    <h2>Quotes</h2>
    <p>A quote is valid for 48 hours and subject to availability. If the supplier no longer has the part, we will tell you and the quote lapses at no cost to you.</p>

    <h2>Contact</h2>
    <ul>
      <li>WhatsApp: <a href="https://wa.me/{WA_52}">{WA_52_DISPLAY}</a></li>
      <li>Email: <a href="mailto:{EMAIL_52}">{EMAIL_52}</a></li>
      <li>Website: <a href="{SITE_52}">www.52carparts.co.za</a></li>
    </ul>

    <h2>Policies</h2>
    <ul>{POLICY_LIST}</ul>
  </div>
</main>"""

write("52-car-parts/index.html", page(
    "52 Car Parts | Vyf Twee",
    f"52 Car Parts, a brand of {LEGAL_NAME}, sources new, aftermarket, reconditioned and used vehicle parts from suppliers in Gauteng and delivers them by courier anywhere in South Africa. Inspect first, pay only if you accept.",
    CAR_PARTS,
))


# --- Policy pages: content/policies/<name>.md -> site/<name>/index.html -------------

for name, _ in POLICIES:
    source = ROOT / "content" / "policies" / f"{name}.md"
    text = source.read_text(encoding="utf-8").replace("{EFFECTIVE_DATE_V11}", POLICY_V11_EFFECTIVE_DATE).replace("{EFFECTIVE_DATE}", POLICY_EFFECTIVE_DATE)
    left = re.findall(r"\{[A-Z_]+\}", text)
    if left:
        raise SystemExit(f"{source}: unreplaced placeholder(s) {left}")
    title = re.search(r"^#\s+(.+)$", text, re.M)[1].strip()
    blocks = [b.strip() for b in text.split("\n\n")]
    description = next(b for b in blocks if b and not b.startswith(("#", "|")))
    body = f'<main class="doc">\n  <div class="wrap">\n{markdown(text)}\n  </div>\n</main>'
    write(f"{name}/index.html", page(f"{title} | Vyf Twee", " ".join(description.split()), body))


# --- Brand assets -------------------------------------------------------------------

for src in [ROOT / "brand" / "vyftwee-groep-logo.svg", *sorted((ROOT / "brand" / "website-icons").iterdir())]:
    shutil.copyfile(src, SITE / src.name)
    print("copied", src.name)
