import unittest
from tealium import Tealium


class TestTrackCalls(unittest.TestCase):

    def test_enableCollect(self):
        t = Tealium.enable(Tealium('tealiummobile', 'demo', 'dev'))
        self.assertNotEqual(200, t, 'status result {} is unexpected'.format(t))
        t = None

    def tealiumCallback(self, info, success, error=None):
        self.assertTrue(success, info)
        self.assertIsNone(error, info)
        expectedDataSourceKeys = ["tealium_library_name",
                                  "tealium_library_version",
                                  "platform_name",
                                  "platform_version",
                                  "tealium_account",
                                  "tealium_profile",
                                  "tealium_environment",
                                  "tealium_random",
                                  "event_name",
                                  "tealium_timestamp_epoch",
                                  "tealium_session_id",
                                  "tealium_visitor_id",
                                  "tealium_event",
                                  "tealium_event_type"]

        sentURL = info['encoded-url']
        for i in expectedDataSourceKeys:
            self.assertIn(i, sentURL, 'expected key {} not in sent '
                                      'url {}'.format(i, sentURL))

    def test_trackEvent(self):
        t = Tealium('tealiummobile', 'demo', 'dev')
        d = {"foo": "bar"}
        t.trackEvent("test",
                     data=d,
                     eventtype=Tealium.EVENT_TYPE_VIEW,
                     callback=self.tealiumCallback)
        t = None

    def test_randomNumber(self):
        t = Tealium('tealiummobile', 'demo', 'dev')
        numberArray = []
        for i in range(1000):
            s = t.generateRandomNumber()
            self.assertNotIn(s, numberArray, '{} is repeated therefore'
                                             'sufficient randomness is not'
                                             'occuring'
                                             .format(s))
            numberArray.append(s)
        t = None

    def testUUID(self):
        t = Tealium('tealiummobile', 'demo', 'dev')
        uuid = t.getUUIDandSave()
        self.assertEqual(uuid, t.uuid, '{} is not expected {}'.format(uuid,
                                                                      t.uuid))
        t = None

if __name__ == '__main__':
    unittest.main()
