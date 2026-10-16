import pytest
from gilded_rose import GildedRose, Item

BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"


@pytest.mark.parametrize(
    "sell_in, quality, expected_sell_in, expected_quality",
    [
        # > 10 days: +1 quality
        (11, 20, 10, 21),

        # 10 days or less: +2 quality
        (10, 20, 9, 22),
        (6, 20, 5, 22),

        # 5 days or less: +3 quality
        (5, 20, 4, 23),
        (1, 20, 0, 23),

        # Concert day and after: quality drops to 0
        (0, 20, -1, 0),
        (-1, 20, -2, 0),
    ],
)
def test_backstage_pass_quality_rules(
    sell_in,
    quality,
    expected_sell_in,
    expected_quality,
):
    item = Item(BACKSTAGE_PASSES, sell_in, quality)

    GildedRose([item]).update_quality()

    assert item.sell_in == expected_sell_in
    assert item.quality == expected_quality


@pytest.mark.parametrize(
    "sell_in, quality, expected_quality",
    [
        # +1 would exceed 50
        (11, 50, 50),

        # +2 would exceed 50
        (10, 49, 50),

        # +3 would exceed 50
        (5, 49, 50),

        # +3 would exceed 50 by more than one
        (5, 48, 50),
    ],
)
def test_backstage_pass_quality_never_exceeds_50(
    sell_in,
    quality,
    expected_quality,
):
    item = Item(BACKSTAGE_PASSES, sell_in, quality)

    GildedRose([item]).update_quality()

    assert item.quality == expected_quality