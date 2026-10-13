from gilded_rose import GildedRose, Item


def test_update_quality_preserves_item_name():
    item = Item("foo", sell_in=0, quality=0)

    GildedRose([item]).update_quality()

    assert item.name == "foo"
