'''
    Python libary that utilizes Tealium Collect
'''
import requests
import sys
from random import randint
import time
import json
import gzip

class Tealium(object):

    '''
        Base class for the libary.
    '''
    EVENT_TYPE_ACTIVITY = "activity"
    EVENT_TYPE_CONVERSION = "conversion"
    EVENT_TYPE_DERIVED = "derived"
    EVENT_TYPE_INTERACTION = "interaction"
    EVENT_TYPE_VIEW = "view"


# argument labels for track call.
    TRACK_EVENT_TYPE = "eventType"
    TRACK_CALLBACK = "tealiumCallback"
    TRACK_DATA = "data"
    TRACK_TITLE = "title"

    LIBRARY_VERSION = "2.0.0"

    platformversion = ""
    if sys.version_info[:3] >= (3, 0):
        platformversion = 3.0
    else:
        platformversion = 2.7

    T_BASE_URL = 'https://collect.tealiumiq.com/event'

    '''
        Returns an instance of a Tealium object.
    '''

    def __init__(self, account, profile, environment=None, datasource=None):
        self.account = account
        self.profile = profile
        self.datasource = datasource
        self.environment = environment

    def generateRandomNumber(self):

        s = ''
        for i in range(16):
            s = s + str(randint(0, 9))
        return s

    def generateTimeStamp(self):

        return int(time.time())

    def isValidEventType(self, eventType):
        eventTypeArray = [self.EVENT_TYPE_VIEW,
                          self.EVENT_TYPE_DERIVED,
                          self.EVENT_TYPE_ACTIVITY,
                          self.EVENT_TYPE_CONVERSION,
                          self.EVENT_TYPE_INTERACTION]
        return (eventType in eventTypeArray)

    def trackEvent(self, title, eventtype=None, data={}, callback=None):

        '''
            Call with a title and optional dictionary to track an event in
            stream.

        Args:
            Title (String): A title for the event being tracked.

            EventType(optional String): (Tealium.EVENT_TYPE_CONVERSION,
                                    Tealium.EVENT_TYPE_DERIVED,
                                    Tealium.EVENT_TYPE_ACTIVITY,
                                    Tealium.EVENT_TYPE_VIEW,
                                    Tealium.EVENT_TYPE_INTERACTION )

            Data (optional dictionary): Add any additional data sources for the
                    corresponding event.

            Callback(optional callback):
                Args:
                    Info : Optional dictionary of data from call (i.e.
                        response headers, encoded Url String etc.)
                    Success: Whether completion succeeded or encountered
                        a failure.
                    Error: Error encounter, if any.
        '''

        if (eventtype is not None and self.isValidEventType):
            eventType = eventtype
        else:
            eventType = self.EVENT_TYPE_ACTIVITY

        randomNumber = self.generateRandomNumber()

        TRACK_URL = self.T_BASE_URL
        body = {
            'tealium_account': self.account,
            'tealium_profile': self.profile,
            'tealium_random': randomNumber,
            'event_name': title,
            'tealium_timestamp_epoch': self.generateTimeStamp(),
            'tealium_event': title,
            'tealium_event_type': eventType,
            'platform_name': 'python',
            'tealium_library_name': 'python',
            'tealium_library_version': self.LIBRARY_VERSION,
            'platform_version': self.platformversion
        }

        if self.environment is not None:
            body['tealium_environment'] = self.environment

        if self.datasource is not None:
            body['tealium_datasource'] = self.datasource
        
        if data is not None:
            body.update(data)

        postdata = json.dumps(body).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        try:
            postdata = gzip.compress(postdata)
            headers['Content-Encoding'] = 'gzip'
        except:
            print('Error trying to compress data. Proceeding without compression.')
        finally:
            r = requests.post(TRACK_URL, data=postdata, headers=headers)
        if callback is None:
            return
        infoDict = {"encoded-url": TRACK_URL, 'request-data': body}
        error = None

        try:
            r.raise_for_status()
        except Exception as e:
            error = e
        infoDict["response_headers"] = r.headers

        if error is None and 'X-Error' in r.headers:
            error = r.headers['X-Error']

        callback(infoDict, error is None, error)
