import unittest
from recommend import recommend, load_catalog

class RecommendationTests(unittest.TestCase):
    def setUp(self):
        self.catalog=load_catalog()
        self.ratings={"u":{"a":5},"v":{"a":5,"b":4},"w":{"a":4,"b":3}}
    def test_relevant_candidate_ranked_and_rated_items_excluded(self):
        result=recommend("u",self.ratings,[{"id":"a","title":"A"},{"id":"b","title":"B"},{"id":"c","title":"C"}])
        self.assertEqual([r["item"]["id"] for r in result],["b"])
        self.assertAlmostEqual(result[0]["score"],5)
        self.assertEqual(result[0]["evidence"][0]["source_item"],"a")
    def test_stable_order_and_limits(self):
        result=recommend("ava",{"ava":{"tea":5},"ben":{"tea":4,"coffee":4,"mug":4}},self.catalog,limit=1)
        self.assertEqual(len(result),1)
        self.assertEqual(recommend("ava",{"ava":{"tea":5},"ben":{"tea":4,"coffee":4,"mug":4}},self.catalog,limit=0),[])
    def test_validation_and_no_similarity(self):
        with self.assertRaises(ValueError): recommend("missing",self.ratings,self.catalog)
        with self.assertRaises(ValueError): recommend("u",self.ratings,self.catalog,limit=-1)
        with self.assertRaises(ValueError): recommend("u",{"u":{"a":6}},[{"id":"a","title":"A"}])
        self.assertEqual(recommend("u",{"u":{"a":5}},[{"id":"a"},{"id":"b"}]),[])
    def test_duplicate_catalog_ids_rejected(self):
        with self.assertRaises(ValueError): recommend("u",{"u":{}},[{"id":"a"},{"id":"a"}])

if __name__ == "__main__": unittest.main()
