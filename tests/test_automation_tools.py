import tempfile
import unittest
from pathlib import Path

from automation_tools import extract_emails, move_jpg_files


class AutomationTests(unittest.TestCase):
    def test_moves_jpg_files_only(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            destination = Path(directory) / "destination"
            source.mkdir()
            (source / "photo.JPG").write_text("image")
            (source / "notes.txt").write_text("text")
            self.assertEqual(move_jpg_files(source, destination), 1)
            self.assertTrue((destination / "photo.JPG").exists())
            self.assertTrue((source / "notes.txt").exists())

    def test_extracts_unique_emails(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.txt"
            output = Path(directory) / "emails.txt"
            source.write_text("Contact A@Example.com and a@example.com, plus b@test.org")
            self.assertEqual(extract_emails(source, output), ["A@Example.com", "a@example.com", "b@test.org"])


if __name__ == "__main__":
    unittest.main()
