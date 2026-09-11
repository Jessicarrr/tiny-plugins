#!/usr/bin/env python3
"""Print a concise execution trace for a local Codex rollout JSONL file."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path
from typing import Any, Iterable


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, indent=2)


def shorten(value: Any, limit: int = 500) -> str:
    result = " ".join(text(value).split())
    if len(result) <= limit:
        return result
    return result[: limit - 1].rstrip() + "…"


def field(value: Any, *names: str) -> Any:
    if not isinstance(value, dict):
        return None
    for name in names:
        if name in value and value[name] not in (None, ""):
            return value[name]
    return None


def timestamp(record: dict[str, Any]) -> str:
    return str(record.get("timestamp", ""))


def clock(value: str) -> str:
    if not value:
        return ""
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.astimezone().strftime("%H:%M:%S")
    except ValueError:
        return value[:8]


def content_text(content: Any) -> str:
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                value = field(item, "text", "input_text", "output_text")
                if value:
                    parts.append(str(value))
        return "\n".join(parts)
    return text(content)


def print_block(title: str, body: Any, indent: str = "  ") -> None:
    print(title)
    value = text(body).rstrip()
    if not value:
        print(indent + "(unavailable)")
        return
    for line in value.splitlines():
        print(indent + line)


def session_directory(date: str) -> Path:
    user_profile = os.environ.get("USERPROFILE")
    if not user_profile:
        user_profile = str(Path.home())
    return Path(user_profile) / ".codex" / "sessions" / date[0:4] / date[5:7] / date[8:10]


def select_rollout(date: str, index: int) -> Path:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise ValueError("date must use YYYY-MM-DD")
    if index < 0:
        raise IndexError("index must be zero or greater")
    directory = session_directory(date)
    if not directory.is_dir():
        raise FileNotFoundError(f"session directory not found: {directory}")
    files = list(directory.glob("rollout-*.jsonl"))
    if not files:
        raise FileNotFoundError(f"no rollout files found in: {directory}")

    def sort_time(path: Path) -> float:
        try:
            stat = path.stat()
            creation = getattr(stat, "st_birthtime", 0)
            return creation if creation and creation > 0 else stat.st_mtime
        except OSError:
            return 0

    files.sort(key=sort_time, reverse=True)
    try:
        return files[index]
    except IndexError as error:
        raise IndexError(f"index {index} is outside 0..{len(files) - 1}") from error


def extract_detail(record: dict[str, Any], details: dict[str, str]) -> None:
    payload = record.get("payload")
    if record.get("type") == "world_state" and isinstance(payload, dict):
        state = payload.get("state", payload)
        agents = state.get("agents_md") if isinstance(state, dict) else None
        if isinstance(agents, dict) and agents.get("text"):
            details.setdefault("AGENTS.md", agents["text"])
        details.setdefault("WORLD STATE", text(payload))
        for key, label in (("system_prompt", "SYSTEM PROMPT"), ("developer_prompt", "DEVELOPER PROMPT"),
                           ("permissions", "PERMISSION INSTRUCTIONS"), ("skills", "SKILLS CATALOGUE")):
            value = field(state, key) if isinstance(state, dict) else None
            if value:
                details.setdefault(label, text(value))
        if isinstance(state, dict):
            permission = state.get("permissions")
            if isinstance(permission, dict):
                details.setdefault("PERMISSION INSTRUCTIONS", text(permission))
            skill_state = state.get("skills") or state.get("skills_catalogue")
            if skill_state:
                details.setdefault("SKILLS CATALOGUE", text(skill_state))
            host_skills = state.get("host_skills")
            if isinstance(host_skills, dict) and host_skills.get("body"):
                details.setdefault("SKILLS CATALOGUE", str(host_skills["body"]))
    if record.get("type") == "turn_context" and isinstance(payload, dict):
        details.setdefault("PERMISSION INSTRUCTIONS", text({
            key: payload[key] for key in ("approval_policy", "approvals_reviewer", "permission_profile", "sandbox_policy")
            if key in payload
        }))
        details.setdefault("WORLD STATE", text(payload))
        for key, label in (("system_prompt", "SYSTEM PROMPT"), ("developer_prompt", "DEVELOPER PROMPT"),
                           ("permissions", "PERMISSION INSTRUCTIONS"), ("skills", "SKILLS CATALOGUE")):
            value = payload.get(key)
            if value:
                details.setdefault(label, text(value))
    if record.get("type") == "response_item" and isinstance(payload, dict):
        if payload.get("type") == "message" and payload.get("role") in {"system", "developer"}:
            details.setdefault(str(payload["role"]).upper() + " PROMPT", content_text(payload.get("content")))


def message_event(record: dict[str, Any]) -> tuple[str, str] | None:
    payload = record.get("payload")
    if not isinstance(payload, dict):
        return None
    kind = payload.get("type", record.get("type"))
    if record.get("type") == "response_item" and kind == "message":
        role = payload.get("role")
        if role not in {"user", "assistant"}:
            return None
        body = content_text(payload.get("content"))
        return role.upper(), body
    if record.get("type") == "event_msg" and kind == "user_message":
        return "USER", str(payload.get("message", ""))
    return None


def tool_event(record: dict[str, Any]) -> tuple[str, str, str] | None:
    payload = record.get("payload")
    if not isinstance(payload, dict):
        return None
    if record.get("type") == "response_item" and payload.get("type") in {
        "function_call", "local_shell_call", "custom_tool_call", "web_search_call"
    }:
        name = field(payload, "name", "tool_name", "type")
        arguments = field(payload, "arguments", "input", "command")
        return str(name), shorten(arguments, 700), str(payload.get("call_id", ""))
    if record.get("type") == "response_item" and payload.get("type") == "custom_tool_call_output":
        output = shorten(payload.get("output"), 500)
        return "RESULT", output, str(payload.get("call_id", ""))
    return None


def scan(path: Path, detailed: bool) -> tuple[dict[str, Any], dict[str, str], list[tuple[str, str, str]], list[str], dict[str, int]]:
    session: dict[str, Any] = {}
    details: dict[str, str] = {}
    events: list[tuple[str, str, str]] = []
    warnings: list[str] = []
    tokens: dict[str, int] = {}
    seen_messages: set[tuple[str, str]] = set()
    pending_tools: dict[str, int] = {}
    with path.open("r", encoding="utf-8", errors="replace") as source:
        for line_number, line in enumerate(source, 1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                warnings.append(f"line {line_number}: malformed JSON ({error.msg})")
                continue
            if not isinstance(record, dict):
                continue
            payload = record.get("payload")
            if record.get("type") == "session_meta" and isinstance(payload, dict):
                session.update(payload)
            if record.get("type") == "turn_context" and isinstance(payload, dict):
                for source, target in (("model", "model"), ("effort", "effort"), ("collaboration_mode", "collaboration")):
                    if payload.get(source):
                        session[target] = payload[source]
                for source in ("agent_role", "agent_nickname"):
                    if payload.get(source):
                        session[source] = payload[source]
            if record.get("type") == "event_msg" and isinstance(payload, dict) and payload.get("type") == "token_count":
                usage = payload.get("info", {}).get("total_token_usage", {})
                names = (("input_tokens", "input"), ("cached_input_tokens", "cached input"),
                         ("output_tokens", "output"), ("reasoning_output_tokens", "reasoning"),
                         ("total_tokens", "total"))
                for source, target in names:
                    if usage.get(source) is not None:
                        tokens[target] = int(usage[source])
            if record.get("type") == "token_usage_record" and isinstance(payload, dict):
                usage = payload.get("thread_token_usage") or payload.get("turn_token_usage") or payload.get("usage") or {}
                for source, target in (("input_tokens", "input"), ("cached_input_tokens", "cached input"),
                                       ("output_tokens", "output"), ("reasoning_output_tokens", "reasoning"),
                                       ("total_tokens", "total")):
                    if usage.get(source) is not None:
                        tokens[target] = int(usage[source])
            if detailed:
                extract_detail(record, details)
            message = message_event(record)
            if message:
                key = (message[0], message[1])
                if key not in seen_messages:
                    seen_messages.add(key)
                    events.append((timestamp(record), message[0], shorten(message[1], 1000)))
                continue
            tool = tool_event(record)
            if tool:
                if tool[0] == "RESULT" and tool[2] in pending_tools:
                    position = pending_tools[tool[2]]
                    events[position] = (events[position][0], events[position][1], events[position][2] + f"\n  result: {tool[1]}")
                else:
                    pending_tools[tool[2]] = len(events) if tool[2] else -1
                    events.append((timestamp(record), "TOOL", f"{tool[0]}\n  {tool[1]}"))
                continue
            if isinstance(payload, dict) and record.get("type") == "event_msg":
                event_type = payload.get("type", "")
                if event_type in {"task_started", "task_completed", "agent_spawned", "agent_completed", "agent_failed", "agent_interrupted"}:
                    events.append((timestamp(record), event_type.upper().replace("_", " "), shorten(payload, 800)))
    return session, details, events, warnings, tokens


def related_agents(path: Path, session: dict[str, Any]) -> list[dict[str, Any]]:
    """Read only session metadata from sibling rollouts to show basic children."""
    root_id = session.get("id") or session.get("session_id")
    if not root_id:
        return []
    result = []
    for candidate in path.parent.glob("rollout-*.jsonl"):
        if candidate == path:
            continue
        try:
            with candidate.open("r", encoding="utf-8", errors="replace") as source:
                for line in source:
                    record = json.loads(line)
                    if record.get("type") != "session_meta":
                        continue
                    payload = record.get("payload", {})
                    if payload.get("parent_thread_id") == root_id:
                        result.append(payload)
                    break
        except (OSError, json.JSONDecodeError):
            continue
    return result


def print_session(path: Path, session: dict[str, Any], children: list[dict[str, Any]]) -> None:
    stat = path.stat()
    print("SELECTED SESSION")
    print(f"  file: {path.name}")
    print(f"  timestamp: {dt.datetime.fromtimestamp(stat.st_mtime).isoformat(timespec='seconds')}")
    print("\nSESSION")
    values = (("repo", Path(str(session.get("cwd", ""))).name), ("branch", session.get("branch")),
              ("cwd", session.get("cwd")), ("cli", session.get("cli_version")),
              ("model", session.get("model")), ("effort", session.get("effort")),
              ("collaboration", session.get("collaboration")))
    for name, value in values:
        if value:
            print(f"  {name}: {value}")
    print("\nCONFIG")
    print(f"  AGENTS.md: {'loaded' if session.get('cwd') else 'unknown'}")
    for name in ("multi_agent_mode", "network"):
        if session.get(name):
            print(f"  {name}: {session[name]}")
    print("\nAGENTS")
    print("  /root")
    if session.get("model"):
        print(f"    model: {session['model']}")
    if session.get("effort"):
        print(f"    effort: {session['effort']}")
    source = session.get("source")
    if isinstance(source, dict) and source.get("subagent"):
        print("  agent type: unknown (custom type not present in session metadata)")
    for child in children:
        print("  └─ " + str(child.get("id") or child.get("session_id") or "child"))
        print(f"     agent type: {child.get('agent_role', 'unknown')}")
        if child.get("model"):
            print(f"     model: {child['model']}")
        if child.get("effort"):
            print(f"     effort: {child['effort']}")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="session date, YYYY-MM-DD")
    parser.add_argument("index", type=int, help="0 is the most recent session")
    parser.add_argument("detail", nargs="?", choices=["Detailed"], help="include full context")
    args = parser.parse_args(argv)
    try:
        path = select_rollout(args.date, args.index)
        session, details, events, warnings, tokens = scan(path, args.detail == "Detailed")
    except (FileNotFoundError, IndexError, ValueError, OSError) as error:
        parser.error(str(error))
        return 2

    if args.detail == "Detailed":
        print("DETAILED CONTEXT")
        for title, body in details.items():
            print_block(title, body)
        print()
    print_session(path, session, related_agents(path, session))
    for moment, kind, body in sorted(events, key=lambda item: item[0]):
        marker = "" if kind not in {"TOOL"} else ""
        print(f"\n{clock(moment)} {kind}{marker}")
        for line in body.splitlines():
            print(f"  {line}")
    if warnings:
        print("\nWARNINGS")
        for warning in warnings:
            print(f"  {warning}")
    if tokens:
        print("\nTOKENS")
        for name in ("input", "cached input", "output", "reasoning", "total"):
            if name in tokens:
                print(f"  {name}: {tokens[name]:,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
