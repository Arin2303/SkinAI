from flask import Blueprint, jsonify, session, request

# Blueprint disesuaikan agar seragam dengan pendaftaran di app.py
skincare_guide_blueprint = Blueprint('skincare_guide', __name__)

# FUNGSI PEMBANTU: Menentukan tipe kulit (Prioritas: URL > Session)
def get_skin_type_context():
    # 1. Coba ambil dari parameter URL (query string: ?type=...)
    tipe_kulit = request.args.get('type')
    
    # 2. Jika tidak ada di URL, ambil dari session
    if not tipe_kulit:
        tipe_kulit = session.get('skin_type')
        
    return tipe_kulit

# ===================================================================================================
# 1. ENDPOINT RUMUS RUTINITAS
# ===================================================================================================
@skincare_guide_blueprint.route('/get-rumus', methods=['GET'])
def get_rumus_data():
    tipe_kulit = get_skin_type_context()
    
    if not tipe_kulit:
        return jsonify({
            "status": "locked",
            "message": "Silakan lakukan pemindaian kulit terlebih dahulu untuk membuka fitur ini!"
        })
        
    response_data = {
        "status": "success",
        "skin_type": tipe_kulit,
        "urutan_pagi": "",
        "urutan_malam": "",
        "pagi": [],
        "malam": [],
        "mingguan": {}
    }
    
    # KONDISI UNTUK COMBINATION SKIN
    if "Combination" in tipe_kulit:
        response_data["urutan_pagi"] = "Cleanser → Toner → Serum → Pelembap Gel → Sunscreen"
        response_data["urutan_malam"] = "Micellar Water → Facial Wash → Serum Aktif → Ceramide Moisturizer"
        response_data["pagi"] = [
            {"step": "1", "item": "Gel Cleanser", "desc": "Membersihkan minyak subuh tanpa bikin pipi ketarik."},
            {"step": "2", "item": "Toner Hidrasi", "desc": "Menyeimbangkan pH kulit di seluruh area wajah."},
            {"step": "3", "item": "Serum Niacinamide", "desc": "Mengontrol sebum T-zone sekaligus mencerahkan."},
            {"step": "4", "item": "Moisturizer Gel", "desc": "Pelembap berbahan dasar air yang ringan."},
            {"step": "5", "item": "Sunscreen SPF 50", "desc": "Wajib! Proteksi agar bekas jerawat tidak menghitam."}
        ]
        response_data["malam"] = [
            {"step": "1", "item": "Micellar Water", "desc": "Double cleansing untuk angkat sisa sunscreen & debu."},
            {"step": "2", "item": "Facial Wash Gel", "desc": "Membersihkan sisa residu makeup/kotoran."},
            {"step": "3", "item": "Serum/Toner Aktif", "desc": "Menggunakan bahan aktif sesuai jadwal mingguan."},
            {"step": "4", "item": "Ceramide Moisturizer", "desc": "Mengunci kelembapan dan memperbaiki skin barrier saat tidur."}
        ]
        response_data["mingguan"] = {
            "Senin": {"tipe": "Eksfoliasi", "detail": "Gunakan Toner/Serum BHA untuk membersihkan komedo T-Zone."},
            "Selasa": {"tipe": "Hidrasi & Pemulihan", "detail": "Gunakan Serum Hyaluronic / Ceramide untuk menenangakn kulit."},
            "Rabu": {"tipe": "Hidrasi & Pemulihan", "detail": "Fokus hidrasi penuh di area U-zone (pipi)."},
            "Kamis": {"tipe": "Eksfoliasi", "detail": "Gunakan BHA kembali untuk *deep cleansing* pori-pori."},
            "Jumat": {"tipe": "Hidrasi & Pemulihan", "detail": "Gunakan Serum Niacinamide + Moisturizer penenang."},
            "Sabtu": {"tipe": "Hidrasi & Pemulihan", "detail": "Malam pemulihan skin barrier."},
            "Minggu": {"tipe": "Hidrasi & Pemulihan", "detail": "Istirahatkan kulit dengan basic skincare (tanpa bahan aktif berat)."}
        }

    # KONDISI UNTUK OILY SKIN
    elif "Oily" in tipe_kulit:
        response_data["urutan_pagi"] = "Acne Wash → BHA Toner → Serum Zinc → Oil-Free Gel → Matte Sunscreen"
        response_data["urutan_malam"] = "Micellar Matte → Deep Cleanser → Serum Aktif (Retinol/BHA) → Water Gel"
        response_data["pagi"] = [
            {"step": "1", "item": "Salicylic Acid Cleanser", "desc": "Mengurangi tumpukan minyak berlebih sejak pagi."},
            {"step": "2", "item": "BHA Toner Light", "desc": "Mempersiapkan pori-pori agar tidak mudah tersumbat."},
            {"step": "3", "item": "Zinc + Niacinamide Serum", "desc": "Menekan kilap minyak dan meredakan kemerahan."},
            {"step": "4", "item": "Oil-Free Gel Cream", "desc": "Melembapkan tanpa menambah sumbatan minyak baru."},
            {"step": "5", "item": "Matte Sunscreen SPF 50", "desc": "Proteksi sinar UV dengan hasil akhir bebas kilap."}
        ]
        response_data["malam"] = [
            {"step": "1", "item": "Cleansing Water / Matte Micellar", "desc": "Mengangkat kotoran penyumbat pori secara menyeluruh."},
            {"step": "2", "item": "Deep Facial Wash Gel", "desc": "Pembersihan sisa sebum jauh ke dalam pori."},
            {"step": "3", "item": "Serum Retinol / BHA", "desc": "Regenerasi kulit dan mencegah pembentukan jerawat."},
            {"step": "4", "item": "Light Water Gel Night", "desc": "Hidrasi ringan sepanjang tidur malam."}
        ]
        response_data["mingguan"] = {
            "Senin": {"tipe": "Eksfoliasi Pori", "detail": "Gunakan serum BHA 2% ke seluruh wajah."},
            "Selasa": {"tipe": "Anti-Aging & Acne Care", "detail": "Gunakan Retinol tipis-tipis untuk kontrol sebum jangka panjang."},
            "Rabu": {"tipe": "Sooting Hidrasi", "detail": "Gunakan Centella Asiatica Serum untuk menenangkan pori."},
            "Kamis": {"tipe": "Eksfoliasi Pori", "detail": "Eksfoliasi ulang dengan toner BHA."},
            "Jumat": {"tipe": "Anti-Aging & Acne Care", "detail": "Aplikasi Retinol malam kedua."},
            "Sabtu": {"tipe": "Deep Clay Mask", "detail": "Gunakan masker lumpur (Clay Mask) 10 menit untuk menyedot sisa minyak."},
            "Minggu": {"tipe": "Calming Night", "detail": "Gunakan basic skincare penenang barrier kulit."}
        }

    # KONDISI UNTUK DRY SKIN
    elif "Dry" in tipe_kulit:
        response_data["urutan_pagi"] = "Milk Wash → Milky Toner → Hyaluronic Serum → Rich Cream → Dewy Sunscreen"
        response_data["urutan_malam"] = "Cleansing Balm → Gentle Wash → Barrier Serum → Intensive Cream"
        response_data["pagi"] = [
            {"step": "1", "item": "Non-Foaming Milk Cleanser", "desc": "Membersihkan sisa tidur dengan sangat lembut tanpa busa."},
            {"step": "2", "item": "Milky Hydrating Toner", "desc": "Memberikan lapisan hidrasi awal yang kaya air."},
            {"step": "3", "item": "Hyaluronic Acid Serum", "desc": "Mengikat kadar air agar kulit tidak bersisik atau pecah-pecah."},
            {"step": "4", "item": "Rich Ceramides Cream", "desc": "Mengunci kelembapan dengan pelembab bertekstur krim tebal."},
            {"step": "5", "item": "Dewy Glow Sunscreen", "desc": "Proteksi UV yang memberi efek lembap sepanjang hari."}
        ]
        response_data["malam"] = [
            {"step": "1", "item": "Cleansing Balm / Oil", "desc": "Melarutkan kotoran tanpa mengikis minyak alami wajah."},
            {"step": "2", "item": "Hydrating Gentle Wash", "desc": "Sabun wajah pH seimbang yang tidak bikin kulit ketarik."},
            {"step": "3", "item": "Nourishing Night Serum", "desc": "Serum barrier repair atau PHA ringan untuk eksfoliasi aman."},
            {"step": "4", "item": "Intensive Barrier Cream", "desc": "Krim malam tebal untuk memperbaiki kulit mengelupas saat tidur."}
        ]
        response_data["mingguan"] = {
            "Senin": {"tipe": "Mild Peeling", "detail": "Gunakan PHA serum yang ramah dan lembut untuk kulit kering."},
            "Selasa": {"tipe": "Deep Moisture", "detail": "Gunakan Sleeping Mask hidrasi setelah pelembab utama."},
            "Rabu": {"tipe": "Skin Barrier Lock", "detail": "Fokus hidrasi berlapis (Metode 7-skin menggunakan toner)."},
            "Kamis": {"tipe": "Mild Peeling", "detail": "Eksfoliasi ringan kedua dengan PHA."},
            "Jumat": {"tipe": "Deep Moisture", "detail": "Gunakan sheet mask varian alpukat/madu selama 15 menit."},
            "Sabtu": {"tipe": "Barrier Repair", "detail": "Gunakan serum Ceramide dosis penuh."},
            "Minggu": {"tipe": "Total Rest", "detail": "Istirahatkan kulit total hanya dengan pelembab tebal."}
        }

    # KONDISI UNTUK NORMAL SKIN
    else:
        response_data["urutan_pagi"] = "Gentle Foam → Brightening Toner → Vitamin C → Light Cream → Sunscreen Gel"
        response_data["urutan_malam"] = "Micellar Classic → Regular Wash → Peptide Serum → Moisturizing Gel"
        response_data["pagi"] = [
            {"step": "1", "item": "Gentle Foam Cleanser", "desc": "Menyegarkan wajah dengan busa lembut seimbang."},
            {"step": "2", "item": "Brightening Toner", "desc": "Menjaga kesegaran dan mempersiapkan penyerapan serum."},
            {"step": "3", "item": "Vitamin C Serum", "desc": "Antioksidan kuat untuk mencerahkan dan menangkal radikal bebas."},
            {"step": "4", "item": "Daily Light Moisturizer", "desc": "Pelembab standar untuk menjaga kestabilan air dan minyak."},
            {"step": "5", "item": "Sunscreen Serum SPF 30+", "desc": "Proteksi harian wajib agar warna kulit merata."}
        ]
        response_data["malam"] = [
            {"step": "1", "item": "Micellar Water Classic", "desc": "Membersihkan debu polusi harian dengan praktis."},
            {"step": "2", "item": "Regular Facial Wash", "desc": "Memastikan wajah bersih sempurna sebelum istirahat."},
            {"step": "3", "item": "Peptide / Brightening Serum", "desc": "Membantu elastisitas kulit dan mempertahankan kilau alami."},
            {"step": "4", "item": "Moisturizing Cream-Gel", "desc": "Menjaga kekenyalan tekstur wajah hingga esok pagi."}
        ]
        response_data["mingguan"] = {
            "Senin": {"tipe": "Brightening Care", "detail": "Gunakan serum Niacinamide konsentrasi standard harian."},
            "Selasa": {"tipe": "Mild Exfoliation", "detail": "Gunakan toner AHA/BHA ringan untuk meratakan tekstur kulit."},
            "Rabu": {"tipe": "Glow Maintenance", "detail": "Gunakan Sheet Mask Vitamin C/Glow variant."},
            "Kamis": {"tipe": "Brightening Care", "detail": "Fokus pada serum pencegah kekusaman."},
            "Jumat": {"tipe": "Mild Exfoliation", "detail": "Eksfoliasi ringan berkala mingguan."},
            "Sabtu": {"tipe": "Hydration Boost", "detail": "Gunakan serum Hyaluronic Acid untuk hidrasi ekstra."},
            "Minggu": {"tipe": "Basic Maintenance", "detail": "Gunakan routine dasar pelindung kelembapan alami."}
        }

    return jsonify(response_data)


# ===================================================================================================
# 2. ENDPOINT REKOMENDASI PRODUK
# ===================================================================================================
@skincare_guide_blueprint.route('/get-rekomendasi', methods=['GET'])
def get_rekomendasi_data():
    tipe_kulit = get_skin_type_context()
    
    if not tipe_kulit:
        return jsonify({
            "status": "locked",
            "message": "Silakan lakukan pemindaian kulit terlebih dahulu untuk membuka fitur ini!"
        })
    
    response_data = {
        "status": "success",
        "skin_type": tipe_kulit,
        "produk": []
    }
    
    if "Combination" in tipe_kulit:
        response_data["produk"] = [
            {"icon": "🧼", "kategori": "Pembersih Wajah (Face Wash)", "tekstur": "Gel Rendah Busa", "penjelasan": "Pilihlah pembersih bertekstur gel transparan yang bebas dari kandungan detergen berlebih (SLS/SLES)."},
            {"icon": "💧", "kategori": "Toner Penghidrasi (Hydrating Toner)", "tekstur": "Cair / Ringan (*Water-based*)", "penjelasan": "Cari toner cair yang kaya akan Hyaluronic Acid atau Centella Asiatica."},
            {"icon": "🧪", "kategori": "Serum Kontrol Sebum & Sawar Kulit", "tekstur": "Cair Ringan", "penjelasan": "Pilih serum Niacinamide 2%-5% untuk kontrol minyak dan perbaikan skin barrier."},
            {"icon": "🍦", "kategori": "Pelembap (Moisturizer)", "tekstur": "Gel-Cream Ringan", "penjelasan": "Tekstur Gel-Cream memberikan sensasi dingin dan mengunci kelembapan."},
            {"icon": "☀️", "kategori": "Tabir Surya (Sunscreen)", "tekstur": "Cair Gel (*Water-based*)", "penjelasan": "Gunakan sunscreen berbasis air yang ringan dan Non-Comedogenic."}
        ]
        
    elif "Oily" in tipe_kulit:
        response_data["produk"] = [
            {"icon": "🧼", "kategori": "Pembersih Wajah (Face Wash)", "tekstur": "Deep Gel / Foam Low pH", "penjelasan": "Gunakan pembersih dengan kandungan Salicylic Acid (BHA) untuk membersihkan sumbatan sebum."},
            {"icon": "💧", "kategori": "Toner Pemurni (Purifying Toner)", "tekstur": "Sangat Cair", "penjelasan": "Gunakan toner yang mengandung Zinc PCA atau Tea Tree untuk menenangkan kelenjar minyak."},
            {"icon": "🧪", "kategori": "Serum Pengontrol Minyak", "tekstur": "Lightweight Liquid", "penjelasan": "Kombinasi Niacinamide tinggi (5-10%) dengan Zinc efektif menahan produksi minyak."},
            {"icon": "🍦", "kategori": "Pelembap (Moisturizer)", "tekstur": "Water-Gel / Aqua Cream", "penjelasan": "Mutlak gunakan pelembab berbentuk gel bening murni (oil-free)."},
            {"icon": "☀️", "kategori": "Tabir Surya (Sunscreen)", "tekstur": "Fluid / Matte Finish", "penjelasan": "Pilih sunscreen berlabel 'Oil Control' atau 'Matte Look'."}
        ]

    elif "Dry" in tipe_kulit:
        response_data["produk"] = [
            {"icon": "🧼", "kategori": "Pembersih Wajah (Face Wash)", "tekstur": "Milk / Cream Cleanser", "penjelasan": "Gunakan sabun pembersih bertekstur susu atau krim yang diperkaya Vitamin E."},
            {"icon": "💧", "kategori": "Toner Penghidrasi Utama", "tekstur": "Kental & Licin (*Rich*)", "penjelasan": "Pilih toner essence dengan kandungan Panthenol atau Amino Acid."},
            {"icon": "🧪", "kategori": "Serum Perbaikan Sawar Kulit", "tekstur": "Emulsi Lembut", "penjelasan": "Gunakan serum kaya Ceramides, Squalane, atau Asam Hialuronat."},
            {"icon": "🍦", "kategori": "Pelembap (Moisturizer)", "tekstur": "Rich Cream / Balm-Cream", "penjelasan": "Gunakan pelembab berbasis krim padat untuk mengunci hidrasi secara total."},
            {"icon": "☀️", "kategori": "Tabir Surya (Sunscreen)", "tekstur": "Cream Hydrating Base", "penjelasan": "Pilih sunscreen dengan efek 'Dewy Glow' untuk perlindungan dan kelembapan."}
        ]

    else:
        response_data["produk"] = [
            {"icon": "🧼", "kategori": "Pembersih Wajah (Face Wash)", "tekstur": "Gentle Balancing Foam", "penjelasan": "Gunakan sabun wajah lembut untuk mengangkat debu permukaan."},
            {"icon": "💧", "kategori": "Toner Penyegar", "tekstur": "Cair Ringan", "penjelasan": "Gunakan hydrating toner ringan yang mengandung Aloe Vera atau Rose Water."},
            {"icon": "🧪", "kategori": "Serum Antioksidan", "tekstur": "Cair Ringan", "penjelasan": "Pilih serum Vitamin C atau Alpha Arbutin untuk menjaga skin tone tetap cerah."},
            {"icon": "🍦", "kategori": "Pelembap (Moisturizer)", "tekstur": "Light Cream / Lotion", "penjelasan": "Gunakan pelembab losion atau krim ringan agar senantiasa kenyal."},
            {"icon": "☀️", "kategori": "Tabir Surya (Sunscreen)", "tekstur": "Sunscreen Gel", "penjelasan": "Gunakan varian sunscreen gel atau essence minimal SPF 30 PA+++."}
        ]
        
    return jsonify(response_data)