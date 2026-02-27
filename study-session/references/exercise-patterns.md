# Exercise Patterns

How to generate, present, and evaluate coding exercises for technical study sessions.

## Exercise File Structure

Every exercise file follows this pattern:

```python
# ============================================================
# Exercise: [Title]
# Topic: [topic] / [subtopic]
# Difficulty: [easy | medium | hard]
# Expected time: [N] minutes
# ============================================================
#
# Instructions:
# [Clear description of the problem]
#
# Constraints:
# - [constraint 1]
# - [constraint 2]
#
# Examples:
# Input: [example input]
# Output: [expected output]
#
# Input: [example input 2]
# Output: [expected output 2]
#
# Hints (try without these first):
# 1. [hint 1]
# 2. [hint 2]
# ============================================================


def solution(args):
    """Your solution here."""
    pass


# ============================================================
# Tests — run to verify your solution
# ============================================================

def test_solution():
    assert solution([2, 7, 11, 15], 9) == [0, 1], "Basic case"
    assert solution([3, 2, 4], 6) == [1, 2], "Non-adjacent"
    assert solution([3, 3], 6) == [0, 1], "Duplicate values"
    print("All tests passed!")


if __name__ == "__main__":
    test_solution()
```

## Language-Specific Patterns

Read the plan frontmatter `language` field. Adapt file extension, runner, and idioms:

### Python (.py)
- Runner: `uv run python3 exercises/<topic>/<name>.py` or `uv run pytest exercises/<topic>/<name>.py`
- Stubs: `def solution(...)`, type hints encouraged
- Tests: simple `assert` statements + `if __name__` block

### JavaScript (.js)
- Runner: `bun exercises/<topic>/<name>.js` or `bun test exercises/<topic>/<name>.test.js`
- Stubs: `function solution(...)` or `const solution = (...) => {}`
- Tests: `console.assert()` or separate `.test.js` with bun test

### TypeScript (.ts)
- Runner: `bun exercises/<topic>/<name>.ts`
- Stubs: typed function signatures
- Tests: `bun test`

### Java (.java)
- Runner: `javac exercises/<topic>/<Name>.java && java -cp exercises/<topic> <Name>`
- Stubs: class + method signatures
- Tests: main method with assertions

### Go (.go)
- Runner: `go run exercises/<topic>/<name>.go`
- Stubs: `func solution(...)` with return types
- Tests: `go test` with `_test.go` file

### SQL (.sql)
- Runner: depends on DB (sqlite3, psql, etc.) — note in exercise header
- Stubs: commented schema + empty SELECT
- Tests: expected output as comments

### If language is null/unspecified
Ask during the session: "What language do you want to work in for exercises?"

## Two Versions Per Concept

For each concept, generate two exercises:

### Version 1: Guided
- More detailed instructions
- Helper function stubs provided
- Step-by-step hints available
- Simpler test cases
- Purpose: learn the pattern

### Version 2: From Scratch
- Minimal instructions (just the problem statement)
- No stubs beyond the function signature
- No hints
- Edge cases in tests
- Purpose: prove mastery

Name convention: `<concept>-guided.py` and `<concept>.py`

## Difficulty Calibration

| Difficulty | Expected Time | Characteristics |
|-----------|--------------|-----------------|
| Easy | 10-15 min | Single concept, straightforward, 1-2 data structures |
| Medium | 20-30 min | Combines concepts, requires insight, edge cases matter |
| Hard | 30-45 min | Multiple concepts, optimization needed, tricky edge cases |

If the learner solves an "easy" in < 5 min: they're beyond this level, skip to medium.
If they struggle with "easy" for > 20 min: they need the concept re-taught before more exercises.

## Exercise Evaluation

After the user solves (or gives up):

1. **Correctness** — Do all tests pass?
2. **Approach** — Did they use the expected pattern? A valid alternative? A brute force?
3. **Time** — Compare against expected. Contextualise: "You solved this in 8 min. In an interview, you'd have ~20 min. That's solid."
4. **Code quality** — Clean variable names? Edge cases handled? Could they explain it?
5. **Pattern recognition** — "This is a two-pointer problem. The pattern: [explanation]. You'll see this again in [related problems]."

## After Exercise: Card Generation

For every completed exercise, generate 1-3 SR cards in the background:

- **Pattern card**: "When you see [problem characteristic], consider [approach]."
- **Complexity card**: "What's the time and space complexity of [approach] for [problem type]?"
- **Edge case card**: "What edge cases should you check for in [problem type]?"

These cards reinforce the exercise learning through future SR reviews.

## Exercise Tracking

Log every exercise to `data/exercises.json`:

```bash
uv run python3 ~/.claude/skills/study-plan/scripts/json_helpers.py add-exercise <project>/data/exercises.json '{
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

## Common Exercise Progressions

### Arrays & Strings
Easy: Two Sum → Medium: Three Sum → Hard: Four Sum / Container With Most Water

### Linked Lists
Easy: Reverse List → Medium: Detect Cycle → Hard: Merge K Sorted Lists

### Trees
Easy: Max Depth → Medium: Level Order Traversal → Hard: Serialize/Deserialize

### Dynamic Programming
Easy: Climbing Stairs → Medium: Coin Change → Hard: Edit Distance

### Graphs
Easy: Number of Islands → Medium: Course Schedule → Hard: Word Ladder

### SQL
Easy: Basic SELECT + WHERE → Medium: JOINs + GROUP BY → Hard: Window Functions + CTEs

Adapt to the specific plan topics and the learner's level. These are starting points, not rigid sequences.

---

## Interview Prep Mode

Activates when project has interview-related tags (e.g., `interview`, `leetcode`, `coding-interview`). Read the relevant reference:
- Technical → `~/.claude/skills/study-plan/references/technical-interview.md`
- Oral → `~/.claude/skills/study-plan/references/oral-interview.md`

### Algorithmic Exercises (LC-style)

Based on real LeetCode problems, not generic exercises.

**Exercise file format**:
```python
# ============================================================
# LeetCode 15: 3Sum
# Pattern: Two Pointer
# Difficulty: Medium
# Interview time budget: 25-35 min
# ============================================================
#
# Given an integer array nums, return all the triplets
# [nums[i], nums[j], nums[k]] such that i != j, i != k,
# and j != k, and nums[i] + nums[j] + nums[k] == 0.
#
# Notice that the solution set must not contain duplicate
# triplets.
#
# Constraints:
# - 3 <= nums.length <= 3000
# - -10^5 <= nums[i] <= 10^5
#
# Example 1:
#   Input: nums = [-1,0,1,2,-1,-4]
#   Output: [[-1,-1,2],[-1,0,1]]
#
# Example 2:
#   Input: nums = [0,1,1]
#   Output: []
# ============================================================

from datetime import datetime
_start = datetime.now()


def three_sum(nums: list[int]) -> list[list[int]]:
    """Your solution here."""
    pass


# ============================================================
# Tests
# ============================================================

def test():
    _elapsed = (datetime.now() - _start).total_seconds() / 60
    print(f"Time: {_elapsed:.1f} min")

    result = three_sum([-1, 0, 1, 2, -1, -4])
    assert sorted([sorted(x) for x in result]) == [[-1, -1, 2], [-1, 0, 1]], f"Basic: {result}"

    assert three_sum([0, 1, 1]) == [], "No triplets"
    assert three_sum([0, 0, 0]) == [[0, 0, 0]], "All zeros"
    assert three_sum([1, -1, -1, 0]) == [[-1, 0, 1]], "Duplicates"

    print(f"All tests passed in {_elapsed:.1f} min")


if __name__ == "__main__":
    test()
```

Note the timing built into the file — elapsed time is shown when tests run.

**The solve phase — learning output mode**:

1. After generating the exercise file, Claude enters learning output mode
2. **Claude REFUSES to write any code, give solutions, or offer hints.** No "here's how I'd approach it", no code suggestions, no completions. The user solves it themselves.
3. Claude may ONLY answer clarifying questions about the **problem statement** (not the solution). "What does 'duplicate triplets' mean?" is fine. "Should I use two pointers?" is not — Claude responds: "Work through that yourself."
4. This is the core discipline. If Claude writes the code, the user hasn't learned anything.
5. When the user says "done" / "run it" / equivalent, Claude runs the file.
6. Learning mode deactivates — Claude can now discuss the solution freely.

**After solving — primitive extraction**:

1. Identify the pattern(s) used (reference `technical-interview.md` pattern taxonomy)
2. List 2-5 solution primitives — the transferable building blocks
3. Generate SR cards for the primitives (not the specific problem)
4. Tag cards with both the pattern and the LC problem that surfaced them
5. Evaluate: correctness, approach, time vs interview budget, code quality
6. "You solved LC 15 (3Sum) in 18 min. Interview budget is 25-35 min. Solid pace."

**Exercise tracking** — log with interview-specific fields:
```bash
uv run python3 ~/.claude/skills/study-plan/scripts/json_helpers.py add-exercise <project>/data/exercises.json '{
  "topic": "arrays",
  "subtopic": "two-pointer",
  "pattern": "two-pointer",
  "lc_number": 15,
  "lc_name": "3Sum",
  "difficulty": "medium",
  "assessment_type": "algorithmic",
  "timed": true,
  "interview_time_budget": 30,
  ...
}'
```

### System Design Exercises

1. Claude presents a design scenario ("Design a URL shortener", "Design Twitter's feed")
2. User describes their design (typed — components, data flow, trade-offs)
3. Claude evaluates: requirements gathering, component choices, scalability, trade-offs
4. Primitive extraction → SR cards for design building blocks
5. No learning output mode needed — this is collaborative discussion

### Behavioral / Oral Exercises

1. Claude presents a behavioral question themed to target competency
2. User types their STAR response
3. Claude evaluates: structure, specificity, impact, length, ownership
4. SR cards for: question patterns, which story maps to which competency
5. Feedback is direct: "Your situation was too long. The action was strong but you didn't quantify the result."
