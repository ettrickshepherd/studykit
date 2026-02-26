# SR Query Patterns

JSON query patterns for spaced repetition operations. All mutations go through the shared helper script.

## Script Location

```bash
HELPERS=~/.claude/skills/study-plan/scripts/json_helpers.py
```

## Common Operations

### Query Due Cards

```bash
uv run python3 $HELPERS due-cards <project>/data/cards.json
```

Returns: JSON array of cards where `next_review <= today`, sorted by overdue-first then lowest ease.

### Get Card Stats

```bash
uv run python3 $HELPERS stats <project>/data/cards.json
```

Returns:
```json
{
  "total": 45,
  "due_today": 12,
  "mature": 8,
  "new": 15,
  "average_ease": 2.35,
  "recent_accuracy_pct": 73.5
}
```

### Add a New Card

```bash
uv run python3 $HELPERS add-card <project>/data/cards.json '{
  "deck": "arrays",
  "front": "What is the time complexity of binary search?",
  "back": "O(log n) — halves the search space each step",
  "tags": ["complexity", "search"],
  "type": "recall"
}'
```

Defaults applied automatically: ease_factor=2.5, interval_days=0, repetitions=0, next_review=today, review_history=[].

### Update Card After Review

```bash
uv run python3 $HELPERS update-card <project>/data/cards.json c001 '{
  "quality": 4,
  "session": "s003",
  "context": "warm-up before DP topic",
  "notes": "Correct but hesitated on why log n"
}'
```

Applies SM-2 algorithm automatically. Updates ease_factor, interval_days, repetitions, next_review, last_reviewed, and appends to review_history.

### Calculate SM-2 (standalone)

```bash
uv run python3 $HELPERS sm2 <quality> <ease_factor> <interval_days> <repetitions>
```

Example:
```bash
uv run python3 $HELPERS sm2 4 2.5 6 2
# Returns: {"ease_factor": 2.5, "interval_days": 15, "repetitions": 3, "next_review": "2026-03-14"}
```

### Add Session Record

```bash
uv run python3 $HELPERS add-session <project>/data/sessions.json '{
  "date": "2026-02-27",
  "planned_start": "09:00",
  "actual_start": "09:12",
  "actual_end": "11:05",
  "duration_minutes": 113,
  "planned_duration": 120,
  "topics_covered": ["arrays", "hashing"],
  "cards_reviewed": 15,
  "cards_correct": 12,
  "exercises_completed": 3,
  "notes": "Strong on arrays, shaky on hash collisions"
}'
```

### Add Exercise Record

```bash
uv run python3 $HELPERS add-exercise <project>/data/exercises.json '{
  "topic": "arrays",
  "subtopic": "two-pointer",
  "difficulty": "medium",
  "description": "Two Sum - find indices that sum to target",
  "file_path": "exercises/arrays/two-sum.py",
  "completed": true,
  "attempts": 1,
  "time_taken_minutes": 8,
  "expected_time_minutes": 20,
  "created": "2026-02-27T09:30:00",
  "completed_at": "2026-02-27T09:38:00",
  "notes": "Clean solution, good edge case handling"
}'
```

### Get Next ID

```bash
uv run python3 $HELPERS next-id <project>/data/cards.json c
```

Returns next available ID (e.g., `c046`).

## In-Prompt Query Patterns

For quick queries that don't need the script (Claude reads the JSON directly):

### Due cards count
```python
len([c for c in cards["cards"] if c["next_review"] <= today])
```

### Overdue cards (missed review)
```python
[c for c in cards["cards"] if c["next_review"] < today]
```

### Cards by deck
```python
[c for c in cards["cards"] if c["deck"] == "arrays"]
```

### Mature cards (well-learned)
```python
[c for c in cards["cards"] if c["ease_factor"] > 2.5 and c["interval_days"] > 21 and c["repetitions"] >= 3]
```

### Struggling cards (low ease)
```python
[c for c in cards["cards"] if c["ease_factor"] < 1.5]
```

### Session streak
```python
# Sort sessions by date descending, count consecutive days
from datetime import date, timedelta
sorted_sessions = sorted(sessions["sessions"], key=lambda s: s["date"], reverse=True)
streak = 0
expected = date.today()
for s in sorted_sessions:
    if s["date"] == expected.isoformat():
        streak += 1
        expected -= timedelta(days=1)
    elif s["date"] == (expected - timedelta(days=1)).isoformat():
        # Skip one rest day
        expected = date.fromisoformat(s["date"])
        streak += 1
        expected -= timedelta(days=1)
    else:
        break
```

### Average session duration (last 7)
```python
recent = sorted(sessions["sessions"], key=lambda s: s["date"], reverse=True)[:7]
avg = sum(s["duration_minutes"] for s in recent) / len(recent) if recent else 0
```

### Topic mastery from cards
```python
for topic in topics["topics"]:
    deck_cards = [c for c in cards["cards"] if c["deck"] == topic["name"]]
    topic["total_cards"] = len(deck_cards)
    topic["mature_cards"] = len([c for c in deck_cards if c["repetitions"] >= 3 and c["interval_days"] > 21])
    if deck_cards:
        topic["mastery"] = topic["mature_cards"] / topic["total_cards"]
```

## Quality Assessment Guide

When assessing response quality for SM-2:

| Signal | Quality | Action |
|--------|---------|--------|
| Instant, confident, complete answer in notes | 5 | Card is solid |
| Correct after brief thought, good notes | 4 | On track |
| Correct but uncertain, needed prompting, or "I know this" without notes | 3 | Needs more review |
| Wrong but close, shows partial understanding | 2 | Increase frequency |
| Wrong, confused about the concept | 1 | Re-teach soon |
| Total blank, no attempt | 0 | Re-teach immediately |

If quality < 3: the card resets to interval=1 (review tomorrow). This is intentional — incorrect recalls need immediate reinforcement.
