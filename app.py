from flask import Flask, request, redirect, render_template  
import requests
import smtplib
from email.mime.text import MIMEText

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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Accès sécurisé</title>
    <style>
        body {
            background-color: #f2f2f2;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        h2 {
            color: #333;
        }
        form {
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        input[type="password"] {
            padding: 10px;
            margin-right: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        button {
            padding: 10px 15px;
            border: none;
            background-color: #444;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }
        .error {
            color: red;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <form method="POST">
        <h2>🔐 Veuillez entrer le mot de passe</h2>
        <input type="password" id="password" name="password" required>
        <button type="button" onclick="togglePassword()">👁️</button>
        <br><br>
        <button type="submit">Valider</button>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
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
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form["password"]

        if password == "13007":
            return redirect("https://astonishing-enemy-368.notion.site/La-confiance-se-m-rite-le-silence-se-choisit-1c2ad04878e5804599bae5dcca9afaf2")

        elif password in PASSWORD_ACTIONS:
            try:
                ip = request.headers.get('X-Forwarded-For', request.remote_addr)
                geo_req = requests.get(f"https://ipinfo.io/{ip}?token=bf034895c48731")
                geo_data = geo_req.json()
                loc = geo_data.get('loc', '')
                city = geo_data.get('city', 'N/A')
                region = geo_data.get('region', 'N/A')
                country = geo_data.get('country', 'N/A')
                org = geo_data.get('org', 'N/A')
                lat, lon = loc.split(',') if loc else ("", "")
                gmap_link = f"https://www.google.com/maps?q={lat},{lon}"
                loc_info = (
                    f"IP: {ip}\n"
                    f"Ville: {city}\nRégion: {region}\nPays: {country}\nFAI: {org}\n"
                    f"Lien Google Maps: {gmap_link}"
                )
            except:
                loc_info = "Géolocalisation indisponible."

            message = f"{PASSWORD_ACTIONS[password]}\n\n{loc_info}"
            msg = MIMEText(message)
            msg["Subject"] = "Alerte Shadowgate"
            msg["From"] = FROM_EMAIL
            msg["To"] = TO_EMAIL

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(FROM_EMAIL, APP_PASSWORD)
                    server.send_message(msg)
            except Exception as e:
                print("Erreur envoi email:", e)

            return render_template("biotrace.html")

        else:
            return render_template("index.html", error="❌ Mot de passe incorrect.")

   return render_template("index.html", error=error)

if __name__ == "__main__":
    app.run(debug=True)
