
from flask import Flask, request, redirect, render_template_string
import requests
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

IPINFO_TOKEN = "bf034895c48731"
ALERT_EMAIL = "alertimediate@gmail.com"
SENDER_EMAIL = "mzo.fpa@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_PASSWORD = "jevt qvas vrpj bveo"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang='fr'>
<head>
    <meta charset='UTF-8'>
    <title>Accès sécurisé</title>
    <style>
        body {
            background: linear-gradient(to right, #1f1c2c, #928dab);
            font-family: 'Segoe UI', sans-serif;
            color: white;
            text-align: center;
            padding-top: 100px;
        }
        input[type="password"] {
            padding: 12px 20px;
            margin: 8px;
            border: none;
            border-radius: 4px;
            width: 300px;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .box {
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 12px;
            display: inline-block;
        }
        .error {
            color: #ff6b6b;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>Entrez votre mot de passe :</h1>
        <form method="post">
            <input type="password" name="password" required autofocus>
            <br>
            <input type="submit" value="Valider">
        </form>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

def get_location(ip):
    try:
        url = f"https://ipinfo.io/{ip}?token={IPINFO_TOKEN}"
        response = requests.get(url)
        data = response.json()
        return (
            data.get("ip", "Unknown"),
            data.get("city", "None"),
            data.get("region", "None"),
            data.get("country", "None"),
            data.get("org", "None")
        )
    except Exception:
        return ("Unknown", "None", "None", "None", "None")

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = ALERT_EMAIL
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form.get("password")
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        ip, city, region, country, org = get_location(ip)

        if password == "13007":
            return redirect("https://astonishing-enemy-368.notion.site/La-confiance-se-m-rite-le-silence-se-choisit-1c2ad04878e5804599bae5dcca9afaf2")
        elif password.startswith("Ther@pi"):
            codes = {
                "Ther@pi1": "🟡 Agent captif volontaire – infiltré, opération assumée.",
                "Ther@pi2": "🟢 Agent captif, non hostile – coopération établie.",
                "Ther@pi3": "🟠 Agent captif, hostile – situation tendue.",
                "Ther@pi4": "🔴 Agent repéré – détruisez tout.",
                "Ther@pi5": "⚫ Agent repéré – FUYER IMMÉDIATEMENT."
            }
            subject = "⚠️ Alerte Shadowgate"
            message = codes[password] + f"\n\n📍 Localisation :\nIP: {ip}, City: {city}, Region: {region}, Country: {country}, ISP: {org}"
            send_email(subject, message)
            return redirect("https://astonishing-enemy-368.notion.site/Page-m-dicale-fictive-pour-mot-de-passe-84057c7e0a1e45d5a7bc89fdf65a7c3f")
        else:
            return render_template_string(HTML_TEMPLATE, error="❌ Mot de passe incorrect. Réessayez.")
    return render_template_string(HTML_TEMPLATE, error=None)
