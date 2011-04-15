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
    twitterClassifierTrainedModelsFolder = '%sclassifier/trained_models/'%twitterDataFolder
#    twitterClassifierCombinedSetsFolder = '%sclassifier/combined_sets/'%twitterDataFolder
    
    usersToCrawl = '%susers/crawl/users_to_crawl'%twitterDataFolder
    
    twitter_api_time_format = '%a %b %d %H:%M:%S +0000 %Y'
    
    # Time data
    startTime=datetime(2011,3,19)
    endTime=datetime(2011,4,12)
    
    numberOfExperts = 125
    expertListSizes = xrange(50,550,50)
    
    
    # Experiments
    stats_folder = 'stats/'
    stats_to_determine_fixed_window_length = stats_folder+'stats_to_determine_fixed_window_length'
