import medialab_contracts

REMOVED_NAMES = ("DISCOVER_LIBRARY_NAMES", "JellyfinRequestEvent", "PlaceholderState")


def test_placeholder_names_are_no_longer_exported() -> None:
    for name in REMOVED_NAMES:
        assert not hasattr(medialab_contracts, name)
        assert name not in medialab_contracts.__all__
