#!/usr/bin/env python3
"""
Initialize a study project directory structure and JSON data files.

Usage:
    uv run python3 ~/.claude/skills/study-plan/scripts/init_study_project.py \
        --name <project-name> \
        --location <path> \
        --mode <technical|knowledge|mixed> \
        [--language <python|java|go|...>] \
        [--topics topic1,topic2,topic3]

Creates:
    <location>/
    ├── plan.md                    (placeholder — written by the skill after)
    ├── learner-context.md         (template)
    ├── learning-schedule.md       (placeholder)
    ├── progress-report.md         (initial state)
    ├── data/
    │   ├── cards.json
    │   ├── sessions.json
    │   ├── exercises.json
    │   └── topics.json
    ├── daily-notes/
    ├── exercises/                  (technical/mixed only)
    │   └── <topic>/               (one per topic)
    └── materials/
"""

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path


def write_json(path: Path, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def write_text(path: Path, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Initialize a study project")
    parser.add_argument("--name", required=True, help="Project name (slug)")
    parser.add_argument("--location", required=True, help="Directory path")
    parser.add_argument("--mode", required=True, choices=["technical", "knowledge", "mixed"])
    parser.add_argument("--language", default=None, help="Programming language (technical mode)")
    parser.add_argument("--topics", default="", help="Comma-separated topic list")
    args = parser.parse_args()

    project_dir = Path(args.location).expanduser().resolve()
    topics = [t.strip() for t in args.topics.split(",") if t.strip()] if args.topics else []
    today = date.today().isoformat()
    now = datetime.now().isoformat(timespec="seconds")

    # Create directory structure
    (project_dir / "data").mkdir(parents=True, exist_ok=True)
    (project_dir / "daily-notes").mkdir(parents=True, exist_ok=True)
    (project_dir / "materials").mkdir(parents=True, exist_ok=True)

    if args.mode in ("technical", "mixed"):
        (project_dir / "exercises").mkdir(parents=True, exist_ok=True)
        for topic in topics:
            (project_dir / "exercises" / topic.lower().replace(" ", "-")).mkdir(parents=True, exist_ok=True)

    # Initialize JSON data files
    write_json(project_dir / "data" / "cards.json", {"cards": []})
    write_json(project_dir / "data" / "sessions.json", {"sessions": []})
    write_json(project_dir / "data" / "exercises.json", {"exercises": []})

    # Initialize topics
    topics_data = {
        "topics": [
            {
                "name": topic,
                "parent": None,
                "mode": args.mode if args.mode != "mixed" else "technical",
                "mastery": 0.0,
                "priority": i + 1,
                "total_cards": 0,
                "mature_cards": 0,
                "exercises_completed": 0,
                "content_source": "claude-generated",
                "notes": None,
            }
            for i, topic in enumerate(topics)
        ]
    }
    write_json(project_dir / "data" / "topics.json", topics_data)

    # Placeholder plan.md
    write_text(project_dir / "plan.md", f"# {args.name} — Study Plan\n\nPlan will be written here after confirmation.\n")

    # learner-context.md template
    write_text(project_dir / "learner-context.md", f"""# Learner Context — {args.name}
Last updated: {today}

## Read This First
This document captures who this learner is in the context of THIS project.
Read it at the start of every session before plan, schedule, or cards.

## Explanation Style
- Preferred: [to be discovered]
- Avoid: [to be discovered]

## Recurring Patterns
- [Will be populated after sessions]

## Confidence Calibration
- [Will be populated after sessions]

## What Motivates Them (observed, not just stated)
- [Will be populated after sessions]

## Session-to-Session Notes
- [Notes will be appended here after notable sessions]
""")

    # learning-schedule.md placeholder
    write_text(project_dir / "learning-schedule.md", f"""# Learning Schedule — {args.name}
Last updated: {today}

## This Week
| Day | Date | Time | Topics | Mode | Status |
|-----|------|------|--------|------|--------|

## Upcoming
[Schedule will be populated from the confirmed plan]

## Adjustments Log
- {today}: Project initialized
""")

    # progress-report.md initial state
    write_text(project_dir / "progress-report.md", f"""# Progress Report — {args.name}
Last updated: {today}

## Current Status
- Day: 0
- Streak: 0 consecutive days
- Overall: Not started
- SR: 0 cards total, 0 mature, 0 due tomorrow
- Exercises: 0 completed out of 0 planned
- Weakest area: N/A
- Strongest area: N/A

## Active Concerns
- None yet

## Session Log
| Date | Duration | Committed | Cards Reviewed | Cards Correct | Exercises | Notes |
|------|----------|-----------|---------------|---------------|-----------|-------|

## Topic Mastery
| Topic | Mastery | Cards (mature/total) | Exercises (done/total) | Notes |
|-------|---------|---------------------|----------------------|-------|
""")

    # Print summary
    print(f"Study project initialized at: {project_dir}")
    print(f"  Mode: {args.mode}")
    if args.language:
        print(f"  Language: {args.language}")
    print(f"  Topics: {', '.join(topics) if topics else 'none yet'}")
    print(f"  Data files: cards.json, sessions.json, exercises.json, topics.json")
    print(f"  Directories: data/, daily-notes/, materials/", end="")
    if args.mode in ("technical", "mixed"):
        print(f", exercises/")
    else:
        print()
    print(f"\nNext steps:")
    print(f"  1. Write plan.md with the confirmed study plan")
    print(f"  2. Write learning-schedule.md with the day-by-day schedule")
    print(f"  3. Update learner-context.md with project-specific observations")
    print(f"  4. Register plan in ~/.claude/skills/study-plan/references/plans/")


if __name__ == "__main__":
    main()
