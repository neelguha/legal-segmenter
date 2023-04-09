from legal_segmenter import __version__
from legal_segmenter.segmenter import Segmenter


def test_version():
    assert __version__ == "0.1.0"


# Test constants are downloaded
def test_segmenter_default_constants():
    seg = Segmenter()
    assert len(seg.constants) > 0


# TODO: add more tests
