import unittest
import tealium


class TestTrackCalls(unittest.TestCase):
    def test_enableCollect(self):
        self.assertTrue(tealium.enable("demo", "profile"))

    def test_trackCall(self):
        self.assertTrue(tealium.trackEvent("myTitle"))

    def testUUID(self):
        self.assertTrue(tealium.createVistorID())


if __name__ == '__main__':
    unittest.main()
