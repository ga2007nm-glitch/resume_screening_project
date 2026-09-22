"""In-memory notification store for the demo app."""

from datetime import datetime

_notifications: list[dict] = []
_counter = 0


def add_notification(title: str, message: str, ntype: str = "info") -> dict:
    global _counter
    _counter += 1
    note = {
        "id": _counter,
        "title": title,
        "message": message,
        "type": ntype,
        "read": False,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    _notifications.insert(0, note)
    return note


def get_notifications() -> list[dict]:
    return list(_notifications)


def get_unread_count() -> int:
    return sum(1 for n in _notifications if not n["read"])


def mark_read(note_id: int) -> bool:
    for n in _notifications:
        if n["id"] == note_id:
            n["read"] = True
            return True
    return False


def mark_all_read() -> None:
    for n in _notifications:
        n["read"] = True
