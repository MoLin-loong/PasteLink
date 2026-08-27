import unittest
from pathlib import Path


SOURCE = (Path(__file__).parents[1] / "PasteLink.py").read_text(encoding="utf-8")


class CombinedLayoutTests(unittest.TestCase):
    def test_trackpad_is_below_the_text_input_in_one_combined_view(self):
        kb_start = SOURCE.index('<div class=kb-view id=kbView>')
        kb_end = SOURCE.index('<!-- full keyboard -->')
        keyboard_view = SOURCE[kb_start:kb_end]

        self.assertLess(keyboard_view.index('<textarea id=msg'), keyboard_view.index('id=pad'))
        self.assertNotIn('id=mouseView', SOURCE)

    def test_mouse_buttons_flank_the_up_arrow(self):
        left_mouse = SOURCE.index('class="mouse-key mouse-left"')
        up_arrow = SOURCE.index('class="kb-key up"')
        right_mouse = SOURCE.index('class="mouse-key mouse-right"')

        self.assertLess(left_mouse, up_arrow)
        self.assertLess(up_arrow, right_mouse)

    def test_focus_switches_the_space_allocation(self):
        self.assertIn('.kb-view.mouse-active textarea', SOURCE)
        self.assertIn('.kb-view.mouse-active .trackpad-zone', SOURCE)
        self.assertIn('function activateInput()', SOURCE)
        self.assertIn('function activateMouse()', SOURCE)
        self.assertIn('msg.addEventListener("focus",activateInput)', SOURCE)


if __name__ == "__main__":
    unittest.main()
