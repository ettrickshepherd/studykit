# studykit

Two coordinating [Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills) for structured self-study: plan creation and daily sessions with adaptive spaced repetition.

## Installation

```bash
git clone git@github.com:ettrickshepherd/studykit.git ~/dev/studykit

# Symlink both skills into Claude Code's skill directory
ln -sfn ~/dev/studykit/study-plan ~/.claude/skills/study-plan
ln -sfn ~/dev/studykit/study-session ~/.claude/skills/study-session
```

Verify symlinks:
```bash
ls -la ~/.claude/skills/study-plan/SKILL.md   # should point to repo
ls -la ~/.claude/skills/study-session/SKILL.md
```

**Prerequisites**: Python 3.10+, [uv](https://docs.astral.sh/uv/). For technical mode exercises, you'll also need the runtime for your chosen language (Python comes with uv; for JS/TS install [Bun](https://bun.sh/)).

**Recommended**: Enable the Learning output style for study sessions — it makes Claude ask you to write code yourself during exercises:
```
/output-style learning
```

No external dependencies — all scripts use Python stdlib only (`json`, `datetime`, `pathlib`). Run with `uv run python3`.

## Usage

### `/study-plan` — Create a study plan

Invoke in Claude Code. The skill:

1. **Triages urgency** — urgent (days), soon (weeks), or deep (months) determines how much setup to do
2. **Interviews you** — 1-5 rounds depending on urgency: what you're learning, current level, schedule, learning style, honest commitment
3. **Researches the topic** — parallel subagents investigate subject matter, pedagogy, and any materials you provide
4. **Builds a day-by-day plan** — specific time windows, topic progression, rest days, diagnostic checkpoints, triage strategy
5. **Sets up a project directory** — JSON data files, daily notes, exercise stubs, living schedule

### `/study-session` — Run a daily session

Invoke when you're ready to study. The skill:

1. **Loads your plan** — finds active plans, picks the right one (or asks if you have several)
2. **Checks where you left off** — reads progress, schedule, yesterday's notes, due SR cards
3. **Runs the session** — teaches new material, generates exercises, weaves review cards throughout
4. **Tracks everything** — daily notes (pre/during/after), progress report, schedule adjustments, git commits

## Modes

- **Technical** (coding, algorithms): file-based exercises with test cases, language-aware (Python, JS, Java, Go, SQL, etc.)
- **Knowledge** (law, history, theory): JSON-backed spaced repetition using SM-2, interstitial card review
- **Mixed**: both in one project (e.g., data science = coding + statistics theory)

## Architecture

```
/study-plan                          /study-session
    │                                     │
    ├── SKILL.md (workflow)               ├── SKILL.md (workflow)
    ├── references/                       ├── references/
    │   ├── interview-guide.md            │   ├── session-workflow.md
    │   ├── plan-templates.md             │   ├── sr-queries.md
    │   ├── sr-schema.md                  │   └── exercise-patterns.md
    │   ├── user-profile.md (created)     └── scripts/
    │   └── plans/                            ├── sr_review.py
    │       ├── _index.json                   └── session_summary.py
    │       └── <project-slug>.md
    └── scripts/
        ├── json_helpers.py (shared)
        └── init_study_project.py
```

**How they coordinate**: `/study-plan` writes plans to `study-plan/references/plans/` with YAML frontmatter and registers them in `_index.json`. `/study-session` reads the index to discover plans, loads the selected plan's frontmatter for the project path, and connects to the project's `data/` directory.

### Study project directory (created per project)

```
~/study/<project-name>/
├── plan.md                  # The commitment — goals, strategies, what was agreed to (immutable)
├── learner-context.md       # Project-specific learner observations (updated after notable sessions)
├── learning-schedule.md     # Living day-by-day schedule (updated every session)
├── progress-report.md       # Running status, session log table, topic mastery
├── data/
│   ├── cards.json           # SR card deck — SM-2 state, review history per card
│   ├── sessions.json        # Session log — timing, topics, cards, exercises
│   ├── exercises.json       # Exercise tracking — attempts, times, outcomes
│   └── topics.json          # Topic mastery and metadata
├── daily-notes/
│   └── DD-MM-YYYY.md        # Pre-session + per-task + after-session notes
├── exercises/               # Technical mode: exercise files by topic
│   └── <topic>/
│       └── <exercise>.py
└── materials/               # User-provided reference materials
```

## Scripts

All scripts are zero-dependency (Python stdlib). Both skills share `json_helpers.py` for data mutations.

### `json_helpers.py` — Shared data operations

```bash
uv run python3 ~/.claude/skills/study-plan/scripts/json_helpers.py <command> <args>
```

| Command | Description |
|---------|-------------|
| `due-cards <cards.json>` | Cards due today, sorted by overdue-first then lowest ease |
| `add-card <cards.json> '<json>'` | Append a card with auto-ID and SM-2 defaults |
| `update-card <cards.json> <id> '<json>'` | Apply SM-2 update after review |
| `add-session <sessions.json> '<json>'` | Log a session |
| `add-exercise <exercises.json> '<json>'` | Log an exercise |
| `stats <cards.json>` | Card statistics (total, due, mature, accuracy) |
| `sm2 <quality> <ef> <interval> <reps>` | Standalone SM-2 calculation |

### `init_study_project.py` — Project scaffolding

```bash
uv run python3 ~/.claude/skills/study-plan/scripts/init_study_project.py \
  --name <slug> --location <path> --mode <technical|knowledge|mixed> \
  [--language python] [--topics "arrays,hashing,dp"]
```

### `sr_review.py` — Session review helper

```bash
uv run python3 ~/.claude/skills/study-session/scripts/sr_review.py due <cards.json>
uv run python3 ~/.claude/skills/study-session/scripts/sr_review.py summary <cards.json>
```

### `session_summary.py` — Session statistics

```bash
uv run python3 ~/.claude/skills/study-session/scripts/session_summary.py brief <project-dir>
uv run python3 ~/.claude/skills/study-session/scripts/session_summary.py streak <sessions.json>
```

## Spaced Repetition

Uses the **SM-2 algorithm** (Anki's foundation). Cards are reviewed interstitially — woven into natural transition points during sessions, not in a dedicated review block. Quality is assessed from context (0-5 scale), and review uses Claude Code's AskUserQuestion with the notes feature for active recall.

Card types: `recall`, `application`, `comparison`, `synthesis`, `edge_case`, `pattern`.

## Interview Prep

When the study plan context is interview prep, the system activates interview-specific behavior:

1. **Role research** — asks for company, role, level; launches a background subagent to research the interview process, confirms findings with you
2. **Technical interviews** — covers algorithmic (LC-style), online assessments, system design, pair programming, take-homes, CS fundamentals
3. **Oral interviews** — covers behavioral (STAR), case interviews, competency-based, culture fit, presentation
4. **Pattern-based progression** — for algorithmic prep, problems are grouped by ~15 core patterns (two-pointer, sliding window, BFS/DFS, DP, etc.), not just data structures
5. **Learning output mode** — during coding exercises, Claude refuses to write code or give hints. You solve it. When you say "done", Claude runs the tests.
6. **Primitive extraction** — after solving, Claude decomposes the solution into transferable building blocks (the patterns and techniques, not the specific answer) and generates SR cards for those

The system supports curated problem lists (Blind 75, Neetcode 150, Grind 75) or Claude picks based on your level and weak areas — chosen during onboarding.

## Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Data storage | JSON files | Zero deps, git-friendly diffs, Claude reads/writes directly, scales fine for study-scale data |
| SR algorithm | SM-2 | Anki's foundation — simple, well-understood, sufficient for weeks-to-months timelines |
| Review style | Interstitial | No dedicated "card block" — cards woven into topic transitions, exercise breaks, warm-ups |
| Exercise model | File-based | User solves in their editor; two versions per concept (guided + from-scratch) |
| Living documents | Schedule + progress separate from plan | Plan records the commitment (immutable); schedule adapts; progress tracks reality |
| Daily notes | Write after every task | Context window safety valve — protects against compaction during long sessions |
