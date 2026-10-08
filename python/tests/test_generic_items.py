import pytest
from gilded_rose import GildedRose, Item


@pytest.mark.parametrize(
    "sell_in, quality, expected_sell_in, expected_quality",
    [
        # Before expiry
        (10, 10, 9, 9),

        # Expiry boundary
        (0, 10, -1, 8),

        # After expiry degrades twice as fast
        (-1, 10, -2, 8),
    ],
)
def test_generic_item_quality_degradation(
    sell_in,
    quality,
    expected_sell_in,
    expected_quality,
):
    item = Item("Generic Item", sell_in, quality)

    GildedRose([item]).update_quality()

    assert item.sell_in == expected_sell_in
    assert item.quality == expected_quality


@pytest.mark.parametrize(
    "sell_in, quality",
    [
        (10, 0),
        (0, 0),
        (-1, 0),
        (-1, 1),
    ],
)
def test_generic_item_quality_never_negative(
    sell_in,
    quality,
):
    item = Item("Generic Item", sell_in, quality)

    GildedRose([item]).update_quality()

    assert item.quality >= 0