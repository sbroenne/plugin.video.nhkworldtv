"""Tests for vod module"""

from unittest.mock import patch

from lib import vod


def test_extract_images_dict_landscape():
    """Test extract_images with dict containing landscape images"""
    images_obj = {"landscape": [{"url": "thumb.jpg"}, {"url": "fanart.jpg"}]}
    thumb, fanart = vod.extract_images(images_obj)
    assert thumb == "thumb.jpg"
    assert fanart == "fanart.jpg"


def test_extract_images_dict_single_image():
    """Test extract_images with dict containing single image"""
    images_obj = {"landscape": [{"url": "single.jpg"}]}
    thumb, fanart = vod.extract_images(images_obj)
    assert thumb == "single.jpg"
    assert fanart == "single.jpg"


def test_extract_images_dict_empty_landscape():
    """Test extract_images with empty landscape array"""
    images_obj: dict[str, list[dict[str, str]]] = {"landscape": []}
    thumb, fanart = vod.extract_images(images_obj)
    assert thumb == ""
    assert fanart == ""


def test_extract_images_list():
    """Test extract_images with list of images"""
    images_obj = [{"url": "thumb.jpg"}, {"url": "fanart.jpg"}]
    thumb, fanart = vod.extract_images(images_obj)
    assert thumb == "thumb.jpg"
    assert fanart == "fanart.jpg"


def test_extract_images_list_single():
    """Test extract_images with single image in list"""
    images_obj = [{"url": "single.jpg"}]
    thumb, fanart = vod.extract_images(images_obj)
    assert thumb == "single.jpg"
    assert fanart == "single.jpg"


def test_extract_images_empty_list():
    """Test extract_images with empty list"""
    images_obj: list[dict[str, str]] = []
    thumb, fanart = vod.extract_images(images_obj)
    assert thumb == ""
    assert fanart == ""


def test_extract_images_none():
    """Test extract_images with None"""
    images_obj = None
    thumb, fanart = vod.extract_images(images_obj)
    assert thumb == ""
    assert fanart == ""


def test_extract_images_list_with_none_elements():
    """Test extract_images with list containing None elements"""
    images_obj = [None, {"url": "image.jpg"}]
    thumb, fanart = vod.extract_images(images_obj)
    # Should handle None gracefully
    assert isinstance(thumb, str)
    assert isinstance(fanart, str)


def test_get_episode_list_invalid_api():
    """Test get_episode_list with invalid API method"""
    episodes = vod.get_episode_list("invalid_method", "None", 0)
    assert episodes == []


def test_resolve_vod_episode_empty_id():
    """Test resolve_vod_episode with empty vod_id"""
    episode = vod.resolve_vod_episode("")
    assert episode is None


def test_resolve_vod_episode_none_id():
    """Test resolve_vod_episode with None vod_id"""
    episode = vod.resolve_vod_episode(None)
    assert episode is None


def test_resolve_vod_episode_invalid_id():
    """Test resolve_vod_episode with invalid vod_id"""
    episode = vod.resolve_vod_episode("invalid_nonexistent_id_12345")
    assert episode is None


# Tests with mocked API responses


@patch("lib.vod.url.get_json")
def test_get_episode_list_with_valid_response(mock_get_json):
    """Test get_episode_list with successful API response"""
    mock_get_json.return_value = {
        "items": [
            {
                "id": "episode1",
                "title": "Episode Title",
                "subtitle": "Episode Subtitle",
                "description": "Episode description",
                "images": {"landscape": [{"url": "thumb.jpg"}, {"url": "fanart.jpg"}]},
                "movie_duration": 1800,
                "pgm_no": 1,
                "onair": 1609459200000,
                "vod_to": 1609545600000,
            }
        ]
    }

    episodes = vod.get_episode_list("homepage_ondemand", "None", 0)
    assert len(episodes) == 1
    assert episodes[0].title == "Episode Title - Episode Subtitle"
    assert episodes[0].vod_id == "episode1"
    assert episodes[0].duration == 1800


@patch("lib.vod.url.get_json")
def test_get_episode_list_show_subtitle_only(mock_get_json):
    """Test get_episode_list with show_only_subtitle=1"""
    mock_get_json.return_value = {
        "items": [
            {
                "id": "episode1",
                "title": "Episode Title",
                "subtitle": "Episode Subtitle",
                "description": "Description",
                "images": {},
                "movie_duration": 1800,
            }
        ]
    }

    episodes = vod.get_episode_list("homepage_ondemand", "None", 1)
    assert len(episodes) == 1
    assert episodes[0].title == "Episode Subtitle"


@patch("lib.vod.url.get_json")
def test_get_episode_list_subtitle_only_no_subtitle(mock_get_json):
    """Test get_episode_list with show_only_subtitle=1 but no subtitle"""
    mock_get_json.return_value = {
        "items": [
            {
                "id": "episode1",
                "title": "Episode Title",
                "subtitle": "",
                "description": "Description",
                "images": {},
            }
        ]
    }

    episodes = vod.get_episode_list("homepage_ondemand", "None", 1)
    assert len(episodes) == 1
    assert episodes[0].title == "Episode Title"


@patch("lib.vod.url.get_json")
def test_get_episode_list_no_title_uses_subtitle(mock_get_json):
    """Test get_episode_list with no title uses subtitle"""
    mock_get_json.return_value = {
        "items": [
            {
                "id": "episode1",
                "title": "",
                "subtitle": "Episode Subtitle",
                "description": "Description",
                "images": {},
            }
        ]
    }

    episodes = vod.get_episode_list("homepage_ondemand", "None", 0)
    assert len(episodes) == 1
    assert episodes[0].title == "Episode Subtitle"


@patch("lib.vod.url.get_json")
def test_get_episode_list_no_title_uses_program_title(mock_get_json):
    """Test get_episode_list with no title/subtitle uses program title"""
    mock_get_json.return_value = {
        "items": [
            {
                "id": "episode1",
                "title": "",
                "subtitle": "",
                "description": "Description",
                "images": {},
                "video_program": {"title": "Program Title"},
            }
        ]
    }

    episodes = vod.get_episode_list("homepage_ondemand", "None", 0)
    assert len(episodes) == 1
    assert episodes[0].title == "Program Title"


@patch("lib.vod.url.get_json")
def test_get_episode_list_skips_episode_no_titles(mock_get_json):
    """Test get_episode_list skips episode with no title/subtitle/program"""
    mock_get_json.return_value = {
        "items": [
            {
                "id": "episode1",
                "title": "",
                "subtitle": "",
                "description": "Description",
                "images": {},
            },
            {
                "id": "episode2",
                "title": "Valid Episode",
                "subtitle": "",
                "description": "Description",
                "images": {},
            },
        ]
    }

    episodes = vod.get_episode_list("homepage_ondemand", "None", 0)
    assert len(episodes) == 1
    assert episodes[0].vod_id == "episode2"


@patch("lib.vod.url.get_json")
def test_get_episode_list_with_formatted_id(mock_get_json):
    """Test get_episode_list with formatted episode_list_id"""
    mock_get_json.return_value = {
        "items": [
            {
                "id": "episode1",
                "title": "Episode",
                "subtitle": "",
                "description": "Description",
                "images": {},
            }
        ]
    }

    episodes = vod.get_episode_list("get_latest_episodes", "program123", 0)
    assert len(episodes) == 1


@patch("lib.vod.url.get_json")
def test_get_episode_list_invalid_subtitle_param(mock_get_json):
    """Test get_episode_list handles invalid show_only_subtitle param"""
    mock_get_json.return_value = {
        "items": [
            {
                "id": "episode1",
                "title": "Title",
                "subtitle": "Subtitle",
                "description": "Description",
                "images": {},
            }
        ]
    }

    # Should handle string that's not convertible to int
    episodes = vod.get_episode_list("homepage_ondemand", "None", "invalid")
    assert len(episodes) == 1
    assert episodes[0].title == "Title - Subtitle"


@patch("lib.vod.url.get_json")
def test_resolve_vod_episode_with_valid_response(mock_get_json):
    """Test resolve_vod_episode with successful API response"""
    mock_get_json.return_value = {
        "id": "episode123",
        "title": "Episode Title",
        "description": "Episode description",
        "images": {"landscape": [{"url": "thumb.jpg"}, {"url": "fanart.jpg"}]},
        "onair": "2025-10-28T20:00:00+09:00",
        "pgm_no": 42,
        "movie_duration": 1800,
        "video": {"url": "https://example.com/video.m3u8", "duration": 1800},
    }

    episode = vod.resolve_vod_episode("episode123")
    assert episode is not None
    assert episode.title == "Episode Title"
    assert episode.vod_id == "episode123"
    assert episode.url == "https://example.com/video.m3u8"
    assert episode.is_playable is True
    assert episode.duration == 1800


@patch("lib.vod.url.get_json")
def test_resolve_vod_episode_no_id_in_response(mock_get_json):
    """Test resolve_vod_episode with invalid response (no id)"""
    mock_get_json.return_value = {"title": "Episode Title"}

    episode = vod.resolve_vod_episode("episode123")
    assert episode is None


@patch("lib.vod.url.get_json")
def test_resolve_vod_episode_no_video_url(mock_get_json):
    """Test resolve_vod_episode with no video URL"""
    mock_get_json.return_value = {
        "id": "episode123",
        "title": "Episode Title",
        "description": "Description",
        "images": {},
        "video": {},
    }

    episode = vod.resolve_vod_episode("episode123")
    assert episode is None


@patch("lib.vod.url.get_json")
def test_resolve_vod_episode_empty_video_url(mock_get_json):
    """Test resolve_vod_episode with empty video URL"""
    mock_get_json.return_value = {
        "id": "episode123",
        "title": "Episode Title",
        "description": "Description",
        "images": {},
        "video": {"url": ""},
    }

    episode = vod.resolve_vod_episode("episode123")
    assert episode is None


@patch("lib.vod.url.get_json")
def test_resolve_vod_episode_no_video_key(mock_get_json):
    """Test resolve_vod_episode with no video key"""
    mock_get_json.return_value = {
        "id": "episode123",
        "title": "Episode Title",
        "description": "Description",
        "images": {},
    }

    episode = vod.resolve_vod_episode("episode123")
    assert episode is None
