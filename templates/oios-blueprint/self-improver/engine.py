"""
Self-Improvement Engine — Pattern Detection for Wes EA

Reads lessons-queue.jsonl, detects patterns in corrections,
and suggests rules for CLAUDE.md's Learned Rules section.

Usage:
    python self-improver/engine.py              # Show digest
    python self-improver/engine.py --promote    # Mark pattern rules as promoted
"""

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

QUEUE_FILE = Path(__file__).parent / "lessons-queue.jsonl"


def load_lessons():
    """Load all lessons from the JSONL queue."""
    if not QUEUE_FILE.exists():
        return []
    lessons = []
    for i, line in enumerate(QUEUE_FILE.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            lessons.append(json.loads(line))
        except json.JSONDecodeError:
            print(f"  Warning: Skipping malformed line {i}")
    return lessons


def analyze(lessons):
    """Analyze lessons for patterns."""
    if not lessons:
        return None

    # Counts
    total = len(lessons)
    by_severity = Counter(l.get("severity", "unknown") for l in lessons)
    by_source = Counter(l.get("source", "unknown") for l in lessons)
    by_status = Counter(l.get("status", "pending") for l in lessons)

    # Tag frequency
    tag_counts = Counter()
    tag_lessons = defaultdict(list)
    for l in lessons:
        for tag in l.get("tags", []):
            tag_counts[tag] += 1
            tag_lessons[tag].append(l)

    # Patterns: tags appearing 3+ times
    patterns = {
        tag: tag_lessons[tag]
        for tag, count in tag_counts.items()
        if count >= 3
    }

    # Recent lessons (last 7 days)
    now = datetime.now(timezone.utc)
    recent = []
    for l in lessons:
        try:
            ts = datetime.fromisoformat(l["timestamp"].replace("Z", "+00:00"))
            age_days = (now - ts).days
            if age_days <= 7:
                recent.append(l)
        except (KeyError, ValueError):
            pass

    return {
        "total": total,
        "by_severity": by_severity,
        "by_source": by_source,
        "by_status": by_status,
        "tag_counts": tag_counts,
        "patterns": patterns,
        "recent_count": len(recent),
    }


def generate_rule_suggestion(tag, lessons):
    """Generate a suggested rule from a pattern."""
    # Find the most common lesson text for this tag
    lesson_texts = [l.get("lesson", "") for l in lessons]
    # Use the most recent lesson as the basis
    latest = lessons[-1]
    return f'[{tag.upper()}] {latest.get("lesson", "No lesson text")} — pattern detected ({len(lessons)} occurrences)'


def print_digest(analysis):
    """Print a human-readable digest."""
    print("=" * 60)
    print("  Self-Improvement Digest")
    print(f"  Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 60)
    print()

    # Overview
    print(f"Total lessons logged: {analysis['total']}")
    print(f"Last 7 days: {analysis['recent_count']}")
    print()

    # By severity
    print("By severity:")
    for sev in ["high", "medium", "low"]:
        count = analysis["by_severity"].get(sev, 0)
        if count:
            print(f"  {sev}: {count}")
    print()

    # By source
    print("By source:")
    for src, count in analysis["by_source"].most_common():
        print(f"  {src}: {count}")
    print()

    # Top tags
    if analysis["tag_counts"]:
        print("Top correction areas:")
        for tag, count in analysis["tag_counts"].most_common(10):
            marker = " ** PATTERN **" if count >= 3 else ""
            print(f"  {tag}: {count}{marker}")
        print()

    # Patterns and suggested rules
    if analysis["patterns"]:
        print("-" * 60)
        print("SUGGESTED RULES (patterns with 3+ occurrences)")
        print("-" * 60)
        print()
        print("Copy these into CLAUDE.md's Learned Rules section:")
        print()
        for i, (tag, lessons) in enumerate(analysis["patterns"].items(), 1):
            rule = generate_rule_suggestion(tag, lessons)
            print(f"  {i}. {rule}")
        print()
    else:
        print("No patterns detected yet (need 3+ lessons with the same tag).")
        print()

    # Status
    pending = analysis["by_status"].get("pending", 0)
    promoted = analysis["by_status"].get("promoted", 0)
    if pending:
        print(f"Pending lessons: {pending}")
    if promoted:
        print(f"Promoted to rules: {promoted}")


def promote_patterns(lessons, patterns):
    """Mark pattern lessons as promoted and rewrite the queue."""
    pattern_tags = set(patterns.keys())
    updated = 0
    for l in lessons:
        tags = set(l.get("tags", []))
        if tags & pattern_tags and l.get("status") == "pending":
            l["status"] = "promoted"
            updated += 1

    # Rewrite the file
    lines = [json.dumps(l, ensure_ascii=False) for l in lessons]
    QUEUE_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nPromoted {updated} lessons to 'promoted' status.")


def main():
    promote_mode = "--promote" in sys.argv

    lessons = load_lessons()
    if not lessons:
        print("No lessons logged yet. The EA will start capturing corrections here.")
        print(f"Queue file: {QUEUE_FILE}")
        return

    analysis = analyze(lessons)
    print_digest(analysis)

    if promote_mode and analysis["patterns"]:
        promote_patterns(lessons, analysis["patterns"])


if __name__ == "__main__":
    main()
