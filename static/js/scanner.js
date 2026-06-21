// static/js/scanner.js

const video = document.getElementById("camera");
const canvas = document.getElementById("canvas");
const captureButton = document.getElementById("capture"); 
const scoresList = document.getElementById("scores-list");
const recBox = document.getElementById("recommendation-box");
const historyTableBody = document.getElementById("history-table-body");
const laser = document.getElementById("scanner-laser");

// Elemen tambahan untuk fitur Upload, Freeze Foto & Kontrol Efek Visual
const cameraWrapper = document.querySelector(".camera-wrapper");
const btnChooseFile = document.getElementById("btn-choose-file");
const fileInput = document.getElementById("file-input");
const photoFrozen = document.getElementById("photo-frozen"); 

let skinChart = null;
let isFrozen = false; 

// Menyimpan data scan kamera sementara di latar belakang (hidden)
let skorKameraLatarBelakang = null;

// KODE BARU: Mengatur rasio kamera fleksibel untuk HP & Laptop
const constraints = {
    video: {
        width: { ideal: 640 },
        height: { ideal: 480 },
        facingMode: "user", // Memastikan menggunakan kamera depan pada HP
        aspectRatio: { ideal: video.clientWidth / video.clientHeight } // Mengikuti rasio wadah CSS
    },
    audio: false
};

navigator.mediaDevices.getUserMedia(constraints)
.then(stream => { 
    video.srcObject = stream; 
    // Sinkronisasi ukuran canvas secara dinamis saat video mulai berjalan
    video.onloadedmetadata = () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const context = canvas.getContext("2d");
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.save();
        context.translate(canvas.width, 0);
        context.scale(-1, 1);
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        context.restore();
    };
})
.catch(error => {
    console.error("Kamera tidak bisa diakses:", error);
    scoresList.innerHTML = "<li style='color: #d9534f; font-weight:bold;'>⚠️ Akses kamera ditolak browser.</li>";
});

// Fungsi pembuat/pembaru grafik Chart
function updateChart(oily, dry, normal, combi, skipSave = false) {
    const ctx = document.getElementById('skinChart').getContext('2d');
    if (skinChart !== null) { skinChart.destroy(); }
    skinChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Oily', 'Dry', 'Normal', 'Combination'],
            datasets: [{
                data: [oily, dry, normal, combi],
                backgroundColor: [
                    'rgba(112, 130, 56, 0.7)',  /* Sage Green Transparan */
                    'rgba(91, 192, 235, 0.7)',  
                    'rgba(86, 204, 157, 0.7)',  
                    'rgba(194, 125, 102, 0.7)'  /* Clay Accent Transparan */
                ],
                borderColor: ['#708238', '#5bc0eb', '#56cc9d', '#c27d66'], 
                borderWidth: 1.5,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            scales: { 
                y: { beginAtZero: true, max: 100, grid: { color: 'rgba(0,0,0,0.03)' } },
                x: { grid: { display: false } }
            },
            plugins: { legend: { display: false } }
        }
    });

    if (!skipSave) {
        sessionStorage.setItem("saved_chart_data", JSON.stringify({ oily, dry, normal, combi }));
    }
}

// FUNGSI LOG HISTORY (VERSI TERUPDATE DENGAN LINK AKSES)
function addHistoryLog(tipe, oily, dry, normal, combi, customTime = null) {
    const emptyRow = document.getElementById("empty-history");
    if (emptyRow) { emptyRow.remove(); }

    const waktuString = customTime ? customTime : new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

    const existingRows = historyTableBody.querySelectorAll("tr");
    let isDuplicate = false;
    existingRows.forEach(row => {
        if (row.innerHTML.includes(waktuString) && row.innerHTML.includes(tipe)) {
            isDuplicate = true;
        }
    });
    if (isDuplicate) return;

    const row = document.createElement("tr");
    
    // Perubahan ada di baris variabel 'row.innerHTML' di bawah ini:
    row.innerHTML = `
        <td style="padding: 12px; color: #6b7c74;">${waktuString}</td>
        <td style="padding: 12px;">
            <div style="font-weight: 600; color: #c27d66; margin-bottom: 8px;">${tipe}</div>
            <div style="display: flex; gap: 6px;">
                <a href="/rekomendasi-produk?skin_type=${encodeURIComponent(tipe)}" 
                    style="background: #708238; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">
                    Produk
                </a>
                <a href="/rumus-skincare?skin_type=${encodeURIComponent(tipe)}" 
                    style="background: #c27d66; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">
                    Rutinitas
                </a>
            </div>
        </td>
        <td style="padding: 12px;">${oily}%</td>
        <td style="padding: 12px;">${dry}%</td>
        <td style="padding: 12px;">${normal}%</td>
        <td style="padding: 12px;">${combi}%</td>
    `;
    
    historyTableBody.insertBefore(row, historyTableBody.firstChild);
    
    const currentRows = historyTableBody.querySelectorAll("tr");
    if (currentRows.length > 5) {
        historyTableBody.removeChild(historyTableBody.lastChild); 
    }

    if (!customTime) {
        let pemindaianLokal = JSON.parse(sessionStorage.getItem("jurnal_pemindaian_list")) || [];
        pemindaianLokal.unshift({
            waktu: waktuString,
            tipe: tipe,
            oily: oily,
            dry: dry,
            normal: normal,
            combi: combi
        });
        if (pemindaianLokal.length > 5) {
            pemindaianLokal = pemindaianLokal.slice(0, 5);
        }
        sessionStorage.setItem("jurnal_pemindaian_list", JSON.stringify(pemindaianLokal));
    }
}

if (!sessionStorage.getItem("saved_chart_data")) {
    updateChart(0, 0, 0, 0, true);
}

function resetCameraToLive() {
    photoFrozen.style.display = "none";
    video.style.display = "block";
    cameraWrapper.classList.remove("hide-oval");
    cameraWrapper.classList.remove("scanning-active");
    if (video.paused) video.play();
    
    captureButton.innerText = "Mulai Analisis Kulit";
    captureButton.style.background = "#708238"; 
    isFrozen = false;
    
    scoresList.innerHTML = "";
    
    sessionStorage.removeItem("saved_chart_data");
    sessionStorage.removeItem("saved_rec_box");
    sessionStorage.removeItem("saved_quiz_container");
    sessionStorage.removeItem("saved_final_skin_type");
    sessionStorage.removeItem("saved_frozen_photo");
    
    if (recBox) recBox.innerHTML = "";
    updateChart(0, 0, 0, 0, true);

    const daftarJurnalLokal = sessionStorage.getItem("jurnal_pemindaian_list");
    if (daftarJurnalLokal) {
        historyTableBody.innerHTML = "";
        const listData = JSON.parse(daftarJurnalLokal);
        for (let i = listData.length - 1; i >= 0; i--) {
            const item = listData[i];
            addHistoryLog(item.tipe, item.oily, item.dry, item.normal, item.combi, item.waktu);
        }
    } else {
        historyTableBody.innerHTML = `<tr id="empty-history"><td colspan="6" style="padding: 20px; text-align: center; color: #9bb0a5;">Belum ada data pemindaian hari ini.</td></tr>`;
    }

    const quizContainer = document.getElementById("quiz-container");
    if (quizContainer) {
        quizContainer.style.borderColor = "#e3e8e5"; 
        quizContainer.innerHTML = `
            <h3 style="color: #c27d66; margin-top: 0; font-weight: 700; text-align: center;">🎯 Langkah Validasi Akhir</h3>
            <p id="quiz-intro-text" style="font-size: 13.5px; color: #6b7c74; text-align: center; line-height: 1.6; margin: 0 auto; max-width: 320px;">
                Silakan lakukan pemindaian wajah atau unggah foto terlebih dahulu di samping agar sistem AI dapat merekam matriks visual awal kulit Anda.
            </p>
            <div id="quiz-content" style="display: none;">
                <h4 id="quiz-question" style="color: #2c3e35; margin-bottom: 18px; line-height: 1.5; font-weight: 600;">Memuat pertanyaan...</h4>
                <div id="quiz-options" style="display: flex; flex-direction: column; gap: 10px;"></div>
            </div>
            <div id="quiz-footer" style="margin-top: 20px; display: none; justify-content: space-between; align-items: center; font-size: 12px; color: #6b7c74;">
                <span id="quiz-progress">Pertanyaan 1 dari 5</span>
            </div>
        `;
    }
}

function startScanningAnimation() {
    cameraWrapper.classList.add("scanning-active"); 
    cameraWrapper.classList.remove("hide-oval"); 
    scoresList.innerHTML = "<li style='color:#c27d66; font-weight:600;'>⏳ AI sedang menganalisis matriks jaringan kulit...</li>"; 
}

function resetQuizUI() {
    const quizContainer = document.getElementById("quiz-container");
    if (quizContainer) {
        quizContainer.style.borderColor = "#708238"; 
        quizContainer.innerHTML = `
            <h3 style="color: #c27d66; margin-top: 0; font-weight: 700; text-align: center;">🎯 Langkah Validasi Akhir</h3>
            <p id="quiz-intro-text" style="font-size: 13px; color: #6b7c74; text-align: center; margin-bottom: 20px; display: none;">
                Matriks visual kamera berhasil disimpan! Sempurnakan analisis dengan menjawab 5 pertanyaan singkat ini agar hasil akurat & personalisasi formula tepat.
            </p>
            <div id="quiz-content" style="display: block;">
                <h4 id="quiz-question" style="color: #2c3e35; margin-bottom: 15px; line-height: 1.4; font-weight: 600;">Memuat pertanyaan...</h4>
                <div id="quiz-options" style="display: flex; flex-direction: column; gap: 10px;"></div>
            </div>
            <div id="quiz-footer" style="margin-top: 20px; display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #6b7c74;">
                <span id="quiz-progress">Pertanyaan 1 dari 5</span>
            </div>
        `;
    }
}

function stopScanningAndHideOval() {
    cameraWrapper.classList.remove("scanning-active");
    cameraWrapper.classList.add("hide-oval");
}

// PROSES PENGAMBILAN CITRA KAMERA
if (captureButton) {
    captureButton.addEventListener("click", function() {
        if (isFrozen) {
            resetCameraToLive();
            return;
        }

        startScanningAnimation();
        
        const context = canvas.getContext("2d");
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.save();
        context.translate(canvas.width, 0);
        context.scale(-1, 1);
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        context.restore();
        
        const imageData = canvas.toDataURL("image/png");

        photoFrozen.src = imageData;
        photoFrozen.style.display = "block";
        video.style.display = "none"; 
        photoFrozen.style.transform = "none"; 
        isFrozen = true;

        fetch("/api/scanner/upload", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: imageData, answers: [] }) 
        })
        .then(response => response.json())
        .then(data => {
            stopScanningAndHideOval();

            if(data.status === "success") {
                const tipeUtama = data.tipe_terdeteksi;
                if (tipeUtama.includes("Gagal") || tipeUtama.includes("Tidak Pas") || tipeUtama.includes("Kurang Pas") || tipeUtama.includes("Terhalang")) {
                    scoresList.innerHTML = `<li style="color: #d9534f; font-weight: 600; background:#fff2f2; padding:10px; border-radius:8px;">❌ Analisis Kamera Ditolak</li>`;
                    recBox.innerHTML = `<div style="color: #d9534f; margin-top: 15px; font-size: 13px; background: #fff5f5; padding: 15px; border-radius: 12px; border: 1px solid #ffe3e3; text-align:center;"><strong>Masalah:</strong> ${data.rekomendasi.tips}</div>`;
                    resetCameraToLive();
                } else {
                    scoresList.innerHTML = "<li style='color:#56cc9d; font-weight:600;'>✅ Struktur wajah terekam! Selesaikan kuesioner.</li>";
                    
                    skorKameraLatarBelakang = {
                        oily: parseInt(data.scores["Oily Skin"]),
                        dry: parseInt(data.scores["Dry Skin"]),
                        normal: parseInt(data.scores["Normal Skin"]),
                        combi: parseInt(data.scores["Combination Skin"]),
                        tipe_awal: tipeUtama
                    };

                    captureButton.innerText = "Reset Analisis";
                    captureButton.style.background = "#c27d66"; 
                    
                    pemicuKuisValidasi();
                }
            } else {
                scoresList.innerHTML = "<li style='color: red;'>⚠️ Gagal mendapatkan respons data AI.</li>";
                resetCameraToLive();
            }
        }
        )
        .catch(err => {
            stopScanningAndHideOval();
            resetCameraToLive();
            console.error(err);
            scoresList.innerHTML = "<li style='color: red;'>⚠️ Pemutusan koneksi server Flask.</li>";
        });
    });
}

// PROSES UNGGAH BERKAS FILE GALERI
if (btnChooseFile && fileInput) {
    btnChooseFile.addEventListener("click", function() {
        if (isFrozen) { resetCameraToLive(); }
        fileInput.click();
    });

    fileInput.addEventListener("change", function(e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function(event) {
            const img = new Image();
            img.onload = function() {
                startScanningAnimation();
                
                const context = canvas.getContext("2d");
                context.clearRect(0, 0, canvas.width, canvas.height);
                context.drawImage(img, 0, 0, canvas.width, canvas.height);
                const imageData = canvas.toDataURL("image/png");

                photoFrozen.style.transform = "none"; 
                photoFrozen.src = imageData;
                photoFrozen.style.display = "block";
                video.style.display = "none";
                isFrozen = true;

                fetch("/api/scanner/upload", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ image: imageData, answers: [] })
                })
                .then(response => response.json())
                .then(data => {
                    stopScanningAndHideOval();
                    if(data.status === "success") {
                        const tipeUtama = data.tipe_terdeteksi;
                        if (tipeUtama.includes("Gagal") || tipeUtama.includes("Tidak Pas") || tipeUtama.includes("Kurang Pas") || tipeUtama.includes("Terhalang")) {
                            scoresList.innerHTML = `<li style="color: #d9534f; font-weight: 600;">❌ File Ditolak</li>`;
                            recBox.innerHTML = `<div style="color: #d9534f; margin-top: 15px;">${data.rekomendasi.tips}</div>`;
                            resetCameraToLive();
                        } else {
                            scoresList.innerHTML = "<li style='color:#56cc9d; font-weight:600;'>✅ File terverifikasi! Selesaikan kuesioner.</li>";
                            
                            skorKameraLatarBelakang = {
                                oily: parseInt(data.scores["Oily Skin"]),
                                dry: parseInt(data.scores["Dry Skin"]),
                                normal: parseInt(data.scores["Normal Skin"]),
                                combi: parseInt(data.scores["Combination Skin"]),
                                tipe_awal: tipeUtama
                            };

                            captureButton.innerText = "Reset Analisis";
                            captureButton.style.background = "#c27d66"; 
                            
                            pemicuKuisValidasi();
                        }
                    } else {
                        scoresList.innerHTML = "<li style='color: red;'>⚠️ File gagal dieksekusi.</li>";
                        resetCameraToLive();
                    }
                })
                .catch(err => {
                    stopScanningAndHideOval();
                    resetCameraToLive();
                    console.error(err);
                });
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    });
}

// LOGIKA MODUL INTEGRASI KUIS VALIDASI
let kuisPertanyaanData = [];
let indeksPertanyaanSekarang = 0;
let arrayJawabanUser = [];

function pemicuKuisValidasi() {
    fetch('/api/quiz/get-questions')
    .then(res => res.json())
    .then(data => {
        if(data.status === "success") {
            kuisPertanyaanData = data.questions;
            indeksPertanyaanSekarang = 0;
            arrayJawabanUser = [];
            
            resetQuizUI();
            
            const intro = document.getElementById("quiz-intro-text");
            if(intro) intro.style.display = "none";
            
            tampilkanPertanyaanKuis();
        }
    })
    .catch(err => console.error("Gagal memuat kuis:", err));
}

function tampilkanPertanyaanKuis() {
    if (indeksPertanyaanSekarang >= kuisPertanyaanData.length) {
        kirimJawabanKuisKeServer();
        return;
    }
    
    const dataSkrg = kuisPertanyaanData[indeksPertanyaanSekarang];
    document.getElementById("quiz-question").innerText = `${dataSkrg.id}. ${dataSkrg.pertanyaan}`;
    document.getElementById("quiz-progress").innerText = `Pertanyaan ${indeksPertanyaanSekarang + 1} dari ${kuisPertanyaanData.length}`;
    
    const opsiContainer = document.getElementById("quiz-options");
    opsiContainer.innerHTML = "";
    
    Object.entries(dataSkrg.pilihan).forEach(([kunci, teks]) => {
        const btnOpsi = document.createElement("button");
        btnOpsi.innerText = teks;
        btnOpsi.style.cssText = `
            text-align: left; padding: 12px 15px; border: 1px solid #e3e8e5; 
            background: #fff; border-radius: 8px; cursor: pointer; font-size: 13px;
            transition: all 0.2s ease; color: #2c3e35; font-weight: 500;
        `;
        
        btnOpsi.onmouseenter = () => { btnOpsi.style.background = "#f4f6f0"; btnOpsi.style.borderColor = "#708238"; };
        btnOpsi.onmouseleave = () => { btnOpsi.style.background = "#fff"; btnOpsi.style.borderColor = "#e3e8e5"; };
        
        btnOpsi.onclick = () => {
            arrayJawabanUser.push(kunci); 
            indeksPertanyaanSekarang++;   
            tampilkanPertanyaanKuis();
        };
        
        opsiContainer.appendChild(btnOpsi);
    });
}

function kirimJawabanKuisKeServer() {
    document.getElementById("quiz-content").innerHTML = "<h4 style='text-align:center; color:#c27d66; padding: 20px 0;'>⏳ Memproses data analisis...</h4>";
    
    fetch('/api/quiz/calculate-accuracy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            vision_scores: skorKameraLatarBelakang, 
            answers: arrayJawabanUser
        })
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === "success") {
            if (data.new_scores) {
                updateChart(
                    parseInt(data.new_scores.oily), 
                    parseInt(data.new_scores.dry), 
                    parseInt(data.new_scores.normal), 
                    parseInt(data.new_scores.combi)
                );
            }

            const htmlRekomendasi = `
                <div style="margin-top: 20px; text-align: left;">
                    <div style="background: #f4f6f0; border: 1px solid #e3e8e5; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 15px;">
                        <span style="font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #708238; font-weight:600;">Kondisi Akhir Akumulasi</span>
                        <h2 style="margin: 5px 0 0 0; color: #708238; font-size: 24px; font-weight:700;">${data.final_skin_type}</h2>
                    </div>
                    
                    <div style="background: #fafbfa; border: 1px solid #e3e8e5; padding: 15px; border-radius: 12px; margin-bottom: 12px; font-size: 13px; line-height:1.5;">
                        <h4 style="color: #c27d66; margin: 0 0 5px 0; font-weight:600;">🧪 Kandungan Formula Cocok:</h4>
                        <p style="margin: 0; color: #2c3e35;">${data.rekomendasi.kandungan.join(", ")}</p>
                    </div>

                    <div style="background: #ffffff; border: 1px solid #e3e8e5; padding: 15px; border-radius: 12px; font-size: 13px; line-height:1.5;">
                        <h4 style="color: #708238; margin: 0 0 5px 0; font-weight:600;">☀️ Sirkut Perawatan & Tips:</h4>
                        <p style="margin: 0; color: #2c3e35;">${data.rekomendasi.tips}</p>
                    </div>
                </div>
            `;
            recBox.innerHTML = htmlRekomendasi;
            sessionStorage.setItem("saved_rec_box", htmlRekomendasi);
            sessionStorage.setItem("saved_final_skin_type", data.final_skin_type);

            addHistoryLog(
                data.final_skin_type, 
                data.new_scores.oily, 
                data.new_scores.dry, 
                data.new_scores.normal, 
                data.new_scores.combi
            );
            
            sessionStorage.setItem("saved_frozen_photo", photoFrozen.src);

            const htmlQuizSuccess = `
                <div style="text-align: center; padding: 30px 10px;">
                    <div style="font-size: 45px; margin-bottom: 10px;">✅</div>
                    <h3 style="color: #56cc9d; margin: 0 0 8px 0; font-weight:700;">Analisis Selesai!</h3>
                    <div style="margin-top:15px; background:#eefaf5; padding:8px 15px; border-radius:20px; display:inline-block; color:#2ecc71; font-weight:600;">
                        Tipe Kulit: ${data.final_skin_type}
                    </div>
                </div>
            `;
            document.getElementById("quiz-container").style.borderColor = "#56cc9d";
            document.getElementById("quiz-container").innerHTML = htmlQuizSuccess;
            sessionStorage.setItem("saved_quiz_container", htmlQuizSuccess);
            
            // SINKRONISASI AKTIF: Pastikan modal pop-up muncul setelah data benar-benar tersimpan
            const modalNotif = document.getElementById("notif-modal");
            if (modalNotif) {
                modalNotif.style.display = "flex";
            }
            
            document.getElementById("skinChart").scrollIntoView({ behavior: 'smooth' });
        }
    })
    .catch(err => console.error("Gagal memproses skor akumulasi akhir:", err));
}

// LOGIKA MENJAGA DATA ANTAR-HALAMAN
document.addEventListener("DOMContentLoaded", function() {
    const savedChart = sessionStorage.getItem("saved_chart_data");
    if (savedChart) {
        const cData = JSON.parse(savedChart);
        updateChart(cData.oily, cData.dry, cData.normal, cData.combi, true);
    } else {
        updateChart(0, 0, 0, 0, true);
    }

    const daftarJurnalLokal = sessionStorage.getItem("jurnal_pemindaian_list");
    if (daftarJurnalLokal) {
        historyTableBody.innerHTML = "";
        const listData = JSON.parse(daftarJurnalLokal);
        for (let i = listData.length - 1; i >= 0; i--) {
            const item = listData[i];
            addHistoryLog(item.tipe, item.oily, item.dry, item.normal, item.combi, item.waktu);
        }
    } else {
        historyTableBody.innerHTML = `<tr id="empty-history"><td colspan="6" style="padding: 20px; text-align: center; color: #9bb0a5;">Belum ada data pemindaian hari ini.</td></tr>`;
    }

    const savedPhoto = sessionStorage.getItem("saved_frozen_photo");
    if (savedPhoto && photoFrozen) {
        photoFrozen.src = savedPhoto;
        photoFrozen.style.display = "block";
        photoFrozen.style.transform = "none";
        if (video) video.style.display = "none";
        isFrozen = true;
        if (captureButton) {
            captureButton.innerText = "Reset Analisis";
            captureButton.style.background = "#c27d66"; 
        }
        if (cameraWrapper) {
            cameraWrapper.classList.add("hide-oval");
        }
    }

    const savedRec = sessionStorage.getItem("saved_rec_box");
    if (savedRec && recBox) {
        recBox.innerHTML = savedRec;
    }

    const savedQuiz = sessionStorage.getItem("saved_quiz_container");
    if (savedQuiz) {
        const qContainer = document.getElementById("quiz-container");
        if (qContainer) {
            qContainer.style.borderColor = "#56cc9d";
            qContainer.innerHTML = savedQuiz;
        }
    }
});