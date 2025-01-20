from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hotel_management.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Kullanıcı Modeli
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Veritabanını oluştur
with app.app_context():
    db.create_all()

# Giriş Sayfası
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect(url_for("dashboard"))
        else:
            return "Hatalı giriş bilgileri!"

    return """
    <form method="POST">
        Kullanıcı Adı: <input type="text" name="username" required><br>
        Şifre: <input type="password" name="password" required><br>
        <button type="submit">Giriş Yap</button>
    </form>
    """

# Ana Menü (Dashboard)
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return """
    <h1>Hoş Geldiniz! Ana Menü</h1>
    <ul>
        <li><a href='/front_office'>Ön Büro & Fiyat Yönetimi</a></li>
        <li><a href='/task_tracking'>İş Takibi</a></li>
        <li><a href='/salary_management'>Personel Maaş Takip Sistemi</a></li>
    </ul>
    <a href='/logout'>Çıkış Yap</a>
    """

# Çıkış Yap
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

# Sunucuyu çalıştır
if __name__ == "__main__":
    app.run(debug=True)
