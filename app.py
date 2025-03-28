from flask import Flask, request, redirect, render_template_string
import requests
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Mot de passe principal (ne déclenche pas d'alerte)
MAIN_PASSWORD = "13007"

# Codes secrets déclenchant une alerte
ALERT_CODES = {
    "Ther@pi1": "🟡 Agent captif volontaire – infiltré, opération assumée.",
    "Ther@pi2": "🔵 Agent captif, non hostile – coopération relative.",
    "Ther@pi3": "🟠 Agent captif, hostile – situation tendue.",
    "Ther@pi4": "🔴 Agent repéré – détruisez tout.",
    "Ther@pi5": "⚫ Agent repéré – FUYEZ IMMÉDIATEMENT.",
}

# Email d'alerte
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "mzo.fpa@gmail.com"
SMTP_PASSWORD = "jevt qvas vrpj bveo"
EMAIL_FROM = "mzo.fpa@gmail.com"
EMAIL_TO = "alertimediate@gmail.com"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang='fr'>
<head>
    <meta charset='UTF-8'>
    <title>Shadowgate | Accès sécurisé</title>
    <style>
        body {
            background-color: #0d1117;
            color: #f0f6fc;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        h1 {
            font-size: 1.8rem;
            margin-bottom: 20px;
        }
        form {
            background-color: #161b22;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0,255,255,0.1);
        }
        input[type="password"] {
            padding: 10px;
            border: none;
            border-radius: 6px;
            width: 250px;
            background-color: #0d1117;
            color: #f0f6fc;
            font-size: 1rem;
        }
        button {
            margin-top: 15px;
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            background-color: #58a6ff;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
        .error {
            margin-top: 15px;
            color: #ff7b72;
            font-weight: bold;
        }
        .toggle-eye {
            margin-left: -30px;
            cursor: pointer;
            color: #58a6ff;
        }
    </style>
</head>
<body>
    <h1>Entrez votre mot de passe :</h1>
    <form method="post">
        <div style="display: flex; align-items: center;">
            <input type="password" name="password" id="password" required>
            <span class="toggle-eye" onclick="togglePassword()">👁️</span>
        </div>
        <button type="submit">Valider</button>
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
    </form>
    <script>
        function togglePassword() {
            const pwd = document.getElementById('password');
            pwd.type = pwd.type === 'password' ? 'text' : 'password';
        }
    </script>
</body>
</html>
"""

def get_geolocation(ip):
    try:
        url = f"https://ipinfo.io/{ip}?token=bf034895c48731"
        response = requests.get(url)
        data = response.json()
        return f"\n📍 Localisation :\nIP: {ip}, City: {data.get('city', 'None')}, Region: {data.get('region', 'None')}, Country: {data.get('country', 'None')}, ISP: {data.get('org', 'None')}"
    except:
        return f"\n📍 Localisation :\nIP: {ip}, données de géolocalisation indisponibles."

def send_alert(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form.get("password")
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if password == MAIN_PASSWORD:
            return redirect("https://astonishing-enemy-368.notion.site/La-confiance-se-m-rite-le-silence-se-choisit-1c2ad04878e5804599bae5dcca9afaf2")
        elif password in ALERT_CODES:
            geo = get_geolocation(ip)
            alert_msg = ALERT_CODES[password] + geo
            send_alert("⚠️ Alerte Shadowgate", alert_msg)
            return redirect("https://astonishing-enemy-368.notion.site/Page-m-dicale-Shadowgate-4335093ddea44d3db361689f4a3736be")
        else:
            return render_template_string(HTML_TEMPLATE, error="Mot de passe incorrect.")
    return render_template_string(HTML_TEMPLATE, error=None)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
