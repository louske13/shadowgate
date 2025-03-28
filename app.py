
from flask import Flask, request, redirect, render_template_string
import smtplib
import requests
import os
from email.mime.text import MIMEText

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Shadowgate | Accès sécurisé</title>
    <style>
        body {
            background-color: #11141b;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            text-align: center;
        }
        .form-box {
            background-color: #1d212f;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 0 20px #0096FF;
            display: inline-block;
        }
        input[type="password"] {
            padding: 10px;
            border: none;
            border-radius: 5px;
            width: 200px;
            margin-right: 10px;
        }
        button {
            background-color: #0096FF;
            color: white;
            border: none;
            padding: 10px 20px;
            margin-top: 15px;
            border-radius: 5px;
            cursor: pointer;
        }
        .eye {
            cursor: pointer;
            position: absolute;
            margin-left: -25px;
            margin-top: 12px;
        }
        .error {
            color: red;
            margin-top: 10px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="form-box">
            <h2>Entrez votre mot de passe :</h2>
            <form method="POST">
                <div style="position: relative;">
                    <input type="password" name="password" id="password" required>
                    <span class="eye" onclick="togglePassword()">👁️</span>
                </div>
                <button type="submit">Valider</button>
            </form>
            {% if error %}
                <div class="error">{{ error }}</div>
            {% endif %}
        </div>
    </div>
    <script>
        function togglePassword() {
            var x = document.getElementById("password");
            if (x.type === "password") {
                x.type = "text";
            } else {
                x.type = "password";
            }
        }
    </script>
</body>
</html>
"""

EMAIL_SENDER = "mzo.fpa@gmail.com"
EMAIL_RECEIVER = "alertimediate@gmail.com"
EMAIL_PASSWORD = "jevt qvas vrpj bveo"

API_TOKEN = "bf034895c48731"

PASSWORD_ACTIONS = {
    "Ther@pi1": "⚠️ Agent captif volontaire – infiltré, opération assumée.",
    "Ther@pi2": "⚠️ Agent captif, non hostile – coopération en cours.",
    "Ther@pi3": "⚠️ Agent captif, hostile – situation tendue.",
    "Ther@pi4": "⚠️ Agent repéré – détruisez tout.",
    "Ther@pi5": "⚠️ Agent repéré – FUYEZ IMMÉDIATEMENT.",
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form.get("password")
        if password in PASSWORD_ACTIONS:
            ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
            geo_data = requests.get(f"https://ipinfo.io/{ip}?token={API_TOKEN}").json()

            location_info = (
                f"IP: {ip}, "
                f"City: {geo_data.get('city', 'None')}, "
                f"Region: {geo_data.get('region', 'None')}, "
                f"Country: {geo_data.get('country', 'None')}, "
                f"ISP: {geo_data.get('org', 'None')}"
            )

            msg = MIMEText(f"{PASSWORD_ACTIONS[password]}

📍 Localisation :
{location_info}")
            msg["Subject"] = "🚨 Alerte Shadowgate"
            msg["From"] = EMAIL_SENDER
            msg["To"] = EMAIL_RECEIVER

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)

            return redirect("https://astonishing-enemy-368.notion.site/La-confiance-se-m-rite-le-silence-se-choisit-1c2ad04878e5804599bae5dcca9afaf2")
        else:
            return render_template_string(HTML_TEMPLATE, error="❌ Mot de passe incorrect.")

    return render_template_string(HTML_TEMPLATE, error=None)

if __name__ == "__main__":
    app.run(debug=True)
