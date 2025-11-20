from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Pfad zur JSON-Datei
POSTS_FILE = "posts.json"


# ---------------------------
# Hilfsfunktionen
# ---------------------------

def load_posts():
    """Lädt Blogposts aus der JSON-Datei."""
    if not os.path.exists(POSTS_FILE):
        return []
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_posts(posts):
    """Speichert Blogposts in die JSON-Datei."""
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4)


# ---------------------------
# ROUTES
# ---------------------------

@app.route("/")
def index():
    posts = load_posts()
    return render_template("index.html", posts=posts)


# Neue Route: /add
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        posts = load_posts()
        new_id = max([post["id"] for post in posts], default=0) + 1
        posts.append({"id": new_id, "author": author, "title": title, "content": content})
        save_posts(posts)
        return redirect(url_for("index"))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
