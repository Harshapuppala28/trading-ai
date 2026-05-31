
from flask import Flask
import threading
import os
import subprocess

app = Flask(__name__)


# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/")
def home():

    return "Trading AI Scanner Running 🚀"


# ==========================================
# START SCANNER
# ==========================================

def run_scanner(): 
    subprocess.Popen( 
        ["python", "data_fetcher.py"] 
    )


scanner_thread = threading.Thread(
    target=run_scanner
)

scanner_thread.start()


# ==========================================
# RUN FLASK
# ==========================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(

        host="0.0.0.0",

        port=port

    )

