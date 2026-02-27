# studykit

Two Claude Code skills for structured self-study with adaptive spaced repetition.

## The problem

Self-study breaks down in predictable ways:

- **No structure** — "learn DP this week" isn't a plan. No progression, no checkpoints, no idea what to cut when you're behind.
- **No retention** — study something Monday, forget it by Friday. No systematic review.
- **No accountability** — skip a day, then two, then quit. Nobody tracking whether you actually showed up.
- **For interviews: no strategy** — grinding LC randomly is slow. Every company tests differently. Memorising solutions doesn't transfer.
- **AI does it for you** — ask Claude for help with an exercise and it writes the whole solution. You haven't learned anything.

## How studykit works

Two skills that coordinate through shared data:

**`/study-plan`** — builds a structured study plan through interview + research.
Classifies what you're preparing for (interview, exam, or general learning), identifies the target, researches it in the background, then builds a day-by-day schedule with topic progression, SR card integration, diagnostic checkpoints, and triage strategy.

**`/study-session`** — runs daily sessions adapted to where you are.
Loads your plan, checks what's due, teaches new material, generates exercises, weaves review cards throughout, tracks everything (timing, accuracy, progress), and commits to git.

### What it does differently

| Problem | Solution |
|---------|----------|
| Forget what you learned | SM-2 spaced repetition — cards woven into session transitions, not a separate review block |
| No exercise discipline | Learning output mode — Claude creates exercises but refuses to write code during the solve phase |
| Generic interview prep | Background research on your specific company/role; pattern-based progression (15 core patterns, not random problems) |
| Solutions don't transfer | Primitive extraction — after solving, decomposes into transferable building blocks and generates SR cards for those |
| Skip days, lose track | Missed-day handling, schedule adaptation, honest progress tracking |

### Modes

- **Technical** (coding, algorithms): file-based exercises with test cases, language-aware
- **Knowledge** (law, history, theory): JSON-backed spaced repetition, interstitial card review
- **Mixed**: both in one project

## Installation

```bash
git clone git@github.com:ettrickshepherd/studykit.git ~/dev/studykit

ln -sfn ~/dev/studykit/study-plan ~/.claude/skills/study-plan
ln -sfn ~/dev/studykit/study-session ~/.claude/skills/study-session
```

Verify:
```bash
ls -la ~/.claude/skills/study-plan/SKILL.md
ls -la ~/.claude/skills/study-session/SKILL.md
```

**Prerequisites**: Python 3.10+, [uv](https://docs.astral.sh/uv/). For coding exercises, you need the runtime for your language (Python comes with uv; JS/TS needs [Bun](https://bun.sh/)).

**Recommended** for coding sessions:
```
/output-style learning
```

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
| `progress <cards.json>` | Per-deck breakdown (total, due, mature, struggling, new) |
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

## Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Data storage | JSON files | Zero deps, git-friendly diffs, Claude reads/writes directly, scales fine for study-scale data |
| SR algorithm | SM-2 | Anki's foundation — simple, well-understood, sufficient for weeks-to-months timelines |
| Review style | Interstitial | No dedicated "card block" — cards woven into topic transitions, exercise breaks, warm-ups |
| Exercise model | File-based | User solves in their editor; two versions per concept (guided + from-scratch) |
| Living documents | Schedule + progress separate from plan | Plan records the commitment (immutable); schedule adapts; progress tracks reality |
| Daily notes | Write after every task | Context window safety valve — protects against compaction during long sessions |
