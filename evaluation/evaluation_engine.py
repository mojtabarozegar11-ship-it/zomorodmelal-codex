class EvaluationEngine:
    def evaluate(self, knowledge, sources):
        score = 0.0
        reasons = []

        if sources:
            score += 0.4
            reasons.append("منبع ارائه شده است.")
        else:
            reasons.append("منبعی ارائه نشده است.")

        if len(sources) >= 2:
            score += 0.3
            reasons.append("چند منبع برای مقایسه وجود دارد.")

        if knowledge and len(knowledge.strip()) >= 20:
            score += 0.2
            reasons.append("اطلاعات دارای محتوای کافی است.")

        score += 0.1
        reasons.append("ساختار اولیه ارزیابی تکمیل شد.")

        if score >= 0.8:
            level = "high"
        elif score >= 0.5:
            level = "medium"
        else:
            level = "low"

        return {
            "score": round(min(score, 1.0), 2),
            "level": level,
            "verified": False,
            "reasons": reasons,
            "requires_review": True
        }


if __name__ == "__main__":
    evaluator = EvaluationEngine()

    result = evaluator.evaluate(
        "این یک دانش آزمایشی برای بررسی سیستم ارزیابی است.",
        ["source-1", "source-2"]
    )

    print("🧪 Evaluation Engine فعال شد.")
    print("📊 امتیاز:", result["score"])
    print("📈 سطح:", result["level"])
    print("✅ تأیید نهایی:", result["verified"])
    print("🔎 نیاز به بررسی:", result["requires_review"])

    for reason in result["reasons"]:
        print("•", reason)
