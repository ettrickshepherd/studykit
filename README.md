# studykit

Two coordinating Claude Code skills for structured self-study: plan creation and daily sessions with adaptive spaced repetition.

## Skills

### `/study-plan`
Structured interview → research → day-by-day study plan with commitment tracking. Creates a project directory with JSON-backed data files, living schedule, and progress reports.

### `/study-session`
Daily study sessions with interstitial spaced repetition (SM-2), coding exercises, progress tracking, and honest assessment. Reads the plan, adapts to your pace, and holds you to what you committed to.

## Installation

Clone and symlink into `~/.claude/skills/`:

```bash
git clone git@github.com:bengaskin/studykit.git ~/dev/studykit

# Symlink both skills
ln -sfn ~/dev/studykit/study-plan ~/.claude/skills/study-plan
ln -sfn ~/dev/studykit/study-session ~/.claude/skills/study-session
```

## Modes

- **Technical** (coding, algorithms): file-based exercises, test-driven practice
- **Knowledge** (law, history, theory): JSON-backed spaced repetition, interstitial card review
- **Mixed**: both in one project

## How It Works

1. `/study-plan` — interviews you, researches the topic, builds a day-by-day schedule with specific time commitments
2. `/study-session` — loads your plan, checks where you left off, runs the session (teaching + exercises + SR cards woven throughout), writes daily notes, tracks everything
3. Data lives in your study project directory as JSON files — git-friendly, zero dependencies

## Dependencies

None. All scripts use Python stdlib only (`json`, `datetime`, `pathlib`). Run with `uv run python3`.
