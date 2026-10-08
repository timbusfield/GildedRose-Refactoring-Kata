import pytest

from gilded_rose import GildedRose, Item


CONJURED = "Conjured"


@pytest.mark.parametrize(
    "sell_in, quality, expected_sell_in, expected_quality",
    [
        # Before expiry
        (10, 10, 9, 8),

        # Expiry boundary
        (0, 10, -1, 6),

        # After expiry
        (-1, 10, -2, 6),
    ],
)
def test_conjured_item_degradation(
    sell_in,
    quality,
    expected_sell_in,
    expected_quality,
):
    item = Item(CONJURED, sell_in, quality)

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
        (-1, 2),
    ],
)
def test_conjured_quality_never_negative(
    sell_in,
    quality,
):
    item = Item(CONJURED, sell_in, quality)

    GildedRose([item]).update_quality()

    assert item.quality >= 0