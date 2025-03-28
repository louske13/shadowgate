
from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText
import requests

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Shadowgate | Accès sécurisé</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #1a1a1d;
            color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        h2 {
            margin-bottom: 30px;
            font-size: 28px;
        }
        .container {
            background-color: #2e2e33;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0,255,255,0.3);
            text-align: center;
        }
        input[type="password"], input[type="text"] {
            padding: 12px;
            font-size: 18px;
            border: none;
            border-radius: 6px;
            margin-bottom: 15px;
            width: 100%;
            text-align: center;
            background-color: #444;
            color: #fff;
        }
        button {
            background-color: #3399ff;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 18px;
            cursor: pointer;
        }
        .error {
            margin-top: 15px;
            color: red;
            font-weight: bold;
        }
        .eye {
            position: absolute;
            margin-left: -30px;
            margin-top: 12px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h2>Entrez votre mot de passe :</h2>
    <form method="POST">
        <div class="container">
            <input type="password" name="password" id="password" required>
            <span class="eye" onclick="togglePassword()">👁️</span><br>
            <button type="submit">Valider</button>
            {% if error %}
                <div class="error">{{ error }}</div>
            {% endif %}
        </div>
    </form>
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
'''

PASSWORD_ACTIONS = {
    "Ther@pi1": "⚠️ Agent captif volontaire – infiltré, opération assumée.",
    "Ther@pi2": "⚠️ Agent captif, non hostile – coopération.",
    "Ther@pi3": "⚠️ Agent captif, hostile – situation tendue.",
    "Ther@pi4": "⚠️ Agent repéré – détruisez tout.",
    "Ther@pi5": "⚠️ Agent repéré – FUYEZ IMMÉDIATEMENT.",
}

TO_EMAIL = "alertimediate@gmail.com"
FROM_EMAIL = "mzo.fpa@gmail.com"
APP_PASSWORD = "jevt qvas vrpj bveo"

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

msg = MIMEText(f"{PASSWORD_ACTIONS[password]}\n\nLocalisation :\nIP: {ip}, City: {city}, Region: {region}, Country: {country}, ISP: {org}")

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
