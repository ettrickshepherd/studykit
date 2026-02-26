#!/usr/bin/env python3
"""
Shared JSON helpers for study-plan and study-session skills.
Zero external dependencies — stdlib only.

Usage:
    uv run python3 ~/.claude/skills/study-plan/scripts/json_helpers.py <command> <args...>

Commands:
    load <file>                       Print JSON file contents
    due-cards <cards.json>            Print cards due today (next_review <= today)
    add-card <cards.json> <json-str>  Append a card to cards.json
    update-card <cards.json> <id> <json-str>  Update card fields after review
    add-session <sessions.json> <json-str>    Append a session record
    add-exercise <exercises.json> <json-str>  Append an exercise record
    stats <cards.json>                Print card statistics
    next-id <file> <prefix>           Print next available ID (e.g., c004, s002)
"""

import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path


def load_json(path: str) -> dict:
    """Load a JSON file. Returns empty structure if file doesn't exist."""
    p = Path(path)
    if not p.exists():
        return {}
    with open(p) as f:
        return json.load(f)


def save_json(path: str, data: dict) -> None:
    """Write JSON file with pretty printing."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def next_id(items: list, prefix: str) -> str:
    """Generate next ID like c001, s001, e001."""
    if not items:
        return f"{prefix}001"
    max_num = max(int(item["id"][len(prefix):]) for item in items)
    return f"{prefix}{max_num + 1:03d}"


def query_due_cards(cards_data: dict, today_str: str | None = None) -> list:
    """Return cards due for review, sorted by overdue first then lowest ease."""
    today_str = today_str or date.today().isoformat()
    due = [c for c in cards_data.get("cards", []) if c["next_review"] <= today_str]
    due.sort(key=lambda c: (c["next_review"], c["ease_factor"]))
    return due


def sm2_update(quality: int, ease_factor: float, interval_days: int, repetitions: int, today_str: str | None = None) -> dict:
    """Apply SM-2 algorithm. Returns updated fields."""
    today_str = today_str or date.today().isoformat()
    today_date = datetime.strptime(today_str, "%Y-%m-%d")

    if quality >= 3:  # correct
        if repetitions == 0:
            interval_days = 1
        elif repetitions == 1:
            interval_days = 6
        else:
            interval_days = round(interval_days * ease_factor)
        repetitions += 1
    else:  # incorrect
        repetitions = 0
        interval_days = 1

    ease_factor = max(
        1.3,
        ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    )

    next_review = (today_date + timedelta(days=interval_days)).strftime("%Y-%m-%d")

    return {
        "ease_factor": round(ease_factor, 4),
        "interval_days": interval_days,
        "repetitions": repetitions,
        "next_review": next_review,
    }


def append_card(cards_path: str, card_data: dict) -> str:
    """Append a card to cards.json. Returns the assigned ID."""
    data = load_json(cards_path)
    if "cards" not in data:
        data["cards"] = []

    card_id = next_id(data["cards"], "c")
    card_data["id"] = card_id

    # Ensure defaults
    card_data.setdefault("ease_factor", 2.5)
    card_data.setdefault("interval_days", 0)
    card_data.setdefault("repetitions", 0)
    card_data.setdefault("next_review", date.today().isoformat())
    card_data.setdefault("created", datetime.now().isoformat(timespec="seconds"))
    card_data.setdefault("last_reviewed", None)
    card_data.setdefault("review_history", [])
    card_data.setdefault("tags", [])
    card_data.setdefault("type", "recall")

    data["cards"].append(card_data)
    save_json(cards_path, data)
    return card_id


def update_card_after_review(cards_path: str, card_id: str, quality: int,
                              session_id: str = "", context: str = "", notes: str = "") -> dict:
    """Update a card after review using SM-2. Returns updated card."""
    data = load_json(cards_path)
    today_str = date.today().isoformat()
    now_str = datetime.now().isoformat(timespec="seconds")

    for card in data["cards"]:
        if card["id"] == card_id:
            # Apply SM-2
            updates = sm2_update(
                quality, card["ease_factor"], card["interval_days"],
                card["repetitions"], today_str
            )
            card.update(updates)
            card["last_reviewed"] = now_str

            # Append to review history
            card["review_history"].append({
                "date": now_str,
                "quality": quality,
                "session": session_id,
                "context": context,
                "notes": notes,
            })

            save_json(cards_path, data)
            return card

    raise ValueError(f"Card {card_id} not found")


def append_session(sessions_path: str, session_data: dict) -> str:
    """Append a session record. Returns assigned ID."""
    data = load_json(sessions_path)
    if "sessions" not in data:
        data["sessions"] = []

    session_id = next_id(data["sessions"], "s")
    session_data["id"] = session_id
    data["sessions"].append(session_data)
    save_json(sessions_path, data)
    return session_id


def append_exercise(exercises_path: str, exercise_data: dict) -> str:
    """Append an exercise record. Returns assigned ID."""
    data = load_json(exercises_path)
    if "exercises" not in data:
        data["exercises"] = []

    exercise_id = next_id(data["exercises"], "e")
    exercise_data["id"] = exercise_id
    data["exercises"].append(exercise_data)
    save_json(exercises_path, data)
    return exercise_id


def card_stats(cards_data: dict) -> dict:
    """Compute card statistics."""
    cards = cards_data.get("cards", [])
    today_str = date.today().isoformat()

    total = len(cards)
    due = len([c for c in cards if c["next_review"] <= today_str])
    mature = len([c for c in cards
                  if c["ease_factor"] > 2.5 and c["interval_days"] > 21 and c["repetitions"] >= 3])
    new = len([c for c in cards if c["repetitions"] == 0])

    # Average ease
    avg_ease = sum(c["ease_factor"] for c in cards) / total if total else 0

    # Accuracy from recent reviews (last 50)
    all_reviews = []
    for c in cards:
        for r in c.get("review_history", []):
            all_reviews.append(r)
    all_reviews.sort(key=lambda r: r["date"], reverse=True)
    recent = all_reviews[:50]
    accuracy = (sum(1 for r in recent if r["quality"] >= 3) / len(recent) * 100) if recent else 0

    return {
        "total": total,
        "due_today": due,
        "mature": mature,
        "new": new,
        "average_ease": round(avg_ease, 2),
        "recent_accuracy_pct": round(accuracy, 1),
    }


# --- CLI interface ---

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "load":
        data = load_json(sys.argv[2])
        print(json.dumps(data, indent=2))

    elif cmd == "due-cards":
        data = load_json(sys.argv[2])
        due = query_due_cards(data)
        print(json.dumps(due, indent=2))

    elif cmd == "add-card":
        card_data = json.loads(sys.argv[3])
        card_id = append_card(sys.argv[2], card_data)
        print(f"Added card {card_id}")

    elif cmd == "update-card":
        cards_path = sys.argv[2]
        card_id = sys.argv[3]
        updates = json.loads(sys.argv[4])
        quality = updates.get("quality", 3)
        session = updates.get("session", "")
        context = updates.get("context", "")
        notes = updates.get("notes", "")
        card = update_card_after_review(cards_path, card_id, quality, session, context, notes)
        print(json.dumps(card, indent=2))

    elif cmd == "add-session":
        session_data = json.loads(sys.argv[3])
        session_id = append_session(sys.argv[2], session_data)
        print(f"Added session {session_id}")

    elif cmd == "add-exercise":
        exercise_data = json.loads(sys.argv[3])
        exercise_id = append_exercise(sys.argv[2], exercise_data)
        print(f"Added exercise {exercise_id}")

    elif cmd == "stats":
        data = load_json(sys.argv[2])
        stats = card_stats(data)
        print(json.dumps(stats, indent=2))

    elif cmd == "next-id":
        data = load_json(sys.argv[2])
        # Detect which collection
        for key in ["cards", "sessions", "exercises", "topics"]:
            if key in data:
                prefix = {"cards": "c", "sessions": "s", "exercises": "e", "topics": "t"}[key]
                print(next_id(data[key], prefix))
                return
        print(f"{sys.argv[3]}001")

    elif cmd == "sm2":
        # sm2 <quality> <ease_factor> <interval_days> <repetitions>
        quality = int(sys.argv[2])
        ef = float(sys.argv[3])
        interval = int(sys.argv[4])
        reps = int(sys.argv[5])
        result = sm2_update(quality, ef, interval, reps)
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
