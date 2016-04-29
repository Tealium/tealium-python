#!/usr/bin/env python
'''
 Sample script on how the Collect library call works. When initializing \
 Tealium instance replace 'tealiummobile' and 'demo' with your credentials. \
 Use trackEvent to create a call to Tealium Collect that relates to a \
 users'action that needs to be tracked. The dictionary for the trackEvent \
 call is optional, however a title is mandatory.
'''

from tealium import Tealium

t = Tealium('tealiummobile', 'demo', 'dev')
d = {'tealium_anything': 'value3'}
t.resetSessionId()
t.trackEvent('title', d)
