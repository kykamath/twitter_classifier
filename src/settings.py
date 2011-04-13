'''
Created on Mar 18, 2011

@author: kykamath
'''
from datetime import datetime
class Settings:
    twitterDataFolder = '/mnt/chevron/kykamath/data/twitter/'
    twitterUsersTweetsFolder = '%susers/tweets/'%twitterDataFolder
    twitterClassifierTrainingSetsFolder = '%sclassifier/training_sets/'%twitterDataFolder
    twitterClassifierTestSetsFolder = '%sclassifier/test_sets/'%twitterDataFolder
    twitterClassifierCombinedSetsFolder = '%sclassifier/combined_sets/'%twitterDataFolder
    
    usersToCrawl = '%susers/crawl/users_to_crawl'%twitterDataFolder
    
    twitter_api_time_format = '%a %b %d %H:%M:%S +0000 %Y'
    
    # Classifier data
    startTime=datetime(2011,3,19)
    endTime=datetime(2011,4,12)
    
    expertListSizes = xrange(50,550,50)

class DataType:
    raw = 'raw'