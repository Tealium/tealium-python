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
    sessionId = ""
    platformversion = ""
    if sys.version_info[:3] >= (3, 0):
        platformversion = 3.0
    else:
        platformversion = 2.7

    T_BASE_URL = 'https://collect.tealiumiq.com/vdata/i.gif?tealium_library_' \
                 'name=python&tealium_library_version=1.0.0&platform_name=' \
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
                         'epoch={}tealium_session_id={}tealium_visitor_' \
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

    def trackEvent(self, title, data=None):

        '''
            Call with a title and optional dictionary to track an event in
            stream.

        Args:
            Title (String): A title for the event being tracked.

            Data (optional dictionary): Add any additional data sources for the
            corresponding event.
        '''
        randomNumber = self.generateRandomNumber()
        TRACK_URL = '{}tealium_account={}&tealium_profile={}&tealium_'\
                    'environment={}&tealium_vid={}&tealium_random='\
                    '{}&event_name={}&tealium_timestamp_epoch={}' \
                    '&tealium_session_id={}&tealium_'\
                    'visitor_id={}'.format(self.T_BASE_URL, self.account,
                                           self.profile, self.environment,
                                           self.uuid, randomNumber, title,
                                           self.generateTimeStamp(), sessionId,
                                           self.uuid)
        if data is not None:
            for key in data:
                if sys.version_info[:3] >= (3, 0):
                    TRACK_URL += '&' + urllib.parse.quote(str(key), safe='') \
                                 + '=' + urllib.parse.quote(str(data[key]),
                                                            safe='')
                else:
                    TRACK_URL += '&' + urllib.quote(str(key), safe='') \
                                 + '=' + urllib.quote(str(data[key]), safe='')
        r = requests.get(TRACK_URL)
        print (TRACK_URL)
        if r.status_code == 200:
            statusResult = True
        else:
            statusResult = False
        return statusResult
