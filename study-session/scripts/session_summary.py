#!/usr/bin/env python3
"""
Generate session stats and daily note content.

Usage:
    uv run python3 ~/.claude/skills/study-session/scripts/session_summary.py stats <sessions.json>
    uv run python3 ~/.claude/skills/study-session/scripts/session_summary.py streak <sessions.json>
    uv run python3 ~/.claude/skills/study-session/scripts/session_summary.py timing <sessions.json>
    uv run python3 ~/.claude/skills/study-session/scripts/session_summary.py brief <project-dir>
"""

import json
import sys
from datetime import date, timedelta
from pathlib import Path

# Import shared helpers
HELPERS_PATH = Path.home() / ".claude" / "skills" / "study-plan" / "scripts"
sys.path.insert(0, str(HELPERS_PATH))
from json_helpers import load_json, query_due_cards, card_stats


def session_stats(sessions_data: dict) -> dict:
    """Compute session statistics."""
    sessions = sessions_data.get("sessions", [])
    if not sessions:
        return {"total_sessions": 0, "streak": 0}

    total = len(sessions)
    total_minutes = sum(s.get("duration_minutes", 0) for s in sessions)
    total_committed = sum(s.get("planned_duration", 0) for s in sessions)

    # Average duration
    avg_duration = total_minutes / total if total else 0

    # Commitment ratio
    commitment_ratio = total_minutes / total_committed if total_committed else 0

    # Recent sessions (last 7)
    recent = sorted(sessions, key=lambda s: s["date"], reverse=True)[:7]
    avg_recent = sum(s.get("duration_minutes", 0) for s in recent) / len(recent) if recent else 0

    # Total cards and exercises
    total_cards = sum(s.get("cards_reviewed", 0) for s in sessions)
    total_exercises = sum(s.get("exercises_completed", 0) for s in sessions)

    return {
        "total_sessions": total,
        "total_minutes": total_minutes,
        "total_committed_minutes": total_committed,
        "commitment_ratio": round(commitment_ratio, 2),
        "avg_duration_minutes": round(avg_duration, 1),
        "avg_recent_duration": round(avg_recent, 1),
        "total_cards_reviewed": total_cards,
        "total_exercises_completed": total_exercises,
    }


def calculate_streak(sessions_data: dict) -> dict:
    """Calculate current study streak."""
    sessions = sessions_data.get("sessions", [])
    if not sessions:
        return {"streak": 0, "last_session": None}

    sorted_sessions = sorted(sessions, key=lambda s: s["date"], reverse=True)
    last_date = sorted_sessions[0]["date"]

    streak = 0
    expected = date.today()

    # Check if studied today
    if last_date != expected.isoformat():
        # Check if yesterday (allow one-day gap for current day)
        if last_date == (expected - timedelta(days=1)).isoformat():
            expected = expected - timedelta(days=1)
        else:
            return {"streak": 0, "last_session": last_date, "days_since": (expected - date.fromisoformat(last_date)).days}

    unique_dates = sorted(set(s["date"] for s in sessions), reverse=True)

    for d in unique_dates:
        session_date = date.fromisoformat(d)
        diff = (expected - session_date).days
        if diff <= 1:  # Allow one rest day gap
            streak += 1
            expected = session_date - timedelta(days=1)
        else:
            break

    return {
        "streak": streak,
        "last_session": last_date,
        "days_since": (date.today() - date.fromisoformat(last_date)).days,
    }


def timing_analysis(sessions_data: dict) -> dict:
    """Analyze timing patterns — late starts, short sessions, etc."""
    sessions = sessions_data.get("sessions", [])
    if not sessions:
        return {}

    late_starts = 0
    short_sessions = 0
    total_with_timing = 0

    for s in sessions:
        planned = s.get("planned_start")
        actual = s.get("actual_start")
        if planned and actual:
            total_with_timing += 1
            # Simple string comparison for HH:MM format
            if actual > planned:
                late_starts += 1

        duration = s.get("duration_minutes", 0)
        committed = s.get("planned_duration", 0)
        if committed > 0 and duration < committed * 0.6:
            short_sessions += 1

    return {
        "total_with_timing": total_with_timing,
        "late_starts": late_starts,
        "late_start_pct": round(late_starts / total_with_timing * 100, 1) if total_with_timing else 0,
        "short_sessions": short_sessions,
        "short_session_pct": round(short_sessions / len(sessions) * 100, 1) if sessions else 0,
    }


def session_brief(project_dir: str) -> dict:
    """Generate a consolidated session brief from all project data."""
    p = Path(project_dir)

    # Load all data
    sessions = load_json(str(p / "data" / "sessions.json"))
    cards = load_json(str(p / "data" / "cards.json"))
    exercises = load_json(str(p / "data" / "exercises.json"))
    topics = load_json(str(p / "data" / "topics.json"))

    # Session stats
    stats = session_stats(sessions)
    streak = calculate_streak(sessions)
    timing = timing_analysis(sessions)

    # Card stats
    c_stats = card_stats(cards)
    due = query_due_cards(cards)

    # Exercise stats
    ex_completed = len([e for e in exercises.get("exercises", []) if e.get("completed")])
    ex_total = len(exercises.get("exercises", []))

    return {
        "session": stats,
        "streak": streak,
        "timing": timing,
        "cards": c_stats,
        "due_cards_count": len(due),
        "exercises_completed": ex_completed,
        "exercises_total": ex_total,
        "topics_count": len(topics.get("topics", [])),
    }


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "stats":
        data = load_json(sys.argv[2])
        stats = session_stats(data)
        print(json.dumps(stats, indent=2))

    elif cmd == "streak":
        data = load_json(sys.argv[2])
        streak = calculate_streak(data)
        print(json.dumps(streak, indent=2))

    elif cmd == "timing":
        data = load_json(sys.argv[2])
        timing = timing_analysis(data)
        print(json.dumps(timing, indent=2))

    elif cmd == "brief":
        brief = session_brief(sys.argv[2])
        print(json.dumps(brief, indent=2))

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
