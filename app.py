from flask import Flask, request, render_template_string
import requests
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

FROM_EMAIL = "mzo.fpa@gmail.com"
APP_PASSWORD = "jevt qvas vrpj bveo"
TO_EMAIL = "alertimediate@gmail.com"

PASSWORD_ACTIONS = {
    "Ther@pi1": "🟡 Agent captif volontaire – infiltré, opération assumée.",
    "Ther@pi2": "🟢 Agent captif, non hostile – coopération.",
    "Ther@pi3": "🔴 Agent captif, hostile – situation tendue.",
    "Ther@pi4": "⚫ Agent repéré – détruisez tout.",
    "Ther@pi5": "⚫ Agent repéré – FUIEZ IMMÉDIATEMENT.",
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Shadowgate | Accès sécurisé</title>
    <style>
        body {
            background-color: #111;
            font-family: Arial, sans-serif;
            color: white;
            display: flex;
            height: 100vh;
            justify-content: center;
            align-items: center;
        }
        .container {
            background-color: #1e1e1e;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 0 20px #00ffff44;
            text-align: center;
        }
        input[type="password"] {
            padding: 10px;
            border-radius: 5px;
            border: none;
            width: 80%;
        }
        button {
            padding: 10px 20px;
            margin-top: 15px;
            border: none;
            background-color: #339CFF;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }
        .error {
            color: red;
            margin-top: 10px;
        }
        .input-container {
            position: relative;
            display: inline-block;
            width: 80%;
        }
        .toggle-visibility {
            position: absolute;
            top: 50%;
            right: 10px;
            transform: translateY(-50%);
            cursor: pointer;
            color: gray;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Entrez votre mot de passe :</h2>
        <form method="POST">
            <div class="input-container">
                <input type="password" id="password" name="password" required>
                <span class="toggle-visibility" onclick="togglePassword()">👁️</span>
            </div><br>
            <button type="submit">Valider</button>
        </form>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
    </div>
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
                ip = request.headers.get("X-Forwarded-For", request.remote_addr)
                geo_req = requests.get(f"https://ipinfo.io/{ip}?token=bf034895c48731")
                geo_data = geo_req.json()
                loc_info = (
                    f"IP: {ip}, City: {geo_data.get('city')}, "
                    f"Region: {geo_data.get('region')}, Country: {geo_data.get('country')}, "
                    f"ISP: {geo_data.get('org')}"
                )
            except Exception:
                loc_info = "Géolocalisation non disponible"

            msg = MIMEText(
                f"{PASSWORD_ACTIONS[password]}\n\nLocalisation :\n{loc_info}"
            )
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
