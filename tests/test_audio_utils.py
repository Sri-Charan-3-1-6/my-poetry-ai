import unittest
from unittest.mock import patch
from pathlib import Path
from contextlib import nullcontext

import audio_utils

# Import the application module to test create_audio_from_text
import app


class TestAudioUtils(unittest.TestCase):
    def setUp(self):
        audio_utils.init_audio_cache()
        audio_utils.clean_audio_cache()

    def test_clean_text_for_tts_removes_markdown(self):
        raw = "**Bold** and *italic* with # headers\nNew line"
        cleaned = audio_utils.clean_text_for_tts(raw)
        self.assertNotIn("*", cleaned)
        self.assertNotIn("#", cleaned)
        self.assertIn("Bold", cleaned)
        self.assertIn("New line", cleaned)

    def test_validate_speed_within_profile_bounds(self):
        self.assertAlmostEqual(audio_utils.validate_speed(0.1, "male_1"), 0.8)
        self.assertAlmostEqual(audio_utils.validate_speed(5.0, "female_2"), 1.5)
        self.assertAlmostEqual(audio_utils.validate_speed(1.2, "neutral"), 1.2)

    def test_get_cache_path_consistency(self):
        text = "Testing cache path"
        params = (text, "en", 1.0, "neutral")
        path1 = audio_utils.get_cache_path(*params)
        path2 = audio_utils.get_cache_path(*params)
        self.assertEqual(path1, path2)
        self.assertTrue(path1.name.endswith(".mp3"))

    @patch("audio_utils.is_internet_available", return_value=True)
    @patch("gtts.gTTS")
    def test_create_audio_from_text_creates_cached_file(self, mock_tts, _mock_internet):
        def fake_save(path):
            Path(path).write_bytes(b"fake audio data")

        mock_tts.return_value.save.side_effect = fake_save

        with patch.object(app.st, "warning"), \
             patch.object(app.st, "error"), \
             patch.object(app.st, "info"), \
             patch.object(app.st, "spinner", return_value=nullcontext()):
            generated_path = app.create_audio_from_text("Hello world", "English", 1.0, "neutral")

        self.assertIsNotNone(generated_path)
        cache_path = Path(generated_path)
        self.assertTrue(cache_path.exists())
        self.assertGreater(cache_path.stat().st_size, 0)

        # Subsequent call should reuse cache and not invoke save again
        mock_tts.return_value.save.reset_mock()
        with patch.object(app.st, "warning"), \
             patch.object(app.st, "error"), \
             patch.object(app.st, "info"), \
             patch.object(app.st, "spinner", return_value=nullcontext()):
            second_path = app.create_audio_from_text("Hello world", "English", 1.0, "neutral")

        self.assertEqual(generated_path, second_path)
        mock_tts.return_value.save.assert_not_called()

        # Clean up generated file
        cache_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
