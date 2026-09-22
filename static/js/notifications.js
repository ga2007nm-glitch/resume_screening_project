const icons = { info: "fa-info-circle", success: "fa-check-circle", warning: "fa-exclamation-triangle" };

async function loadNotifications() {
    const list = document.getElementById("notifList");
    try {
        const res = await fetch("/api/notifications");
        const data = await res.json();
        const notes = data.notifications || [];
        if (notes.length === 0) {
            list.innerHTML = '<p style="color:#94a3b8;text-align:center;padding:40px;">No notifications yet.</p>';
            return;
        }
        list.innerHTML = notes.map((n) => `
            <li class="notif-item ${n.type} ${n.read ? "" : "unread"}" onclick="markOne(${n.id})">
                <i class="fa-solid ${icons[n.type] || icons.info} notif-icon"></i>
                <div class="notif-body">
                    <h4>${n.title}</h4><p>${n.message}</p>
                    <div class="notif-time">${n.time}</div>
                </div>
            </li>`).join("");
        updateNotificationBadge();
    } catch (_) {
        list.innerHTML = '<p class="alert alert-error">Could not load notifications.</p>';
    }
}

async function markOne(id) {
    await fetch(`/api/notifications/read/${id}`, { method: "POST" });
    loadNotifications();
}

async function markAllRead() {
    await fetch("/api/notifications/read-all", { method: "POST" });
    loadNotifications();
}

loadNotifications();
setInterval(loadNotifications, 8000);
