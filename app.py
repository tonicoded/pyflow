from flask import Flask, render_template, Response, jsonify, request
from flask_mail import Mail, Message
import os
import random
from flask import send_from_directory
import time
from flask import request, redirect
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urlparse
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



@app.route("/website-scan", methods=["POST"])
def website_scan():
    import re
    import time
    from urllib.parse import urljoin
    from bs4 import BeautifulSoup
    import requests

    url = request.json.get("url")
    if not url:
        return jsonify({"issues": ["Geen URL opgegeven."], "score": 0, "positives": []})
    if not url.startswith("http"):
        url = "https://" + url

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        start_time = time.time()
        response = requests.get(url, timeout=10, headers=headers)
        load_time = time.time() - start_time
        soup = BeautifulSoup(response.text, "html.parser")
        html = response.text.lower()

        issues = []
        positives = []

        # CONTACT
        if soup.find("form"):
            positives.append("Formulier aanwezig – contactmogelijkheid gedetecteerd.")
        else:
            issues.append("Geen formulieren gevonden – mogelijk geen contactmogelijkheid.")

        if soup.find(string=lambda t: t and ("contact" in t.lower() or "afspraak" in t.lower())):
            positives.append("Contact/afspraak-link aanwezig.")
        else:
            issues.append("Geen duidelijke 'contact' of 'afspraak'-link.")

        if "mailto:" in html:
            positives.append("E-mailadres zichtbaar.")
        else:
            issues.append("Geen e-mailadres zichtbaar.")

        if "tel:" in html:
            positives.append("Telefoonnummer zichtbaar.")
        else:
            issues.append("Geen telefoonnummer zichtbaar.")

        # AUTOMATISERING
        if "automatisering" in html:
            positives.append("Focus op automatisering gevonden.")
        else:
            issues.append("Geen focus op automatisering – kans om dit beter te vermelden.")

        if len(soup.find_all("script")) >= 2:
            positives.append("Dynamische scripts aanwezig.")
        else:
            issues.append("Weinig interactieve scripts – zijn er dynamische elementen aanwezig?")

        # JURIDISCH
        if re.search(r"cookie|privacy|avg|gdpr", html):
            positives.append("Cookie- of privacybeleid aanwezig.")
        else:
            issues.append("Geen cookie- of privacybeleid gevonden – juridisch risico.")

        # CHATBOT
        if any(service in html for service in ["tawk.to", "intercom", "crisp.chat", "livechatinc"]):
            positives.append("Chatbot gedetecteerd.")
        else:
            issues.append("Geen chatbot gedetecteerd – overweeg live chat voor klantenservice.")

        # TRACKING
        if any(tag in html for tag in ["gtag", "google-analytics", "hotjar", "clarity"]):
            positives.append("Analytics/tracking gevonden.")
        else:
            issues.append("Geen analytics/tracking gevonden – weet je wat bezoekers doen?")

        # VIEWPORT
        if soup.find("meta", attrs={"name": "viewport"}):
            positives.append("Viewport-tag aanwezig – goed voor mobiel.")
        else:
            issues.append("Geen viewport-tag – kan slecht werken op mobiel.")

        # SEO
        title = soup.find("title")
        if title and title.text.strip():
            positives.append("Bevat <title> tag – essentieel voor SEO.")
        else:
            issues.append("Geen <title> tag gevonden.")

        description = soup.find("meta", attrs={"name": "description"})
        if description and description.get("content", "").strip():
            positives.append("Meta-description aanwezig.")
        else:
            issues.append("Geen meta-description – belangrijk voor Google.")

        if soup.find("img", alt=True):
            positives.append("Afbeeldingen met alt-tekst aanwezig.")
        else:
            issues.append("Afbeeldingen zonder alt-tekst – slechter voor SEO/toegankelijkheid.")

        h1_tags = soup.find_all("h1")
        h1_count = len(h1_tags)
        if h1_count == 1:
            positives.append("Bevat één <h1> tag – goed voor SEO.")
        elif h1_count == 0:
            issues.append("Geen <h1> tag gevonden – essentieel voor SEO.")
        else:
            issues.append("Meerdere <h1> tags gevonden – kan verwarrend zijn voor zoekmachines.")

        # STRUCTURED DATA
        if "schema.org" in html:
            positives.append("Gestructureerde data (Schema.org) gevonden.")
        else:
            issues.append("Geen gestructureerde data (Schema.org) gevonden.")

        # LAADTIJD
        if load_time <= 3:
            positives.append(f"Goede laadtijd ({round(load_time, 2)} sec).")
        else:
            issues.append(f"Laadtijd is traag ({round(load_time, 2)} sec) – optimalisatie aanbevolen.")

        # CACHE & CDN
        if "cache-control" in response.headers:
            positives.append("Cache-Control header aanwezig.")
        else:
            issues.append("Geen 'Cache-Control' header – kan prestaties beïnvloeden.")

        if "cloudflare" in response.headers.get("Server", "").lower():
            positives.append("CDN gedetecteerd (Cloudflare).")
        else:
            issues.append("Geen CDN gedetecteerd (zoals Cloudflare) – mogelijk te verbeteren.")

        # LINK CHECK
        links = soup.find_all("a", href=True)
        broken = 0
        for link in links[:10]:
            href = link["href"]
            if href.startswith("http") and url not in href:
                continue
            try:
                test_url = urljoin(url, href)
                r = requests.get(test_url, timeout=5)
                if r.status_code >= 400:
                    broken += 1
            except:
                broken += 1
        if broken > 0:
            issues.append(f"{broken} interne links lijken niet te werken (404 of foutmelding).")
        else:
            positives.append("Alle geteste interne links werken goed.")

        # CAPTCHA CHECK
        forms = soup.find_all("form")
        if forms:
            try:
                form_action = forms[0].get("action") or url
                action_url = urljoin(url, form_action)
                post_result = requests.post(action_url, data={"test": "pyflow-scan"}, timeout=5)
                if "captcha" in post_result.text.lower():
                    positives.append("Formulier bevat CAPTCHA – goed tegen spam.")
                else:
                    positives.append("Formulier getest – geen CAPTCHA gedetecteerd.")
            except:
                issues.append("Formuliertest mislukt – kan niet worden verzonden.")

        # ✅ Positieve lijst opschonen (voorkom rare strings zoals 'Bevat')
        positives = [p for p in positives if p.strip() and len(p.strip()) > 5 and not re.fullmatch(r"\b(bevat)\b", p.strip(), re.IGNORECASE)]

        # ✅ Score berekenen
        score = max(30, 100 - len(issues) * 5)

        return jsonify({
            "issues": issues,
            "positives": positives,
            "score": score
        })

    except Exception as e:
        return jsonify({
            "issues": [f"❌ Fout tijdens analyse: {str(e)}"],
            "positives": [],
            "score": 0
        })



if __name__ == "__main__":
    app.run(debug=False)
