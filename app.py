from flask import Flask, request, redirect, render_template_string
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Accès sécurisé</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            width: 300px;
        }
        input[type="password"], input[type="submit"] {
            padding: 10px;
            font-size: 16px;
            margin-top: 10px;
            width: 100%;
        }
        .error {
            color: red;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔐 Entrez votre mot de passe :</h2>
        <form method="post">
            <input type="password" name="password" required>
            <input type="submit" value="Valider">
        </form>
        {% if error %}
            <div class="error">❌ {{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

EMAILS = {
    "Ther@pi1": "⚠️ Agent captif volontaire – infiltré, opération assumée.",
    "Ther@pi2": "⚠️ Agent captif, non hostile – coopération stable.",
    "Ther@pi3": "⚠️ Agent captif, hostile – situation tendue.",
    "Ther@pi4": "⚠️ Agent repéré – détruisez tout.",
    "Ther@pi5": "⚠️ Agent repéré – FUYEZ IMMÉDIATEMENT."
}

NOTION_LINK = "https://astonishing-enemy-368.notion.site/La-confiance-se-m-rite-le-silence-se-choisit-1c2ad04878e5804599bae5dcca9afaf2"
FAKE_MEDICAL_PAGE = "https://www.ameli.fr/assure/sante/medecine/remboursements"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "mzo.fpa@gmail.com"
SMTP_PASS = "jevt qvas vrpj bveo"
ALERT_EMAIL = "alertimediate@gmail.com"

def send_alert(subject):
    msg = MIMEText(subject)
    msg['Subject'] = "🔔 Alerte Shadowgate"
    msg['From'] = SMTP_USER
    msg['To'] = ALERT_EMAIL
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Erreur envoi e-mail : {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pwd = request.form['password']
        if pwd == "13007":
            return redirect(NOTION_LINK)
        elif pwd in EMAILS:
            send_alert(EMAILS[pwd])
            return redirect(FAKE_MEDICAL_PAGE)
        else:
            return render_template_string(HTML_TEMPLATE, error="Mot de passe incorrect, veuillez réessayer.")
    return render_template_string(HTML_TEMPLATE, error=None)

if __name__ == '__main__':
    app.run()
