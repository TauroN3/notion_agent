#!/usr/bin/env python3
"""
Notion API Rate Limiter Gatekeeper

Enforces Notion API rate limits: average of 3 requests per second.
Use this before any curl/bash command that calls the Notion API.

Usage:
    # Check if request is allowed (exits 0 if allowed, 1 if should wait)
    python3 notion_rate_limiter.py check

    # Wait until a request is allowed (blocks until safe)
    python3 notion_rate_limiter.py wait

    # Record a request was made
    python3 notion_rate_limiter.py record

    # Check, wait if needed, and record (all-in-one before API call)
    python3 notion_rate_limiter.py gate

    # Show current status
    python3 notion_rate_limiter.py status

    # Reset the rate limiter state
    python3 notion_rate_limiter.py reset
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import List, Tuple

# Configuration based on Notion API docs
RATE_LIMIT_REQUESTS = 3  # requests per second (average)
WINDOW_SIZE_SECONDS = 1.0  # sliding window size
BURST_ALLOWANCE = 2  # extra requests allowed for short bursts
STATE_FILE = Path("/tmp/notion_rate_limiter_state.json")


def load_state() -> List[float]:
    """Load request timestamps from state file."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                return data.get("timestamps", [])
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_state(timestamps: List[float]) -> None:
    """Save request timestamps to state file."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"timestamps": timestamps}, f)


def cleanup_old_timestamps(timestamps: List[float], now: float) -> List[float]:
    """Remove timestamps older than the sliding window."""
    # Keep a 10-second history for accurate rate calculation
    cutoff = now - 10.0
    return [ts for ts in timestamps if ts > cutoff]


def calculate_rate(timestamps: List[float], now: float) -> float:
    """Calculate current request rate (requests per second)."""
    recent = [ts for ts in timestamps if ts > now - WINDOW_SIZE_SECONDS]
    return len(recent) / WINDOW_SIZE_SECONDS


def get_wait_time(timestamps: List[float], now: float) -> float:
    """Calculate how long to wait before next request is allowed."""
    recent = [ts for ts in timestamps if ts > now - WINDOW_SIZE_SECONDS]
    max_allowed = RATE_LIMIT_REQUESTS + BURST_ALLOWANCE

    if len(recent) < max_allowed:
        return 0.0

    # Wait until the oldest request in the window expires
    oldest_in_window = min(recent)
    wait_time = (oldest_in_window + WINDOW_SIZE_SECONDS) - now
    return max(0.0, wait_time)


def check_rate_limit() -> Tuple[bool, float, str]:
    """
    Check if a request can be made now.
    Returns: (allowed, wait_time, message)
    """
    now = time.time()
    timestamps = load_state()
    timestamps = cleanup_old_timestamps(timestamps, now)

    wait_time = get_wait_time(timestamps, now)
    current_rate = calculate_rate(timestamps, now)

    if wait_time == 0:
        return (True, 0.0, f"✓ Request allowed (current rate: {current_rate:.1f}/s)")
    else:
        return (False, wait_time, f"⏳ Rate limit: wait {wait_time:.2f}s (current rate: {current_rate:.1f}/s)")


def record_request() -> str:
    """Record that a request was made."""
    now = time.time()
    timestamps = load_state()
    timestamps = cleanup_old_timestamps(timestamps, now)
    timestamps.append(now)
    save_state(timestamps)
    return f"✓ Recorded request at {now:.3f}"


def wait_for_allowance() -> str:
    """Wait until a request is allowed, then return."""
    while True:
        allowed, wait_time, msg = check_rate_limit()
        if allowed:
            return msg
        print(f"⏳ Waiting {wait_time:.2f}s for rate limit...", file=sys.stderr)
        time.sleep(wait_time + 0.05)  # Small buffer


def gate_request() -> str:
    """All-in-one: check, wait if needed, and record the request."""
    wait_msg = wait_for_allowance()
    record_msg = record_request()
    return f"{wait_msg}\n{record_msg}"


def get_status() -> str:
    """Get current rate limiter status."""
    now = time.time()
    timestamps = load_state()
    timestamps = cleanup_old_timestamps(timestamps, now)

    current_rate = calculate_rate(timestamps, now)
    allowed, wait_time, _ = check_rate_limit()

    recent_1s = len([ts for ts in timestamps if ts > now - 1.0])
    recent_5s = len([ts for ts in timestamps if ts > now - 5.0])
    recent_10s = len([ts for ts in timestamps if ts > now - 10.0])

    status_lines = [
        "Notion API Rate Limiter Status",
        "=" * 35,
        f"Rate limit: {RATE_LIMIT_REQUESTS} req/s (avg)",
        f"Burst allowance: +{BURST_ALLOWANCE} requests",
        "",
        f"Current rate: {current_rate:.2f} req/s",
        f"Requests (last 1s): {recent_1s}",
        f"Requests (last 5s): {recent_5s}",
        f"Requests (last 10s): {recent_10s}",
        "",
        f"Can send now: {'Yes ✓' if allowed else 'No ✗'}",
    ]

    if not allowed:
        status_lines.append(f"Wait time: {wait_time:.2f}s")

    return "\n".join(status_lines)


def reset_state() -> str:
    """Reset the rate limiter state."""
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    return "✓ Rate limiter state reset"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "check":
        allowed, wait_time, msg = check_rate_limit()
        print(msg)
        sys.exit(0 if allowed else 1)

    elif command == "wait":
        msg = wait_for_allowance()
        print(msg)

    elif command == "record":
        msg = record_request()
        print(msg)

    elif command == "gate":
        msg = gate_request()
        print(msg)

    elif command == "status":
        print(get_status())

    elif command == "reset":
        msg = reset_state()
        print(msg)

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
