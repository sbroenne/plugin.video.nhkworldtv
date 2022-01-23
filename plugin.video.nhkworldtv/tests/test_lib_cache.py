import lib.cache_api as cache


def test_get_metadata_cache():
    assert (isinstance(cache.get_program_metdadata_cache(), dict))
