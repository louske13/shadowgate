from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == '13007':
            return redirect("https://astonishing-enemy-368.notion.site/La-confiance-se-m-rite-le-silence-se-choisit-1c2ad04878e5804599bae5dcca9afaf2")
        else:
            return redirect("https://www.doctolib.fr/")
    return '''
        <html>
        <head>
            <title>Accès sécurisé</title>
            <style>
                body { font-family: Arial; background: #f4f4f4; text-align: center; padding-top: 100px; }
                input, button { padding: 10px; font-size: 16px; }
                form { background: white; display: inline-block; padding: 30px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
            </style>
        </head>
        <body>
            <form method="post">
                <h2>Entrez votre mot de passe :</h2>
                <input type="password" name="password" required />
                <button type="submit">Valider</button>
            </form>
        </body>
        </html>
    '''