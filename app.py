from flask import Flask, request, redirect, render_template, render_template_string
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

app = Flask(__name__)

FROM_EMAIL = "mzo.fpa@gmail.com"
APP_PASSWORD = "jevt qvas vrpj bveo"
TO_EMAIL = "alertimediate@gmail.com"

PASSWORD_ACTIONS = {
    "Ther@pi1": "🟢 Captif volontairement (mission infiltrée assumée)",
    "Ther@pi2": "🟡 Captif, non hostile (coopération, situation calme)",
    "Ther@pi3": "🟠 Captif, hostile (situation tendue ou agressive)",
    "Ther@pi4": "🔴 Danger imminent (urgence absolue)",
    "Ther@pi5": "⚫ Situation critique, intervention immédiate requise"
}

def get_location_info(ip):
    try:
        geo_req = requests.get(f"https://ipinfo.io/{ip}?token=bf034895c48731")
        geo_data = geo_req.json()
        loc = geo_data.get('loc', '')
        city = geo_data.get('city', 'N/A')
        region = geo_data.get('region', 'N/A')
        country = geo_data.get('country', 'N/A')
        org = geo_data.get('org', 'N/A')
        lat, lon = loc.split(',') if loc else ("", "")
        gmap_link = f"https://www.google.com/maps?q={lat},{lon}"
        return f"IP: {ip}\nVille: {city}\nRégion: {region}\nPays: {country}\nFAI: {org}\nLien Google Maps: {gmap_link}"
    except:
        return "Géolocalisation indisponible."

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(FROM_EMAIL, APP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print("Erreur envoi email:", e)

@app.route("/", methods=["GET", "POST"])
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    location = get_location_info(ip)

    if request.method == "GET":
        # Email silencieux : QR code flashé
        now = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S UTC")
        send_email("QR Code Flashé", f"QR code accédé à {now}\n{location}")
        return render_template("index.html", error=None)

    if request.method == "POST":
        password = request.form["password"]

        if password == "13007":
            # Email silencieux : consultation réelle
            now = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S UTC")
            send_email("Consultation Données", f"Consultation réelle à {now}\n{location}")
            return redirect("https://astonishing-enemy-368.notion.site/La-confiance-se-m-rite-le-silence-se-choisit-1c2ad04878e5804599bae5dcca9afaf2")

        elif password in PASSWORD_ACTIONS:
            message = f"{PASSWORD_ACTIONS[password]}\n\n{location}"
            send_email("Alerte Shadowgate", message)
            return render_template("biotrace.html")

        else:
            return render_template("index.html", error="❌ Mot de passe incorrect.")

if __name__ == "__main__":
    app.run(debug=True)
