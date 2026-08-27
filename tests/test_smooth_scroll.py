import sys
import unittest
from pathlib import Path
from unittest.mock import patch

if sys.platform == "win32":
    import PasteLink


class FakeUser32:
    def __init__(self):
        self.calls = []

    def mouse_event(self, *args):
        self.calls.append(args)


class SmoothScrollTests(unittest.TestCase):
    @unittest.skipUnless(sys.platform == "win32", "Windows mouse API only")
    def test_mouse_scroll_accepts_fractional_detents(self):
        fake = FakeUser32()

        with patch.object(PasteLink, "user32", fake):
            PasteLink.mouse_scroll(0.15)
            PasteLink.mouse_scroll(123 / 120)

        self.assertEqual(
            fake.calls,
            [(0x0800, 0, 0, 18, 0), (0x0800, 0, 0, 123, 0)],
        )

    def test_touch_scroll_is_frame_coalesced_without_detent_bursts(self):
        source = (Path(__file__).parents[1] / "PasteLink.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("function queueScroll(dy)", source)
        self.assertIn('sendRaw("MSCROLL "+(delta/120))', source)
        self.assertNotIn(
            'for(var i=0;i<cnt;i++)sendRaw("MSCROLL "+dir)',
            source,
        )


if __name__ == "__main__":
    unittest.main()
