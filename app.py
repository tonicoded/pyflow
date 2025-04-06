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

from bs4 import BeautifulSoup
import requests
import re

@app.route("/website-scan", methods=["POST"])
def website_scan():
    url = request.json.get("url")
    if not url:
        return jsonify({"issues": ["❌ Geen URL opgegeven."]})

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=' ').lower()
        html = response.text.lower()

        issues = []

        # 🔍 Diepe analyse:
        if not soup.find("form"):
            issues.append("❌ Geen formulieren gevonden – contactmogelijkheid ontbreekt.")
        else:
            issues.append("✅ Formulier gedetecteerd.")

        if not soup.find(string=re.compile(r"afspraak|contact", re.IGNORECASE)):
            issues.append("❌ Geen zichtbare 'contact' of 'afspraak'-mogelijkheid op de homepage.")
        else:
            issues.append("✅ Contact/Afspraak genoemd in tekst.")

        if "mailto:" not in html:
            issues.append("❌ Geen e-mailadres (mailto:) gevonden.")
        else:
            issues.append("✅ E-mailadres gevonden.")

        if "tel:" not in html:
            issues.append("❌ Geen telefoonnummer (tel:) gevonden.")
        else:
            issues.append("✅ Telefoonnummer gevonden.")

        if not any(word in text for word in ["automatisering", "procesoptimalisatie", "workflow", "efficiëntie"]):
            issues.append("❌ Geen duidelijke vermelding van automatisering of processen.")
        else:
            issues.append("✅ Vermelding van automatisering of gerelateerde termen.")

        if "cookie" not in text and "privacy" not in text:
            issues.append("❌ Geen cookie- of privacybeleid vermeld – mogelijk juridisch risico.")
        else:
            issues.append("✅ Cookie- of privacybeleid vermeld.")

        if not any("contact" in link.get("href", "").lower() for link in soup.find_all("a", href=True)):
            issues.append("❌ Geen link naar contactpagina gevonden.")
        else:
            issues.append("✅ Link naar contactpagina aanwezig.")

        if not any(kw in text for kw in ["neem contact op", "plan een demo", "vraag een offerte aan"]):
            issues.append("❌ Geen duidelijke call-to-action.")
        else:
            issues.append("✅ Call-to-action aanwezig.")

        if "wp-content" in html:
            issues.append("ℹ️ Website draait waarschijnlijk op WordPress.")
        elif "shopify" in html:
            issues.append("ℹ️ Website draait waarschijnlijk op Shopify.")
        elif "wix" in html or "wixsite" in html:
            issues.append("ℹ️ Website draait waarschijnlijk op Wix.")
        else:
            issues.append("ℹ️ CMS onbekend of maatwerk.")

        page_size_kb = len(response.content) / 1024
        if page_size_kb > 2500:
            issues.append(f"⚠️ Pagina is vrij groot ({int(page_size_kb)}KB) – kan invloed hebben op laadtijd.")
        else:
            issues.append(f"✅ Paginaformaat is normaal ({int(page_size_kb)}KB).")

        return jsonify({"issues": issues})

    except Exception as e:
        return jsonify({"issues": [f"❌ Fout bij analyseren: {str(e)}"]})


if __name__ == "__main__":
    app.run(debug=False)
