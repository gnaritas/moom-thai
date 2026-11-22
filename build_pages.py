#!/usr/bin/env python3
# Moom Thai — grab-and-go Thai street food, Madison WI (websites desk, t_1d414d27, 2026-11-22)
# Generates public/*.html + sitemap.xml + robots.txt. style.css is hand-rolled static; pixel.gif copied byte-exact.
# Facts ONLY from card t_1d414d27 verified-facts + this run's sourced refresh (madison.com article_eca32b05,
# captimes 498dba68, ibmadison, cash.app/$moomthaigrabandgo order page, monsoonsiamwi.com, nominatim geo).
import json, os

ORIGIN = "https://moom-thai-demo.up.railway.app"
SITE = "Moom Thai"
TEL = "+16082341276"
TEL_DISPLAY = "(608) 234-1276"
ADDR1 = "1017 S Park St"
ADDR_FULL = "1017 S Park St, Madison, WI 53715"
LAT, LNG = 43.0560055, -89.3976982
MAP_Q = "1017+S+Park+St,+Madison,+WI+53715&output=embed"
BUILT = "2026-11-22"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")

NAH = "Thai street food, grab-and-go, on the South Park &amp; Lakeside corner"

NAV = [("/menu", "Menu"), ("/thai-omelet-madison", "Thai omelet"),
       ("/pad-thai-madison", "Pad Thai"), ("/visit", "Visit"), ("/contact", "Send a note")]

def nav(active):
    items = []
    for href, label in NAV:
        cls = ' class="on"' if href == active else ""
        items.append(f'<a href="{href}"{cls}>{label}</a>')
    return ('<nav id="nav"><a class="brand" href="/">Moom Thai<span class="brandmark" aria-hidden="true"></span></a>'
            '<input type="checkbox" id="navopen" class="navcheck" aria-label="Open menu">'
            '<label class="navtoggle" for="navopen">Menu</label>'
            f'<div class="navlinks" id="navlinks"><a href="tel:{TEL}" class="navtel">Call {TEL_DISPLAY}</a>{"".join(items)}</div></nav>')

FOOTER = f"""<footer>
<div class="footline">
  <div class="fcol"><p class="fbrand">Moom Thai</p><p class="ftag">{NAH}</p></div>
  <div class="fcol"><p class="fk">Find us</p><p>{ADDR1}<br>Madison, WI 53715</p><p class="fsub">Corner of South Park &amp; Lakeside</p></div>
  <div class="fcol"><p class="fk">Hours</p><p>Tue&ndash;Sun 12&ndash;7<br><span class="fsub">Closed Monday</span></p></div>
  <div class="fcol"><p class="fk">Call</p><p><a href="tel:{TEL}">{TEL_DISPLAY}</a></p><p class="fsub">Order at the counter, grab and go</p></div>
</div>
<p class="fnote">Moom means &ldquo;corner&rdquo; in Thai &mdash; this is ours. &copy; Moom Thai &middot; Madison, Wisconsin</p>
</footer>"""

def head(title, desc, path, ld):
    canon = ORIGIN + ("/" if path == "/" else path)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<!-- BUILT-{BUILT} -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Moom Thai">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{ORIGIN}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{ORIGIN}/og.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
</head><script type="application/ld+json">
{json.dumps(ld, indent=1)}
</script>
<body>
<a class="skip" href="#main">Skip to content</a>
{nav(path if path != "/" else None)}
"""

def page(fname, title, desc, path, ld, main, active=None):
    h = head(title, desc, path, ld)
    h = h.replace('<nav id="nav">', '<nav id="nav">', 1)
    body = h + f'<main id="main">\n{main}\n</main>\n{FOOTER}\n</body>\n</html>\n'
    # re-render nav with the active page marked
    body = body.replace(nav(None), nav(active))
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(body)
    return len(body.encode())

def ld_graph(parts):
    return {"@graph": parts}

def breadcrumb(path, name):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": ORIGIN + "/"}]
    if path != "/":
        items.append({"@type": "ListItem", "position": 2, "name": name, "item": ORIGIN + path})
    return {"@type": "BreadcrumbList", "itemListElement": items}

RESTAURANT = {
    "@type": "Restaurant", "@id": ORIGIN + "/#restaurant", "name": "Moom Thai",
    "image": ORIGIN + "/og.png",
    "url": ORIGIN + "/",
    "telephone": "+1-608-234-1276",
    "servesCuisine": ["Thai"],
    "address": {"@type": "PostalAddress", "streetAddress": "1017 S Park St",
                "addressLocality": "Madison", "addressRegion": "WI",
                "postalCode": "53715", "addressCountry": "US"},
    "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LNG},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": "12:00", "closes": "19:00"}
        for d in ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    ],
    "hasMenu": {"@type": "Menu", "name": "Moom Thai counter menu", "url": ORIGIN + "/menu"},
    "sameAs": ["https://cash.app/$moomthaigrabandgo"],
}
WEBSITE = {"@type": "WebSite", "@id": ORIGIN + "/#website", "name": "Moom Thai",
           "url": ORIGIN + "/", "inLanguage": "en"}

FAQ = lambda qs: {"@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}

def faq_main(qs):
    out = ['<div class="faq">']
    for q, a in qs:
        out.append(f"<details><summary>{q}</summary><p>{a}</p></details>")
    out.append("</div>")
    return "".join(out)

MAP_HTML = (f'<div class="mapwrap"><iframe src="https://www.google.com/maps?q={MAP_Q}" '
            'title="Map of Moom Thai at 1017 S Park St, Madison, WI 53715" loading="lazy" '
            'referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>')

os.makedirs(OUT, exist_ok=True)
sizes = {}

# ---------- HOME ----------
home_main = f"""
<section class="hero">
  <div class="wrap">
    <p class="kick">South Park &amp; Lakeside &middot; Madison&rsquo;s South Side</p>
    <h1>Moom means<br><span class="hl">&ldquo;corner.&rdquo;</span></h1>
    <p class="lede">A small grab-and-go Thai kitchen on the corner. Order at the counter, everything
    cooked fresh to order &mdash; noodles, curries, street plates &mdash; and out the door in minutes.
    Still in soft opening, and cooking every plate herself.</p>
    <p class="ctarow"><a class="btn" href="/menu">See the menu</a>
    <a class="btn ghost" href="tel:{TEL}">Call {TEL_DISPLAY}</a></p>
    <p class="herohours">Open Tue&ndash;Sun, noon to 7 &middot; closed Mondays &middot; {ADDR1}</p>
  </div>
  <span class="corner tl" aria-hidden="true"></span>
  <span class="corner br" aria-hidden="true"></span>
</section>

<section class="how">
  <div class="wrap">
    <p class="kick">How it works</p>
    <h2>Quick by design, made from scratch anyway</h2>
    <div class="cards3">
      <div class="card"><h3>Order at the counter</h3><p>Tap your order on the counter iPad. Everything is
      made to order, even though the shop is built for speed.</p></div>
      <div class="card"><h3>Grab and go &mdash; or sit a while</h3><p>Two long tables seat eight each.
      Most boxes head out the door; friends linger.</p></div>
      <div class="card"><h3>A short menu, done well</h3><p>It runs about half the size of sister restaurant
      Monsoon Siam&rsquo;s &mdash; with street plates you can&rsquo;t get there.</p></div>
    </div>
  </div>
</section>

<section class="plates">
  <div class="wrap">
    <p class="kick">Straight from the pass</p>
    <h2>Plates people cross town for</h2>
    <ul class="plated">
      <li><h3>Lad na mee khob</h3><p>Crispy egg noodles topped with Chinese broccoli and a sweet, thick
      soy&ndash;oyster sauce.</p></li>
      <li><h3>Puffy fried Thai omelet</h3><p>Fried puffy over rice, with a protein to add &mdash; shrimp is
      the house pick. <a href="/thai-omelet-madison">The full story &rarr;</a></p></li>
      <li><h3>Moo ma now</h3><p>Sliced marinated pork with steamed Chinese broccoli and a green
      chili&ndash;garlic dipping sauce.</p></li>
      <li><h3>Pad Thai</h3><p>The Atwood Avenue favorite that moved to the South Side.
      <a href="/pad-thai-madison">Why this one &rarr;</a></p></li>
    </ul>
  </div>
</section>

<section class="story">
  <div class="wrap narrow">
    <p class="kick">The corner story</p>
    <h2>&ldquo;I bring a taste of Thai street food&rdquo;</h2>
    <blockquote>&ldquo;I bring a taste of Thai street food, and I&rsquo;m cooking on my own, too, so
    everything is made from scratch and quick grab-and-go.&rdquo;</blockquote>
    <p class="qwho">&mdash; Dutdao &ldquo;Pooh&rdquo; Wonglaka, owner and cook, to the Wisconsin State
    Journal</p>
    <p>Pooh opened Monsoon Siam on Atwood Avenue in 2014. Moom Thai &mdash; her restaurant alone, on its
    own corner, in the old Asian Sweet Bakery space &mdash; is the South Side version: the street plates,
    a shorter menu, and the same hands on the wok. <a href="/about">Read more about the corner &rarr;</a></p>
  </div>
</section>

<section class="visit-cta">
  <div class="wrap">
    <h2>Finding us</h2>
    <p>{ADDR_FULL}, right where South Park meets Lakeside &mdash; next to Siam Boutique, in the old Asian
    Sweet Bakery space.</p>
    <p class="ctarow"><a class="btn" href="/visit">Hours &amp; map</a>
    <a class="btn ghost" href="/contact">Send a note</a></p>
  </div>
</section>
"""
page("index.html", "Moom Thai &mdash; Thai Street Food &amp; Grab-and-Go, Madison WI",
     "Moom Thai is a grab-and-go Thai street food kitchen at 1017 S Park St on Madison&rsquo;s South Side: made-to-order plates, short menu, open Tue&ndash;Sun noon&ndash;7.",
     "/", ld_graph([RESTAURANT, WEBSITE, breadcrumb("/", "")]), home_main, active=None)

# ---------- MENU ----------
menu_main = f"""
<section class="pagehead">
  <div class="wrap">
    <p class="kick">The counter menu</p>
    <h1>A short menu, cooked to order</h1>
    <p class="lede">Moom Thai&rsquo;s menu runs about half the size of sister restaurant Monsoon
    Siam&rsquo;s &mdash; and it carries street plates you can&rsquo;t get on Atwood Avenue. Prices live at
    the counter.</p>
  </div>
</section>

<section class="cats">
  <div class="wrap">
    <p class="kick">Sections on the order screen</p>
    <ul class="cats">
      <li>Starters</li><li>Salads</li><li>Thai Foods</li>
      <li>Coconut Curries</li><li>Noodle &amp; Soups</li><li>Beverages</li>
    </ul>
  </div>
</section>

<section class="featured">
  <div class="wrap">
    <p class="kick">What the press ordered</p>
    <h2>Street-food favorites, from the Wisconsin State Journal&rsquo;s first visit</h2>
    <div class="featgrid">
      <div class="feat"><h3>Lad na mee khob</h3><p>Crispy egg noodles, Chinese broccoli, and a sweet,
      thick soy&ndash;oyster sauce poured over the top. One of the dishes found only at Moom Thai.</p></div>
      <div class="feat"><h3>Puffy fried Thai omelet over rice</h3><p>A street classic fried puffy,
      served over rice. Add a protein &mdash; shrimp is the way many regulars take it.
      <a href="/thai-omelet-madison">More about the omelet &rarr;</a></p></div>
      <div class="feat"><h3>Moo ma now</h3><p>Sliced marinated pork with steamed Chinese broccoli and a
      green chili&ndash;garlic dipping sauce on the side.</p></div>
      <div class="feat"><h3>Pad Thai</h3><p>One of Monsoon Siam&rsquo;s most popular plates &mdash; the
      only one of them to move to the South Side. <a href="/pad-thai-madison">More about the pad Thai &rarr;</a></p></div>
    </div>
    <p class="fineprint">Massaman curry and kao soi stay on the Monsoon Siam menu for now. Dishes and
    availability can shift during soft opening &mdash; ask at the counter for what&rsquo;s cooking today.</p>
  </div>
</section>

<section class="strip">
  <div class="wrap">
    <h2>Order it now</h2>
    <p>Call ahead or come by the corner &mdash; everything is made to order.</p>
    <p class="ctarow"><a class="btn" href="tel:{TEL}">Call {TEL_DISPLAY}</a>
    <a class="btn ghost" href="/visit">Hours &amp; map</a></p>
  </div>
</section>
"""
MENU_LD = {
    "@type": "Menu", "@id": ORIGIN + "/menu#menu", "name": "Moom Thai counter menu",
    "url": ORIGIN + "/menu", "hasMenuSection": [
        {"@type": "MenuSection", "name": n} for n in
        ["Starters", "Salads", "Thai Foods", "Coconut Curries", "Noodle / Soups", "Beverages"]],
    "hasMenuItem": [
        {"@type": "MenuItem", "name": "Lad na mee khob", "description": "Crispy egg noodles topped with Chinese broccoli and a sweet, thick soy-oyster sauce"},
        {"@type": "MenuItem", "name": "Puffy fried Thai omelet over rice", "description": "Fried puffy Thai omelet over rice; add a protein such as shrimp"},
        {"@type": "MenuItem", "name": "Moo ma now", "description": "Sliced marinated pork with steamed Chinese broccoli and a green chili-garlic dipping sauce"},
        {"@type": "MenuItem", "name": "Pad Thai", "description": "Wok-fried noodles; one of the most popular plates from sister restaurant Monsoon Siam"},
    ],
}
page("menu.html", "Menu &mdash; Moom Thai, Madison WI",
     "Moom Thai&rsquo;s short grab-and-go menu: lad na mee khob, puffy fried Thai omelet over rice, moo ma now, pad Thai. Starters, salads, curries, noodles and soups. Prices at the counter.",
     "/menu", ld_graph([MENU_LD, {"@id": ORIGIN + "/menu", "@type": "WebPage", "name": "Menu — Moom Thai, Madison WI", "url": ORIGIN + "/menu", "isPartOf": {"@id": ORIGIN + "/#website"}}, breadcrumb("/menu", "Menu")]),
     menu_main, active="/menu")

# ---------- THAI OMELET detail ----------
omelet_main = f"""
<section class="pagehead">
  <div class="wrap">
    <p class="kick">The signature plate</p>
    <h1>Puffy fried Thai omelet,<br>over rice</h1>
    <p class="lede">Eggs fried puffy and golden, served over rice, with a protein to add &mdash; shrimp is
    the counter&rsquo;s go-to. It was on the first table the Wisconsin State Journal visited, and it is
    exactly what Thai street food looks like.</p>
    <p class="ctarow"><a class="btn" href="tel:{TEL}">Call {TEL_DISPLAY}</a>
    <a class="btn ghost" href="/visit">Hours &amp; map</a></p>
  </div>
</section>

<section class="detail">
  <div class="wrap">
    <h2>Made to order, every time</h2>
    <p>Nothing sits in a warmer at Moom Thai. Tell the counter iPad what you want &mdash; omelet plain or
    with shrimp &mdash; and it hits the hot wok the moment your order lands. Grab a box or take one of the
    two long tables.</p>
    <p>The omelet is one of the street plates that makes Moom Thai different from sister restaurant Monsoon
    Siam: a shorter menu, built around the quick, egg-and-wok side of Thai street cooking.</p>
    {faq_main([
        ("Where can I get a fried Thai omelet in Madison?",
         f"At Moom Thai, {ADDR_FULL} — the corner of South Park and Lakeside. Open Tuesday–Sunday, noon to 7; closed Monday."),
        ("Can I get the omelet to go?",
         "Yes — the whole shop is built for grab-and-go. Two long tables seat eight each if you would rather sit a while."),
        ("Can I add protein?",
         "Yes. Add a protein such as shrimp to the omelet at the counter."),
        ("Is Moom Thai the same restaurant as Monsoon Siam?",
         "Different restaurant, same owner. Pooh Wonglaka opened Monsoon Siam on Atwood Avenue in 2014; Moom Thai is hers alone and carries street plates the Atwood menu does not."),
    ])}
  </div>
</section>

<section class="strip">
  <div class="wrap">
    <h2>Come by the corner</h2>
    <p>{ADDR_FULL} &middot; Tue&ndash;Sun noon&ndash;7, closed Mondays.</p>
    <p class="ctarow"><a class="btn" href="/menu">Full menu</a>
    <a class="btn ghost" href="/contact">Send a note</a></p>
  </div>
</section>
"""
page("thai-omelet-madison.html", "Puffy Fried Thai Omelet with Rice &mdash; Moom Thai, Madison WI",
     "A puffy fried Thai omelet served over rice, with shrimp or another protein to add — made to order at Moom Thai, 1017 S Park St, Madison. Tue–Sun noon–7.",
     "/thai-omelet-madison",
     ld_graph([
        {"@type": "FoodService", "name": "Puffy fried Thai omelet over rice", "serviceType": "Thai street food",
         "provider": {"@id": ORIGIN + "/#restaurant"},
         "areaServed": {"@type": "City", "name": "Madison"},
         "url": ORIGIN + "/thai-omelet-madison"},
        {"@id": ORIGIN + "/thai-omelet-madison", "@type": "WebPage",
         "name": "Puffy Fried Thai Omelet with Rice — Moom Thai, Madison WI",
         "url": ORIGIN + "/thai-omelet-madison", "isPartOf": {"@id": ORIGIN + "/#website"}},
        FAQ([("Where can I get a fried Thai omelet in Madison?",
              "At Moom Thai, 1017 S Park St, Madison, WI 53715 — the corner of South Park and Lakeside. Open Tuesday–Sunday, noon to 7."),
             ("Can I get the omelet to go?",
              "Yes — the whole shop is built for grab-and-go."),
             ("Is Moom Thai the same restaurant as Monsoon Siam?",
              "Different restaurant, same owner — Pooh Wonglaka. Moom Thai carries street plates the Atwood Avenue menu does not.")]),
        breadcrumb("/thai-omelet-madison", "Thai omelet")]),
     omelet_main, active="/thai-omelet-madison")

# ---------- PAD THAI detail ----------
pad_main = f"""
<section class="pagehead">
  <div class="wrap">
    <p class="kick">The one that traveled</p>
    <h1>Pad Thai on<br>South Park Street</h1>
    <p class="lede">Pad Thai, massaman curry and khao soi are the plates Monsoon Siam&rsquo;s regulars
    order most. Pooh moved one of them to the South Side &mdash; the pad Thai &mdash; and left the rest on
    Atwood Avenue.</p>
    <p class="ctarow"><a class="btn" href="tel:{TEL}">Call {TEL_DISPLAY}</a>
    <a class="btn ghost" href="/visit">Hours &amp; map</a></p>
  </div>
</section>

<section class="detail">
  <div class="wrap">
    <h2>Same favorite, shorter walk</h2>
    <p>If you already know the Atwood kitchen, this is the plate you know, cooked to order on the corner of
    South Park and Lakeside. If you are new to it: wok-fried noodles, sweet-tangy sauce, the works &mdash;
    boxed for the road or eaten at one of the long tables.</p>
    <p>South Side regulars who used to drive across town for it no longer have to. In the State
    Journal&rsquo;s telling, the reaction has been warm: &ldquo;They&rsquo;re so excited that
    we&rsquo;re here, too.&rdquo;</p>
    {faq_main([
        ("Where can I get pad Thai on Madison&rsquo;s South Side?",
         f"At Moom Thai, {ADDR_FULL} — the corner of South Park and Lakeside. Open Tuesday–Sunday, noon to 7; closed Monday."),
        ("Do Monsoon Siam and Moom Thai share a menu?",
         "No. Moom Thai&rsquo;s menu is about half the size of Monsoon Siam&rsquo;s. Pad Thai is the one Atwood favorite served at both; massaman curry and kao soi stay at Monsoon Siam."),
        ("Is it grab-and-go or sit-down?",
         "Built for grab-and-go, with two long tables that seat eight each if you want to eat in."),
        ("Are there other dishes only at Moom Thai?",
         "Yes — street-food plates like lad na mee khob (crispy egg noodles with Chinese broccoli and a sweet soy-oyster sauce) and the puffy fried Thai omelet over rice."),
    ])}
  </div>
</section>

<section class="strip">
  <div class="wrap">
    <h2>Order ahead or swing by</h2>
    <p>{ADDR_FULL} &middot; Tue&ndash;Sun noon&ndash;7, closed Mondays.</p>
    <p class="ctarow"><a class="btn" href="/menu">Full menu</a>
    <a class="btn ghost" href="/contact">Send a note</a></p>
  </div>
</section>
"""
page("pad-thai-madison.html", "Pad Thai near South Park Street &mdash; Moom Thai, Madison WI",
     "Pad Thai made to order at Moom Thai — the Atwood Avenue favorite now on South Park Street. 1017 S Park St, Madison. Open Tue–Sun noon–7.",
     "/pad-thai-madison",
     ld_graph([
        {"@type": "FoodService", "name": "Pad Thai", "serviceType": "Thai street food",
         "provider": {"@id": ORIGIN + "/#restaurant"},
         "areaServed": {"@type": "City", "name": "Madison"},
         "url": ORIGIN + "/pad-thai-madison"},
        {"@id": ORIGIN + "/pad-thai-madison", "@type": "WebPage",
         "name": "Pad Thai near South Park Street — Moom Thai, Madison WI",
         "url": ORIGIN + "/pad-thai-madison", "isPartOf": {"@id": ORIGIN + "/#website"}},
        FAQ([("Where can I get pad Thai on Madison's South Side?",
              "At Moom Thai, 1017 S Park St, Madison, WI 53715 — the corner of South Park and Lakeside. Open Tuesday–Sunday, noon to 7."),
             ("Do Monsoon Siam and Moom Thai share a menu?",
              "No. Pad Thai is the one Atwood favorite served at both; massaman curry and khao soi stay at Monsoon Siam."),
             ("Is it grab-and-go or sit-down?",
              "Built for grab-and-go, with two long tables that seat eight each.")]),
        breadcrumb("/pad-thai-madison", "Pad Thai")]),
     pad_main, active="/pad-thai-madison")

# ---------- VISIT ----------
visit_main = f"""
<section class="pagehead">
  <div class="wrap">
    <p class="kick">Visit</p>
    <h1>The corner of South Park &amp; Lakeside</h1>
    <p class="lede">{ADDR_FULL}. Look for the corner windows &mdash; next to Siam Boutique, in the same
    building as Cronometro bike shop, in the old Asian Sweet Bakery space.</p>
  </div>
</section>

<section class="visgrid">
  <div class="wrap">
    <div class="vinfo">
      <h3>Hours</h3>
      <table class="hours">
        <tr><th scope="row">Monday</th><td>Closed</td></tr>
        <tr><th scope="row">Tuesday&ndash;Friday</th><td>12:00 pm &ndash; 7:00 pm</td></tr>
        <tr><th scope="row">Saturday&ndash;Sunday</th><td>12:00 pm &ndash; 7:00 pm</td></tr>
      </table>
      <h3>Order &amp; pay</h3>
      <ul class="ticks">
        <li>Order on the counter iPad &mdash; everything made to order.</li>
        <li>Pay by Cash App: <a href="https://cash.app/$moomthaigrabandgo">$moomthaigrabandgo</a></li>
        <li>Two long tables, eight seats each &mdash; or grab the box and go.</li>
        <li>Questions before coming? Call <a href="tel:{TEL}">{TEL_DISPLAY}</a> or <a href="/contact">send a note</a>.</li>
      </ul>
      <h3>Good to know</h3>
      <p>Soft opening: the shop is getting to know the neighborhood, so the menu list can shift a dish or
      two. The counter is the ground truth.</p>
    </div>
    <div class="vmap">
      {MAP_HTML}
      <p class="mapcap">Moom Thai &middot; {ADDR1} &middot; Madison, WI 53715</p>
    </div>
  </div>
</section>

<section class="strip">
  <div class="wrap">
    <h2>Hungry yet?</h2>
    <p>Start with the omelet or the pad Thai &mdash; the counter will take it from there.</p>
    <p class="ctarow"><a class="btn" href="/menu">See the menu</a>
    <a class="btn ghost" href="tel:{TEL}">Call {TEL_DISPLAY}</a></p>
  </div>
</section>
"""
page("visit.html", "Visit &mdash; Moom Thai, South Park &amp; Lakeside, Madison WI",
     "Moom Thai is at 1017 S Park St, Madison, WI 53715 — the South Park & Lakeside corner. Hours: Tue–Sun noon–7, closed Monday. Counter iPad ordering, Cash App, grab-and-go.",
     "/visit",
     ld_graph([
        {"@id": ORIGIN + "/visit", "@type": "WebPage", "name": "Visit — Moom Thai, Madison WI",
         "url": ORIGIN + "/visit", "isPartOf": {"@id": ORIGIN + "/#website"}},
        RESTAURANT, breadcrumb("/visit", "Visit")]),
     visit_main, active="/visit")

# ---------- ABOUT ----------
about_main = f"""
<section class="pagehead">
  <div class="wrap">
    <p class="kick">About</p>
    <h1>Her corner, her wok, her rules</h1>
    <p class="lede">Moom Thai is the South Side restaurant that Dutdao &ldquo;Pooh&rdquo; Wonglaka built
    for one reason: the corner opened, and she said yes.</p>
  </div>
</section>

<section class="detail">
  <div class="wrap narrow">
    <h2>&ldquo;Okay, I&rsquo;ll do one more here&rdquo;</h2>
    <p>The space at 1017 S Park St &mdash; 900 square feet on the corner of South Park and Lakeside
    &mdash; was Asian Sweet Bakery, Madison&rsquo;s first Chinese bakery, for twelve years. It closed in
    August. By late October, Pooh had rearranged the tables, put in kitchen equipment built for a Thai
    kitchen, and started cooking.</p>
    <blockquote>&ldquo;It&rsquo;s a good opportunity that this building is open, so I just said,
    &lsquo;Okay, I&rsquo;ll do one more here.&rsquo;&rdquo;</blockquote>
    <p class="qwho">&mdash; Pooh Wonglaka, to the Wisconsin State Journal</p>
    <h2>The name is the place</h2>
    <p>&ldquo;Moom&rdquo; is a Thai word meaning &ldquo;corner,&rdquo; and the restaurant sits on one:
    South Park and Lakeside. That is the whole naming story, told by Pooh herself.</p>
    <h2>Sister, not twin</h2>
    <p>Pooh also owns <a href="https://monsoonsiamwi.com">Monsoon Siam</a> on Atwood Avenue, which she
    opened in 2014. Moom Thai is hers alone &mdash; a different name, a shorter menu built for
    grab-and-go, and some street plates the Atwood menu does not carry. Her gift shop, Siam Boutique, is
    right next door.</p>
    <p>She cooks everything at Moom Thai herself, with two employees on the counter side. During soft
    opening she is keeping promotion quiet on purpose: &ldquo;I want them to come try,&rdquo; she told
    the State Journal.</p>
  </div>
</section>

<section class="strip">
  <div class="wrap">
    <h2>Come try it</h2>
    <p>{ADDR_FULL} &middot; Tue&ndash;Sun noon&ndash;7, closed Mondays.</p>
    <p class="ctarow"><a class="btn" href="/menu">See the menu</a>
    <a class="btn ghost" href="/visit">Hours &amp; map</a></p>
  </div>
</section>
"""
page("about.html", "About &mdash; Moom Thai, Madison WI",
     "How Moom Thai began: owner Pooh Wonglaka — of Monsoon Siam — opened her own grab-and-go Thai street food shop in the old Asian Sweet Bakery space at South Park & Lakeside. Moom means corner.",
     "/about",
     ld_graph([
        {"@id": ORIGIN + "/about", "@type": "WebPage", "name": "About — Moom Thai, Madison WI",
         "url": ORIGIN + "/about", "isPartOf": {"@id": ORIGIN + "/#website"}},
        RESTAURANT, breadcrumb("/about", "About")]),
     about_main, active="/about")

# ---------- CONTACT ----------
contact_main = f"""
<section class="pagehead">
  <div class="wrap">
    <p class="kick">Send a note</p>
    <h1>Talk to the counter</h1>
    <p class="lede">A question about a dish, hours, or feeding a crowd? Write it here and it lands with
    the shop &mdash; or just call <a href="tel:{TEL}">{TEL_DISPLAY}</a> during Tue&ndash;Sun,
    noon&ndash;7.</p>
  </div>
</section>

<section class="formsec">
  <div class="wrap">
    <form class="cform" method="post" action="/contact">
      <label>Your name<input name="name" type="text" required maxlength="120" autocomplete="name" placeholder="First name is fine"></label>
      <label>Phone (optional)<input name="phone" type="tel" maxlength="60" autocomplete="tel" placeholder="(608) 555-0123"></label>
      <label>Email (optional)<input name="email" type="email" maxlength="120" autocomplete="email" placeholder="you@example.com"></label>
      <label>Message<textarea name="message" rows="5" required maxlength="4000" placeholder="What would you like to ask?"></textarea></label>
      <p><button class="btn" type="submit">Send it</button></p>
    </form>
    <aside class="cinfo">
      <h3>Moom Thai</h3>
      <p>{ADDR1}<br>Madison, WI 53715</p>
      <p class="fk">Hours</p><p>Tue&ndash;Sun 12&ndash;7<br>closed Monday</p>
      <p class="fk">Phone</p><p><a href="tel:{TEL}">{TEL_DISPLAY}</a></p>
      {MAP_HTML}
    </aside>
  </div>
</section>
"""
page("contact.html", "Contact &mdash; Moom Thai, Madison WI",
     "Contact Moom Thai, grab-and-go Thai street food at 1017 S Park St, Madison WI 53715. Send a note or call (608) 234-1276. Tue–Sun noon–7, closed Monday.",
     "/contact",
     ld_graph([
        {"@id": ORIGIN + "/contact", "@type": "WebPage", "name": "Contact — Moom Thai, Madison WI",
         "url": ORIGIN + "/contact", "isPartOf": {"@id": ORIGIN + "/#website"},
         "mainEntity": {"@type": "PostalAddress", "streetAddress": "1017 S Park St",
                        "addressLocality": "Madison", "addressRegion": "WI",
                        "postalCode": "53715", "addressCountry": "US"}},
        breadcrumb("/contact", "Contact")]),
     contact_main, active="/contact")

# ---------- PRIVACY ----------
priv_main = f"""
<section class="pagehead">
  <div class="wrap">
    <p class="kick">Privacy</p>
    <h1>What this site does with your information</h1>
  </div>
</section>

<section class="detail">
  <div class="wrap narrow">
    <h3>The contact form</h3>
    <p>The form asks for a name and a message, and optionally a phone number and an email address. Those
    details go to Moom Thai so the counter can answer you &mdash; nothing else. Notes are kept only as
    long as it takes to reply and settle the question.</p>
    <h3>No trackers, no cookies</h3>
    <p>This site sets no cookies and loads no advertising or analytics scripts. A tiny invisible image on
    the shop&rsquo;s email messages counts views only as a whole &mdash; no personal profiles are
    built.</p>
    <h3>The map on the Visit and Contact pages</h3>
    <p>The location map is loaded from Google Maps, so Google sees the page request that paints it. The
    shop stores no map data about you.</p>
    <h3>Your call</h3>
    <p>Calling the shop number is ordinary phone traffic between you and Moom Thai.</p>
    <h3>Questions</h3>
    <p>Use the <a href="/contact">contact form</a> and this site&rsquo;s team will pass it to the
    shop.</p>
  </div>
</section>
"""
page("privacy.html", "Privacy &mdash; Moom Thai, Madison WI",
     "Privacy notice for moom-thai's site: the contact form goes straight to the shop, no cookies, no trackers, map embed served by Google.",
     "/privacy",
     ld_graph([
        {"@id": ORIGIN + "/privacy", "@type": "WebPage", "name": "Privacy — Moom Thai, Madison WI",
         "url": ORIGIN + "/privacy", "isPartOf": {"@id": ORIGIN + "/#website"}},
        breadcrumb("/privacy", "Privacy")]),
     priv_main, active=None)

# ---------- THANKS ----------
thanks_main = f"""
<section class="pagehead">
  <div class="wrap">
    <p class="kick">Note received</p>
    <h1>Your message is in.</h1>
    <p class="lede">The counter reads every note and answers in the order they arrive. For anything
    urgent while the shop is open, call <a href="tel:{TEL}">{TEL_DISPLAY}</a>.</p>
    <p class="ctarow"><a class="btn" href="/">Back to the front page</a>
    <a class="btn ghost" href="/menu">See the menu</a></p>
  </div>
</section>
"""
page("thanks.html", "Note received &mdash; Moom Thai",
     "Your note reached Moom Thai, grab-and-go Thai street food on South Park & Lakeside, Madison WI.",
     "/thanks",
     {"@type": "WebPage", "name": "Note received — Moom Thai", "url": ORIGIN + "/thanks"},
     thanks_main, active=None)

# ---------- 404 ----------
nf_main = f"""
<section class="pagehead">
  <div class="wrap">
    <p class="kick">404 &mdash; wrong corner</p>
    <h1>This page isn&rsquo;t here.</h1>
    <p class="lede">The food is, though: {ADDR_FULL}, Tue&ndash;Sun noon&ndash;7.</p>
    <p class="ctarow"><a class="btn" href="/">Front page</a>
    <a class="btn ghost" href="/menu">Menu</a></p>
  </div>
</section>
"""
page("404.html", "Page not found &mdash; Moom Thai",
     "Page not found — Moom Thai is grab-and-go Thai street food at 1017 S Park St, Madison WI.",
     "/404",
     {"@type": "WebPage", "name": "Page not found — Moom Thai", "url": ORIGIN + "/404"},
     nf_main, active=None)

# ---------- sitemap + robots ----------
core_paths = ["/", "/menu", "/thai-omelet-madison", "/pad-thai-madison", "/visit", "/about", "/contact", "/privacy"]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in core_paths:
    loc = ORIGIN + ("/" if p == "/" else p)
    sm.append(f"<url><loc>{loc}</loc><lastmod>{BUILT}</lastmod></url>")
sm.append("</urlset>")
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")
open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(
    "User-agent: *\nDisallow: /thanks\nDisallow: /404\n\nSitemap: " + ORIGIN + "/sitemap.xml\n")

for f in sorted(os.listdir(OUT)):
    sizes[f] = os.path.getsize(os.path.join(OUT, f))
print(json.dumps(sizes, indent=1))
print("pages written:", len([f for f in sizes if f.endswith('.html')]))
