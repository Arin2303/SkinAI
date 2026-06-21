# modules/scanner_mod.py
import cv2
import numpy as np
import base64
import random
from flask import Blueprint, request, jsonify, session

scanner_blueprint = Blueprint('scanner', __name__)

FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@scanner_blueprint.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.get_json()
        
        # SINKRONISASI BANTALAN JAVASCRIPT: Menyediakan struktur default jika gagal
        fallback_scores = {"Oily Skin": 0, "Dry Skin": 0, "Normal Skin": 0, "Combination Skin": 0}

        if not data or 'image' not in data:
            return jsonify({
                "status": "success", 
                "tipe_terdeteksi": "Gagal Pemindaian", 
                "scores": fallback_scores,
                "rekomendasi": {"tips": "Data gambar tidak ditemukan."}
            })

        # 1. DECODE GAMBAR
        image_data = data['image'].split(",")[1]
        image_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({
                "status": "success", 
                "tipe_terdeteksi": "Gagal Pemindaian", 
                "scores": fallback_scores,
                "rekomendasi": {"tips": "Format file gambar rusak atau tidak didukung."}
            })

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # SENSITIVITAS KETAT: Menolak wajah setengah keluar atau miring
        faces = FACE_CASCADE.detectMultiScale(
            gray, 
            scaleFactor=1.05,  
            minNeighbors=6,     
            minSize=(140, 180)  
        )

        # Jika wajah tidak terdeteksi utuh
        if len(faces) == 0:
            return jsonify({
                "status": "success", 
                "tipe_terdeteksi": "Wajah Tidak Pas / Terhalang", 
                "scores": fallback_scores,
                "rekomendasi": {
                    "tips": "Pastikan seluruh wajah terlihat utuh di dalam oval pink, posisi tegak, tidak terhalang rambut, masker, atau pencahayaan yang terlalu redup."
                }
            })

        (x, y, w, h) = faces[0]
        
        # Validasi koordinat posisi (Symmetrical Check)
        img_h, img_w, _ = img.shape
        face_center_x = x + (w // 2)
        if face_center_x < (img_w * 0.3) or face_center_x > (img_w * 0.7):
            return jsonify({
                "status": "success",
                "tipe_terdeteksi": "Posisi Kurang Pas",
                "scores": fallback_scores,
                "rekomendasi": {"tips": "Posisikan wajah Anda tepat di tengah-tengah garis oval pemindaian."}
            })

        # EKSTRAKSI WARNA HSV UNTUK ANALISIS DASAR
        face_roi = img[y:y+h, x:x+w]
        hsv_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)
        avg_h, avg_s, avg_v = cv2.mean(hsv_face)[:3]

        # Menentukan Tipe Dominan Awal berdasarkan parameter HSV
        tipe_dominan_vision = "Normal Skin"
        if avg_v > 155 and avg_s > 75: 
            tipe_dominan_vision = "Oily Skin"
        elif avg_v < 115: 
            tipe_dominan_vision = "Dry Skin"
        elif 115 <= avg_v <= 155 and avg_s > 65: 
            tipe_dominan_vision = "Combination Skin"

        # 🌟 LOGIKA BARU: DISTRIBUSI MATEMATIKA AMAN (Bebas dari ValueError randint)
        skor_acak_dominan = random.randint(58, 76)
        sisa_skor = 100 - skor_acak_dominan

        # Membagi sisa skor ke 3 variabel dengan aman menggunakan bobot acak pecahan
        porsi = [random.random() for _ in range(3)]
        total_porsi = sum(porsi)
        
        # Konversi pecahan bobot menjadi nilai integer yang genap menyentuh sisa_skor
        skor_1 = int((porsi[0] / total_porsi) * sisa_skor)
        skor_2 = int((porsi[1] / total_porsi) * sisa_skor)
        skor_3 = sisa_skor - (skor_1 + skor_2)  # Menjaga sisa presisi agar akumulasinya pas 100%

        # Susun struktur skor sesuai tipe dominan
        skor_final = {}
        if tipe_dominan_vision == "Oily Skin":
            skor_final = {"Oily Skin": skor_acak_dominan, "Dry Skin": skor_1, "Normal Skin": skor_2, "Combination Skin": skor_3}
        elif tipe_dominan_vision == "Dry Skin":
            skor_final = {"Dry Skin": skor_acak_dominan, "Oily Skin": skor_1, "Normal Skin": skor_2, "Combination Skin": skor_3}
        elif tipe_dominan_vision == "Combination Skin":
            skor_final = {"Combination Skin": skor_acak_dominan, "Oily Skin": skor_1, "Dry Skin": skor_2, "Normal Skin": skor_3}
        else:
            skor_final = {"Normal Skin": skor_acak_dominan, "Oily Skin": skor_1, "Dry Skin": skor_2, "Combination Skin": skor_3}

        db_rekomendasi = {
            "Oily Skin": {"tips": "Mengoptimalkan pembersihan minyak berlebih via kuesioner harian."},
            "Dry Skin": {"tips": "Mengoptimalkan tingkat hidrasi mendalam via kuesioner harian."},
            "Combination Skin": {"tips": "Mengoptimalkan keseimbangan T-Zone via kuesioner harian."},
            "Normal Skin": {"tips": "Mempertahankan kondisi kulit stabil via kuesioner harian."}
        }

        # Menyimpan hasil pemindaian sementara ke session
        session['scan_preview_type'] = tipe_dominan_vision

        return jsonify({
            "status": "success",
            "tipe_terdeteksi": tipe_dominan_vision,
            "scores": skor_final,
            "rekomendasi": db_rekomendasi[tipe_dominan_vision]
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500