import pytest
from gilded_rose import GildedRose, Item

AGED_BRIE = "Aged Brie"


@pytest.mark.parametrize(
    "sell_in, quality, expected_sell_in, expected_quality",
    [
        # Before expiry
        (10, 10, 9, 11),

        # On expiry boundary
        (0, 10, -1, 12),

        # After expiry quality increases twice as fast
        (-1, 10, -2, 12),
    ],
)
def test_aged_brie_quality_increases(
    sell_in,
    quality,
    expected_sell_in,
    expected_quality,
):
    item = Item(AGED_BRIE, sell_in, quality)

    GildedRose([item]).update_quality()

    assert item.sell_in == expected_sell_in
    assert item.quality == expected_quality


@pytest.mark.parametrize(
    "sell_in, quality",
    [
        (10, 50),
        (0, 50),
        (-1, 50),
        (-1, 49),
    ],
)
def test_aged_brie_quality_never_exceeds_50(
    sell_in,
    quality,
):
    item = Item(AGED_BRIE, sell_in, quality)

    GildedRose([item]).update_quality()

    assert item.quality <= 50