'''
    Python libary that utilizes Tealium Collect
'''
import requests
import uuid
import urllib
import pickle
import os
import sys
from random import randint
import time


class Tealium(object):

    '''
        Base class for the libary.
    '''
    EVENT_TYPE_CONVERSION = "conversion"
    EVENT_TYPE_DERIVED = "derived"
    EVENT_TYPE_ACTIVITY = "activity"
    EVENT_TYPE_VIEW = "view"
    EVENT_TYPE_INTERACTION = "interaction"

    sessionId = ""
    platformversion = ""
    if sys.version_info[:3] >= (3, 0):
        platformversion = 3.0
    else:
        platformversion = 2.7

    T_BASE_URL = 'https://collect.tealiumiq.com/vdata/i.gif?tealium_library_' \
                 'name=python&tealium_library_version=1.1.0&platform_name=' \
                 'python&platform_version={}&'.format(platformversion)

    '''
        Returns an instance of a Tealium object, path is optional.
    '''

    def __init__(self, account, profile, environment, path=None):
        self.account = account
        self.profile = profile
        self.path = path
        self.uuid = self.getUUIDandSave()
        self.sessionId = self.resetSessionId()
        self.environment = environment
        self.enable()

    def generateRandomNumber(self):

        s = ''
        for i in range(16):
            s = s + str(randint(0, 9))
        return s

    def generateTimeStamp(self):

        return time.time()

    def getUUIDandSave(self):
        '''
            Builds and saves a unique identifer for each instance.
        '''

        if self.path is None:
            self.path = os.path.join(os.getcwd(), 'tealium_vid')
        if not os.path.exists(self.path):
            path = open(self.path, 'wb')
            UUID = str(uuid.uuid1()).replace("-", "")
            pickle.dump(UUID, path)
            path.close()
        else:
            afile = open(self.path, 'rb')
            UUID = pickle.load(afile)
            afile.close()
        return UUID

    def resetSessionId(self):
        '''
            Used to reset tealium_session_id as a data source.
        '''

        global sessionId
        sessionId = int(round(time.time() * 1000))
        return sessionId

    def enable(self):
        '''
            Builds and calls the inital http request to Tealium Collect with
            provided profile and account name
        '''

        FINAL_BASE_URL = '{}tealium_account={}&tealium_profile={}&tealium_' \
                         'environment={}&tealium_vid={}&tealium_timestamp_' \
                         'epoch={}tealium_session_id={}&tealium_visitor_' \
                         'id={}'.format(self.T_BASE_URL, self.account,
                                        self.profile, self.environment,
                                        self.uuid, self.generateTimeStamp(),
                                        sessionId, self.uuid)
        r = requests.get(FINAL_BASE_URL)
        if r.status_code == 200:
            statusResult = True
        else:
            print('fail')
            statusResult = False
        return statusResult

    def trackEvent(self, title, eventType=None, data=None, tealiumCallback=None):
        '''
            Call with a title and optional dictionary to track an event in
            stream.

        Args:
            Title (String): A title for the event being tracked.

            EventType(String): (Tealium.EVENT_TYPE_CONVERSION,
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
        randomNumber = self.generateRandomNumber()
        if eventType is None:
            eventType = self.EVENT_TYPE_ACTIVITY

        TRACK_URL = '{}tealium_account={}&tealium_profile={}&tealium_'\
                    'environment={}&tealium_vid={}&tealium_random='\
                    '{}&event_name={}&tealium_timestamp_epoch={}' \
                    '&tealium_session_id={}&tealium_'\
                    'visitor_id={}&tealium_event={}&'\
                    'tealium_event_type={}'.format(self.T_BASE_URL,
                                                   self.account,
                                                   self.profile,
                                                   self.environment,
                                                   self.uuid,
                                                   randomNumber,
                                                   title,
                                                   self.generateTimeStamp(),
                                                   sessionId,
                                                   self.uuid,
                                                   title,
                                                   eventType)
        if data is not None:
            for key in data:
                if self.platformversion >= 3:
                    TRACK_URL += '&' + urllib.parse.quote(str(key), safe='') \
                        + '=' + urllib.parse.quote(str(data[key]),
                                                   safe='')
                else:
                    TRACK_URL += '&' + urllib.quote(str(key), safe='') \
                        + '=' + urllib.quote(str(data[key]), safe='')
        r = requests.get(TRACK_URL)

        if tealiumCallback is None:
            return

        infoDict = {"encoded-url": TRACK_URL}
        error = r.raise_for_status()

        if r.status_code != 200:
            tealiumCallback(infoDict, False, error)
            return

        infoDict["response_headers"] = r.headers

        if 'X-error' in r.headers:
            tealiumCallback(infoDict, False, error)
            return

        tealiumCallback(infoDict, True)
