#!/usr/bin/env python
'''
 Sample script on how the Collect library call works. When initializing \
 Tealium instance replace 'tealiummobile' and 'demo' with your credentials. \
 Use trackEvent to create a call to Tealium Collect that relates to a \
 users'action that needs to be tracked. The dictionary for the trackEvent \
 call is optional, however a title is mandatory.
'''

from tealium import Tealium


def tealiumCallback(info, success, error=None):
    if error is not None:
        print (info, success, error)
        return
    print (info, success)

t = Tealium('tealiummobile', 'demo', 'dev')
d = {'testkey': 'testvalue'}
t.trackEvent('title', Tealium.EVENT_TYPE_VIEW, d, tealiumCallback)
t.trackEvent('title', d)
