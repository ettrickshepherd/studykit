# Spaced Repetition Schema + SM-2 Algorithm

## JSON Data File Schemas

### cards.json

```json
{
  "cards": [
    {
      "id": "c001",
      "deck": "arrays",
      "front": "What is the time complexity of binary search?",
      "back": "O(log n) — halves the search space each step",
      "tags": ["complexity", "search", "fundamentals"],
      "type": "recall",
      "ease_factor": 2.5,
      "interval_days": 0,
      "repetitions": 0,
      "next_review": "2026-02-27",
      "created": "2026-02-27T09:15:00",
      "last_reviewed": null,
      "review_history": []
    }
  ]
}
```

**Card fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique ID, format "c001", "c002", etc. Auto-increment. |
| deck | string | Topic/deck name (matches topic name in topics.json) |
| front | string | The question or prompt |
| back | string | The answer or explanation |
| tags | string[] | Searchable tags |
| type | string | One of: recall, application, comparison, synthesis, edge_case |
| ease_factor | float | SM-2 ease factor, starts at 2.5 |
| interval_days | int | Current interval in days |
| repetitions | int | Consecutive correct reviews |
| next_review | string | ISO date "YYYY-MM-DD" |
| created | string | ISO datetime |
| last_reviewed | string|null | ISO datetime of last review |
| review_history | array | Embedded review records (see below) |

**Review history entry:**
```json
{
  "date": "2026-02-28T09:30:00",
  "quality": 4,
  "session": "s003",
  "context": "between exercises on two-pointer problems",
  "notes": "Got it but hesitated on the 'why'"
}
```

**Card types:**
- `recall` — Definition, key facts, dates, rules
- `application` — "Given [scenario], which [concept] applies?"
- `comparison` — "How does [A] differ from [B]?"
- `synthesis` — "Explain how [concept A] relates to [concept B] and why it matters for [context]"
- `edge_case` — "What happens when [unusual condition]?"

### sessions.json

```json
{
  "sessions": [
    {
      "id": "s001",
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
      "notes": "Strong on arrays, shaky on hash collision strategies"
    }
  ]
}
```

### exercises.json

```json
{
  "exercises": [
    {
      "id": "e001",
      "topic": "arrays",
      "subtopic": "two-pointer",
      "difficulty": "easy",
      "description": "Two Sum - find indices that sum to target",
      "file_path": "exercises/arrays/two-sum.py",
      "completed": false,
      "attempts": 0,
      "time_taken_minutes": null,
      "expected_time_minutes": 20,
      "created": "2026-02-27T09:30:00",
      "completed_at": null,
      "notes": null
    }
  ]
}
```

### topics.json

```json
{
  "topics": [
    {
      "name": "arrays",
      "parent": null,
      "mode": "technical",
      "mastery": 0.0,
      "priority": 1,
      "total_cards": 0,
      "mature_cards": 0,
      "exercises_completed": 0,
      "content_source": "claude-generated",
      "notes": null
    }
  ]
}
```

---

## SM-2 Algorithm

The SuperMemo 2 algorithm. This is Anki's foundation.

### Parameters
- **quality** (0-5): Response quality rating
  - 5 = instant, confident, correct
  - 4 = correct after thinking
  - 3 = correct but uncertain or needed hint
  - 2 = wrong but close
  - 1 = wrong and confused
  - 0 = total blank
- **ease_factor**: Multiplier for interval growth. Starts at 2.5, minimum 1.3.
- **interval_days**: Days until next review.
- **repetitions**: Consecutive correct reviews.

### Update Rules

```python
def sm2_update(quality: int, ease_factor: float, interval_days: int, repetitions: int, today: str):
    """
    Apply SM-2 algorithm to a card after review.

    Args:
        quality: 0-5 rating of response quality
        ease_factor: current ease factor (starts at 2.5)
        interval_days: current interval in days
        repetitions: consecutive correct reviews
        today: ISO date string "YYYY-MM-DD"

    Returns:
        dict with updated ease_factor, interval_days, repetitions, next_review
    """
    from datetime import datetime, timedelta

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

    # Update ease factor (always, regardless of correct/incorrect)
    ease_factor = max(
        1.3,
        ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    )

    next_review = (
        datetime.strptime(today, "%Y-%m-%d") + timedelta(days=interval_days)
    ).strftime("%Y-%m-%d")

    return {
        "ease_factor": round(ease_factor, 4),
        "interval_days": interval_days,
        "repetitions": repetitions,
        "next_review": next_review,
    }
```

### Quality Assessment (Interstitial Mode)

Claude assesses quality from context, not a formal 0-5 prompt:

| Response | Quality |
|----------|---------|
| Instant, confident, correct | 5 |
| Correct after thinking | 4 |
| Correct but uncertain or needed hint | 3 |
| Wrong but close | 2 |
| Wrong and confused | 1 |
| Total blank | 0 |

For AskUserQuestion open-recall flow:
- Option "I know this" + accurate notes → 4-5
- Option "I know this" + no notes → 3 (claimed, didn't prove it)
- Option "Partially" + notes showing partial knowledge → 2-3
- Option "No idea" → 0-1

### Card Maturity

A card is "mature" when:
- ease_factor > 2.5
- interval_days > 21
- At least 3 consecutive correct reviews (repetitions >= 3)

### Querying Due Cards

```python
from datetime import date

today = date.today().isoformat()
due_cards = [c for c in cards["cards"] if c["next_review"] <= today]

# Sort: overdue first, then lowest ease factor
due_cards.sort(key=lambda c: (c["next_review"], c["ease_factor"]))
```

### ID Generation

Auto-increment from highest existing ID:

```python
def next_card_id(cards):
    if not cards["cards"]:
        return "c001"
    max_id = max(int(c["id"][1:]) for c in cards["cards"])
    return f"c{max_id + 1:03d}"
```

Same pattern for sessions (s001), exercises (e001).
