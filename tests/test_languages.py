import json
import unittest
from pathlib import Path


class LanguageResourceTests(unittest.TestCase):
    def test_languages_have_matching_keys(self):
        resource_path = Path(__file__).parents[1] / ".archium" / "languages.json"
        with resource_path.open(encoding="utf-8") as language_file:
            languages = json.load(language_file)

        self.assertEqual(set(languages), {"en", "bg"})
        self.assertEqual(set(languages["en"]), set(languages["bg"]))
        self.assertEqual(languages["bg"]["column_title"], "Заглавие")


if __name__ == "__main__":
    unittest.main()