from flask import Flask, render_template, request, redirect, session
from datetime import datetime, timedelta
import smtplib
import requests
from email.mime.text import MIMEText
import json
import secrets

app = Flask(__name__)
app.secret_key = "shadowgate2025"

FROM_EMAIL = "mzo.fpa@gmail.com"
APP_PASSWORD = "jevt qvas vrpj bveo"
TO_EMAIL = "alertimediate@gmail.com"

NOTION_URL = "https://astonishing-enemy-368.notion.site/La-confiance-se-m-rite-le-silence-se-choisit-1c2ad04878e5804599bae5dcca9afaf2"

PASSWORD_ACTIONS = {
    "Ther@pi1": "🟢 Captif volontairement (mission infiltrée assumée)",
    "Ther@pi2": "🟡 Captif, non hostile (coopération, situation calme)",
    "Ther@pi3": "🟠 Captif, hostile (situation tendue ou agressive)",
    "Ther@pi4": "🔴 Danger imminent (urgence absolue)",
    "Ther@pi5": "⚫ Situation critique, intervention immédiate requise"
}

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
        print(f"[EMAIL ERROR] {e}")

def get_location_info(request, lat, lon):
    if lat and lon:
        link = f"https://www.google.com/maps?q={lat},{lon}&z=18"
        return f"✅ Coordonnées GPS confirmées\nLatitude : {lat}\nLongitude : {lon}\nLien : {link}"
    else:
        ip_raw = request.headers.get('X-Forwarded-For', request.remote_addr)
        ip = ip_raw.split(',')[0].strip()
        try:
            geo_req = requests.get(f"https://ipinfo.io/{ip}?token=bf034895c48731")
            geo_data = geo_req.json()
            loc = geo_data.get("loc", "")
            city = geo_data.get("city", "N/A")
            region = geo_data.get("region", "N/A")
            country = geo_data.get("country", "N/A")
            org = geo_data.get("org", "N/A")
            latlon = f"Coordonnées : {loc}" if loc else ""
            link = f"https://www.google.com/maps?q={loc}&z=18" if loc else ""
            return f"❌ Coordonnées estimées via IP / FAI\nIP : {ip}\nVille : {city}, {region}, {country}\nFAI : {org}\n{latlon}\nLien : {link}"
        except:
            return f"🌐 Impossible d’obtenir la localisation\nIP : {ip}"

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    lat_form = request.form.get("lat", "")
    lon_form = request.form.get("lon", "")
    if request.method == "POST":
        password = request.form.get("password")
        if password == "13007":
            location_info = get_location_info(request, lat_form, lon_form)
            send_email("📍 Coordonnées consultées – Code 13007", location_info)
            return redirect("/confidentiel")
        elif password in PASSWORD_ACTIONS:
            code_desc = PASSWORD_ACTIONS[password]
            location_info = get_location_info(request, lat_form, lon_form)
            message = f"{code_desc}\n\n{location_info}"
            send_email("⚠️ Alerte Shadowgate", message)
            token = secrets.token_urlsafe(16)
            session["access_token"] = token
            session["access_time"] = datetime.utcnow().isoformat()
            return redirect(f"/biotrace?token={token}")
        else:
            error = "❌ Mot de passe incorrect."
    return render_template("index.html", error=error)

@app.route("/biotrace")
def biotrace():
    token = request.args.get("token")
    session_token = session.get("access_token")
    access_time_str = session.get("access_time")
    if not token or token != session_token:
        return redirect("/")
    if access_time_str:
        access_time = datetime.fromisoformat(access_time_str)
        if datetime.utcnow() - access_time > timedelta(minutes=10):
            session.clear()
            return redirect("/")
    access_time = datetime.now().strftime("%d/%m/%Y à %H:%M")
    return render_template("biotrace.html", access_time=access_time)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/flash", methods=["POST"])
def flash_position():
    try:
        data = json.loads(request.data)
        lat = data.get("lat")
        lon = data.get("lon")
        if lat and lon:
            link = f"https://www.google.com/maps?q={lat},{lon}&z=18"
            body = f"📍 Carte flashée\nCoordonnées : {lat}, {lon}\n{link}"
            send_email("📩 Flash position – Shadowgate", body)
    except Exception as e:
        print(f"[FLASH ERROR] {e}")
    return "", 204

@app.route("/track-status")
def track_status():
    try:
        with open("track_status.txt", "r") as f:
            return f.read().strip()
    except:
        return "off"

@app.route("/confidentiel")
def proxy_notion():
    try:
        response = requests.get(NOTION_URL, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            return response.text
        else:
            return "Erreur de chargement Notion.", 500
    except Exception as e:
        return f"Erreur Notion : {e}", 500

if __name__ == "__main__":
    app.run(debug=True)
