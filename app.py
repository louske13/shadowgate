from flask import Flask, request, render_template_string, redirect, render_template
import requests
import smtplib
from email.mime.text import MIMEText
import os

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

# HTML simple avec mot de passe masqué + œil
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Shadowgate</title>
    <style>
        body { font-family: Arial; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
        input[type="password"] { padding: 10px; font-size: 16px; }
        button, .eye { padding: 10px; font-size: 16px; margin-left: 5px; }
        form { display: flex; align-items: center; }
    </style>
</head>
<body>
    <h2>Entrez votre code</h2>
    <form method="POST">
        <input type="password" id="password" name="password" required>
        <button type="submit">Valider</button>
        <span class="eye" onclick="togglePassword()" style="cursor:pointer;">👁️</span>
    </form>
    {% if error %}
    <p style="color:red;">{{ error }}</p>
    {% endif %}
    <script>
        function togglePassword() {
            var x = document.getElementById("password");
            x.type = (x.type === "password") ? "text" : "password";
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form.get("password")

        if password == VALID_PASSWORD:
            return redirect("https://astonishing-enemy-368.notion.site/La-confiance-se-m-rite-le-silence-se-choisit-1c2ad04878e5804599bae5dcca9afaf2")

        elif password in ALERT_PASSWORDS:
            try:
                ip = request.headers.get('X-Forwarded-For', request.remote_addr)
                geo_req = requests.get(f"https://ipinfo.io/{ip}?token=bf034895c48731")
                geo_data = geo_req.json()
                loc_info = (
                    f"IP: {ip}\n"
                    f"Ville: {geo_data.get('city')}, Région: {geo_data.get('region')}, Pays: {geo_data.get('country')}\n"
                    f"Coordonnées: {geo_data.get('loc')}\n"
                    f"Fournisseur: {geo_data.get('org')}"
                )
                lat, lon = geo_data.get("loc", "0,0").split(",")
                gmap_link = f"https://www.google.com/maps?q={lat},{lon}"
            except Exception:
                loc_info = "Géolocalisation non disponible"
                gmap_link = ""

            msg_content = f"{ALERT_PASSWORDS[password]}\n\n{loc_info}\n\nLien Google Maps : {gmap_link}"
            msg = MIMEText(msg_content)
            msg["Subject"] = "🛑 Alerte Shadowgate"
            msg["From"] = FROM_EMAIL
            msg["To"] = TO_EMAIL

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(FROM_EMAIL, APP_PASSWORD)
                server.send_message(msg)

            return render_template("biotrace.html")  # redirige vers la fausse page médicale

        else:
            return render_template_string(HTML_TEMPLATE, error="❌ Mot de passe incorrect.")

    return render_template_string(HTML_TEMPLATE, error=None)

if __name__ == "__main__":
    app.run(debug=True)

