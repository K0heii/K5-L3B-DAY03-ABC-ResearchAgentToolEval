"""Streamlit chat UI. Run from starter_v0: python -m streamlit run app.py.

Runs the shared agent/tool loop and saves complete conversation transcripts.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from ui_transcripts import new_transcript, now_iso, save_transcript, transcript_json
from ui_agent import PROVIDERS, create_agent_session, run_live_turn, safe_error


TRANSCRIPTS_DIR = Path(__file__).resolve().parent / "transcripts"

SUGGESTIONS = (
    (
        "Tìm tài liệu",
        "Khám phá một chủ đề nghiên cứu.",
        "Tìm 5 bài nghiên cứu về ứng dụng AI trong giáo dục.",
    ),
    (
        "Đọc bài viết",
        "Bắt đầu từ một đường dẫn cụ thể.",
        "Tôi muốn tóm tắt một bài viết. Tôi cần cung cấp thông tin gì?",
    ),
    (
        "Theo dõi tin tức",
        "Tìm thông tin theo chủ đề và thời gian.",
        "Tìm tin tức về AI trong 7 ngày gần đây và kèm nguồn tham khảo.",
    ),
)


def new_conversation() -> None:
    st.session_state.messages = []
    st.session_state.transcript = new_transcript(mode=st.session_state.get("ui_mode", "live"))
    st.session_state.save_error = None
    st.session_state.pop("agent_session", None)
    st.session_state.pop("pending_prompt", None)


def save_current_transcript() -> None:
    try:
        save_transcript(TRANSCRIPTS_DIR, st.session_state.transcript)
    except OSError as exc:
        st.session_state.save_error = str(exc)
    else:
        st.session_state.save_error = None


def initialize_conversation() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "transcript" in st.session_state:
        return
    st.session_state.transcript = new_transcript(
        mode="demo" if st.session_state.messages else "live",
    )
    st.session_state.save_error = None
    # Preserve chats already open when this feature is loaded by hot reload.
    # Their original timestamps were not recorded, so leave them unknown.
    messages = st.session_state.messages
    for index in range(0, len(messages) - 1, 2):
        st.session_state.transcript["turns"].append({
            "turn_index": index // 2 + 1,
            "started_at": None,
            "ended_at": None,
            "user": messages[index]["content"],
            "assistant_text": messages[index + 1]["content"],
            "status": "demo_answered",
            "rounds": [],
            "tool_events": [],
        })
    if st.session_state.transcript["turns"]:
        save_current_transcript()


def choose_suggestion(prompt: str) -> None:
    st.session_state.pending_prompt = prompt


def demo_reply() -> str:
    return (
        "Đã nhận câu hỏi của bạn. Đây là **phản hồi mẫu** để thử giao diện; "
        "Agent chưa được kết nối và chưa có thao tác tìm kiếm nào được thực hiện.\n\n"
        "Bạn có thể gửi thêm tin nhắn để kiểm tra lịch sử hội thoại, "
        "hoặc chọn **Cuộc trò chuyện mới** ở thanh bên để bắt đầu lại."
    )


def render_sidebar() -> dict:
    transcript = st.session_state.transcript
    locked = bool(transcript["turns"])
    st.session_state.setdefault("ui_mode", transcript["mode"])
    with st.sidebar:
        st.markdown("### ◈ Research Desk")
        st.caption("Trợ lý nghiên cứu của nhóm")
        st.button(
            "＋ Cuộc trò chuyện mới",
            key="new_conversation",
            type="primary",
            width="stretch",
            on_click=new_conversation,
        )
        st.divider()
        st.markdown("**Phiên hiện tại**")
        turns = len(transcript["turns"])
        st.caption(f"{turns} câu hỏi đã gửi")
        mode = st.selectbox(
            "Chế độ", ("live", "demo"), key="ui_mode", disabled=locked,
            format_func=lambda value: "Agent thật" if value == "live" else "Demo giao diện",
        )
        with st.expander("Cấu hình Agent", expanded=not locked and mode == "live"):
            provider = st.selectbox("Provider", PROVIDERS, key="ui_provider", disabled=locked or mode == "demo")
            model = st.text_input(
                "Model", key="ui_model", placeholder="Để trống dùng model mặc định",
                disabled=locked or mode == "demo",
            )
            version = st.text_input("Phiên bản prompt/tool", value="v3", key="ui_version", disabled=locked or mode == "demo")
            history_window = st.number_input(
                "Số lượt trước giữ trong ngữ cảnh", min_value=1, max_value=20,
                value=5, key="ui_history", disabled=locked or mode == "demo",
            )
            max_tool_rounds = st.number_input(
                "Số vòng gọi tool tối đa mỗi lượt", min_value=1, max_value=10,
                value=4, key="ui_rounds", disabled=locked or mode == "demo",
            )
            st.caption("API key được đọc từ cấu hình trên máy chủ.")
        if locked:
            st.caption("Tạo cuộc trò chuyện mới để đổi cấu hình.")
        if transcript.get("model"):
            st.caption(f"{transcript['provider']} · {transcript['model']}")
        if mode == "demo":
            st.info("Bản thử giao diện · phản hồi mẫu")
        st.markdown("**Transcript**")
        if st.session_state.save_error:
            st.error("Chưa lưu được transcript. Bạn vẫn có thể tải JSON bên dưới.")
            st.button("Thử lưu lại", key="retry_save", on_click=save_current_transcript)
            with st.expander("Chi tiết lỗi lưu file"):
                st.code(st.session_state.save_error, language=None)
        elif transcript["turns"]:
            st.caption("Đã tự động lưu sau lượt chat gần nhất.")
        else:
            st.caption("Transcript sẽ được lưu khi bạn gửi câu hỏi đầu tiên.")
        st.download_button(
            "Tải transcript JSON",
            data=transcript_json(transcript).encode("utf-8"),
            file_name=f"{transcript['transcript_id']}.transcript.json",
            mime="application/json",
            key="download_transcript",
            disabled=not transcript["turns"],
            on_click="ignore",
            width="stretch",
        )
        with st.expander("Cách bắt đầu", expanded=True):
            st.markdown(
                "1. Nhập câu hỏi hoặc chọn một gợi ý.\n"
                "2. Nhấn Enter để gửi.\n"
                "3. Tiếp tục trò chuyện trong cùng phiên."
            )
        st.divider()
        st.caption(
            "Mỗi cuộc trò chuyện được lưu thành một file JSON riêng. "
            "Tạo cuộc trò chuyện mới sẽ giữ lại các file đã lưu."
        )
    return {
        "mode": mode, "provider_name": provider, "model": model, "version": version,
        "history_window": int(history_window), "max_tool_rounds": int(max_tool_rounds),
    }


def render_suggestions() -> None:
    st.markdown("#### Bạn muốn tìm hiểu điều gì?")
    st.write("Chọn một gợi ý bên dưới hoặc nhập câu hỏi của riêng bạn.")
    for column, (title, description, prompt) in zip(st.columns(3), SUGGESTIONS):
        with column, st.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(description)
            st.button(
                "Thử câu hỏi này",
                key=f"suggestion_{title}",
                width="stretch",
                on_click=choose_suggestion,
                args=(prompt,),
            )


def render_result(result: dict) -> None:
    if result["status"] in {"provider_error", "configuration_error"}:
        st.error(result["assistant_text"])
        with st.expander("Chi tiết lỗi", expanded=True):
            st.code(result["error"], language=None)
    else:
        st.markdown(result["assistant_text"] or "Model chưa trả về nội dung văn bản.")
    if result["status"] == "waiting_for_user":
        st.info("Agent đang chờ bạn bổ sung thông tin hoặc xác nhận ở ô chat bên dưới.")
    elif result["status"] == "max_tool_rounds":
        st.warning("Đã đạt giới hạn vòng xử lý của lượt này.")
    events = result.get("tool_events", [])
    if events:
        with st.expander(f"Hoạt động tool · {len(events)} lần gọi"):
            for index, event in enumerate(events, start=1):
                st.markdown(f"**{index}. {event['tool']}**")
                st.caption("Arguments")
                st.json(event.get("args", {}))
                st.caption("Kết quả")
                st.json(event.get("result", event))
                if isinstance(event.get("result"), dict) and event["result"].get("error"):
                    st.warning("Tool trả về lỗi; xem kết quả ở trên.")
    if result.get("rounds"):
        with st.expander("Chi tiết các vòng xử lý"):
            st.json(result["rounds"])


def process_prompt(prompt: str, settings: dict) -> None:
    transcript = st.session_state.transcript
    started_at = now_iso()

    if settings["mode"] == "demo":
        result = {"assistant_text": demo_reply(), "status": "demo_answered", "rounds": [], "tool_events": []}
    else:
        transcript["requested_configuration"] = {
            key: value for key, value in settings.items() if key != "mode"
        }
        try:
            if "agent_session" not in st.session_state:
                options = {key: value for key, value in settings.items() if key != "mode"}
                st.session_state.agent_session = create_agent_session(**options)
                transcript.update(st.session_state.agent_session.metadata)
        except Exception as exc:
            result = {
                "status": "configuration_error", "assistant_text": "Chưa khởi tạo được Agent. Kiểm tra cấu hình hoặc tạo phiên mới để đổi cấu hình.",
                "error": safe_error(exc), "rounds": [], "tool_events": [],
            }
        else:
            with st.status("Agent đang xử lý…", expanded=True) as activity:
                def show_round(record: dict) -> None:
                    names = ", ".join(call["name"] for call in record["tool_calls"])
                    st.write(f"Vòng {record['round']}: {names or 'soạn câu trả lời'}")

                result = run_live_turn(
                    st.session_state.agent_session, transcript["turns"], prompt,
                    on_round=show_round,
                )
                activity.update(
                    label="Đã xử lý xong" if result["status"] != "provider_error" else "Gặp lỗi từ provider",
                    state="error" if result["status"] == "provider_error" else "complete",
                    expanded=False,
                )
    ended_at = now_iso()
    transcript["turns"].append({
        "turn_index": len(transcript["turns"]) + 1,
        "started_at": started_at, "ended_at": ended_at, "user": prompt, **result,
    })
    transcript["updated_at"] = ended_at
    save_current_transcript()


def main() -> None:
    st.set_page_config(
        page_title="Research Desk | Research Agent",
        page_icon="🔎",
        layout="centered",
        initial_sidebar_state="auto",
    )
    initialize_conversation()

    settings = render_sidebar()
    if not st.session_state.transcript["turns"] and st.session_state.transcript["mode"] != settings["mode"]:
        st.session_state.transcript = new_transcript(mode=settings["mode"])
    st.caption("RESEARCH AGENT / KHÔNG GIAN NGHIÊN CỨU")
    st.title("Từ câu hỏi đến khám phá.")
    st.markdown("Một nơi để đặt câu hỏi, tìm tài liệu và theo dõi cuộc trò chuyện.")
    if settings["mode"] == "demo":
        st.info("Bạn đang thử giao diện với phản hồi mẫu. Chưa gọi Agent hoặc sử dụng API.", icon="ℹ️")
    else:
        st.caption("Agent dùng các tool nghiên cứu của nhóm và lưu lại hoạt động sau mỗi lượt chat.")
    st.divider()

    chat_area = st.container()
    typed_prompt = st.chat_input("Nhập câu hỏi nghiên cứu của bạn…", key="chat_prompt")
    prompt = (st.session_state.pop("pending_prompt", None) or typed_prompt or "").strip()
    with chat_area:
        for turn in st.session_state.transcript["turns"]:
            with st.chat_message("user"):
                st.markdown(turn["user"])
            with st.chat_message("assistant"):
                render_result(turn)

        if prompt:
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                process_prompt(prompt, settings)
            # Refresh the sidebar counter after storing the new turn.
            st.rerun()
        elif not st.session_state.transcript["turns"]:
            render_suggestions()


if __name__ == "__main__":
    main()
