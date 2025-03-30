from flask import Flask, request, redirect, render_template, jsonify
import requests
import smtplib
from email.mime.text import MIMEText

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

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        password = request.form.get("password")
        lat = request.form.get("lat", "")
        lon = request.form.get("lon", "")
        coords_provided = lat and lon

        if password == "13007":
            try:
                ip_raw = request.headers.get('X-Forwarded-For', request.remote_addr)
                ip = ip_raw.split(',')[0].strip()
                geo = requests.get(f"https://ipinfo.io/{ip}?token=bf034895c48731").json()
                loc = geo.get('loc', '')
                city = geo.get('city', 'N/A')
                region = geo.get('region', 'N/A')
                country = geo.get('country', 'N/A')
                org = geo.get('org', 'N/A')
                lat, lon = loc.split(',') if loc else ("", "")
                gmap = f"https://www.google.com/maps?q={lat},{lon}"
                msg = MIMEText(f"📌 Code 13007 consulté\nIP : {ip}\nVille : {city}, {region}, {country}\nFAI : {org}\nCoordonnées : {lat}, {lon}\n{gmap}")
                msg["Subject"] = "Coordonnées consultées – Code 13007"
                msg["From"] = FROM_EMAIL
                msg["To"] = TO_EMAIL
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(FROM_EMAIL, APP_PASSWORD)
                    server.send_message(msg)
            except Exception as e:
                print("Erreur mail 13007 :", e)
            return redirect("https://astonishing-enemy-368.notion.site/La-confiance-se-m-rite-le-silence-se-choisit-1c2ad04878e5804599bae5dcca9afaf2")

        elif password in PASSWORD_ACTIONS:
            try:
                if coords_provided:
                    gmap = f"https://www.google.com/maps?q={lat},{lon}&z=18"
                    loc_info = f"Coordonnées GPS : {lat}, {lon}\nGoogle Maps : {gmap}"
                else:
                    ip_raw = request.headers.get('X-Forwarded-For', request.remote_addr)
                    ip = ip_raw.split(',')[0].strip()
                    geo = requests.get(f"https://ipinfo.io/{ip}?token=bf034895c48731").json()
                    loc = geo.get('loc', '')
                    city = geo.get('city', 'N/A')
                    region = geo.get('region', 'N/A')
                    country = geo.get('country', 'N/A')
                    org = geo.get('org', 'N/A')
                    lat, lon = loc.split(',') if loc else ("", "")
                    gmap = f"https://www.google.com/maps?q={lat},{lon}&z=18"
                    loc_info = f"IP : {ip}\n{city}, {region}, {country}\nFAI : {org}\nCoords : {lat}, {lon}\nGoogle Maps : {gmap}"
                msg = MIMEText(f"{PASSWORD_ACTIONS[password]}\n\n{loc_info}")
                msg["Subject"] = "Alerte Shadowgate"
                msg["From"] = FROM_EMAIL
                msg["To"] = TO_EMAIL
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(FROM_EMAIL, APP_PASSWORD)
                    server.send_message(msg)
            except Exception as e:
                print("Erreur envoi alerte :", e)
            return render_template("biotrace.html")
        else:
            error = "❌ Mot de passe incorrect."
    return render_template("index.html", error=error)

@app.route("/flash", methods=["POST"])
def flash_position():
    try:
        data = request.get_json()
        lat = data.get("lat", "")
        lon = data.get("lon", "")
        gmap = f"https://www.google.com/maps?q={lat},{lon}&z=18"
        msg = MIMEText(f"📍 Carte flashée\nCoordonnées : {lat}, {lon}\n{gmap}")
        msg["Subject"] = "Flash position – Shadowgate"
        msg["From"] = FROM_EMAIL
        msg["To"] = TO_EMAIL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(FROM_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        return "ok", 200
    except:
        return "fail", 500

if __name__ == "__main__":
    app.run(debug=True)
