import json
from pathlib import Path


with (Path(__file__).resolve().parent.parent / "languages.json").open(
    encoding="utf-8"
) as language_file:
    LANGUAGES = json.load(language_file)
