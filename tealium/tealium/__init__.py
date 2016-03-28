import requests
import uuid
import urllib
import pickle
import os


class Tealium(object):
    '''
        Base class for the libary
    '''
    T_BASE_URL = "https://datacloud.tealiumiq.com/vdata/i.gif?origin=python&"

    def __init__(self, account, profile, path=None):
        '''
            returns an instance of a Tealium object, path is optional
        '''
        self.account = account
        self.profile = profile
        self.path = path
        self.uuid = self.getUUIDandSave()
        self.enable()

    def getUUIDandSave(self):
        '''
            Builds and saves a unique identifer for each instance
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

    def enable(self):
        '''
            Builds and calls the inital http request to Tealium Collect with \
             provided profile and account name
        '''
        BASE_URL = '{}tealium_account={}&tealium_profile={}&tealium_vid=' \
            '{}'.format(self.T_BASE_URL, self.account, self.profile,
                        self.uuid)
        r = requests.get(BASE_URL)
        if r.status_code == 200:
            statusResult = True
        else:
            statusResult = False
        return statusResult

    def trackEvent(self, mytitle, data=None):
        '''
            call with a title and optional dictionary to track an event in
            stream
        '''
        if data is None:
            TRACK_URL = '{}tealium_account={}&tealium_profile={}' \
                        '&tealium_vid={}&link_id={}'.format(self.T_BASE_URL,
                                                            self.account, self.
                                                            profile, self.uuid,
                                                            mytitle)
            r = requests.get(TRACK_URL)
        else:
            TRACK_URL = '{}tealium_account={}&tealium_profile={}' \
                        '&tealium_vid={}&link_id={}'.format(self.T_BASE_URL,
                                                            self.account, self.
                                                            profile, self.uuid,
                                                            mytitle)
            for key in data:
                TRACK_URL += '&' + urllib.quote(str(key)) + '=' \
                            + urllib.quote(str(data[key]))
                r = requests.get(TRACK_URL)
        if r.status_code == 200:
            statusResult = True
        else:
            statusResult = False
        return statusResult
