'''
Created on Mar 18, 2011

@author: kykamath
'''
import os
from datetime import datetime

class Settings:
    applicationSourceDirectory = '/'.join(os.path.realpath(__file__).split('/')[:-1])+'/'
    applicationCommonFilesFolder = applicationSourceDirectory+'common_files/'
    
    globalClassifierData = applicationCommonFilesFolder+'gloabl_classifier_data'
    
    twitterDataFolder = '/mnt/chevron/kykamath/data/twitter/'
    twitterUsersTweetsFolder = '%susers/tweets/'%twitterDataFolder
    twitterClassifierTrainingSetsFolder = '%sclassifier/training_sets/'%twitterDataFolder
    twitterClassifierTestSetsFolder = '%sclassifier/test_sets/'%twitterDataFolder
    twitterClassifierTrainedModelsFolder = '%sclassifier/trained_models/'%twitterDataFolder
    twitterClassifierCollocationsFolder = '%sclassifier/collocations/'%twitterDataFolder
    twitterClassifierStreamingSetsFolder = '%sclassifier/streaming_datasets/'%twitterDataFolder
    
    usersToCrawl = '%susers/crawl/users_to_crawl'%twitterDataFolder
    
    twitter_api_time_format = '%a %b %d %H:%M:%S +0000 %Y'
    
    # Time data
    startTime=datetime(2011,3,19)
    endTime=datetime(2011,4,12)
    
    numberOfExperts = 125
    numberOfExpertsSecondSet = 375
    expertListSizes = xrange(50,550,50)
    
    #Collocations
    collocations_percentage_of_collocations_to_output = 0.01
    
    #Stream classifier.
    stream_classifier_class_probability_threshold = 0.60
    stream_classifier_decay_rate = 0.75
    
    # Experiments
    stats_folder = 'stats/'
    stats_to_determine_fixed_window_length = stats_folder+'stats_to_determine_fixed_window_length'
    stats_for_diminishing_aucm = stats_folder+'stats_for_diminishing_aucm'
    stats_to_compare_different_document_types = stats_folder+'stats_to_compare_different_document_types'
    stats_to_compare_collocations = stats_folder+'stats_to_compare_collocations'
    stats_to_observe_performance_by_relabeling_documents = stats_folder+'stats_to_observe_performance_by_relabeling_documents'
    stats_for_most_informative_features = stats_folder+'stats_for_most_informative_features'
    stats_for_training_data = stats_folder+'stats_for_training_data'