import json
import unittest
from unittest.mock import patch
import catalog

SAMPLE = json.dumps([
    {'slug':'s1','title':'Agent Evals and Verification','url':'https://ai.engineer/talks/abc-1','event':'World Fair', 'topics':[{'name':'Evals'}], 'summary':'test'},
    {'slug':'s2','title':'Billing engine protection','url':'https://ai.engineer/talks/abc-2','topics':[{'name':'Payments'}], 'summary':'billing tests'},
    {'slug':'s3','title':'Creative video agent','url':'https://ai.engineer/talks/abc-3','topics':[], 'summary':'cinematic design'},
]).encode()

class CatalogTests(unittest.TestCase):
    def test_valid(self): self.assertEqual(3, len(catalog.parse_catalog(SAMPLE)))
    def test_schema_rejected(self):
        with self.assertRaises(ValueError): catalog.parse_catalog(b'{}')
    def test_malformed_record_skipped(self): self.assertEqual([], catalog.parse_catalog(b'[null,4,{"slug":"x"}]'))
    def test_offsite_rejected(self):
        v = json.dumps([{'slug':'a','title':'Agent','url':'https://evil.example/talk'}]).encode()
        self.assertEqual([], catalog.parse_catalog(v))
    def test_duplicates_dropped(self): self.assertEqual(3, len(catalog.parse_catalog(SAMPLE + b' ')))
    def test_duplicate_slug_dropped(self):
        data=json.loads(SAMPLE);data.append(data[0]);self.assertEqual(3,len(catalog.parse_catalog(json.dumps(data))))
    def test_topic_list_validation(self):
        x=[{'slug':'z','title':'hi','url':'https://ai.engineer/talks/z','topics':'wrong'}]
        self.assertEqual([], catalog.parse_catalog(json.dumps(x))[0]['topics'])
    def test_rank_area(self): self.assertEqual('s2', catalog.rank(catalog.parse_catalog(SAMPLE),'Recover / finance')[0]['slug'])
    def test_report_scope(self):
        x=catalog.build_report(SAMPLE,'Studios / BTWW',1)
        self.assertEqual('s3',x['talks'][0]['slug']);self.assertNotIn('summary',x['talks'][0]);self.assertEqual(64,len(x['source_sha256']))
    def test_disallow_external_url(self):
        with self.assertRaises(ValueError): catalog.get_data('https://example.com')
    def test_oversize(self):
        class Fake:
            def __enter__(self):return self
            def __exit__(self,*a): pass
            def geturl(self):return catalog.SOURCE
            def read(self,*a):return b'x'*(catalog.MAX_BYTES+1)
        with patch('catalog.urllib.request.urlopen',return_value=Fake()):
            with self.assertRaises(ValueError):catalog.get_data()
    def test_cross_origin_redirect(self):
        class Fake:
            def __enter__(self):return self
            def __exit__(self,*a):pass
            def geturl(self):return 'https://other.example/'
        with patch('catalog.urllib.request.urlopen',return_value=Fake()):
            with self.assertRaises(ValueError):catalog.get_data()

if __name__ == '__main__':unittest.main()
