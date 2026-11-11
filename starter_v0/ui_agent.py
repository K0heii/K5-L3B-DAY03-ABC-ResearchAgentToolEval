"""Connect the UI to the same provider/tool loop used by the CLI."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from chat import assistant_tool_message, run_model_tool_loop, tool_results_message
from env_loader import load_lab_env
from providers import make_provider
from providers.base import ToolCall
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).resolve().parent
PROVIDERS = ("openrouter", "openai", "anthropic", "gemini", "ollama")


@dataclass
class AgentSession:
    provider: Any
    system_prompt: str
    tools: list[dict[str, Any]]
    metadata: dict[str, Any]


def create_agent_session(
    provider_name: str, model: str, version: str,
    *, history_window: int = 5, max_tool_rounds: int = 4,
) -> AgentSession:
    load_lab_env(ROOT)
    provider = make_provider(provider_name)
    key_name = getattr(provider, "api_key_env", None)
    if key_name and not (os.getenv(key_name) or getattr(provider, "api_key_default", None)):
        raise ValueError(f"Thiếu {key_name}. Hãy cấu hình trong starter_v0/.env.")
    if not version.strip():
        raise ValueError("Hãy nhập phiên bản prompt/tool, ví dụ v3.")
    prompt_path, tools_path = ROOT / "artifacts/system_prompt.md", ROOT / "artifacts/tools.yaml"
    declarations = load_tool_declarations(tools_path)
    missing = [item["name"] for item in declarations if item["name"] not in TOOL_FUNCTIONS]
    if missing:
        raise ValueError(f"Tool chưa có code đăng ký: {', '.join(missing)}")
    metadata = {
        **artifact_version_dict(build_artifact_version(version.strip(), prompt_path, tools_path)),
        "provider": provider_name,
        "model": model.strip() or provider.default_model,
        "system_prompt": str(prompt_path),
        "tools": str(tools_path),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
    }
    return AgentSession(
        provider, prompt_path.read_text(encoding="utf-8"), to_openai_tools(declarations), metadata,
    )


def history_messages(turns: list[dict[str, Any]], window: int) -> list[dict[str, str]]:
    """Keep whole turns, including sources/tool results and clarification state."""
    messages: list[dict[str, str]] = []
    for turn in turns[-window:] if window > 0 else []:
        messages.append({"role": "user", "content": turn["user"]})
        for record in turn.get("rounds", []):
            calls = [ToolCall(**call) for call in record["tool_calls"]]
            if calls:
                messages.append(assistant_tool_message(record.get("assistant_text"), calls))
                if record.get("tool_results"):
                    messages.append(tool_results_message(record["tool_results"]))
            elif record.get("assistant_text"):
                messages.append({"role": "assistant", "content": record["assistant_text"]})
        if turn.get("assistant_text") and (
            not turn.get("rounds") or turn["status"] in {"waiting_for_user", "max_tool_rounds"}
        ) and turn["status"] not in {"provider_error", "configuration_error"}:
            messages.append({"role": "assistant", "content": turn["assistant_text"]})
    return messages


def safe_error(exc: Exception) -> str:
    message = f"{type(exc).__name__}: {exc}"
    for key, value in os.environ.items():
        if any(word in key.upper() for word in ("KEY", "TOKEN", "SECRET", "PASSWORD")) and len(value) >= 6:
            message = message.replace(value, "[đã ẩn]")
    return message


def run_live_turn(
    session: AgentSession, turns: list[dict[str, Any]], prompt: str,
    *, on_round: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    captured: list[dict[str, Any]] = []

    def capture(record: dict[str, Any]) -> None:
        captured.append(record)
        if on_round:
            on_round(record)

    messages = [
        {"role": "system", "content": session.system_prompt},
        *history_messages(turns, session.metadata["history_window"]),
        {"role": "user", "content": prompt},
    ]
    try:
        result = run_model_tool_loop(
            provider=session.provider, messages=messages, tools=session.tools,
            model=session.metadata["model"], max_tool_rounds=session.metadata["max_tool_rounds"],
            on_round=capture,
            previous_turn=turns[-1] if turns else None,
        )
    except Exception as exc:
        return {
            "status": "provider_error",
            "assistant_text": "Chưa nhận được câu trả lời từ model. Xem chi tiết lỗi bên dưới.",
            "error": safe_error(exc),
            "rounds": captured,
            "tool_events": [event for record in captured for event in record["tool_results"]],
        }
    if result["status"] == "max_tool_rounds":
        result["assistant_text"] = (
            "Đã đạt giới hạn số vòng gọi tool. Bạn có thể xem kết quả bên dưới "
            "và gửi yêu cầu tiếp theo, hoặc tạo phiên mới với giới hạn cao hơn."
        )
    return result
