from flask import Flask, render_template, request, redirect, url_for, flash
# Importe les modules nécessaires de Flask pour gérer le web
import re # Importe le module d'expressions régulières.
import requests # Permet de faire des requêtes HTTP.
import random, string # Pour générer des chaînes aléatoires.
import os # Gère les opérations sur le système de fichiers.
app = Flask(__name__) # Crée une instance de l'application Flask


app.secret_key = "a3k7$#1r9!2jdlNcmwQ^z"  # Add this line!
# Clé secrète utilisée pour sécuriser les sessions
app.config['DOWNLOAD_FOLDER'] = 'static/downloads' # Définit le dossier de téléchargement
app.config['ALLOWED_EXTENSIONS'] = {'mp4'} # Types de fichiers autorisés.



# Ensure download directory exists
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True) # Crée le dossier de téléchargement s’il n’existe pas.
print("Wellcome to my app")  # Affiche un message au démarrage.
Fyle_type=None  # Variable globale pour stocker le type de fichier téléchargé.



def rand_str(n): return ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=n)) # Génère une chaîne aléatoire.


def download_video(video_url): # Fonction principale pour télécharger une vidéo Facebook
    try:
        global Fyle_type
        cookies = { # Définit des cookies aléatoires pour simuler un navigateur.
    'sb': rand_str(24),
    'fr': f"{rand_str(20)}.{rand_str(30)}.{rand_str(22)}..AAA.0.0.{(p:=rand_str(6))}.{rand_str(40)}",
    'datr': rand_str(24),
    'wd': f"1920x{random.choice([945, 1080, 1000])}",
    'ps_l': '1',
    'ps_n': '1'
}
        headers = { # Définit les en-têtes pour simuler un navigateur.
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}
        # Send a GET request to the video URL
        # os.system('cls')
        print('\033[1;33m==================================================================================')
        print("\033[1;36mDownloading video from: \033[1;31m", video_url)
        response = requests.get(video_url, headers=headers,cookies=cookies).text.replace('\\','') # Requête HTTP
        # open(os.path.join(app.config['DOWNLOAD_FOLDER'], 'tempssxx.txt'), 'w' ,encoding= 'utf-8').write(response)
        try:
            browser_native_hd_url= 'https://video'+re.findall(r'd_url":"https://video(.*?)"', response)[-1] # Extrait le lien vidéo.

            output_file = "facebook_video.mp4"
            Fyle_type ="Video"
        except :
            browser_native_hd_url= re.search(r'"image":{"uri":"(.*?)"', response).group(1) # Si échec, on prend une image.
            output_file = "facebook_photo.jpg"
            Fyle_type ="Image"
        # print(browser_native_hd_url)
        # open('tempss.txt', 'w' ,encoding= 'utf-8').write(response)
        # Download the video
        response = requests.get(browser_native_hd_url, stream=True) # Télécharge le contenu du média
        filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], output_file)
        if response.status_code == 200:
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):  # Sauvegarde par morceaux de 1Mo.
                    if chunk:
                        f.write(chunk)
            print("✅ \033[1;32mDownload complete:", output_file)
            return filepath
        else:
            print("❌ Failed to download, status code:", response.status_code)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
@app.route("/", methods=["GET", "POST"]) # Déclare la route principale.

def index():
    global Fyle_type
    if request.method == "POST":
        video_url = request.form.get("video_url", "").strip()

        if not video_url:
            flash("Please enter a valid Facebook video URL.", "error")
            return redirect(url_for("index"))
            
        # Validate Facebook URL
        if not any(domain in video_url for domain in ['facebook.com', 'fb.watch']):
            flash("Please enter a valid Facebook video URL.", "error")
            return redirect(url_for("index"))
        # Try to download the video
        filename = download_video(video_url)
        
        if not filename:
            flash("Could not download video. Please check the URL and try again.", "error")
            return redirect(url_for("index"))
            
        # In a real app, you would serve the actual downloaded file
        # For demo, we'll just show a success message
        # download_link = url_for('static', filename=filename)
        flash(f"{Fyle_type} downloaded successfully!", "success")
        return render_template("index.html", download_link=filename)

    return render_template("index.html", download_link=None)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
