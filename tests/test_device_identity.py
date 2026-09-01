import unittest
from pathlib import Path


SOURCE = (Path(__file__).parents[1] / "PasteLink.py").read_text(encoding="utf-8")


class DeviceIdentityTests(unittest.TestCase):
    def test_server_builds_a_stable_default_identity_and_sends_it_first(self):
        self.assertIn("def get_device_info():", SOURCE)
        self.assertIn("getpass.getuser()", SOURCE)
        self.assertIn("hashlib.sha256", SOURCE)
        self.assertIn("def build_device_message(info):", SOURCE)
        self.assertIn('DEVICE_MESSAGE = build_device_message(DEVICE_INFO)', SOURCE)

        handler = SOURCE[SOURCE.index("async def ws_handler(ws):"):]
        self.assertLess(
            handler.index("await ws.send(DEVICE_MESSAGE)"),
            handler.index("async for msg in ws"),
        )

    def test_connected_device_name_appears_beside_status(self):
        header = SOURCE[SOURCE.index('<div class=header>'):SOURCE.index('<!-- settings -->')]
        self.assertLess(header.index('id=status'), header.index('id=deviceName'))
        self.assertIn('class="device-name hidden"', header)

    def test_alias_is_edited_in_a_modal_and_saved_per_device(self):
        self.assertIn('id=deviceOverlay', SOURCE)
        self.assertIn('id=deviceNameInput', SOURCE)
        self.assertIn('id=deviceSave', SOURCE)
        self.assertIn('function applyDeviceInfo(info)', SOURCE)
        self.assertIn('function deviceStorageKey(id)', SOURCE)
        self.assertIn('localStorage.setItem(deviceStorageKey(deviceId)', SOURCE)
        self.assertIn('localStorage.removeItem(deviceStorageKey(deviceId))', SOURCE)


if __name__ == "__main__":
    unittest.main()
