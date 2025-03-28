
from flask import Flask, request, render_template_string, redirect
import smtplib
from email.mime.text import MIMEText
import json

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<html>
  <head>
    <title>Shadowgate</title>
    <script>
      fetch('https://ipinfo.io/json?token=bf034895c48731')
        .then(response => response.json())
        .then(data => {
          const geo = document.createElement("input");
          geo.type = "hidden";
          geo.name = "geodata";
          geo.value = JSON.stringify(data);
          document.querySelector("form").appendChild(geo);
        });
    </script>
  </head>
  <body>
    <h2>Entrez votre mot de passe :</h2>
    <form method="post">
      <input type="text" name="password" />
      <button type="submit">Valider</button>
    </form>
    {% if error %}
    <p style="color:red;">{{ error }}</p>
    {% endif %}
  </body>
</html>
'''

EMAIL_MAP = {
    "Ther@pi1": "⚠️ Agent captif volontaire – infiltré, opération assumée.",
    "Ther@pi2": "⚠️ Agent captif, non hostile – coopération temporaire.",
    "Ther@pi3": "⚠️ Agent captif, hostile – situation tendue.",
    "Ther@pi4": "⚠️ Agent repéré – détruisez tout.",
    "Ther@pi5": "⚠️ Agent repéré – FUYEZ IMMÉDIATEMENT.",
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form.get("password")
        geo_data = request.form.get("geodata")
        if geo_data:
            geo = json.loads(geo_data)
            ip = geo.get("ip", "N/A")
            city = geo.get("city", "N/A")
            region = geo.get("region", "N/A")
            country = geo.get("country", "N/A")
            isp = geo.get("org", "N/A")
        else:
            ip = city = region = country = isp = "None"

        if password == "13007":
            return redirect("https://astonishing-enemy-368.notion.site/La-confiance-se-m-rite-le-silence-se-choisit-1c2ad04878e5804599bae5dcca9afaf2")
        elif password in EMAIL_MAP:
            send_alert_email(EMAIL_MAP[password], ip, city, region, country, isp)
            return redirect("https://astonishing-enemy-368.notion.site/Page-m-dicale-fictive")
        else:
            return render_template_string(HTML_TEMPLATE, error="❌ Mot de passe incorrect.")

    return render_template_string(HTML_TEMPLATE, error=None)

def send_alert_email(message, ip, city, region, country, isp):
    msg = MIMEText(f"{message}\n\n📍 Localisation :\nIP: {ip}, City: {city}, Region: {region}, Country: {country}, ISP: {isp}")
    msg["Subject"] = "⚠️ Alerte Shadowgate"
    msg["From"] = "mzo.fpa@gmail.com"
    msg["To"] = "alertimediate@gmail.com"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("mzo.fpa@gmail.com", "jevt qvas vrpj bveo")
        smtp.send_message(msg)

if __name__ == "__main__":
    app.run(debug=True)
