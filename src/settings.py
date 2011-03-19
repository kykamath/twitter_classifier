'''
Created on Mar 18, 2011

@author: kykamath
'''
from datetime import datetime
class Settings:
    twitterDataFolder = '/mnt/chevron/kykamath/data/twitter/'
    twitterUsersTweetsFolder = '%susers/tweets/'%twitterDataFolder
    usersToCrawl = '%susers/crawl/users_to_crawl'%twitterDataFolder
    
    twitter_api_time_format = '%a %b %d %H:%M:%S +0000 %Y'
    
    startTime=datetime(2011,3,9)
    endTime=datetime(2011,3,18)