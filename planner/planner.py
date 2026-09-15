class Planner:
    def create_plan(self, goal):
        goal_lower = goal.lower()

        if "سایت" in goal_lower or "website" in goal_lower:
            actions = [
                "تحلیل هدف سایت",
                "بررسی ساختار و نیازمندی‌ها",
                "طراحی برنامه توسعه",
                "ایجاد وظایف اجرایی",
                "درخواست تأیید مالک"
            ]

        elif "اپ" in goal_lower or "app" in goal_lower:
            actions = [
                "تحلیل نیازمندی اپلیکیشن",
                "طراحی معماری",
                "طراحی رابط کاربری",
                "توسعه",
                "تست",
                "درخواست تأیید مالک"
            ]

        elif "بازی" in goal_lower or "game" in goal_lower:
            actions = [
                "تحلیل ایده بازی",
                "طراحی گیم‌پلی",
                "طراحی معماری",
                "توسعه",
                "تست",
                "درخواست تأیید مالک"
            ]

        else:
            actions = [
                "تحلیل هدف",
                "تحقیق و جمع‌آوری اطلاعات",
                "طراحی برنامه",
                "ایجاد وظایف",
                "درخواست تأیید مالک"
            ]

        return {
            "goal": goal,
            "status": "waiting_approval",
            "approval_required": True,
            "actions": actions
        }


if __name__ == "__main__":
    planner = Planner()

    plan = planner.create_plan("ساخت و توسعه سایت شرکت")

    print("🧠 Planner فعال شد.")
    print("🎯 هدف:", plan["goal"])
    print("🔐 نیاز به تأیید مالک:", plan["approval_required"])
    print("📋 برنامه:")

    for number, action in enumerate(plan["actions"], 1):
        print(f"{number}. {action}")
