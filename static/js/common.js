function initDarkMode() {
    const btn = document.getElementById("darkModeBtn");
    if (!btn) return;
    if (localStorage.getItem("darkMode") === "1") {
        document.body.classList.add("dark-mode");
        btn.innerHTML = '<i class="fa-solid fa-sun"></i> Light Mode';
    }
    btn.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        const on = document.body.classList.contains("dark-mode");
        localStorage.setItem("darkMode", on ? "1" : "0");
        btn.innerHTML = on
            ? '<i class="fa-solid fa-sun"></i> Light Mode'
            : '<i class="fa-solid fa-moon"></i> Dark Mode';
    });
}

async function updateNotificationBadge() {
    const badge = document.getElementById("notifBadge");
    if (!badge) return;
    try {
        const res = await fetch("/api/notifications");
        const data = await res.json();
        const count = data.unread_count || 0;
        badge.textContent = count;
        badge.style.display = count > 0 ? "inline-flex" : "none";
    } catch (_) {
        badge.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    initDarkMode();
    updateNotificationBadge();
    setInterval(updateNotificationBadge, 10000);
});
