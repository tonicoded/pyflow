from flask import Flask, render_template, Response, jsonify, request
from flask_mail import Mail, Message
import os
import random
import json

app = Flask(__name__, static_folder='static', template_folder='templates')


# ✅ E-mailconfiguratie (Gebruik Gmail SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'anthonyvvza@gmail.com'  # 🔹 Vervang dit met jouw Gmail-adres
app.config['MAIL_PASSWORD'] = 'cnuq lqwd ccns zhuc'  # 🔹 Gebruik een app-wachtwoord, niet je gewone wachtwoord!
app.config['MAIL_DEFAULT_SENDER'] = 'anthonyvvza@gmail.com'  # 🔹 Zelfde als MAIL_USERNAME

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/robots.txt')
def robots():
    return Response("User-agent: *\nAllow: /\nSitemap: https://www.pyflow.nl/sitemap.xml", mimetype="text/plain")

@app.route('/sitemap.xml')
def sitemap():
    sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">
        <url><loc>https://www.pyflow.nl/</loc><priority>1.0</priority></url>
        <url><loc>https://www.pyflow.nl/contact</loc><priority>0.8</priority></url>
        <url><loc>https://www.pyflow.nl/overons</loc><priority>0.7</priority></url>
        <url><loc>https://www.pyflow.nl/besparings-calculator</loc><priority>0.8</priority></url>
    </urlset>
    """
    return Response(sitemap_xml, mimetype="application/xml")

def load_stats():
    try:
        if not os.path.exists("stats.json"):
            print("📄 stats.json niet gevonden, nieuw bestand aangemaakt.")
            return {"clicks": 0, "live_visitors": 0, "messages_sent": 0, "calculator_uses": 0}
        with open("stats.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Fout bij het laden van stats.json: {e}")
        return {"clicks": 0, "live_visitors": 0, "messages_sent": 0, "calculator_uses": 0}


def save_stats(data):
    with open("stats.json", "w") as f:
        json.dump(data, f)

@app.before_request
def track_clicks():
    if request.endpoint not in ['static', 'dashboard_data', 'live_automation']:
        stats = load_stats()
        stats["clicks"] += 1
        stats["live_visitors"] = min(stats.get("live_visitors", 0) + 1, 999)
        save_stats(stats)

@app.after_request
def track_exit(response):
    try:
        stats = load_stats()
        stats["live_visitors"] = max(stats.get("live_visitors", 1) - 1, 0)
        save_stats(stats)
    except Exception as e:
        print(f"⚠️ Fout in after_request: {e}")
    return response




@app.route('/automatiseren')
def automatiseren():
    return render_template('automatiseren.html')

@app.route('/overons')
def overons():
    return render_template('overons.html')

@app.route('/besparings-calculator')
def besparings_calculator():
    return render_template('timetracker.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        stats = load_stats()
        stats["messages_sent"] += 1
        save_stats(stats)
        return jsonify({"message": "⚠️ Vul alle velden in!"})

    # ✅ E-mail versturen
    try:
        msg = Message(subject=f"Nieuw Contactbericht van {name}",
                      recipients=["anthonyvvza@gmail.com"],  # 🔹 Jouw e-mailadres
                      body=f"Naam: {name}\nE-mail: {email}\n\nBericht:\n{message}")

        mail.send(msg)
        return jsonify({"message": "✅ Bericht verzonden! We nemen spoedig contact op."})

    except Exception as e:
        print(f"Fout bij verzenden e-mail: {e}")
        return jsonify({"message": "⚠️ Er is iets misgegaan. Probeer later opnieuw."})


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
    stats = load_stats()
    stats["calculator_uses"] += 1
    save_stats(stats)
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
@app.route("/stats")
def stats():
    key = request.args.get("key")
    if key != "geheim123":  # Vervang dit door een unieke sleutel
        return "Niet toegestaan", 403
    return render_template("stats.html")

@app.route("/get-stats")
def get_stats():
    key = request.args.get("key")
    if key != "geheim123":
        return jsonify({"error": "Niet toegestaan"}), 403
    return jsonify(load_stats())


if __name__ == "__main__":
    app.run(debug=False)
