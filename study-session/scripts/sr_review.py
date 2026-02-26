#!/usr/bin/env python3
"""
Query due cards and update after review.
Thin wrapper around json_helpers for study-session convenience.

Usage:
    uv run python3 ~/.claude/skills/study-session/scripts/sr_review.py due <cards.json>
    uv run python3 ~/.claude/skills/study-session/scripts/sr_review.py review <cards.json> <card-id> <quality> [session-id] [context] [notes]
    uv run python3 ~/.claude/skills/study-session/scripts/sr_review.py summary <cards.json>
    uv run python3 ~/.claude/skills/study-session/scripts/sr_review.py overdue <cards.json>
"""

import json
import sys
from pathlib import Path

# Import shared helpers
HELPERS_PATH = Path.home() / ".claude" / "skills" / "study-plan" / "scripts"
sys.path.insert(0, str(HELPERS_PATH))
from json_helpers import load_json, query_due_cards, update_card_after_review, card_stats


def get_overdue(cards_path: str) -> list:
    """Get cards that are overdue (next_review < today, not just <=)."""
    from datetime import date
    today = date.today().isoformat()
    data = load_json(cards_path)
    overdue = [c for c in data.get("cards", []) if c["next_review"] < today]
    overdue.sort(key=lambda c: (c["next_review"], c["ease_factor"]))
    return overdue


def review_summary(cards_path: str) -> dict:
    """Generate a review summary for session brief."""
    data = load_json(cards_path)
    stats = card_stats(data)

    from datetime import date
    today = date.today().isoformat()
    due = query_due_cards(data, today)
    overdue = [c for c in due if c["next_review"] < today]

    # Group due by deck
    by_deck = {}
    for c in due:
        deck = c.get("deck", "unknown")
        by_deck[deck] = by_deck.get(deck, 0) + 1

    return {
        **stats,
        "overdue_count": len(overdue),
        "due_by_deck": by_deck,
    }


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    cards_path = sys.argv[2]

    if cmd == "due":
        data = load_json(cards_path)
        due = query_due_cards(data)
        print(json.dumps(due, indent=2))

    elif cmd == "review":
        if len(sys.argv) < 5:
            print("Usage: review <cards.json> <card-id> <quality> [session-id] [context] [notes]")
            sys.exit(1)
        card_id = sys.argv[3]
        quality = int(sys.argv[4])
        session_id = sys.argv[5] if len(sys.argv) > 5 else ""
        context = sys.argv[6] if len(sys.argv) > 6 else ""
        notes = sys.argv[7] if len(sys.argv) > 7 else ""
        card = update_card_after_review(cards_path, card_id, quality, session_id, context, notes)
        print(json.dumps(card, indent=2))

    elif cmd == "summary":
        summary = review_summary(cards_path)
        print(json.dumps(summary, indent=2))

    elif cmd == "overdue":
        overdue = get_overdue(cards_path)
        print(json.dumps(overdue, indent=2))

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
