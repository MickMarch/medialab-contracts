import medialab_contracts

REMOVED_NAMES = (
    "DISCOVER_CLIP_FILENAME",
    "DISCOVER_CLIP_SUBDIR",
    "DISCOVER_LIBRARY_NAMES",
    "JELLYFIN_ITEM_TYPES",
    "PLACEHOLDER_TITLE_SEPARATOR",
    "PLACEHOLDER_TITLE_SUFFIXES",
    "FavoriteScope",
    "JellyfinRequestEvent",
    "PlaceholderInfo",
    "PlaceholdersResponse",
    "PlaceholderState",
    "PlaceholderWrite",
    "placeholder_title",
)


def test_placeholder_names_are_no_longer_exported() -> None:
    for name in REMOVED_NAMES:
        assert not hasattr(medialab_contracts, name)
        assert name not in medialab_contracts.__all__
