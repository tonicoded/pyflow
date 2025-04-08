from flask import Flask, render_template, Response, jsonify, request
from flask_mail import Mail, Message
import os
import random
from flask import send_from_directory
import time
from flask import request, redirect
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
import re
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')


# ✅ E-mailconfiguratie (Gebruik Gmail SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")


mail = Mail(app)

@app.route('/')
def index():
    return render_template("index.html", time=int(time.time()))

@app.route('/robots.txt')
def robots():
    return Response(
        "User-agent: *\n"
        "Allow: /\n"
        "Sitemap: https://www.pyflow.nl/sitemap.xml",
        mimetype="text/plain"
    )

@app.route('/favicon.ico')
def favicon_ico():
    return send_from_directory('static', 'favicon.ico')


@app.context_processor
def inject_canonical_url():
    return {'canonical_url': request.url}

@app.before_request
def force_https_and_www():
    # Alleen doorgaan als host niet www.pyflow.nl
    if request.host != 'www.pyflow.nl':
        # Maak nieuwe URL met www
        new_url = request.url.replace(request.host, 'www.pyflow.nl')
        # Vervang http met https indien nodig
        if request.scheme == 'http':
            new_url = new_url.replace('http://', 'https://')
        return redirect(new_url, code=301)



@app.route('/sitemap.xml')
def sitemap():
    sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">
        <url><loc>https://www.pyflow.nl/</loc><priority>1.0</priority></url>
        <url><loc>https://www.pyflow.nl/contact</loc><priority>0.8</priority></url>
        <url><loc>https://www.pyflow.nl/overons</loc><priority>0.7</priority></url>
        <url><loc>https://www.pyflow.nl/besparings-calculator</loc><priority>0.8</priority></url>
        <url><loc>https://www.pyflow.nl/automatiseren</loc><priority>0.9</priority></url>
        <url><loc>https://www.pyflow.nl/prijsindicatie</loc><priority>0.7</priority></url>
        <url><loc>https://www.pyflow.nl/live-automation</loc><priority>0.6</priority></url>
        <url><loc>https://www.pyflow.nl/dashboard-data</loc><priority>0.6</priority></url>
        <url><loc>https://www.pyflow.nl/blog/tijdbesparen-met-automatisering</loc><priority>0.6</priority></url>
        <url><loc>https://www.pyflow.nl/blog/automatiseren-voor-kappers</loc><priority>0.7</priority></url>
        <url><loc>https://www.pyflow.nl/blog/automatiseren-voor-rijscholen</loc><priority>0.7</priority></url>
    </urlset>
    """
    return Response(sitemap_xml, mimetype="application/xml")






@app.route('/favicon.png')
def favicon():
    return send_from_directory('static', 'favicon.png')
@app.route('/automatiseren')
def automatiseren():
    return render_template("automatiseren.html", time=int(time.time()))

@app.route('/overons')
def overons():
    return render_template("overons.html", time=int(time.time()))
@app.route('/scan')
def scan():
    return render_template("scan.html", time=int(time.time()))

@app.route('/blog')
def blog():
    blog_posts = [
        {
            "title": "Hoe deze Rijschoolhouder 6 Avonden Vrij won met Automatisering",
            "url": "/blog/automatiseren-voor-rijscholen",
            "date": datetime.strptime("2025-04-06", "%Y-%m-%d"),
            "img": "/static/rijschool.jpg",
            "desc": "Jan uit Utrecht had genoeg van losse appjes, Excel en vergeten facturen..."
        },
        {
            "title": "Automatisering voor Kappers: Minder Gedoe, Meer Tijd",
            "url": "/blog/automatiseren-voor-kappers",
            "date": datetime.strptime("2025-04-05", "%Y-%m-%d"),
            "img": "/static/kapper.jpg",
            "desc": "Als kapper heb je al genoeg aan je hoofd. Ontdek hoe salons tijd besparen..."
        },
        {
            "title": "Hoe Automatisering je Bedrijf Elke Maand Uren Tijd Bespaart",
            "url": "/blog/tijdbesparen-met-automatisering",
            "date": datetime.strptime("2025-04-01", "%Y-%m-%d"),
            "img": "/static/tijdbesparen.jpg",
            "desc": "Ontdek hoe slimme tools je helpen repetitieve taken te verminderen..."
        }
    ]
    return render_template("blog.html", blog_posts=blog_posts, time=int(time.time()))



@app.route('/blog/tijdbesparen-met-automatisering')
def blog_tijdbesparen():
    return render_template("blog_tijdbesparen.html", time=int(time.time()))

@app.route('/blog/automatiseren-voor-kappers')
def automatisering_kapper():
    return render_template("automatisering_kapper.html", time=int(time.time()))
@app.route('/blog/automatiseren-voor-rijscholen')
def automatisering_rijschool():
    return render_template("blog_rijschool.html", time=int(time.time()))


@app.route('/prijsindicatie')
def prijsindicatie():
    return render_template("prijsindicatie.html", time=int(time.time()))

@app.route('/besparings-calculator')
def besparings_calculator():
    return render_template("timetracker.html", time=int(time.time()))

@app.route('/contact')
def contact():
    return render_template("contact.html", time=int(time.time()))

@app.route('/send-message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    subject = request.form.get('subject', '')
    topic = request.form.get('topic', 'Geen onderwerp opgegeven')

    if not name or not email or not message:
        return jsonify({"message": "⚠️ Vul alle verplichte velden in."})

    try:
        msg = Message(
            subject=f"PyFlow Contact - {name}",
            recipients=["anthonyvvza@gmail.com"],
            body=f"""
📩 Nieuw bericht via het PyFlow contactformulier:

👤 Naam: {name}
📧 E-mail: {email}
📂 Onderwerp: {subject if subject else 'Geen onderwerp ingevuld'}
📋 Categorie: {topic}

📝 Bericht:
{message}
            """.strip()
        )

        mail.send(msg)
        return jsonify({"message": "✅ Bedankt! We nemen spoedig contact op."})

    except Exception as e:
        print(f"Fout bij verzenden e-mail: {e}")
        return jsonify({"message": "⚠️ Er ging iets mis. Probeer het later opnieuw."})




@app.route('/live-automation')
def live_automation():
    """Genereert real-time automatiseringstaken voor demonstratie."""
    actions = [
        "Genereert maandelijkse financiële rapporten...",
        "Synchroniseert klantgegevens tussen systemen...",
        "Voert automatische voorraadbeheer-updates uit...",
        "Traint machine learning modellen op real-time data...",
        "Voert geautomatiseerde software-tests uit...",
        "Back-ups en bestandsbeheer uitvoeren...",
        "Analyseert gebruikersgedrag voor AI-optimalisatie...",
        "Verstuurd automatische facturen naar klanten...",
        "Chatbot leert nieuwe klantvragen en verbetert antwoorden...",
        "Realtime server monitoring en foutdetectie...",
        "Automatische API-koppeling tussen verschillende platformen...",
        "Predictive maintenance analyse draait en detecteert afwijkingen..."
    ]
    return Response(random.choice(actions), mimetype="text/plain")

@app.route('/dashboard-data')
def dashboard_data():
    """Genereert live KPI-statistieken voor automatisering."""
    data = {
        "cost_saving": random.randint(5000, 20000),  # € Bespaard
        "time_saved": random.randint(100, 500),  # Tijd bespaard in uren
        "tasks_automated": random.randint(500, 2000),  # Aantal taken geautomatiseerd
        "server_load": random.randint(10, 85),  # Server load %
        "efficiency_improvement": random.randint(15, 70),  # Efficiëntie %
        "error_reduction": random.randint(10, 50)  # Foutenreductie %
    }
    
    return jsonify(data)

@app.route("/calculate_savings", methods=["POST"])
def calculate_savings():
    data = request.json
    task_time = float(data["task_time"])
    tasks_per_month = float(data["tasks_per_month"])
    hourly_rate = float(data["hourly_rate"])

    current_time = (task_time * tasks_per_month) / 60
    automated_time = current_time * 0.1
    time_saved = current_time - automated_time
    cost_saved = time_saved * hourly_rate
    roi = round(5000 / cost_saved, 2) if cost_saved > 0 else 0

    return jsonify({
        "current_time": round(current_time, 2),
        "automated_time": round(automated_time, 2),
        "time_saved": round(time_saved, 2),
        "cost_saved": round(cost_saved, 2),
        "roi_months": roi
    })



from flask import request, jsonify
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import time
import re

@app.route("/website-scan", methods=["POST"])
def website_scan():
    def add_positive(positives, text):
        if text and len(text.strip()) > 6 and not re.fullmatch(r"(?i)\s*bevat[ .]*", text.strip()):
            positives.append(text.strip())

    def add_issue(issues, text):
        if text and len(text.strip()) > 6 and not re.match(r"(?i)^geen[ .]*$", text.strip()):
            issues.append(text.strip())

    url = request.json.get("url")
    if not url:
        return jsonify({"issues": ["Geen URL opgegeven."], "score": 0, "positives": []})
    if not url.startswith("http"):
        url = "https://" + url

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        visited = set()
        to_visit = [url]
        html_dump = ""
        max_pages = 15
        start_time = time.time()

        # Crawl tot max_pages bereikt is
        while to_visit and len(visited) < max_pages:
            current = to_visit.pop(0)
            if current in visited or not current.startswith(url):
                continue
            try:
                response = requests.get(current, timeout=8, headers=headers)
                visited.add(current)
                soup = BeautifulSoup(response.text, "html.parser")
                html_dump += response.text.lower()

                for a in soup.find_all("a", href=True):
                    href = urljoin(current, a["href"])
                    if href.startswith(url) and href not in visited:
                        to_visit.append(href)
            except:
                continue

        soup = BeautifulSoup(html_dump, "html.parser")
        html = html_dump

        issues = []
        positives = []

        # CONTACT
        if soup.find("form"):
            add_positive(positives, "Formulier aanwezig – contactmogelijkheid gedetecteerd.")
        else:
            add_issue(issues, "Geen formulieren gevonden – mogelijk geen contactmogelijkheid.")

        if soup.find(string=lambda t: t and ("contact" in t.lower() or "afspraak" in t.lower())):
            add_positive(positives, "Contact/afspraak-link aanwezig.")
        else:
            add_issue(issues, "Geen duidelijke 'contact' of 'afspraak'-link.")

        if "mailto:" in html:
            add_positive(positives, "E-mailadres zichtbaar.")
        else:
            add_issue(issues, "Geen e-mailadres zichtbaar.")

        if "tel:" in html:
            add_positive(positives, "Telefoonnummer zichtbaar.")
        else:
            add_issue(issues, "Geen telefoonnummer zichtbaar.")

        # LIVE CHAT (uitgebreid)
        chat_keywords = ["tawk.to", "intercom", "crisp.chat", "livechat", "chat-widget", "chatlio", "tidio", "zendesk", "olark"]
        live_chat_detected = any(kw in html for kw in chat_keywords)
        if not live_chat_detected:
            for div in soup.find_all("div", class_=True):
                if any("chat" in cls for cls in div.get("class", [])):
                    live_chat_detected = True
                    break
        if live_chat_detected:
            add_positive(positives, "Live chat gedetecteerd.")
        else:
            add_issue(issues, "Geen live chat gevonden – overweeg directe klantenservice.")

        # AUTOMATISERING
        if "automatisering" in html:
            add_positive(positives, "Focus op automatisering gevonden.")
        else:
            add_issue(issues, "Geen focus op automatisering – kans om dit beter te vermelden.")

        if len(soup.find_all("script")) >= 2:
            add_positive(positives, "Dynamische scripts aanwezig.")
        else:
            add_issue(issues, "Weinig interactieve scripts – zijn er dynamische elementen aanwezig?")

        # JURIDISCH
        if re.search(r"cookie|privacy|avg|gdpr", html):
            add_positive(positives, "Cookie- of privacybeleid aanwezig.")
        else:
            add_issue(issues, "Geen cookie- of privacybeleid gevonden – juridisch risico.")

        # TRACKING
        if any(tag in html for tag in ["gtag", "google-analytics", "hotjar", "clarity"]):
            add_positive(positives, "Analytics/tracking gevonden.")
        else:
            add_issue(issues, "Geen analytics/tracking gevonden – weet je wat bezoekers doen?")

        # VIEWPORT
        if soup.find("meta", attrs={"name": "viewport"}):
            add_positive(positives, "Viewport-tag aanwezig – goed voor mobiel.")
        else:
            add_issue(issues, "Geen viewport-tag – kan slecht werken op mobiel.")

        # SEO
        title = soup.find("title")
        if title and title.text.strip():
            add_positive(positives, "Bevat <title> tag – essentieel voor SEO.")
        else:
            add_issue(issues, "Geen <title> tag gevonden – essentieel voor SEO.")

        description = soup.find("meta", attrs={"name": "description"})
        if description and description.get("content"):
            add_positive(positives, "Meta-description aanwezig.")
        else:
            add_issue(issues, "Geen meta-description – belangrijk voor Google.")

        if soup.find("img", alt=True):
            add_positive(positives, "Afbeeldingen met alt-tekst aanwezig.")
        else:
            add_issue(issues, "Afbeeldingen zonder alt-tekst – slechter voor SEO/toegankelijkheid.")

        h1_tags = soup.find_all("h1")
        if len(h1_tags) == 1:
            add_positive(positives, "Bevat één <h1> tag – goed voor SEO.")
        elif len(h1_tags) == 0:
            add_issue(issues, "Geen <h1> tag gevonden – essentieel voor SEO.")
        else:
            add_issue(issues, "Meerdere <h1> tags gevonden – kan verwarrend zijn voor zoekmachines.")

        # STRUCTURED DATA
        if "schema.org" in html:
            add_positive(positives, "Gestructureerde data (Schema.org) gevonden.")
        else:
            add_issue(issues, "Geen gestructureerde data (Schema.org) gevonden.")

        # EXTRA'S
        if soup.find("link", rel=lambda x: x and "icon" in x.lower()):
            add_positive(positives, "Favicon gedetecteerd – visuele herkenbaarheid aanwezig.")
        else:
            add_issue(issues, "Geen favicon gevonden – favicon verhoogt herkenning van je site.")

        if any(s in html for s in ["facebook.com", "linkedin.com", "x.com", "instagram.com", "twitter.com"]):
            add_positive(positives, "Social media links aanwezig.")
        else:
            add_issue(issues, "Geen social media links gevonden – kan je bereik beperken.")

        try:
            sitemap_url = url.rstrip("/") + "/sitemap.xml"
            sitemap_res = requests.get(sitemap_url, timeout=5)
            if sitemap_res.status_code == 200 and "<urlset" in sitemap_res.text.lower():
                add_positive(positives, "Sitemap.xml aanwezig – goed voor zoekmachines.")
            else:
                add_issue(issues, "Geen sitemap.xml gevonden – essentieel voor SEO.")
        except:
            add_issue(issues, "Sitemap.xml niet bereikbaar – controleer of deze goed staat ingesteld.")

        try:
            robots_url = url.rstrip("/") + "/robots.txt"
            robots_res = requests.get(robots_url, timeout=5)
            if "user-agent" in robots_res.text.lower():
                add_positive(positives, "robots.txt aanwezig – goed voor zoekmachinecontrole.")
            else:
                add_issue(issues, "robots.txt lijkt niet correct ingesteld.")
        except:
            add_issue(issues, "Geen robots.txt gevonden – zoekmachines weten niet wat ze moeten volgen.")

        # DARK MODE DETECTIE
        if "prefers-color-scheme" in html:
            add_positive(positives, "Ondersteuning voor dark mode – modern en toegankelijk.")
        else:
            add_issue(issues, "Geen dark mode ondersteuning gevonden.")

        # CMS HERKENNING
        if "wp-content" in html:
            add_positive(positives, "CMS gedetecteerd: WordPress.")
        elif "shopify" in html:
            add_positive(positives, "CMS gedetecteerd: Shopify.")
        elif "joomla" in html:
            add_positive(positives, "CMS gedetecteerd: Joomla.")
        elif "drupal" in html:
            add_positive(positives, "CMS gedetecteerd: Drupal.")
        else:
            add_issue(issues, "CMS niet herkend – mogelijk custom-built.")

        # LAADTIJD
        load_time = time.time() - start_time
        if load_time <= 3:
            add_positive(positives, f"Goede initiële laadtijd ({round(load_time, 2)} sec).")
        else:
            add_issue(issues, f"Initiële laadtijd is traag ({round(load_time, 2)} sec).")

        # FILTERS
        positives = [p for p in positives if p and len(p.strip()) > 6]
        issues = [i for i in issues if i and len(i.strip()) > 6]

        score = max(30, 100 - len(issues) * 5)

        return jsonify({
            "issues": issues,
            "positives": positives,
            "score": score,
            "pages_checked": len(visited)
        })

    except Exception as e:
        return jsonify({
            "issues": [f"❌ Fout tijdens analyse: {str(e)}"],
            "positives": [],
            "score": 0
        })


if __name__ == "__main__":
    app.run(debug=False)
