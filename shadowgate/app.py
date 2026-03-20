from flask import Flask, request, redirect, render_template
import os
import requests

app = Flask(__name__)

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
TO_EMAIL = os.getenv("RECEIVER_EMAIL")

PASSWORD_ACTIONS = {
    "Ther@pi1": "🟢 Captif volontairement (mission infiltrée assumée)",
    "Ther@pi2": "🟡 Captif, non hostile (coopération, situation calme)",
    "Ther@pi3": "🟠 Captif, hostile (situation tendue ou agressive)",
    "Ther@pi4": "🔴 Danger imminent (urgence absolue)",
    "Ther@pi5": "⚫ Situation critique, intervention immédiate requise"
}

def send_email(subject, message):
    print("🔥 ENVOI EMAIL EN COURS")

    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": "shadowgate",
            "email": SENDER_EMAIL
        },
        "to": [
            {
                "email": TO_EMAIL
            }
        ],
        "subject": subject,
        "textContent": message
    }

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, timeout=15)

    print("📩 STATUS CODE :", response.status_code)
    print("📩 RESPONSE :", response.text)

    if response.status_code != 201:
        raise Exception(f"Erreur Brevo : {response.status_code} - {response.text}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form.get("password", "").strip()

        print("🔐 PASSWORD SAISI :", password)

        if password == "13007":
            return redirect(
                "https://astonishing-enemy-368.notion.site/La-confiance-se-m-rite-le-silence-se-choisit-1c2ad04878e5804599bae5dcca9afaf2"
            )

        elif password in PASSWORD_ACTIONS:
            print("✅ PASSWORD RECONNU")

            try:
                ip = request.headers.get("X-Forwarded-For", request.remote_addr)
                if ip and "," in ip:
                    ip = ip.split(",")[0].strip()

                geo_req = requests.get(
                    f"https://ipinfo.io/{ip}?token=bf034895c48731",
                    timeout=10
                )
                geo_data = geo_req.json()

                loc = geo_data.get("loc", "")
                city = geo_data.get("city", "N/A")
                region = geo_data.get("region", "N/A")
                country = geo_data.get("country", "N/A")
                org = geo_data.get("org", "N/A")

                lat, lon = loc.split(",") if loc else ("", "")
                gmap_link = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else "N/A"

                loc_info = (
                    f"IP: {ip}\n"
                    f"Ville: {city}\n"
                    f"Région: {region}\n"
                    f"Pays: {country}\n"
                    f"FAI: {org}\n"
                    f"Lien Google Maps: {gmap_link}"
                )

            except Exception as e:
                print("Erreur géolocalisation :", e)
                loc_info = "Géolocalisation indisponible."

            message = f"{PASSWORD_ACTIONS[password]}\n\n{loc_info}"

            try:
                send_email("Alerte Shadowgate", message)
                return render_template("biotrace.html")

            except Exception as e:
                print("❌ ERREUR ENVOI EMAIL :", e)
                return render_template("index.html", error="❌ Alerte non envoyée.")

        else:
            print("❌ PASSWORD INCORRECT")
            return render_template("index.html", error="❌ Mot de passe incorrect.")

    return render_template("index.html", error=None)

if __name__ == "__main__":
    app.run(debug=True)
