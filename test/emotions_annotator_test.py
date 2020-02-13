import unittest 

from src.emotions_annotator import EmotionsAnnotator
  
class TestEmotionsAnnotator(unittest.TestCase): 
    #TODO: TEST FOR READING/WRITING CORRECTLY TO FILES

    # Returns True or False.  
    # def test(self):         
    #     self.assertTrue(True) 

    def test_annotate(self):
        tweets = ["John le Carrie: \"We Brits are all nationalists now. Or so [Boris] Johnson would have us believe. But to be a nationalist you need enemies and the shabbiest trick in the Brexiteers\u2019 box was to make an enemy of Europe.\" https://t.co/EHAMvOzLlA",
              "Incredible reporting from @NicoHines &amp; great courage from @thedailybeast in publishing this. These messages with siginificant new info about Banks\u2019s r\u2019ship with Wikileaks &amp; Cambridge Analytica leaked in Nov, but no British news org reported on it...\nhttps://t.co/ADAQQsstDR"
             ]

        annotated_tweets_for_test = [{"tweet": "John le Carrie: \"We Brits are all nationalists now. Or so [Boris] Johnson would have us believe. But to be a nationalist you need enemies and the shabbiest trick in the Brexiteers\u2019 box was to make an enemy of Europe.\" https://t.co/EHAMvOzLlA",
                        "emotions": {
                            "Excited": 0.2577851425,
                            "Angry": 0.1524900477,
                            "Sad": 0.1487795139,
                            "Happy": 0.2628388403,
                            "Bored": 0.0,
                            "Fear": 0.1781064555
                            }
                        },
                        {"tweet": "Incredible reporting from @NicoHines &amp; great courage from @thedailybeast in publishing this. These messages with siginificant new info about Banks\u2019s r\u2019ship with Wikileaks &amp; Cambridge Analytica leaked in Nov, but no British news org reported on it...\nhttps://t.co/ADAQQsstDR",
                        "emotions": {
                            "Excited": 0.3115705996,
                            "Angry": 0.0912803042,
                            "Sad": 0.0213960821,
                            "Happy": 0.4949304459,
                            "Bored": 0.0141670891,
                            "Fear": 0.0666554792
                        }}]

        annotator = EmotionsAnnotator()
        annotated_tweets = annotator.annotate(tweets)

        self.assertEqual(annotated_tweets, annotated_tweets_for_test, "Tweets are annotated correctly")
  
if __name__ == '__main__': 
    unittest.main() 