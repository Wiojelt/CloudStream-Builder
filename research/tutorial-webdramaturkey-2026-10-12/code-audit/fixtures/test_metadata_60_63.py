"""19 offline checks of historical tutorial metadata; NOT a CloudStream live test."""
import json, unittest
from pathlib import Path
from urllib.parse import urlparse
d=json.loads(Path(__file__).with_name('metadata_60_63.json').read_text(encoding='utf-8'))
def https_icon(x):
 p=urlparse(x);return p.scheme=='https' and bool(p.netloc) and p.username is None and p.password is None
def release_ready(v):return all(v.get(x) is True for x in ('cs3_download_verified','catalog_hash_verified','fresh_device_playback_verified'))
class TestVideoMetadata(unittest.TestCase):
 def test_01(self):self.assertIsInstance(d['version'],int)
 def test_02(self):self.assertGreater(d['version'],0)
 def test_03(self):self.assertGreater(d['version']+1,d['version'])
 def test_04(self):self.assertEqual(d['authors'],['kraptor'])
 def test_05(self):self.assertEqual(d['language'],'tr')
 def test_06(self):self.assertTrue(d['description'])
 def test_07(self):self.assertEqual(d['status'],1)
 def test_08(self):self.assertIn(d['status'],{0,1,2,3})
 def test_09(self):self.assertEqual(len(d['tvTypes']),len(set(d['tvTypes'])))
 def test_10(self):self.assertEqual(d['tvTypes'],['AsianDrama','Movie','Anime'])
 def test_11(self):self.assertTrue(https_icon(d['iconUrl']))
 def test_12(self):self.assertFalse(https_icon('http://bad.example/icon.png'))
 def test_13(self):self.assertFalse(https_icon('data:image/png;base64,xxx'))
 def test_14(self):self.assertEqual(d['video_commit_files'],4)
 def test_15(self):self.assertTrue(d['video_git_push_seen'])
 def test_16(self):self.assertFalse(release_ready(d))
 def test_17(self):self.assertFalse(release_ready(dict(cs3_download_verified=True,catalog_hash_verified=False,fresh_device_playback_verified=True)))
 def test_18(self):self.assertFalse(release_ready(dict(cs3_download_verified=True,catalog_hash_verified=True,fresh_device_playback_verified=False)))
 def test_19(self):self.assertTrue(release_ready(dict(cs3_download_verified=True,catalog_hash_verified=True,fresh_device_playback_verified=True)))
if __name__=='__main__':unittest.main()