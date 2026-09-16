class CommandRouter:
    """Translate Telegram commands into Master Agent requests."""

    def route(self, text):
        text = text.strip()

        if text == "/status":
            return {"type": "status"}

        if text.startswith("/mission"):
            return {
                "type": "mission",
                "goal": text.replace("/mission", "", 1).strip(),
            }

        if text.startswith("/approve"):
            return {
                "type": "approve",
                "action_id": text.replace("/approve", "", 1).strip(),
            }

        if text.startswith("/reject"):
            return {
                "type": "reject",
                "action_id": text.replace("/reject", "", 1).strip(),
            }

        return {"type": "message", "text": text}
