from flask import Flask, request, render_template_string, redirect
import smtplib
from email.mime.text import MIMEText
import requests
import os

app = Flask(__name__)

FROM_EMAIL = "mzo.fpa@gmail.com"
TO_EMAIL = "alertimediate@gmail.com"
APP_PASSWORD = "jevt qvas vrpj bveo"
IPINFO_TOKEN = "bf034895c48731"

PASSWORD_ACTIONS = {
    "13007": "🔓 Accès autorisé – agent sécurisé.",
    "Ther@pi1": "🟡 Agent captif volontaire – infiltré, opération assumée.",
    "Ther@pi2": "🟠 Agent captif, non hostile – coopération possible.",
    "Ther@pi3": "🔴 Agent captif, hostile – situation tendue.",
    "Ther@pi4": "⚫ Agent repéré – détruisez tout.",
    "Ther@pi5": "⚫ Agent repéré – FUYEZ IMMÉDIATEMENT."
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Shadowgate | Accès sécurisé</title>
    <style>
        body {
            background-color: #121212;
            color: #f1f1f1;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        .box {
            background-color: #1e1e1e;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 15px #00f0ff3b;
        }
        input[type="password"] {
            padding: 10px;
            border-radius: 5px;
            border: none;
            width: 200px;
            margin-right: 5px;
        }
        button {
            padding: 10px 20px;
            background-color: #4e8df5;
            border: none;
            border-radius: 5px;
            color: white;
            cursor: pointer;
        }
        .eye {
            position: relative;
            left: -30px;
            cursor: pointer;
        }
        .error {
            color: red;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <form method="post">
        <div class="box">
            <h2>Entrez votre mot de passe :</h2>
            <div style="display:flex; align-items:center;">
                <input type="password" name="password" id="password">
                <span class="eye" onclick="togglePassword()">👁️</span>
            </div>
            <br>
            <button type="submit">Valider</button>
            {% if error %}
                <div class="error">{{ error }}</div>
            {% endif %}
        </div>
    </form>
<script>
    function togglePassword() {
        var input = document.getElementById("password");
        input.type = input.type === "password" ? "text" : "password";
    }
</script>
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
    loc = geo_data.get('loc', '0,0')
    lat, lon = loc.split(',')

    gmap_link = f"https://www.google.com/maps?q={lat},{lon}"
    loc_info = (
        f"IP: {ip}\n"
        f"City: {geo_data.get('city')}\n"
        f"Region: {geo_data.get('region')}\n"
        f"Country: {geo_data.get('country')}\n"
        f"ISP: {geo_data.get('org')}\n"
        f"Google Maps: {gmap_link}"
    )
except Exception as e:
    loc_info = f"Géolocalisation non disponible ({str(e)})"

            msg = MIMEText(f"{PASSWORD_ACTIONS[password]}\n\n📍 Localisation :\n{loc_info}")
            msg["Subject"] = "⚠️ Alerte Shadowgate"
            msg["From"] = FROM_EMAIL
            msg["To"] = TO_EMAIL

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(FROM_EMAIL, APP_PASSWORD)
                server.send_message(msg)

            if password == "13007":
                return redirect("https://notion.so/tonlienreel")  # lien réel
            else:
                return redirect("https://notion.so/fauxdossiermedical")  # faux
        else:
            return render_template_string(HTML_TEMPLATE, error="❌ Mot de passe incorrect.")
    return render_template_string(HTML_TEMPLATE, error=None)

if __name__ == "__main__":
    app.run(debug=True)
