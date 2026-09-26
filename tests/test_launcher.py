import tempfile
import unittest
import zipfile
import json
from unittest.mock import Mock
from pathlib import Path
from unittest.mock import patch

from launcher import ArchiumLauncher


class ArchiumLauncherTests(unittest.TestCase):
    def make_launcher(self, root_dir):
        launcher = ArchiumLauncher()
        launcher.root_dir = Path(root_dir)
        launcher.app_dir = launcher.root_dir / ".archium"
        launcher.version_file = launcher.app_dir / "version.json"
        return launcher

    def test_compares_numeric_version_parts(self):
        launcher = ArchiumLauncher()

        self.assertTrue(launcher.compare_versions("2.0.10", "2.0.9"))
        self.assertFalse(launcher.compare_versions("2.1", "2.1.0"))
        self.assertFalse(launcher.compare_versions("invalid", "2.1.0"))

    def test_finds_installed_supported_python(self):
        launcher = ArchiumLauncher()
        with patch("launcher.shutil.which", side_effect=lambda name: "C:/Python/python.exe" if name == "python" else None), patch(
            "launcher.subprocess.run",
            return_value=Mock(returncode=0, stdout="Python 3.11.9", stderr=""),
        ):
            self.assertEqual(launcher.find_python_command(), ["C:/Python/python.exe"])

    def test_rejects_python_older_than_supported_minimum(self):
        launcher = ArchiumLauncher()
        with patch("launcher.shutil.which", side_effect=lambda name: "C:/Python/python.exe" if name == "python" else None), patch(
            "launcher.subprocess.run",
            return_value=Mock(returncode=0, stdout="Python 3.7.9", stderr=""),
        ):
            self.assertIsNone(launcher.find_python_command())

    def test_installs_python_only_when_missing(self):
        launcher = ArchiumLauncher()
        with patch.object(launcher, "find_python_command", side_effect=[None, ["python"]]), patch.object(
            launcher, "install_python", return_value=["python"]
        ) as install_python:
            self.assertEqual(launcher.ensure_python(), ["python"])
        install_python.assert_called_once_with()

    def test_logging_is_safe_without_a_console(self):
        launcher = ArchiumLauncher()

        with patch("launcher.sys.stdout", None):
            launcher.log("silent windowed log")

    def test_gui_python_command_prefers_matching_pythonw(self):
        launcher = ArchiumLauncher()
        with tempfile.TemporaryDirectory() as temporary_dir:
            python_executable = Path(temporary_dir) / "python.exe"
            pythonw_executable = Path(temporary_dir) / "pythonw.exe"
            python_executable.touch()
            pythonw_executable.touch()

            self.assertEqual(
                launcher.gui_python_command([str(python_executable)]),
                [str(pythonw_executable)],
            )

    def test_new_github_release_triggers_download(self):
        launcher = ArchiumLauncher()
        launcher.current_version = "2.0.1"
        response = Mock()
        response.read.return_value = json.dumps({
            "tag_name": "v2.0.2",
            "assets": [{
                "name": "archium-v2.0.2.zip",
                "browser_download_url": "https://example.invalid/archium.zip",
            }],
        }).encode("utf-8")
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)

        with patch("launcher.urllib.request.urlopen", return_value=response), patch.object(
            launcher, "download_and_update", return_value=True
        ) as download:
            launcher.check_for_updates()

        download.assert_called_once_with("https://example.invalid/archium.zip", "2.0.2")
        self.assertEqual(launcher.current_version, "2.0.2")

    def test_update_preserves_user_data(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            root_dir = Path(temporary_dir)
            launcher = self.make_launcher(root_dir)
            launcher.app_dir.mkdir()
            (launcher.app_dir / "archium.py").write_text("old app", encoding="utf-8")
            (launcher.app_dir / "db").mkdir()
            (launcher.app_dir / "db" / "library.txt").write_text("my books", encoding="utf-8")
            (launcher.app_dir / "settings").mkdir()
            (launcher.app_dir / "settings" / "settings.json").write_text("{}", encoding="utf-8")

            archive_path = root_dir / "release.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("archium.py", "new app")
                archive.writestr("version.json", '{"version": "2.0.2"}')
                archive.writestr("classes_and_funcs/library.py", "new module")

            def download_archive(_url, destination):
                Path(destination).write_bytes(archive_path.read_bytes())

            with patch("launcher.urllib.request.urlretrieve", side_effect=download_archive):
                self.assertTrue(launcher.download_and_update("https://example.invalid/release.zip", "2.0.2"))

            self.assertEqual((launcher.app_dir / "archium.py").read_text(encoding="utf-8"), "new app")
            self.assertEqual((launcher.app_dir / "db" / "library.txt").read_text(encoding="utf-8"), "my books")
            self.assertTrue((launcher.app_dir / "settings" / "settings.json").is_file())
            self.assertEqual(launcher.load_current_version(), "2.0.2")

    def test_invalid_archive_leaves_current_app_intact(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            root_dir = Path(temporary_dir)
            launcher = self.make_launcher(root_dir)
            launcher.app_dir.mkdir()
            app_file = launcher.app_dir / "archium.py"
            app_file.write_text("current app", encoding="utf-8")

            archive_path = root_dir / "unsafe.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("../outside.txt", "not allowed")

            def download_archive(_url, destination):
                Path(destination).write_bytes(archive_path.read_bytes())

            with patch("launcher.urllib.request.urlretrieve", side_effect=download_archive):
                self.assertFalse(launcher.download_and_update("https://example.invalid/unsafe.zip", "2.0.2"))

            self.assertEqual(app_file.read_text(encoding="utf-8"), "current app")
            self.assertFalse((root_dir / "outside.txt").exists())


if __name__ == "__main__":
    unittest.main()