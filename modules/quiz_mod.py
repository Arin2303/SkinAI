from flask import Blueprint, request, jsonify, session

quiz_blueprint = Blueprint('quiz', __name__)

# ===================================================================================================
# 1. DATASET 5 PERTANYAAN VALIDASI TIPE KULIT (PILIHAN GANDA)
# ===================================================================================================
DAFTAR_PERTANYAAN = [
    {
        "id": 1,
        "pertanyaan": "Bagaimana kondisi wajah Anda sekitar 1-2 jam setelah mencuci muka (tanpa skincare)?",
        "pilihan": {
            "A": "Mengkilap dan berminyak di seluruh area wajah.",
            "B": "Berminyak di dahi, hidung, atau dagu (T-Zone), tapi pipi terasa kering/biasa.",
            "C": "Terasa kencang, ketarik, kering, atau ada bagian yang mengelupas.",
            "D": "Terasa nyaman, seimbang, tidak terlalu berminyak maupun kering."
        }
    },
    {
        "id": 2,
        "pertanyaan": "Bagaimana tampilan pori-pori di wajah Anda jika dilihat dari dekat?",
        "pilihan": {
            "A": "Besar dan terlihat jelas di seluruh area wajah.",
            "B": "Besar dan jelas hanya di area hidung dan sekitarnya (T-Zone).",
            "C": "Sangat kecil, halus, and hampir tidak terlihat.",
            "D": "Terlihat normal dan tidak terlalu mengganggu."
        }
    },
    {
        "id": 3,
        "pertanyaan": "Apa yang terjadi pada kulit Anda saat berada di ruangan ber-AC dalam waktu lama?",
        "pilihan": {
            "A": "Tetap terasa berminyak atau malah memproduksi lebih banyak minyak.",
            "B": "Area T-Zone tetap berminyak, tetapi area pipi mulai terasa kering.",
            "C": "Kulit menjadi sangat kering, kusam, bersisik, atau terasa perih.",
            "D": "Kulit tetap terasa normal, sehat, dan terhidrasi dengan baik."
        }
    },
    {
        "id": 4,
        "pertanyaan": "Seberapa sering wajah Anda mengalami kemerahan, perih, atau gatal saat mencoba kosmetik baru?",
        "pilihan": {
            "A": "Sangat sering, kulit saya langsung bereaksi negatif dan mudah iritasi.",
            "B": "Hanya terjadi jika produk tersebut mengandung bahan aktif jerawat yang keras.",
            "C": "Jarang sekali, kulit saya cenderung kuat mencoba berbagai produk.",
            "D": "Hampir tidak pernah mengalami reaksi alergi atau iritasi."
        }
    },
    {
        "id": 5,
        "pertanyaan": "Bagaimana kecenderungan kulit Anda terhadap masalah komedo atau jerawat?",
        "pilihan": {
            "A": "Sangat mudah berjerawat parah/kistik dan dipenuhi komedo hitam/putih.",
            "B": "Jerawat atau bruntusan sering muncul hanya di area T-Zone.",
            "C": "Jarang berjerawat, kalaupun ada biasanya hanya bintik kecil akibat dehidrasi.",
            "D": "Hanya muncul satu atau dua jerawat sesekali (misal saat PMS atau stres)."
        }
    }
]

# ===================================================================================================
# 2. ENDPOINT UNTUK MENGAMBIL DAFTAR PERTANYAAN (UNTUK FRONTEND/WEB UI)
# ===================================================================================================
@quiz_blueprint.route('/get-questions', methods=['GET'])
def get_questions():
    # Mengambil context sementara dari preview kamera
    tipe_scan = session.get('scan_preview_type', 'Normal Skin')
    return jsonify({
        "status": "success", 
        "questions": DAFTAR_PERTANYAAN,
        "skin_type_context": tipe_scan
    })

# ===================================================================================================
# 3. ENDPOINT KALKULASI: IMPLEMENTASI FUSI BOBOT (30% CAMERA + 70% KUESIONER)
# ===================================================================================================
@quiz_blueprint.route('/calculate-accuracy', methods=['POST'])
def calculate_accuracy():
    try:
        data = request.get_json() or {}
        
        # 1. Ambil skor mentah dari kamera di latar belakang yang dikirim via JS
        vision_scores = data.get("vision_scores") or {}
        jawaban_user = data.get("answers", [])
        
        if not jawaban_user or len(jawaban_user) < 5:
            return jsonify({"status": "error", "message": "Jawaban kuesioner tidak lengkap!"}), 400

        # 2. Ambil nilai individual kamera (Default ke 25% rata jika data bermasalah)
        v_oily = vision_scores.get("oily", 25)
        v_dry = vision_scores.get("dry", 25)
        v_normal = vision_scores.get("normal", 25)
        v_combi = vision_scores.get("combi", 25)

        # 3. Hitung perolehan nilai dari kuesioner harian (+20 poin per opsi yang cocok)
        quiz_points = {"oily": 0, "combi": 0, "dry": 0, "normal": 0}
        for jawaban in jawaban_user:
            if jawaban == "A":
                quiz_points["oily"] += 20
            elif jawaban == "B":
                quiz_points["combi"] += 20
            elif jawaban == "C":
                quiz_points["dry"] += 20
            elif jawaban == "D":
                quiz_points["normal"] += 20

        # Deteksi diri indikator tambahan kulit sensitif (Soal No. 4 opsi A)
        is_sensitif = (jawaban_user[3] == "A")

        # 4. RUMUS PELEBURAN BERBOBOT (30% Kamera + 70% Kuis)
        final_scores = {
            "oily": int((v_oily * 0.3) + (quiz_points["oily"] * 0.7)),
            "dry": int((v_dry * 0.3) + (quiz_points["dry"] * 0.7)),
            "normal": int((v_normal * 0.3) + (quiz_points["normal"] * 0.7)),
            "combi": int((v_combi * 0.3) + (quiz_points["combi"] * 0.7))
        }

        # Normalisasi pembulatan kecil agar total penjumlahan akhir wajib mutlak 100%
        selisih = 100 - sum(final_scores.values())
        if selisih != 0:
            tipe_tertinggi = max(final_scores, key=final_scores.get)
            final_scores[tipe_tertinggi] += selisih

        # 5. Tentukan tipe pemenang akumulasi tertinggi
        tipe_final_id = max(final_scores, key=final_scores.get)
        
        nama_tipe_kulit = {
            "oily": "Oily Skin",
            "dry": "Dry Skin",
            "normal": "Normal Skin",
            "combi": "Combination Skin"
        }[tipe_final_id]

        if is_sensitif and tipe_final_id != "normal":
            nama_tipe_kulit += " & Sensitive"

        # PERBAIKAN UTAMA: Hasil akhir mutlak SAH hanya disimpan di sini ke session['skin_type']
        session['skin_type'] = nama_tipe_kulit

        # 6. Bangun narasi summary langsung ke hasil tanpa membongkar cara kerja AI
        summary_text = f"Analisis selesai. Tipe kulit Anda teridentifikasi sebagai {nama_tipe_kulit}."

        # 7. Database penentu muatan rekomendasi skincare berdasarkan hasil akhir
        db_rekomendasi = {
            "oily": {
                "kandungan": ["Salicylic Acid (BHA)", "Niacinamide", "Zinc PCA"],
                "tips": "Gunakan pembersih wajah bertekstur gel low-pH. Fokus pada hidrasi ringan berbasis air tanpa kandungan minyak berat."
            },
            "dry": {
                "kandungan": ["Ceramides NP", "Hyaluronic Acid", "Squalane Oil"],
                "tips": "Gunakan pelembab bertekstur krim tebal (*rich cream*). Hindari mencuci muka dengan air hangat atau sabun yang menghasilkan terlalu banyak busa."
            },
            "combi": {
                "kandungan": ["Niacinamide", "Centella Asiatica", "PHA Ringan"],
                "tips": "Gunakan teknik multimasking: berikan gel pengontrol minyak di T-Zone (dahi & hidung) serta krim hidrasi ekstra di area pipi."
            },
            "normal": {
                "kandungan": ["Vitamin C", "Hyaluronic Acid", "Peptides"],
                "tips": "Kondisi kulit Anda sangat seimbang dan ideal. Cukup pertahankan kelembapan dasar serta gunakan proteksi sunscreen minimal SPF 30 PA+++ setiap hari."
            }
        }
        
        # Penanganan fallback aman jika label tambahan sensitif aktif
        id_rekomendasi_clean = "oily" if "Oily" in nama_tipe_kulit else ("dry" if "Dry" in nama_tipe_kulit else ("combi" if "Combination" in nama_tipe_kulit else "normal"))
        rekomendasi_final = db_rekomendasi[id_rekomendasi_clean]

        if is_sensitif:
            rekomendasi_final["kandungan"].insert(0, "Allantoin / Panthenol")
            rekomendasi_final["tips"] = "⚠️ Kulit terindikasi sensitif: " + rekomendasi_final["tips"] + " Hindari produk yang mengandung alkohol denat dan pewangi tambahan (fragrance)."

        return jsonify({
            "status": "success",
            "new_scores": final_scores,
            "final_skin_type": nama_tipe_kulit,
            "summary": summary_text,
            "rekomendasi": rekomendasi_final
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500