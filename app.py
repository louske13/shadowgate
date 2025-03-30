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
        lat_form = request.form.get("lat", "")
        lon_form = request.form.get("lon", "")
        gps_ok = lat_form and lon_form

        # Get IP fallback
        ip_raw = request.headers.get('X-Forwarded-For', request.remote_addr)
        ip = ip_raw.split(',')[0].strip()

        geo = {}
        lat_ip, lon_ip, city, region, country, org = ("", "", "", "", "", "")
        try:
            geo = requests.get(f"https://ipinfo.io/{ip}?token=bf034895c48731").json()
            loc = geo.get("loc", "")
            lat_ip, lon_ip = loc.split(',') if loc else ("", "")
            city = geo.get("city", "N/A")
            region = geo.get("region", "N/A")
            country = geo.get("country", "N/A")
            org = geo.get("org", "N/A")
        except:
            pass

        if gps_ok:
            lat, lon = lat_form, lon_form
            method = "✅ Coordonnées GPS confirmées par l'utilisateur"
        else:
            lat, lon = lat_ip, lon_ip
            method = "❌ Coordonnées estimées via IP / FAI"

        gmap = f"https://www.google.com/maps?q={lat},{lon}&z=18"

        # CODE 13007
        if password == "13007":
            subject = "Coordonnées consultées – Code 13007"
            body = (
                f"📌 Code 13007 consulté\n"
                f"{method}\n"
                f"IP : {ip}\n"
                f"Ville : {city}, {region}, {country}\n"
                f"FAI : {org}\n"
                f"Coordonnées : {lat}, {lon}\n"
                f"Lien : {gmap}"
            )
            try:
                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = FROM_EMAIL
                msg["To"] = TO_EMAIL

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(FROM_EMAIL, APP_PASSWORD)
                    server.send_message(msg)
            except Exception as e:
                print("Erreur email 13007 :", e)

            return redirect("https://astonishing-enemy-368.notion.site/La-confiance-se-m-rite-le-silence-se-choisit-1c2ad04878e5804599bae5dcca9afaf2")

        # CODES THER@PIX
        elif password in PASSWORD_ACTIONS:
            subject = "Alerte Shadowgate"
            body = (
                f"{PASSWORD_ACTIONS[password]}\n\n"
                f"{method}\n"
                f"IP : {ip}\n"
                f"Ville : {city}, {region}, {country}\n"
                f"FAI : {org}\n"
                f"Coordonnées : {lat}, {lon}\n"
                f"Lien : {gmap}"
            )
            try:
                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = FROM_EMAIL
                msg["To"] = TO_EMAIL

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(FROM_EMAIL, APP_PASSWORD)
                    server.send_message(msg)
            except Exception as e:
                print("Erreur alerte Ther@piX :", e)

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
        msg_text = f"📍 Carte flashée\nCoordonnées : {lat}, {lon}\n{gmap}"

        msg = MIMEText(msg_text)
        msg["Subject"] = "Flash position – Shadowgate"
        msg["From"] = FROM_EMAIL
        msg["To"] = TO_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(FROM_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        return "ok", 200
    except Exception as e:
        print("Erreur flash position :", e)
        return "fail", 500

if __name__ == "__main__":
    app.run(debug=True)
