class ToolManager:
    def __init__(self):
        self.tools = {
            "web_research": {
                "enabled": False,
                "risk": "medium",
                "approval_required": True
            },
            "python": {
                "enabled": False,
                "risk": "high",
                "approval_required": True
            },
            "filesystem": {
                "enabled": False,
                "risk": "high",
                "approval_required": True
            },
            "database": {
                "enabled": False,
                "risk": "high",
                "approval_required": True
            },
            "git": {
                "enabled": False,
                "risk": "high",
                "approval_required": True
            },
            "server": {
                "enabled": False,
                "risk": "critical",
                "approval_required": True
            }
        }

    def list_tools(self):
        return self.tools

    def request_access(self, tool_name):
        if tool_name not in self.tools:
            return {
                "success": False,
                "message": "Tool not found."
            }

        tool = self.tools[tool_name]

        return {
            "success": True,
            "tool": tool_name,
            "enabled": tool["enabled"],
            "risk": tool["risk"],
            "approval_required": tool["approval_required"]
        }


if __name__ == "__main__":
    manager = ToolManager()

    print("🛠 Tool Manager فعال شد.")
    print("📋 ابزارهای ثبت‌شده:", len(manager.list_tools()))

    for name, tool in manager.list_tools().items():
        print(
            f"• {name} | "
            f"فعال: {tool['enabled']} | "
            f"ریسک: {tool['risk']} | "
            f"تأیید: {tool['approval_required']}"
        )

    print("\n🔐 آزمایش درخواست دسترسی:")

    result = manager.request_access("python")

    print("🛠 ابزار:", result["tool"])
    print("🔒 تأیید لازم:", result["approval_required"])
    print("⚙️ فعال:", result["enabled"])
