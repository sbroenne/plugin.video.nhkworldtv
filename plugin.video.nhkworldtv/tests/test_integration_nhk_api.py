"""
Integration tests for NHK API endpoints

These tests make REAL API calls to verify:
1. All endpoints in nhk_api.py actually exist and return valid responses
2. Response structures match what the code expects
3. Images are present where expected
4. No authentication errors

Run separately from unit tests as they are slower and require network:
    pytest plugin.video.nhkworldtv/tests/integration_test_nhk_api.py -v
"""

import os
import sys
from datetime import datetime

import pytest
import requests

# Import the actual module (not mocked)
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from lib import nhk_api


class TestNHKAPIEndpoints:
    """Test that all API endpoints actually exist and return valid data"""

    def test_homepage_ondemand_endpoint_exists(self):
        """Verify VOD homepage endpoint returns valid data"""
        endpoint = nhk_api.rest_url["homepage_ondemand"]
        response = requests.get(endpoint, timeout=10)

        assert response.status_code == 200, f"Failed to fetch {endpoint}"
        data = response.json()

        # New API format - should have "items" array
        assert "items" in data, "Response should have 'items' array"
        assert isinstance(data["items"], list), "'items' should be an array"
        assert len(data["items"]) > 0, "Should have at least one episode"

        # Check first episode has expected fields
        episode = data["items"][0]
        assert "id" in episode, "Episode should have 'id'"
        assert "title" in episode, "Episode should have 'title'"
        assert "images" in episode, "Episode should have 'images'"

    def test_get_programs_endpoint_exists(self):
        """Verify programs list endpoint returns valid data"""
        endpoint = nhk_api.rest_url["get_programs"]
        response = requests.get(endpoint, timeout=10)

        assert response.status_code == 200, f"Failed to fetch {endpoint}"
        data = response.json()

        assert "items" in data, "Response should have 'items' array"
        assert isinstance(data["items"], list), "'items' should be an array"

        if len(data["items"]) > 0:
            program = data["items"][0]
            assert "id" in program, "Program should have 'id'"
            assert "title" in program, "Program should have 'title'"

    def test_get_latest_episodes_endpoint_exists(self):
        """Verify latest episodes endpoint returns valid data"""
        endpoint = nhk_api.rest_url["get_latest_episodes"]
        response = requests.get(endpoint, timeout=10)

        assert response.status_code == 200, f"Failed to fetch {endpoint}"
        data = response.json()

        assert "items" in data, "Response should have 'items' array"
        assert isinstance(data["items"], list), "'items' should be an array"
        assert len(data["items"]) > 0, "Should have at least one episode"

    def test_get_episode_detail_endpoint_format(self):
        """Verify episode detail endpoint format is correct"""
        # First get an episode ID from latest episodes
        latest_url = nhk_api.rest_url["get_latest_episodes"]
        response = requests.get(latest_url, timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0

        episode_id = data["items"][0]["id"]

        # Now test the detail endpoint with this ID
        detail_url = nhk_api.rest_url["get_episode_detail"].format(episode_id)
        response = requests.get(detail_url, timeout=10)

        assert response.status_code == 200, f"Failed to fetch episode {episode_id}"
        episode_data = response.json()

        # Should have video URL directly in response
        assert "video" in episode_data, "Episode detail should have 'video' field"
        assert "url" in episode_data["video"], "Video field should have 'url' property"
        assert episode_data["video"]["url"].startswith("http"), (
            "Video URL should be valid HTTP URL"
        )

    def test_live_stream_url_accessible(self):
        """Verify live stream URL is accessible"""
        stream_url = nhk_api.rest_url["live_stream_url"]

        # Just check it's an m3u8 URL and accessible
        response = requests.head(stream_url, timeout=10)
        assert response.status_code == 200, (
            f"Live stream URL not accessible: {stream_url}"
        )
        assert stream_url.endswith(".m3u8"), "Live stream should be HLS playlist"

    def test_homepage_news_endpoint_exists(self):
        """Verify news homepage endpoint returns valid data"""
        endpoint = nhk_api.rest_url["homepage_news"]
        response = requests.get(endpoint, timeout=10)

        assert response.status_code == 200, f"Failed to fetch {endpoint}"
        data = response.json()

        # News endpoint structure
        assert isinstance(data, dict), "News response should be an object"

    def test_all_endpoints_defined(self):
        """Verify all expected endpoints are defined in nhk_api.rest_url"""
        required_endpoints = [
            "homepage_ondemand",
            "get_programs",
            "get_latest_episodes",
            "get_episode_detail",
            "live_stream_url",
            "homepage_news",
            "get_livestream",  # EPG/schedule endpoint
        ]

        for endpoint_name in required_endpoints:
            assert endpoint_name in nhk_api.rest_url, (
                f"Missing required endpoint: {endpoint_name}"
            )


class TestEPGScheduleEndpoint:
    """Test the EPG/schedule endpoint that was missing"""

    def test_get_livestream_endpoint_exists(self):
        """Verify EPG/schedule endpoint exists and returns valid data"""
        # EPG URL requires current date in YYYYMMDD format
        today_str = datetime.now().strftime("%Y%m%d")
        endpoint = f"{nhk_api.rest_url['get_livestream']}{today_str}.json"

        response = requests.get(endpoint, timeout=10)

        assert response.status_code == 200, f"Failed to fetch {endpoint}"
        data = response.json()

        # EPG format: {"data": [...]}
        assert "data" in data, "EPG response should have 'data' array"
        assert isinstance(data["data"], list), "'data' should be an array"
        assert len(data["data"]) > 0, "EPG should have at least one program"

        # Check first program has expected fields
        program = data["data"][0]
        required_fields = [
            "title",
            "startTime",
            "endTime",
            "episodeId",
        ]
        for field in required_fields:
            assert field in program, f"EPG program should have '{field}' field"

    def test_schedule_has_valid_program_times(self):
        """Verify EPG programs have valid time ranges"""
        today_str = datetime.now().strftime("%Y%m%d")
        endpoint = f"{nhk_api.rest_url['get_livestream']}{today_str}.json"

        response = requests.get(endpoint, timeout=10)
        assert response.status_code == 200

        data = response.json()
        assert len(data["data"]) > 0, "EPG should have programs"

        # Verify programs have valid timestamps and structure
        for program in data["data"]:
            # All programs must have start and end times
            assert "startTime" in program, "Program should have startTime"
            assert "endTime" in program, "Program should have endTime"

            # Parse times - should be valid ISO 8601
            start = datetime.fromisoformat(program["startTime"])
            end = datetime.fromisoformat(program["endTime"])

            # End time should be after start time
            assert end > start, (
                f"Program end time should be after start: {program.get('title', 'Unknown')}"
            )

            # If program has VOD flag, should have playURL
            if program.get("vodFlag") == 1:
                assert "playURL" in program, "VOD-enabled program should have playURL"


class TestImageAvailability:
    """Test that images are present in API responses"""

    def test_vod_episodes_have_images(self):
        """Verify VOD episodes include image URLs"""
        endpoint = nhk_api.rest_url["homepage_ondemand"]
        response = requests.get(endpoint, timeout=10)
        assert response.status_code == 200

        data = response.json()
        episodes_with_images = 0

        for episode in data["items"][:10]:  # Check first 10
            # New API uses simple 'images' array, not 'images.landscape'
            if "images" in episode and isinstance(episode["images"], list):
                if len(episode["images"]) > 0:
                    episodes_with_images += 1

        # At least 80% of episodes should have images
        assert episodes_with_images >= 8, (
            f"Most episodes should have images: {episodes_with_images}/10"
        )

    def test_episode_detail_has_images(self):
        """Verify episode detail includes images"""
        # Get an episode ID
        latest_url = nhk_api.rest_url["get_latest_episodes"]
        response = requests.get(latest_url, timeout=10)
        assert response.status_code == 200

        episode_id = response.json()["items"][0]["id"]

        # Get episode detail
        detail_url = nhk_api.rest_url["get_episode_detail"].format(episode_id)
        response = requests.get(detail_url, timeout=10)
        assert response.status_code == 200

        episode = response.json()
        assert "images" in episode, "Episode detail should have 'images' field"

    def test_schedule_programs_have_thumbnails(self):
        """Verify schedule programs include thumbnail URLs"""
        today_str = datetime.now().strftime("%Y%m%d")
        endpoint = f"{nhk_api.rest_url['get_livestream']}{today_str}.json"

        response = requests.get(endpoint, timeout=10)
        assert response.status_code == 200

        data = response.json()
        programs_with_thumbnails = 0

        for program in data["data"][:20]:  # Check first 20
            # EPG uses different field names
            if program.get("thumbnail") or program.get("episodeThumbnailURL"):
                programs_with_thumbnails += 1

        # Many programs should have thumbnails (but not all - some are INFO/fillers)
        assert programs_with_thumbnails >= 10, (
            "Many schedule programs should have thumbnails"
        )


class TestResponseStructureCompatibility:
    """Test that response structures match what the code expects"""

    def test_vod_episode_field_mapping(self):
        """Verify VOD episodes have all required fields with correct names"""
        endpoint = nhk_api.rest_url["homepage_ondemand"]
        response = requests.get(endpoint, timeout=10)
        assert response.status_code == 200

        data = response.json()
        episode = data["items"][0]

        # New API field names (not old ones like vod_id, title_clean, etc.)
        assert "id" in episode, "Should use 'id' not 'vod_id'"
        assert "title" in episode, "Should use 'title' not 'title_clean'"
        # Note: 'subtitle' is optional - some episodes don't have it
        assert "description" in episode, (
            "Should use 'description' not 'description_clean'"
        )
        assert "images" in episode, "Should have 'images' array"
        # New API uses simple array, not nested landscape structure
        assert isinstance(episode["images"], list), "Images should be array"

    def test_schedule_field_mapping(self):
        """Verify schedule programs have expected field structure"""
        today_str = datetime.now().strftime("%Y%m%d")
        endpoint = f"{nhk_api.rest_url['get_livestream']}{today_str}.json"

        response = requests.get(endpoint, timeout=10)
        assert response.status_code == 200

        data = response.json()

        # Response should have 'data' array (EPG format)
        assert "data" in data, "EPG should have 'data' array (not 'channel.item')"

        program = data["data"][0]

        # Check ISO 8601 timestamp format
        assert "startTime" in program
        assert "T" in program["startTime"], "Times should be ISO 8601 format"
        assert program["startTime"].endswith("+09:00"), (
            "Times should have timezone offset"
        )


class TestNewsEndpoints:
    """Test news-related API endpoints"""

    def test_news_homepage_endpoint(self):
        """Verify news homepage endpoint returns valid data"""
        endpoint = nhk_api.rest_url["homepage_news"]
        response = requests.get(endpoint, timeout=10)

        assert response.status_code == 200, f"Failed to fetch {endpoint}"
        data = response.json()

        # News endpoint should return structured data
        assert isinstance(data, dict), "News response should be an object"
        # Should have some news categories
        assert len(data) > 0, "News should have content"

    def test_ataglance_endpoint(self):
        """Verify At-a-Glance news endpoint returns valid data"""
        endpoint = nhk_api.rest_url["get_news_ataglance"]
        response = requests.get(endpoint, timeout=10)

        assert response.status_code == 200, f"Failed to fetch {endpoint}"
        data = response.json()

        assert isinstance(data, dict), "At-a-Glance should be an object"


class TestVODEndpoints:
    """Test all VOD-related endpoints"""

    def test_get_programs_returns_list(self):
        """Verify programs endpoint returns a list of programs"""
        endpoint = nhk_api.rest_url["get_programs"]
        response = requests.get(endpoint, timeout=10)

        assert response.status_code == 200
        data = response.json()

        assert "items" in data
        assert len(data["items"]) > 0, "Should have programs"

        # Check program structure
        program = data["items"][0]
        assert "id" in program
        assert "title" in program

    def test_get_categories_endpoint(self):
        """Verify categories endpoint exists"""
        endpoint = nhk_api.rest_url["get_categories"]
        response = requests.get(endpoint, timeout=10)

        assert response.status_code == 200
        data = response.json()

        assert "items" in data

    def test_most_watched_episodes(self):
        """Verify most watched episodes endpoint"""
        endpoint = nhk_api.rest_url["get_most_watched_episodes"]
        response = requests.get(endpoint, timeout=10)

        assert response.status_code == 200
        data = response.json()

        assert "items" in data


class TestAPICompleteness:
    """Verify all API endpoints defined in nhk_api.py are accessible"""

    def test_all_vod_endpoints_accessible(self):
        """Test that all VOD endpoints return 200"""
        vod_endpoints = [
            "homepage_ondemand",
            "get_programs",
            "get_latest_episodes",
            "get_most_watched_episodes",
        ]

        for endpoint_name in vod_endpoints:
            endpoint = nhk_api.rest_url[endpoint_name]
            response = requests.get(endpoint, timeout=10)
            assert response.status_code == 200, f"{endpoint_name} failed: {endpoint}"

    def test_all_news_endpoints_accessible(self):
        """Test that all news endpoints return 200"""
        news_endpoints = [
            "homepage_news",
            "get_news_ataglance",
        ]

        for endpoint_name in news_endpoints:
            endpoint = nhk_api.rest_url[endpoint_name]
            response = requests.get(endpoint, timeout=10)
            assert response.status_code == 200, f"{endpoint_name} failed: {endpoint}"

    def test_live_endpoints_accessible(self):
        """Test that live/schedule endpoints are accessible"""
        # Live stream
        stream_url = nhk_api.rest_url["live_stream_url"]
        response = requests.head(stream_url, timeout=10)
        assert response.status_code == 200, "Live stream not accessible"

        # EPG/Schedule
        today_str = datetime.now().strftime("%Y%m%d")
        epg_url = f"{nhk_api.rest_url['get_livestream']}{today_str}.json"
        response = requests.get(epg_url, timeout=10)
        assert response.status_code == 200, "EPG not accessible"


class TestVideoPlayback:
    """Test that video URLs are accessible and valid"""

    def test_episode_video_url_format(self):
        """Verify episode detail includes valid video URL"""
        # Get an episode ID
        latest_url = nhk_api.rest_url["get_latest_episodes"]
        response = requests.get(latest_url, timeout=10)
        assert response.status_code == 200

        episode_id = response.json()["items"][0]["id"]

        # Get episode detail
        detail_url = nhk_api.rest_url["get_episode_detail"].format(episode_id)
        response = requests.get(detail_url, timeout=10)
        assert response.status_code == 200

        episode = response.json()

        # Should have video URL
        assert "video" in episode
        assert "url" in episode["video"]

        video_url = episode["video"]["url"]

        # Video URL should be HLS
        assert video_url.startswith("https://")
        assert ".m3u8" in video_url

        # Try to access the video URL
        response = requests.head(video_url, timeout=10)
        assert response.status_code == 200, f"Video URL not accessible: {video_url}"


class TestEpisodeDataProcessing:
    """Test that Episode class can handle real API data"""

    def test_episode_handles_epg_timestamps(self):
        """Verify Episode class handles ISO 8601 timestamps from EPG"""
        from lib.episode import Episode

        # Get real EPG data
        today_str = datetime.now().strftime("%Y%m%d")
        epg_url = f"{nhk_api.rest_url['get_livestream']}{today_str}.json"
        response = requests.get(epg_url, timeout=10)
        assert response.status_code == 200

        data = response.json()
        assert "data" in data and len(data["data"]) > 0

        # Get first program from EPG
        program = data["data"][0]

        # Create Episode and set broadcast dates (this is what plugin.py does)
        episode = Episode()

        # This should not crash with ISO 8601 strings!
        episode.broadcast_start_date = program.get("startTime")
        episode.broadcast_end_date = program.get("endTime")

        # Verify dates were set correctly
        assert episode.broadcast_start_date is not None, (
            "Episode should handle ISO 8601 start time"
        )
        assert episode.broadcast_end_date is not None, (
            "Episode should handle ISO 8601 end time"
        )

    def test_episode_handles_vod_timestamps(self):
        """Verify Episode class still handles Unix timestamps from VOD"""
        from lib.episode import Episode

        # Get VOD data (uses Unix timestamps)
        vod_url = nhk_api.rest_url["get_latest_episodes"]
        response = requests.get(vod_url, timeout=10)
        assert response.status_code == 200

        data = response.json()
        episode_data = data["items"][0]

        # VOD might have broadcast schedules with ISO timestamps
        if "broadcast_schedules" in episode_data:
            schedules = episode_data["broadcast_schedules"]
            if len(schedules) > 0:
                episode = Episode()
                # Should handle ISO format from VOD too
                episode.broadcast_start_date = schedules[0].get("start_at")
                assert episode.broadcast_start_date is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
