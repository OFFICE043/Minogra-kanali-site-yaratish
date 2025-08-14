import os
from flask import Flask, render_template, redirect, url_for
import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def get_anime_list():
    url = f"{SUPABASE_URL}/rest/v1/anime"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }
    resp = requests.get(url, headers=headers, params={"select": "*"})
    return resp.json()

def get_anime_detail(anime_id):
    url = f"{SUPABASE_URL}/rest/v1/anime"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }
    params = {"id": f"eq.{anime_id}", "select": "*"}
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    return data[0] if data else None

app = Flask(__name__)

@app.route("/")
def index():
    anime_list = get_anime_list()
    return render_template("index.html", anime_list=anime_list)

@app.route("/anime/<int:anime_id>")
def anime_detail(anime_id):
    anime = get_anime_detail(anime_id)
    if not anime:
        return redirect(url_for("index"))
    return render_template("anime_detail.html", anime=anime)

if __name__ == "__main__":
    app.run(debug=True)
