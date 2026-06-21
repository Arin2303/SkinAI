# modules/edukasi_kulit_mod.py
from flask import Blueprint, jsonify

edukasi_kulit_blueprint = Blueprint('edukasi_kulit', __name__)

@edukasi_kulit_blueprint.route('/get-edukasi', methods=['GET'])
def get_edukasi_data():
    # Mengembalikan seluruh data ensiklopedia jenis kulit tanpa terkunci session
    all_data = {
        "status": "success",
        "edukasi": {
            "Combination": {
                "nama": "Combination Skin (Kulit Kombinasi)",
                "judul": "Seni Menyeimbangkan Dua Zona Wajah",
                "pembuka": "Kulit kombinasi memiliki tantangan unik karena kelenjar minyak (sebum) aktif di area T-Zone (dahi, hidung, dagu), namun cenderung kering atau normal di area U-Zone (pipi dan rahang). Kuncinya adalah keseimbangan hidrasi tanpa menyumbat.",
                "tips": [
                    "Gunakan teknik **Multi-moisturizing**: Aplikasikan pelembab gel ringan di area T-zone dan pelembab krim yang sedikit lebih tebal di area pipi yang kering.",
                    "Jangan lewatkan toner hidrasi di area pipi agar kulit tidak mengirim sinyal darurat untuk memproduksi minyak berlebih."
                ],
                "pantangan": [
                    {"hal": "Menggunakan scrub fisik yang kasar", "alasan": "Bisa mengikis area pipi yang kering dan memicu iritasi/kemerahan, sekaligus merangsang minyak berlebih di T-zone."},
                    {"hal": "Memakai produk berbahan dasar alkohol kering tinggi", "alasan": "Membuat area pipi semakin bersisik meskipun area hidung terasa kesat sementara."}
                ],
                "mitos_fakta": [
                    {"mitos": "Kulit kombinasi harus punya dua set skincare yang berbeda.", "fakta": "Tidak perlu. Cukup gunakan produk basic yang ramah untuk semua area, lalu kontrol area T-zone dengan serum aktif secara lokal."},
                    {"mitos": "Area T-zone yang berminyak tidak perlu diberi pelembab.", "fakta": "Salah. Jika tidak diberi pelembab, kulit akan mengalami dehidrasi dan justru memproduksi minyak dua kali lipat lebih banyak."}
                ]
            },
            "Oily": {
                "nama": "Oily Skin (Kulit Berminyak)",
                "judul": "Menjinakkan Kilap dan Mencegah Penyumbatan Pori",
                "pembuka": "Kulit berminyak memproduksi sebum secara berlebih di seluruh area wajah. Masalah utama tipe kulit ini adalah pori-pori tersumbat yang memicu komedo dan jerawat. Fokus utama kita adalah regulasi minyak dan eksfoliasi pori.",
                "tips": [
                    "Selalu cari label **Non-Comedogenic** dan **Oil-Free** pada setiap produk skincare yang kamu beli.",
                    "Eksfoliasi rutin menggunakan BHA (Salicylic Acid) sangat efektif memotong rantai pembentukan jerawat dari dalam pori."
                ],
                "pantangan": [
                    {"hal": "Mencuci muka terlalu sering (lebih dari 3 kali sehari)", "alasan": "Menghilangkan minyak alami secara paksa, membuat kulit dehidrasi, dan memicu rebound effect (minyak keluar lebih ganas)."},
                    {"hal": "Menggunakan face oil murni bertekstur berat", "alasan": "Sangat berpotensi menyumbat pori-pori yang sudah sempit akibat tumpukan sebum alami."}
                ],
                "mitos_fakta": [
                    {"mitos": "Minyak di wajah bisa dihilangkan secara permanen.", "fakta": "Minyak adalah pelindung alami kulit. Kita hanya bisa mengontrol jumlah produksinya agar seimbang, bukan menghilangkannya total."},
                    {"mitos": "Sunscreen bikin wajah berminyak semakin kusam dan berjerawat.", "fakta": "Itu jika menggunakan jenis physical sunscreen yang tebal. Jenis chemical atau hybrid serum-gel bertekstur matte justru nyaman dan wajib."}
                ]
            },
            "Dry": {
                "nama": "Dry Skin (Kulit Kering)",
                "judul": "Merajut Kembali Lapisan Pelindung Kelembapan",
                "pembuka": "Kulit kering kekurangan lipid atau minyak alami, sehingga kelembapan sangat mudah menguap (High TEWL). Kulit sering terasa kaku, ketarik, gatal, hingga mengelupas. Fokusnya adalah moisture-locking dan perbaikan skin barrier.",
                "tips": [
                    "Gunakan teknik hidrasi berlapis (layering toner) dan kunci dengan pelembab bertekstur krim padat (occlusive).",
                    "Gunakan produk yang kaya akan kandungan Ceramide, Squalane, dan Hyaluronic Acid."
                ],
                "pantangan": [
                    {"hal": "Manti atau mencuci muka dengan air panas", "alasan": "Air panas melarutkan sisa-sisa lipid alami yang sangat berharga bagi kulit kering, menyebabkannya semakin gersang."},
                    {"hal": "Terlalu sering menggunakan bahan aktif eksfoliasi kuat (AHA/BHA dosis tinggi)", "alasan": "Dapat merusak skin barrier yang tipis dan memicu iritasi hebat berupa rasa perih mendalam."}
                ],
                "mitos_fakta": [
                    {"mitos": "Kulit kering hanya perlu minum air putih yang banyak agar lembap.", "fakta": "Minum air membantu hidrasi tubuh secara umum, namun kulit kering kekurangan minyak di permukaan wajah, sehingga tetap butuh krim pelembab dari luar."},
                    {"mitos": "Kulit yang mengelupas harus digosok pakai scrub agar halus.", "fakta": "Sangat berbahaya. Menggosok kulit kering yang mengelupas justru akan memicu luka mikro dan infeksi barrier."}
                ]
            },
            "Normal": {
                "nama": "Normal Skin (Kulit Normal)",
                "judul": "Mempertahankan Keseimbangan Ideal Kulitmu",
                "pembuka": "Selamat! Kulit normal memiliki rasio air dan minyak yang sangat seimbang, jarang berjerawat, dan tidak sensitif. Tugas utamanya bukan menyembuhkan, melainkan menjaga (maintenance) dan melindunginya dari penuaan dini.",
                "tips": [
                    "Gunakan antioksidan seperti Vitamin C di pagi hari untuk menangkal radikal bebas dan polusi.",
                    "Konsisten dengan basic skincare (Cleanser - Moisturizer - Sunscreen) agar kondisi ideal ini bertahan lama."
                ],
                "pantangan": [
                    {"hal": "Sering bergonta-ganti produk skincare tanpa jeda", "alasan": "Bisa merusak kestabilan pH dan memicu reaksi alergi pada kulit yang semula sehat walafiat."},
                    {"hal": "Mengabaikan penggunaan Sunscreen saat cuaca mendung", "alasan": "Sinar UV-A tetap menembus awan dan kaca, berpotensi memicu flek hitam dini pada kulit normal."}
                ],
                "mitos_fakta": [
                    {"mitos": "Kulit normal tidak perlu menggunakan produk anti-aging sejak dini.", "fakta": "Perawatan anti-aging (seperti penggunaan serum Peptide/Retinol ringan) justru paling efektif dimulai saat kulit dalam kondisi sehat dan normal."},
                    {"mitos": "Skincare mahal pasti memberikan efek glowing dua kali lipat pada kulit normal.", "fakta": "Kulit normal merespon produk dengan bahan dasar sederhana dengan sangat baik. Konsistensi jauh lebih penting daripada harga produk."}
                ]
            }
        }
    }
    return jsonify(all_data)