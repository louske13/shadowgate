from flask import Flask, request, render_template_string
import requests
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Tes identifiants
FROM_EMAIL = "mzo.fpa@gmail.com"
TO_EMAIL = "alertimediate@gmail.com"
APP_PASSWORD = "jevt qvas vrpj bveo"

# Actions déclenchées selon le mot de passe
PASSWORD_ACTIONS = {
    "Ther@pi1": "🟡 Captif volontairement",
    "Ther@pi2": "🟢 Captif non hostile",
    "Ther@pi3": "🔴 Captif hostile",
    "Ther@pi4": "⚫ Captif repéré – détruisez tout",
    "Ther@pi5": "⚫ Captif repéré – fuyez",
    "13007": "✅ Accès autorisé"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><title>Shadowgate</title></head>
<body>
    <h2>🕵️ Entrez votre code</h2>
    <form method="post">
        <input type="password" name="password" required>
        <button type="submit">Valider</button>
    </form>
    {% if error %}
    <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form["password"]
        if password in PASSWORD_ACTIONS:
            try:
                ip = request.headers.get('X-Forwarded-For', request.remote_addr)
                geo_req = requests.get(f"https://ipinfo.io/{ip}?token=bf034895c48731")
                geo_data = geo_req.json()

                city = geo_data.get('city', 'N/A')
                region = geo_data.get('region', 'N/A')
                country = geo_data.get('country', 'N/A')
                loc = geo_data.get('loc', '0,0')
                org = geo_data.get('org', 'N/A')

                lat, lon = loc.split(",")
                gmap_link = f"https://www.google.com/maps?q={lat},{lon}"

                loc_info = f"IP: {ip}\nCity: {city}\nRegion: {region}\nCountry: {country}\nISP: {org}\nGoogle Maps: {gmap_link}"
            except Exception as e:
                loc_info = f"Géolocalisation indisponible : {str(e)}"

            if password != "13007":
                msg = MIMEText(f"{PASSWORD_ACTIONS[password]}\n\n{loc_info}")
                msg["Subject"] = "⚠️ Alerte Shadowgate"
                msg["From"] = FROM_EMAIL
                msg["To"] = TO_EMAIL

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(FROM_EMAIL, APP_PASSWORD)
                    server.send_message(msg)

            return render_template_string(HTML_TEMPLATE, error=None)
        else:
            return render_template_string(HTML_TEMPLATE, error="❌ Mot de passe incorrect.")
    return render_template_string(HTML_TEMPLATE, error=None)

if __name__ == "__main__":
    app.run(debug=True)
