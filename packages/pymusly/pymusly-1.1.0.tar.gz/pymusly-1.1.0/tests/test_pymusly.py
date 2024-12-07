import pymusly as m
from tests.helper import is_windows_platform, is_macos_platform


def test_version():
    assert m.__version__ == "1.1.0"


def test_get_musly_version():
    assert m.get_musly_version() == "0.2"


def test_get_musly_decoders():
    decoders = m.get_musly_decoders()

    assert "none" in decoders

    if is_windows_platform():
        assert "mediafoundation" in decoders
    elif is_macos_platform():
        assert "coreaudio" in decoders


def test_get_musly_methods():
    assert m.get_musly_methods() == ["mandelellis", "timbre"]
