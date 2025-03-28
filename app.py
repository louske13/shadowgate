from flask import Flask, request, redirect, render_template
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

PASSWORDS = {
    "13007": "https://astonishing-enemy-368.notion.site/La-confiance-se-m-rite-le-silence-se-choisit-1c2ad04878e5804599bae5dcca9afaf2",
    "Ther@pi1": "https://www.notion.so/FaussePageMedicale",
    "Ther@pi2": "https://www.notion.so/FaussePageMedicale",
    "Ther@pi3": "https://www.notion.so/FaussePageMedicale",
    "Ther@pi4": "https://www.notion.so/FaussePageMedicale",
    "Ther@pi5": "https://www.notion.so/FaussePageMedicale"
}

ALERTS = {
    "Ther@pi1": "Code 1 - Captif volontairement",
    "Ther@pi2": "Code 2 - Captif non hostile",
    "Ther@pi3": "Code 3 - Captif hostile",
    "Ther@pi4": "Code 4 - Captif repéré – détruisez tout",
    "Ther@pi5": "Code 5 - Captif repéré – fuyez"
}

SMTP_USER = "mzo.fpa@gmail.com"
SMTP_PASS = "jevt qvas vrpj bveo"
TO_EMAIL = "alertimediate@gmail.com"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password in ALERTS:
            send_alert(ALERTS[password])
        return redirect(PASSWORDS.get(password, "https://www.notion.so/PageIntrouvable"))
    return render_template("index.html")

def send_alert(message):
    msg = MIMEText(message)
    msg["Subject"] = "ALERTE CODE SHADOWGATE"
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

if __name__ == "__main__":
    app.run(debug=True)
