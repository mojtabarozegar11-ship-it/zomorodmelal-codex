from __future__ import annotations

from typing import Dict


class SiteFeatureBuilder:
    """Generate a small, deterministic website feature set in the sandbox."""

    def build(self, goal: str) -> Dict[str, str]:
        goal = str(goal).strip()
        if not goal:
            raise ValueError("goal is required")
        return {
            "site/index.html": self._html(goal),
            "site/styles.css": self._css(),
            "site/app.js": self._js(),
        }

    @staticmethod
    def _html(goal: str) -> str:
        return f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>کشت و صنعت زمرد ملل</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <main>
    <section class="hero">
      <p class="eyebrow">ZOMOROD MELAL</p>
      <h1>کشت و صنعت زمرد ملل</h1>
      <p>زنجیره ارزش از پژوهش و تولید تا صنعت و بازار.</p>
      <span class="goal">هدف چرخه: {goal}</span>
    </section>
    <section class="cards">
      <article><h2>کشاورزی</h2><p>تولید، باغ، گلخانه و زنجیره محصولات.</p></article>
      <article><h2>صنعت</h2><p>فرآوری، بسته‌بندی و توسعه محصولات.</p></article>
      <article><h2>دانش و پژوهش</h2><p>دانش‌نامه، تحقیق و توسعه مبتنی بر داده.</p></article>
    </section>
  </main>
  <script src="app.js"></script>
</body>
</html>
'''

    @staticmethod
    def _css() -> str:
        return '''* { box-sizing: border-box; }
body { margin: 0; font-family: sans-serif; background: #f6f3ea; color: #173b2b; }
main { max-width: 1100px; margin: auto; padding: 48px 20px; }
.hero { padding: 56px 32px; border-radius: 24px; background: #fff; box-shadow: 0 12px 40px rgba(0,0,0,.08); }
.eyebrow { letter-spacing: .18em; font-weight: 700; }
h1 { font-size: clamp(2rem, 6vw, 4.5rem); margin: 12px 0; }
.hero p { font-size: 1.15rem; line-height: 1.9; }
.goal { display: inline-block; margin-top: 16px; padding: 10px 14px; border-radius: 12px; background: #eef5ee; }
.cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-top: 22px; }
.cards article { padding: 24px; background: #fff; border-radius: 18px; }
@media (max-width: 760px) { .cards { grid-template-columns: 1fr; } }
'''

    @staticmethod
    def _js() -> str:
        return '''document.documentElement.dataset.ready = "true";
'''
