// static/js/main.js
document.addEventListener("DOMContentLoaded", function () {
    // Ambil path URL halaman saat ini
    const currentPath = window.location.pathname;
    
    // Ambil elemen link menu berdasarkan ID
    const menuDash = document.getElementById("menu-dash");
    const menuChat = document.getElementById("menu-chat");

    // Reset class active terlebih dahulu
    if (menuDash) menuDash.classList.remove("active");
    if (menuChat) menuChat.classList.remove("active");

    // Cek halaman aktif dan tambahkan class active pada menu yang sesuai
    if (currentPath === "/" || currentPath.includes("dashboard")) {
        if (menuDash) menuDash.classList.add("active");
    } else if (currentPath.includes("assistant")) {
        if (menuChat) menuChat.classList.add("active");
    }
});