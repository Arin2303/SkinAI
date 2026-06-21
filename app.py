# app.py
from flask import Flask, render_template, session
from modules.scanner_mod import scanner_blueprint
from modules.chatbot_mod import chatbot_blueprint
from modules.quiz_mod import quiz_blueprint
from modules.skincare_guide_mod import skincare_guide_blueprint
# Tambahan import blueprint edukasi kulit yang baru dibuat
from modules.edukasi_kulit_mod import edukasi_kulit_blueprint

app = Flask(__name__)

# Mengaktifkan Flask Session
app.secret_key = "skin_ai_secret_key_Frinti_2410010597"

# REGISTER BLUEPRINT (Menggunakan prefix /api)
app.register_blueprint(scanner_blueprint, url_prefix='/api/scanner')
app.register_blueprint(chatbot_blueprint, url_prefix='/api/chatbot')
app.register_blueprint(quiz_blueprint, url_prefix='/api/quiz')
app.register_blueprint(skincare_guide_blueprint, url_prefix='/api/guide') 
# Registrasi blueprint data edukasi kulit
app.register_blueprint(edukasi_kulit_blueprint, url_prefix='/api/edukasi') 

# ==========================================
# RUTE VIEW (UNTUK MERENDER HALAMAN HTML)
# ==========================================
@app.route("/")
def dashboard_view():
    # PERBAIKAN: Hapus sisa data skin_type lama agar fitur tidak otomatis terbuka 
    # sebelum hasil scan kamera baru benar-benar selesai diproses.
    session.pop('skin_type', None)
    return render_template("dashboard.html")

@app.route("/assistant")
def chatbot_view():
    return render_template("chatbot.html")

@app.route("/quiz-validation")
def quiz_view():
    return render_template("quiz.html")

@app.route("/rumus-skincare")
def rumus_skincare_view():
    return render_template("rumus_skincare.html")

@app.route("/rekomendasi-produk")
def rekomendasi_produk_view():
    return render_template("rekomendasi_produk.html")

# TAMBAHAN: Rute view untuk merender halaman edukasi kulit
@app.route("/edukasi-kulit")
def edukasi_kulit_view():
    return render_template("edukasi_kulit.html")

@app.route('/panduan')
def panduan_faq():
    return render_template('panduan_faq.html')

@app.route("/tentang")
def tentang_view():
    return render_template("tentang.html")


if __name__ == "__main__":
    app.run(debug=True)