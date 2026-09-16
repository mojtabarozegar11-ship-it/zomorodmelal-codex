"""Health checks for Master Agent components."""

import os


def check_environment():
    return {
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "deepseek": bool(os.getenv("DEEPSEEK_API_KEY")),
        "gemini": bool(os.getenv("GEMINI_API_KEY")),
        "claude": bool(os.getenv("ANTHROPIC_API_KEY")),
        "telegram": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
    }


def status():
    return {
        "runtime": "unknown",
        "providers": check_environment(),
        "approval_required": True,
    }
