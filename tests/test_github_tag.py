"""Safety regressions for Aikya GitHub tag lookup (no network access)."""
from __future__ import annotations
import io
import sys
import unittest
from pathlib import Path
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts/ci"))
import github_tag

REPO="jlema0590/aikya-harness"
TAG="v5.9.1"
SHA="a"*40
OTHER="b"*40


class MockResponse:
    def __init__(self, data):
        import json
        self.data=json.dumps(data).encode("utf-8")
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def read(self):return self.data


class GitHubTagTests(unittest.TestCase):
    def test_404_is_missing_even_when_server_returns_error_body(self):
        def opener(req,timeout):
            raise HTTPError(req.full_url,404,"Not Found",{},io.BytesIO(b'{"message":"Not Found"}'))
        result=github_tag._get_json(REPO,"git/ref/tags/"+TAG,"token",
                                      allow_not_found=True,opener=opener)
        self.assertIsNone(result)
        def getter(path,allow_missing):
            return github_tag._get_json(REPO,path,"token",
                         allow_not_found=allow_missing,opener=opener)
        self.assertEqual("missing",github_tag.compare_tag(REPO,TAG,SHA,"token",getter=getter))

    def test_403_does_not_get_mistaken_for_missing(self):
        def opener(req,timeout):
            raise HTTPError(req.full_url,403,"Forbidden",{},io.BytesIO(b'{"message":"API rate limit"}'))
        with self.assertRaisesRegex(github_tag.TagError,"HTTP 403"):
            github_tag._get_json(REPO,"git/ref/tags/"+TAG,"token",
                                  allow_not_found=True,opener=opener)

    def test_401_and_500_are_errors(self):
        for status in (401,500):
            with self.subTest(status=status):
                def opener(req,timeout):
                    raise HTTPError(req.full_url,status,"Failure",{},io.BytesIO(b'{}'))
                with self.assertRaisesRegex(github_tag.TagError,"HTTP "+str(status)):
                    github_tag._get_json(REPO,"git/ref/tags/"+TAG,"token",
                                         allow_not_found=True,opener=opener)

    def test_lightweight_tag_matches_commit(self):
        def getter(path,allow_missing):
            return {"object":{"type":"commit","sha":SHA}}
        self.assertEqual("match",github_tag.compare_tag(REPO,TAG,SHA,"token",getter=getter))

    def test_lightweight_tag_mismatch_is_not_moved(self):
        def getter(path,allow_missing):
            return {"object":{"type":"commit","sha":OTHER}}
        with self.assertRaisesRegex(github_tag.TagError,"Conflicto real"):
            github_tag.compare_tag(REPO,TAG,SHA,"token",getter=getter)

    def test_annotated_tag_is_peeled_to_commit(self):
        paths=[]
        def getter(path,allow_missing):
            paths.append(path)
            if path=="git/ref/tags/"+TAG:
                return {"object":{"type":"tag","sha":OTHER}}
            if path=="git/tags/"+OTHER:
                return {"object":{"type":"commit","sha":SHA}}
            raise AssertionError(path)
        self.assertEqual("match",github_tag.compare_tag(REPO,TAG,SHA,"token",getter=getter))
        self.assertEqual(["git/ref/tags/"+TAG,"git/tags/"+OTHER],paths)

    def test_nested_annotated_tag_is_supported(self):
        third="c"*40
        table={"git/ref/tags/"+TAG:{"object":{"type":"tag","sha":OTHER}},
               "git/tags/"+OTHER:{"object":{"type":"tag","sha":third}},
               "git/tags/"+third:{"object":{"type":"commit","sha":SHA}}}
        self.assertEqual("match",github_tag.compare_tag(REPO,TAG,SHA,"token",
                         getter=lambda path,allow_missing:table[path]))

    def test_null_object_on_success_is_an_error(self):
        for result in ({"object":{"type":"commit","sha":None}},
                       {"object":None},{"message":"Not Found"}):
            with self.subTest(result=result),self.assertRaises(github_tag.TagError):
                github_tag.compare_tag(REPO,TAG,SHA,"token",
                                      getter=lambda path,allow_missing:result)

    def test_missing_annotation_target_is_an_error_not_missing(self):
        def getter(path,allow_missing):
            return {"object":{"type":"tag","sha":OTHER}} if allow_missing else None
        with self.assertRaisesRegex(github_tag.TagError,"anotado"):
            github_tag.compare_tag(REPO,TAG,SHA,"token",getter=getter)

    def test_host_ref_and_sha_parameters_are_validated(self):
        for repo,tag,sha in [("invalid",TAG,SHA),(REPO,"../x",SHA),
                             (REPO,TAG,"null"),(REPO,"v05.9.1",SHA)]:
            with self.subTest(repo=repo,tag=tag,sha=sha),self.assertRaises(github_tag.TagError):
                github_tag.compare_tag(repo,tag,sha,"token",getter=lambda p,m:None)

    def test_workflow_never_masks_tag_lookup_errors(self):
        workflow=(ROOT/".github/workflows/release.yml").read_text(encoding="utf-8")
        self.assertNotIn("--jq '.object.sha' 2>/dev/null || true",workflow)
        self.assertIn("github_tag.py",workflow)
        self.assertIn("--target \"$GITHUB_SHA\"",workflow)
        self.assertNotIn("gh api -X POST",workflow)


if __name__=="__main__":
    unittest.main()
