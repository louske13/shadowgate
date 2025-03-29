
from flask import Flask, request, redirect, render_template_string
import smtplib
from email.mime.text import MIMEText
import requests

app = Flask(__name__)

PASSWORD_ACTIONS = {
    "Ther@pi1": "⚠️ Agent captif volontaire – infiltré, opération assumée.",
    "Ther@pi2": "⚠️ Agent captif, non hostile – coopération en cours.",
    "Ther@pi3": "⚠️ Agent captif, hostile – situation tendue.",
    "Ther@pi4": "⚠️ Agent repéré – détruisez tout.",
    "Ther@pi5": "⚠️ Agent repéré – FUYEZ IMMÉDIATEMENT."
}

FROM_EMAIL = "mzo.fpa@gmail.com"
TO_EMAIL = "alertimediate@gmail.com"
APP_PASSWORD = "jevt qvas vrpj bveo"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Shadowgate | Accès sécurisé</title>
    <style>
        body {
            background-color: #121212;
            color: #fff;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        h2 {
            font-size: 2rem;
            margin-bottom: 20px;
        }
        .container {
            background-color: #1e1e1e;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.1);
            text-align: center;
        }
        input[type="password"] {
            padding: 12px;
            width: 280px;
            border: none;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 1rem;
        }
        button {
            background-color: #339CFF;
            color: white;
            padding: 12px 28px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
        }
        .eye {
            position: absolute;
            margin-left: -30px;
            margin-top: 12px;
            cursor: pointer;
        }
        .error {
            color: #ff4444;
            margin-top: 15px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h2>Entrez votre mot de passe :</h2>
    <div class="container">
        <form method="POST">
            <div style="position: relative;">
                <input type="password" name="password" id="password" required>
                <span class="eye" onclick="togglePassword()">👁️</span>
            </div>
            <br>
            <button type="submit">Valider</button>
        </form>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </div>
    <script>
        function togglePassword() {
            var input = document.getElementById("password");
            if (input.type === "password") {
                input.type = "text";
            } else {
                input.type = "password";
            }
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
                loc_info = f"IP: {ip}, City: {geo_data.get('city')}, Region: {geo_data.get('region')}, Country: {geo_data.get('country')}, ISP: {geo_data.get('org')}"
            except:
                loc_info = "Géolocalisation non disponible"

            msg = MIMEText(f"{PASSWORD_ACTIONS[password]}

{loc_info}")
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
