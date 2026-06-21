from flask import Blueprint, request, jsonify

chatbot_blueprint = Blueprint('chatbot', __name__)

# ===================================================================================================
# KAMUS VARIASI KATA KUNCI MEGA-LENGKAP (MAPPING ALIAS DAN GEJALA USER)
# ===================================================================================================
KAMUS_KEYWORDS = {
    "jerawat_aktif": ["jerawat", "berjerawat", "acne", "papula", "pustula", "bruntusan", "komedo pasir"],
    "jerawat_parah": ["jerawat batu", "jerawat nodul", "jerawat kistik", "jerawat hormonal", "nodul", "abses kulit"],
    "komedo_hitam": ["komedo hitam", "komedo terbuka", "blackhead", "blackheads", "black bumps", "sebaceous filaments"],
    "komedo_putih": ["komedo putih", "komedo tertutup", "whitehead", "whiteheads", "white bumps"],
    "milia_syringoma": ["milia", "bintik putih mata", "bintil minyak", "sebaceous hyperplasia", "syringoma", "xanthelasma"],
    "pori_tersumbat": ["pori-pori besar", "pori-pori tersumbat", "pori besar", "pori tersumbat"],
    "kulit_berminyak": ["minyak", "berminyak", "sebum", "kilap", "oily", "produksi minyak berlebih"],
    "kulit_kering": ["kering", "sangat kering", "mengelupas", "pecah-pecah", "dry"],
    "kulit_dehidrasi": ["dehidrasi", "ketarik", "kurang air", "kulit kasar akibat dehidrasi"],
    "kulit_kombinasi": ["kombinasi", "combination"],
    "kulit_sensitif_reaktif": ["sensitif", "sensitive", "kulit reaktif", "sensitivitas berlebihan"],
    "kusam_cahaya": ["kusam", "warna kulit tidak merata", "gelap", "belang", "kulit lelah", "fatigued skin", "kulit kehilangan cahaya alami", "dullness"],
    "pigmentasi_flek": ["hiperpigmentasi", "flek hitam", "flek cokelat", "melasma", "freckles", "sunspot", "age spot", "photoaging", "kerusakan akibat sinar matahari", "lentigo"],
    "hipopigmentasi_vitiligo": ["hipopigmentasi", "vitiligo", "bercak putih"],
    "pih_bekas": ["pih", "bekas jerawat hitam", "bekas hitam", "noda cokelat"],
    "pie_bekas": ["pie", "bekas jerawat merah", "bekas kemerahan jerawat", "merah pasca"],
    "bopeng_scar": ["bopeng jerawat", "bopeng", "scar atrofi", "scar hipertrofik", "keloid"],
    "iritasi_peradangan": ["kemerahan wajah", "iritasi kulit", "peradangan kulit", "perih", "gatal", "inflamasi kronis", "kulit stres"],
    "dermatitis_eksim": ["dermatitis kontak", "dermatitis atopik", "dermatitis seboroik", "eksim", "perioral dermatitis"],
    "rosacea_vascular": ["rosacea", "couperose", "telangiektasia", "urat darah di wajah"],
    "tekstur_kasar": ["tekstur kulit kasar", "tekstur kulit tidak rata", "kulit menebal", "kulit menipis"],
    "sunburn": ["sunburn", "terbakar matahari", "gosong"],
    "penuaan_kerutan": ["penuaan dini", "kerutan halus", "garis halus", "kerutan dahi", "garis senyum", "garis marionette", "crow's feet"],
    "kendur_elastisitas": ["kulit kendur", "hilangnya elastisitas", "kehilangan kolagen", "kulit kendur akibat usia", "kulit kendur akibat penurunan berat badan"],
    "mata_area": ["lingkaran hitam bawah mata", "dark circle", "kantung mata", "mata panda", "mata sembap", "mata cekung"],
    "infeksi_bakteri": ["infeksi bakteri", "folikulitis", "impetigo", "hidradenitis suppurativa", "selulit", "cellulitis"],
    "infeksi_jamur_virus": ["infeksi jamur", "infeksi virus", "fungal acne", "herpes simpleks", "kutil", "molluscum contagiosum", "demodicosis"],
    "pertumbuhan_kulit": ["keratosis pilaris", "kulit ayam", "skin tag", "tahi lalat", "nevus", "angioma", "hemangioma", "granuloma"],
    "kanker_pra_kanker": ["keratosis aktinik", "karsinoma sel basal", "karsinoma sel skuamosa", "melanoma", "kanker kulit", "tahi lalat atipikal"],
    "autoimun_wajah": ["lupus kutaneus", "psoriasis wajah"],
    "skin_barrier_mikrobioma": ["skin barrier rusak", "skin barrier lemah", "ketidakseimbangan mikrobioma"],
    "urutan": ["urutan", "tahapan", "layering", "cara pakai", "langkah"],
    "cleansing": ["double cleanse", "double cleansing", "micellar", "cleansing balm"],
    "sunscreen": ["sunscreen", "sunblock", "tabir surya", "spf"],
    "moisturizer": ["moisturizer", "pelembab"]
}

# ===================================================================================================
# DATABASE SOLUSI: KANDUNGAN AKTIF & CARA PAKAI (SUPER PADAT & RELEVAN)
# ===================================================================================================
DATABASE_JAWABAN = {
    "jerawat_aktif": "Solusi jerawat aktif & bruntusan: Gunakan Salicylic Acid (BHA) 2% atau Acne Patch. Cara pakai: Oleskan serum BHA ke seluruh wajah atau totolkan setelah moisturizer pada malam hari harian.",
    "jerawat_parah": "Solusi jerawat batu, kistik, & hormonal: Gunakan Benzoyl Peroxide 5% atau Clindamycin gel. Cara pakai: Totolkan tipis-tipis hanya pada area jerawat yang meradang setelah pelembab di malam hari.",
    "komedo_hitam": "Solusi komedo hitam & sebaceous filaments: Gunakan Exfoliating Serum mengandung BHA 2% dan Clay Mask Kaolin. Cara pakai: Gunakan serum BHA 3 kali seminggu pada malam hari. Clay mask dipakai 10 menit lalu bilas seminggu sekali.",
    "komedo_putih": "Solusi komedo putih & white bumps: Gunakan AHA (Glycolic Acid) atau Lactic Acid serum. Cara pakai: Aplikasikan serum AHA 2-3 kali seminggu pada malam hari setelah mencuci muka untuk membuka sumbatan pori.",
    "milia_syringoma": "Solusi milia & sebaceous hyperplasia: Gunakan serum Retinol 0.5% - 1%. Cara pakai: Oleskan serum retinol secara tipis pada malam hari 2-3 kali seminggu. Kasus syringoma/xanthelasma memerlukan tindakan laser/kauter dokter.",
    "pori_tersumbat": "Solusi pori-pori tersumbat & besar: Gunakan serum Salicylic Acid (BHA) dan Niacinamide 10%. Cara pakai: Serum BHA digunakan malam hari untuk membersihkan dalam pori, Niacinamide digunakan pagi hari untuk mengontrol minyak.",
    "kulit_berminyak": "Solusi kulit berminyak berlebih: Gunakan Pembersih Wajah Gel (Low pH) dan Pelembab Gel mengandung Zinc PCA. Cara pakai: Aplikasikan pelembab gel tipis-tipis secara rutin setiap pagi dan malam hari setelah cuci muka.",
    "kulit_kering": "Solusi kulit sangat kering & mengelupas: Gunakan Moisturizer Krim mengandung Ceramide, Shea Butter, dan Vitamin E. Cara pakai: Oleskan pelembab bertekstur krim tebal pagi dan malam hari saat kulit masih setengah basah.",
    "kulit_dehidrasi": "Solusi kulit dehidrasi & ketarik: Gunakan Hydrating Toner mengandung Hyaluronic Acid atau Polyglutamic Acid. Cara pakai: Tepuk-tepuk toner hidrasi sebanyak 2-3 lapis sesaat setelah cuci muka sebelum pelembab.",
    "kulit_kombinasi": "Solusi kulit kombinasi: Gunakan metode Zoning Skincare. Cara pakai: Aplikasikan Moisturizer Gel di area T-zone yang berminyak, dan Moisturizer Krim tebal di area U-zone (pipi) yang kering.",
    "kulit_sensitif_reaktif": "Solusi kulit sensitif & reaktif: Gunakan produk berlabel Hypoallergenic bebas pewangi yang mengandung Allantoin atau Calendula. Cara pakai: Gunakan sebagai pelindung harian pagi dan malam.",
    "kusam_cahaya": "Solusi kulit kusam & lelah: Gunakan serum Vitamin C di pagi hari dan Fermented Ingredient (Galactomyces) di malam hari. Cara pakai: Teteskan Vitamin C sebelum sunscreen pagi, gunakan essence Galactomyces setelah cuci muka malam.",
    "pigmentasi_flek": "Solusi flek hitam, melasma, & sunspot: Gunakan serum Tranexamic Acid, Alpha Arbutin 2%, dan Cysteamine. Cara pakai: Oleskan serum pagi dan malam, dilanjutkan wajib menggunakan Sunscreen minimal SPF 40 di siang hari.",
    "hipopigmentasi_vitiligo": "Solusi kehilangan pigmen melanosit / vitiligo: Tidak bisa disembuhkan dengan skincare kosmetik biasa. Rekomendasi tindakan: Segera periksakan ke dokter spesialis kulit untuk terapia topikal Kortikosteroid kuat atau Fototerapi.",
    "pih_bekas": "Solusi bekas jerawat hitam (PIH): Gunakan serum Niacinamide 10% kombinasikan dengan eksfoliasi AHA. Cara pakai: Niacinamide dipakai rutin tiap pagi dan malam, serum AHA digunakan 2 malam sekali.",
    "pie_bekas": "Solusi bekas jerawat merah (PIE): Gunakan serum Azelaic Acid 10% atau Centella Asiatica (Cica). Cara pakai: Oleskan serum secara merata ke area bekas kemerahan pada pagi dan malam hari sebelum pelembab.",
    "bopeng_scar": "Solusi bopeng, scar, & keloid: Tidak bisa diperbaiki menggunakan produk skincare oles. Rekomendasi tindakan: Konsultasi dengan dokter untuk tindakan medis klinik seperti Subcisi, Laser CO2 Fractional, atau injeksi Keloid.",
    "iritasi_peradangan": "Solusi kulit iritasi, perih, & inflamasi: Gunakan Soothing Cream mengandung Panthenol (Vitamin B5) atau Madecassoside. Cara pakai: Oleskan ke area kulit yang stres/perih. Stop sementara semua produk eksfoliasi dan retinol.",
    "dermatitis_eksim": "Solusi dermatitis & eksim wajah: Gunakan Pelembab khusus atopi mengandung Colloidal Oatmeal dan Ceramide NP. Cara pakai: Oleskan tebal di area eksim yang kering/gatal. Jika radang parah wajib salep resep dokter.",
    "rosacea_vascular": "Solusi rosacea & urat merah (telangiektasia): Gunakan Azelaic Acid 10% atau serum Green Tea (EGCG) bebas alkohol. Cara pakai: Oleskan tipis pada pagi dan malam hari untuk meredakan kemerahan pembuluh darah.",
    "tekstur_kasar": "Solusi tekstur kulit kasar & menebal: Gunakan Exfoliating Toner mengandung AHA Lactic Acid atau PHA (Gluconolactone). Cara pakai: Tuang ke kapas, usap lembut ke wajah 3 kali seminggu pada malam hari.",
    "sunburn": "Solusi kulit terbakar matahari (Sunburn): Gunakan Pure Aloe Vera Gel atau Cucumber Extract. Cara pakai: Dinginkan gel di kulkas, lalu oleskan tebal ke area wajah yang terbakar matahari untuk meredakan efek panas.",
    "penuaan_kerutan": "Solusi kerutan halus & garis senyum: Gunakan serum Retinol 1% dan Peptide Serum. Cara pakai: Serum Peptide digunakan tiap pagi sebelum pelembab. Serum Retinol digunakan khusus malam hari 2-3 kali seminggu.",
    "kendur_elastisitas": "Solusi kulit kendur & kehilangan kolagen: Gunakan serum Bakuchiol, Collagen serum, atau Retinoid. Cara pakai: Gunakan serum Bakuchiol pagi hari, dan gunakan serum Retinol/Retinoid pada malam hari secara konsisten.",
    "mata_area": "Solusi dark circle & kantung mata: Gunakan Eye Cream mengandung Kafein (Caffeine) atau Acetyl Hexapeptide. Cara pakai: Oleskan seukuran biji kacang hijau, tepuk-tepuk lembut menggunakan jari manis di area mata setiap malam.",
    "infeksi_bakteri": "Solusi infeksi bakteri, folikulitis, & impetigo: Memerlukan penanganan antiseptik atau antibiotik topikal. Rekomendasi tindakan: Gunakan salep antibiotik (seperti Mupirocin atau Fusidic Acid) sesuai instruksi dan resep dokter.",
    "infeksi_jamur_virus": "Solusi infeksi jamur, kutil, & herpes wajah: Gunakan salep Ketoconazole (untuk jamur) atau krim Acyclovir (untuk virus). Cara pakai: Oleskan tipis pada area infeksi 3-4 kali sehari sesuai anjuran medis.",
    "pertumbuhan_kulit": "Solusi keratosis pilaris, skin tag, & tahi lalat: Untuk keratosis pilaris gunakan krim mengandung Urea 10%. Untuk skin tag dan tahi lalat tidak bisa lepas dengan skincare, harus tindakan bedah minor atau elektro-kauter dokter.",
    "kanker_pra_kanker": "Solusi melanoma, karsinoma, & benjolan atipikal: Skincare kosmetik tidak bisa mengobati kanker kulit. Rekomendasi tindakan: Wajib segera lakukan biopsi dan pemeriksaan bedah onkologi kulit dengan dokter spesialis.",
    "autoimun_wajah": "Solusi lupus kutaneus & psoriasis wajah: Fokus pada perbaikan sawar kulit yang rusak akibat autoimun. Cara pakai: Gunakan basic skincare super lembut tanpa kandungan aktif agresif, dan gunakan salep anti-inflamasi resep dokter.",
    "skin_barrier_mikrobioma": "Solusi skin barrier rusak & mikrobioma lemah: Gunakan serum Bifida Ferment Lysate, Ceramide NP, dan Squalane. Cara pakai: Oleskan serum bifida/ceramide pagi dan malam hari untuk membangun kembali benteng pertahanan kulit.",
    "urutan": "Urutan pakai skincare pagi: Facial Wash ➔ Toner ➔ Serum ➔ Moisturizer ➔ Sunscreen. Urutan malam: First Cleanser (Micellar) ➔ Facial Wash ➔ Exfoliating Toner/Serum Active ➔ Moisturizer.",
    "cleansing": "Solusi Double Cleansing: Gunakan Micellar Water (untuk kulit berminyak) atau Cleansing Balm (untuk makeup tebal). Cara pakai: Usap merata pada wajah kering untuk melarutkan sunscreen, lalu cuci muka pakai sabun.",
    "sunscreen": "Solusi perlindungan UV: Gunakan Sunscreen SPF 30-50 PA++++. Cara pakai: Aplikasikan sebanyak 2 jari penuh secara merata ke wajah dan leher pada pagi hari. Lakukan reapply setiap 3 jam sekali.",
    "moisturizer": "Solusi Pelembab: Gunakan Moisturizer Gel (kulit berminyak) or Moisturizer Krim (kulit kering). Cara pakai: Oleskan merata pada wajah setiap pagi dan malam setelah penggunaan serum selesai."
}

@chatbot_blueprint.route('/chat', methods=['POST'])
def chat_response():
    data = request.get_json() or {}
    pesan_user = data.get("message", "").lower()
    
    # ===============================================================================================
    # DETEKSI BERBAGAI POLA PERTANYAAN USER (INTENT DETECTION)
    # ===============================================================================================
    kata_tanya_jenis = ["jenis kulit apa", "tipe kulit apa", "kulit apa yang rentan", "jenis kulit mana", "tipe kulit mana"]
    is_tanya_jenis = any(kata in pesan_user for kata in kata_tanya_jenis)
    
    kata_tanya_penyebab = ["kenapa", "mengapa", "penyebab", "alasan", "sebab", "pemicu", "kok bisa"]
    is_tanya_penyebab = any(kata in pesan_user for kata in kata_tanya_penyebab)
    
    kata_tanya_solusi = ["bagaimana cara", "gimana cara", "cara mengatasi", "cara menyembuhkan", "cara menghilangkan", "solusi untuk"]
    is_tanya_solusi = any(kata in pesan_user for kata in kata_tanya_solusi)
    
    kata_tanya_ciri = ["ciri-ciri", "ciri ciri", "gejala", "tanda-tanda", "tanda tanda", "seperti apa rasanya"]
    is_tanya_ciri = any(kata in pesan_user for kata in kata_tanya_ciri)
    
    kata_tanya_waktu = ["berapa lama", "kapan hilang", "kapan kelihatan hasil", "durasi sembuh"]
    is_tanya_waktu = any(kata in pesan_user for kata in kata_tanya_waktu)
    
    solusi_ditemukan = []
    
    # Scanning kluster keyword yang cocok
    for kluster, daftar_kata in KAMUS_KEYWORDS.items():
        if any(kata in pesan_user for kata in daftar_kata):
            if kluster in DATABASE_JAWABAN:
                solusi_ditemukan.append(DATABASE_JAWABAN[kluster])
                
    if solusi_ditemukan:
        solusi_unik = list(dict.fromkeys(solusi_ditemukan))
        pengantar = ""
        
        # JIKA USER TANYA "JENIS KULIT APA YANG RENTAN..."
        if is_tanya_jenis:
            if "kusam" in pesan_user:
                pengantar = "Jenis kulit yang paling rentan kusam adalah tipe kulit kering (karena kurang kelembapan dan penumpukan sel kulit mati) serta kulit sangat berminyak (karena oksidasi sebum). "
            elif any(k in pesan_user for k in ["jerawat", "bruntusan", "komedo"]):
                pengantar = "Jenis kulit yang paling rentan berjerawat dan berkomedo adalah tipe kulit berminyak dan kulit kombinasi, karena produksi sebum berlebih yang menyumbat pori-pori. "
            elif any(k in pesan_user for k in ["sensitif", "iritasi", "perih", "merah"]):
                pengantar = "Jenis kulit yang rentan mengalami iritasi dan kemerahan adalah tipe kulit sensitif atau kulit yang kondisi skin barrier-nya sedang lemah. "
            else:
                pengantar = "Setiap tipe kulit memiliki risiko masalah yang berbeda-beda tergantung pada keseimbangan kadar air dan minyak wajah. "
            balasan = pengantar + "Berikut adalah rekomendasi penanganan kandungan aktif yang tepat:\n\n" + "\n\n".join(solusi_unik)
            
        # JIKA USER BERTANYA "KENAPA / PENYEBAB" (LOGIKA LEBIH SPESIFIK AGAR TIDAK MIRIP)
        elif is_tanya_penyebab:
            if any(k in pesan_user for k in ["jerawat", "bruntusan", "pms"]):
                pengantar = "Kemunculan jerawat (terutama saat PMS) umumnya dipicu oleh lonjakan hormon progesteron yang merangsang produksi kelenjar minyak secara berlebih, sehingga menyumbat pori-pori dan memicu peradangan bakteri. "
            elif "kusam" in pesan_user:
                pengantar = "Kulit menjadi kusam biasanya disebabkan oleh penumpukan sel kulit mati yang jarang dieksfoliasi, dehidrasi akibat kurangnya hidrasi, atau efek buruk paparan radikal bebas dan sinar UV matahari tanpa perlindungan sunscreen. "
            elif any(k in pesan_user for k in ["komedo", "pori"]):
                pengantar = "Masalah komedo dan pori tersumbat terjadi akibat minyak berlebih yang bercampur dengan kotoran sisa kosmetik atau debu yang mengeras di dalam saluran pori-pori kulit. "
            else:
                pengantar = "Kemunculan masalah tersebut umumnya dipicu oleh faktor internal seperti hormonal/stres, maupun eksternal seperti paparan sinar UV, debu polusi, atau ketidakcocokan formula produk. "
                
            balasan = pengantar + "Berikut adalah rekomendasi penanganan kandungan aktif yang tepat:\n\n" + "\n\n".join(solusi_unik)
            
        # JIKA USER BERTANYA "BAGAGAIMANA CARA MENGATASI"
        elif is_tanya_solusi:
            pengantar = "Untuk mengatasi masalah tersebut, Anda perlu fokus pada penggunaan bahan aktif target yang dikombinasikan dengan basic skincare yang menghidrasi secara konsisten. "
            balasan = pengantar + "\n\n" + "\n\n".join(solusi_unik)
            
        # JIKA USER BERTANYA "CIRI-CIRI / GEJALA"
        elif is_tanya_ciri:
            pengantar = "Ciri dan gejala masalah ini biasanya ditandai dengan perubahan tekstur permukaan kulit (kasar/bintil), perubahan warna (kemerahan/gelap), hingga rasa tidak nyaman seperti ketarik atau gatal. "
            balasan = pengantar + "Sebagai langkah penanganan awal, berikut kandungan aktif dan cara pakai yang disarankan:\n\n" + "\n\n".join(solusi_unik)
            
        # JIKA USER BERTANYA "BERAPA LAMA"
        elif is_tanya_waktu:
            pengantar = "Kecepatan regenerasi dan pemulihan kulit bervariasi, berkisar antara 2 hingga 6 minggu tergantung pada tingkat keparahan masalah kulit Anda. "
            balasan = pengantar + "Untuk hasil optimal, gunakan kandungan aktif berikut sesuai aturan pakai:\n\n" + "\n\n".join(solusi_unik)
            
        else:
            balasan = "\n\n".join(solusi_unik)
            
    else:
        balasan = (
            "Maaf, SkinAI tidak memiliki jawaban atau solusi kecocokan kandungan untuk keluhan tersebut. "
            "Silakan ketik ulang masalah kulit Anda menggunakan istilah yang lebih spesifik "
            "(seperti: jerawat kistik, komedo pasir, flek hitam, skin barrier rusak, kulit dehidrasi, atau kerutan dahi) "
            "agar sistem dapat menemukan rekomendasi bahan aktif dan cara pemakaiannya."
        )

    return jsonify({"reply": balasan})