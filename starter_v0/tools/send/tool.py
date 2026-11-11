from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT, err


def send_telegram(
    text: str = "", confirmed: bool = False, *, expected_chat_id: str | None = None,
) -> dict[str, Any]:
    if confirmed is not True:
        return {
            "tool": "send_telegram",
            "status": "needs_confirmation",
            "message": "Only send after the user explicitly confirms.",
        }
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    try:
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not token or not chat_id:
            raise RuntimeError("Missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID env var")
        if expected_chat_id is not None and chat_id != expected_chat_id:
            raise RuntimeError("Đích Telegram đã đổi. Hãy tạo và xác nhận lại bản tin.")
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        return {"tool": "send_telegram", "status": "sent"}
    except Exception as exc:
        result = err("send_telegram", exc)
        if token:
            result["message"] = result["message"].replace(token, "[đã ẩn]")
        return result

