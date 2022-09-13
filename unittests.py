import unittest
from tealium import Tealium


class TestTrackCalls(unittest.TestCase):

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
                                  "tealium_datasource",
                                  "tealium_random",
                                  "event_name",
                                  "tealium_timestamp_epoch",
                                  "tealium_session_id",
                                  "tealium_visitor_id",
                                  "tealium_event",
                                  "tealium_event_type"]

        sentData = info['request-data']
        for i in expectedDataSourceKeys:
            self.assertIn(i, sentData, 'expected key {} not in sent data')

    def test_trackEvent(self):
        t = Tealium('tealiummobile', 'demo', 'dev', datasource='unittest')
        d = {"foo": "bar", "tealium_visitor_id": "1234567890"}
        t.trackEvent("test",
                     data=d,
                     eventtype=Tealium.EVENT_TYPE_VIEW,
                     callback=self.tealiumCallback)
        t = None

    def test_randomNumber(self):
        t = Tealium('tealiummobile', 'demo', 'dev', datasource='unittest')
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
        t = Tealium('tealiummobile', 'demo', 'dev', datasource='unittest')
        uuid = t.getUUIDandSave()
        self.assertEqual(uuid, t.uuid, '{} is not expected {}'.format(uuid,
                                                                      t.uuid))
        t = None

    def testEventEndpoint(self):
        t = Tealium('tealiummobile', 'demo', 'dev', datasource='unittest')
        self.assertTrue(t.T_BASE_URL.startswith('https://collect.tealiumiq.com/event'))
        t = None

if __name__ == '__main__':
    unittest.main()
