import tempfile
import unittest
from pathlib import Path

from autonomous_core.safe_builder import SafeBuilder
from autonomous_core.site_builder import SiteFeatureBuilder


class SiteFeatureBuilderTests(unittest.TestCase):
    def test_builds_real_site_files_for_sandbox(self):
        files = SiteFeatureBuilder().build("ساخت و توسعه سایت شرکت")
        self.assertEqual(set(files), {"site/index.html", "site/styles.css", "site/app.js"})
        self.assertIn("کشت و صنعت زمرد ملل", files["site/index.html"])
        with tempfile.TemporaryDirectory() as tmp:
            result = SafeBuilder(Path(tmp)).build(files)
            self.assertEqual(len(result), 3)
            self.assertTrue((Path(tmp) / "site" / "index.html").is_file())

    def test_requires_goal(self):
        with self.assertRaises(ValueError):
            SiteFeatureBuilder().build(" ")


if __name__ == "__main__":
    unittest.main()
