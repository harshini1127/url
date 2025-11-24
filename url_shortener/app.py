import os
from datetime import datetime

from flask import Flask, request, redirect, render_template, jsonify, url_for, abort, session
from datetime import datetime
import validators
import os

from db import db
from models import URL, User
from shortener import generate_short_id
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "your_secret_key_here"

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()


# -------------------------
#       HOME PAGE
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
#       REGISTER
# -------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if user exists
        existing = User.query.filter_by(email=email).first()
        if existing:
            return "Email already registered!"

        hashed_pw = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        return redirect("/")

    return render_template("register.html")


# -------------------------
#        LOGIN
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return "Invalid email or password!"

        session["user_id"] = user.id
        return redirect("/")

    return render_template("login.html")


# -------------------------
#        LOGOUT
# -------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# -------------------------
#     CREATE SHORT URL
# -------------------------
@app.route("/api/shorten", methods=["POST"])
def api_shorten():
    data = request.get_json() or {}
    long_url = data.get("url") or request.form.get("url")
    custom = data.get("custom")

    if not long_url or not validators.url(long_url):
        return jsonify({"error": "Invalid or missing URL"}), 400

    # Custom alias
    if custom:
        exists = URL.query.filter_by(short_id=custom).first()
        if exists:
            return jsonify({"error": "This custom alias is already taken"}), 409
        short_id = custom
    else:
        short_id = generate_short_id()
        while URL.query.filter_by(short_id=short_id).first():
            short_id = generate_short_id()

    new_url = URL(long_url=long_url, short_id=short_id)
    db.session.add(new_url)
    db.session.commit()

    short_url = url_for("redirect_short", short_id=short_id, _external=True)

    return jsonify({
        "short_url": short_url,
        "short_id": short_id,
        "long_url": long_url
    }), 201


# -------------------------
#       REDIRECT SHORT URL
# -------------------------
@app.route("/<short_id>")
def redirect_short(short_id):
    url = URL.query.filter_by(short_id=short_id).first()
    if not url:
        abort(404)

    url.clicks += 1
    url.last_accessed = datetime.utcnow()
    db.session.commit()

    return redirect(url.long_url)


# -------------------------
#       URL INFO API
# -------------------------
@app.route("/api/info/<short_id>")
def info(short_id):
    url = URL.query.filter_by(short_id=short_id).first_or_404()

    return jsonify({
        "short_id": url.short_id,
        "long_url": url.long_url,
        "clicks": url.clicks,
        "created_at": url.created_at.isoformat(),
        "last_accessed": url.last_accessed.isoformat() if url.last_accessed else None
    })


# -------------------------
#     RUN APPLICATION
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
