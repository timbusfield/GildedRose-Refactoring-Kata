import pytest
from gilded_rose import GildedRose, Item

SULFURAS = "Sulfuras, Hand of Ragnaros"


@pytest.mark.parametrize(
    "sell_in, quality",
    [
        (10, 80),
        (0, 80),
        (-10, 80),
    ],
)
def test_sulfuras_never_changes(sell_in, quality):
    item = Item(SULFURAS, sell_in=sell_in, quality=quality)

    GildedRose([item]).update_quality()

    assert item.sell_in == sell_in
    assert item.quality == quality