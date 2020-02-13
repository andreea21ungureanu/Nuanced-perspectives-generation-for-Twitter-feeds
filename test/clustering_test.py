import unittest 

from src.clustering import divisive_hierarhical_clustering
from src.clustering import create_centroids

class TestClustering(unittest.TestCase): 
   
    def test_divisive_hierarhical_clustering(self):
        tweets = [{"tweet": "I love Brexit",
                    "emotions": {
                        "Excited": 0.4,
                        "Angry": 0.0,
                        "Sad": 0.0,
                        "Happy": 0.6,
                        "Bored": 0.0,
                        "Fear": 0.0
                        }
                    },
                    {
                    "tweet": "I hate Brexit!",
                    "emotions": {
                        "Excited": 0.3,
                        "Angry": 0.6,
                        "Sad": 0.1,
                        "Happy": 0.0,
                        "Bored": 0.0,
                        "Fear": 0.0
                    }
                    }]

        clustered_tweets_test = [{"tweet": "I hate Brexit!",
                    "emotions": {
                        "Excited": 0.3,
                        "Angry": 0.6,
                        "Sad": 0.1,
                        "Happy": 0.0,
                        "Bored": 0.0,
                        "Fear": 0.0
                    },
                    "cluster": 0
                },
                {"tweet": "I love Brexit",
                        "emotions": {
                            "Excited": 0.4,
                            "Angry": 0.0,
                            "Sad": 0.0,
                            "Happy": 0.6,
                            "Bored": 0.0,
                            "Fear": 0.0
                        },
                        "cluster": 1
                    }
                ]

        clustered_tweets = divisive_hierarhical_clustering(tweets, 2)
        print(clustered_tweets)
        self.assertEqual(clustered_tweets, clustered_tweets_test, "Tweets are clustered correctly")

    def test_create_centroids(self):
        clustered_tweets = [{"tweet": "I hate Brexit!",
                    "emotions": {
                        "Excited": 0.3,
                        "Angry": 0.6,
                        "Sad": 0.1,
                        "Happy": 0.0,
                        "Bored": 0.0,
                        "Fear": 0.0
                    },
                    "cluster": 0
                },
                {"tweet": "I love Brexit",
                        "emotions": {
                            "Excited": 0.4,
                            "Angry": 0.0,
                            "Sad": 0.0,
                            "Happy": 0.6,
                            "Bored": 0.0,
                            "Fear": 0.0
                        },
                        "cluster": 1
                    }
                ]
        centroids_test = {"0": {
                                "Excited": 0.3,
                                "Angry": 0.6,
                                "Sad": 0.1,
                                "Happy": 0.0,
                                "Bored": 0.0,
                                "Fear": 0.0
                            },
                            "1": {
                                "Excited": 0.4,
                                "Angry": 0.0,
                                "Sad": 0.0,
                                "Happy": 0.6,
                                "Bored": 0.0,
                                "Fear": 0.0
                            }}

        centroids = create_centroids(clustered_tweets)
        self.assertEqual(centroids, centroids_test, "Clusters are created correctly")

if __name__ == '__main__': 
    unittest.main() 