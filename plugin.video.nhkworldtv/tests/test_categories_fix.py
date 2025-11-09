"""
Test to verify categories and programs filtering works correctly

This test verifies that the fix for the categories bug is working.
Previously, all categories showed the same content because the API URLs
didn't include query parameters to filter by category or program.
"""

import os
import sys

# Add the plugin directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib import nhk_api


def test_categories_url_includes_category_id():
    """Verify that category episode list URL includes category parameter"""
    category_id = 15  # Documentaries

    # Get the URL template
    url_template = nhk_api.rest_url["get_categories_episode_list"]

    # Format it with the category ID
    formatted_url = url_template.format(category_id)

    # Verify the URL includes the category ID in the path
    assert f"/categories/{category_id}/" in formatted_url, (
        f"Category URL should include '/categories/{category_id}/' in path"
    )
    assert formatted_url == (
        f"https://api.nhkworld.jp/showsapi/v1/en/categories/{category_id}/video_episodes"
    ), "Category URL format is incorrect"


def test_programs_url_includes_program_id():
    """Verify that program episode list URL includes program parameter"""
    program_id = "world-prime"

    # Get the URL template
    url_template = nhk_api.rest_url["get_programs_episode_list"]

    # Format it with the program ID
    formatted_url = url_template.format(program_id)

    # Verify the URL includes the program ID in the path
    assert f"/video_programs/{program_id}/" in formatted_url, (
        f"Program URL should include '/video_programs/{program_id}/' in path"
    )
    assert formatted_url == (
        f"https://api.nhkworld.jp/showsapi/v1/en/video_programs/{program_id}/video_episodes"
    ), "Program URL format is incorrect"


def test_different_categories_generate_different_urls():
    """Verify that different category IDs generate different URLs"""
    category_id_1 = 15  # Documentaries
    category_id_2 = 20  # Drama

    url_template = nhk_api.rest_url["get_categories_episode_list"]

    url_1 = url_template.format(category_id_1)
    url_2 = url_template.format(category_id_2)

    # URLs should be different
    assert url_1 != url_2, "Different category IDs should generate different URLs"
    assert f"/categories/{category_id_1}/" in url_1, (
        "First URL should have /categories/15/"
    )
    assert f"/categories/{category_id_2}/" in url_2, (
        "Second URL should have /categories/20/"
    )


def test_different_programs_generate_different_urls():
    """Verify that different program IDs generate different URLs"""
    program_id_1 = "world-prime"
    program_id_2 = "newsline"

    url_template = nhk_api.rest_url["get_programs_episode_list"]

    url_1 = url_template.format(program_id_1)
    url_2 = url_template.format(program_id_2)

    # URLs should be different
    assert url_1 != url_2, "Different program IDs should generate different URLs"
    assert f"/video_programs/{program_id_1}/" in url_1, (
        "First URL should have /video_programs/world-prime/"
    )
    assert f"/video_programs/{program_id_2}/" in url_2, (
        "Second URL should have /video_programs/newsline/"
    )


def test_url_base_structure_is_correct():
    """Verify the base URL structure is correct for both endpoints"""
    categories_url = nhk_api.rest_url["get_categories_episode_list"]
    programs_url = nhk_api.rest_url["get_programs_episode_list"]

    # Categories should use path structure /categories/{0}/video_episodes
    assert "/categories/{0}/video_episodes" in categories_url, (
        "Categories URL should use path parameter structure /categories/{0}/video_episodes"
    )

    # Programs should use path structure /video_programs/{0}/video_episodes
    assert "/video_programs/{0}/video_episodes" in programs_url, (
        "Programs URL should use path parameter structure /video_programs/{0}/video_episodes"
    )
