"""
Test to verify categories and programs filtering works correctly

This test verifies that the fix for the categories bug is working.
Previously, all categories showed the same content because the API URLs
didn't include query parameters to filter by category or program.
"""

import sys
import os

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
    
    # Verify the URL includes the category parameter
    assert "category=" in formatted_url, (
        "Category URL should include 'category=' query parameter"
    )
    assert f"category={category_id}" in formatted_url, (
        f"Category URL should include 'category={category_id}'"
    )
    assert formatted_url == (
        "https://api.nhkworld.jp/showsapi/v1/en/video_episodes?category=15"
    ), "Category URL format is incorrect"


def test_programs_url_includes_program_id():
    """Verify that program episode list URL includes program parameter"""
    program_id = "world-prime"
    
    # Get the URL template
    url_template = nhk_api.rest_url["get_programs_episode_list"]
    
    # Format it with the program ID
    formatted_url = url_template.format(program_id)
    
    # Verify the URL includes the program parameter
    assert "program=" in formatted_url, (
        "Program URL should include 'program=' query parameter"
    )
    assert f"program={program_id}" in formatted_url, (
        f"Program URL should include 'program={program_id}'"
    )
    assert formatted_url == (
        "https://api.nhkworld.jp/showsapi/v1/en/video_episodes?program=world-prime"
    ), "Program URL format is incorrect"


def test_different_categories_generate_different_urls():
    """Verify that different category IDs generate different URLs"""
    category_id_1 = 15  # Documentaries
    category_id_2 = 20  # Drama
    
    url_template = nhk_api.rest_url["get_categories_episode_list"]
    
    url_1 = url_template.format(category_id_1)
    url_2 = url_template.format(category_id_2)
    
    # URLs should be different
    assert url_1 != url_2, (
        "Different category IDs should generate different URLs"
    )
    assert "category=15" in url_1, "First URL should have category=15"
    assert "category=20" in url_2, "Second URL should have category=20"


def test_different_programs_generate_different_urls():
    """Verify that different program IDs generate different URLs"""
    program_id_1 = "world-prime"
    program_id_2 = "newsline"
    
    url_template = nhk_api.rest_url["get_programs_episode_list"]
    
    url_1 = url_template.format(program_id_1)
    url_2 = url_template.format(program_id_2)
    
    # URLs should be different
    assert url_1 != url_2, (
        "Different program IDs should generate different URLs"
    )
    assert "program=world-prime" in url_1, "First URL should have program=world-prime"
    assert "program=newsline" in url_2, "Second URL should have program=newsline"


def test_url_base_structure_is_correct():
    """Verify the base URL structure is correct for both endpoints"""
    categories_url = nhk_api.rest_url["get_categories_episode_list"]
    programs_url = nhk_api.rest_url["get_programs_episode_list"]
    
    # Both should start with the same base URL
    expected_base = "https://api.nhkworld.jp/showsapi/v1/en/video_episodes?"
    
    assert categories_url.startswith(expected_base), (
        f"Categories URL should start with {expected_base}"
    )
    assert programs_url.startswith(expected_base), (
        f"Programs URL should start with {expected_base}"
    )
    
    # But they should have different query parameters
    assert "category=" in categories_url, "Categories URL should have 'category=' parameter"
    assert "program=" in programs_url, "Programs URL should have 'program=' parameter"
