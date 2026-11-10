"""Transcript storage for the UI, independent of model/provider dependencies."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from uuid import uuid4


LOCAL_TIMEZONE = timezone(timedelta(hours=7))


def now_iso() -> str:
    return datetime.now(LOCAL_TIMEZONE).isoformat(timespec="seconds")


def new_transcript(*, mode: str = "demo") -> dict[str, Any]:
    timestamp = now_iso()
    return {
        "schema_version": 1,
        "transcript_id": f"{mode}_{uuid4().hex}",
        "source": "streamlit",
        "mode": mode,
        "version": "ui-demo" if mode == "demo" else None,
        "provider": None,
        "model": None,
        "created_at": timestamp,
        "updated_at": timestamp,
        "turns": [],
    }


def transcript_json(transcript: dict[str, Any]) -> str:
    return json.dumps(transcript, ensure_ascii=False, indent=2) + "\n"


def save_transcript(directory: Path, transcript: dict[str, Any]) -> Path:
    """Replace one complete JSON file atomically, preserving it on write failure."""
    payload = transcript_json(transcript)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{transcript['transcript_id']}.transcript.json"
    temporary_path: Path | None = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=directory,
            prefix=".transcript-", suffix=".tmp", delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(payload)
        temporary_path.replace(target)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return target
