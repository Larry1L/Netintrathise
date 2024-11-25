import sys
import ssl
import os
import logging
from flask import Flask, render_template, request, redirect, url_for

# Opret Flask-applikationen
app = Flask(__name__)

# Dynamisk opdatering af filstier afhængig af om det er en EXE eller Python script
if getattr(sys, 'frozen', False):
    app_dir = sys._MEIPASS  # Folder extracted when EXE is run
else:
    app_dir = os.path.dirname(os.path.abspath(__file__))  # Script-folder

# Stier for logfil og certifikater
log_file = os.path.join(app_dir, 'interactionIP_log.log')
cert_file = os.path.join(app_dir, 'server.crt')
key_file = os.path.join(app_dir, 'server.key')

# Sæt logning op
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Helper Function to Get Client IP
def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip = request.remote_addr
    return ip

# Flask routes
@app.route("/")
def index():
    return render_template("index.html")
@app.route('/')

def home():
    return render_template('index.html')

@app.route("/log_action", methods=["POST"])
def log_action():
    """Logs user interaction and redirects to the external URL."""
    username = request.form.get("username", "Unknown")  # Default to "Unknown" if no username is provided
    action = request.form.get("action", "logon")  # Default action to "logon"
    ip = get_client_ip()
    
    # Log the action with username and IP
    logging.info(f"Action: {action} - Username: {username}, IP: {ip}")
    
    # Redirect to the specified external link for login
    if action == "logon":
        return redirect("https://thiseintra.dk/index.php/component/users/?view=login&Itemid=101")
    elif action == "forgot_username":
        return redirect("https://thiseintra.dk/index.php/component/users/?view=remind&Itemid=101")
    elif action == "forgot_password":
        return redirect("https://thiseintra.dk/index.php/component/users/?view=reset&Itemid=101")
    else:
        return redirect("/")  # Default to homepage for unknown actions



# Kør Flask-applikationen med SSL-konfiguration
if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_file, key_file)
    app.run(ssl_context=context, host='0.0.0.0', port=5000)
