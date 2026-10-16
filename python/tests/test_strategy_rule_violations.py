
from gilded_rose import GildedRose, Item, SulfurasStrategy


def test_quality_bounds_are_checked_after_update_and_report_changed_quality(
    caplog,
):
    out_of_range_item = Item("ordinary item", sell_in=5, quality=53)
    following_item = Item("another item", sell_in=5, quality=10)

    with caplog.at_level("WARNING", logger="gilded_rose"):
        GildedRose([out_of_range_item, following_item]).update_quality()

    assert out_of_range_item.sell_in == 4
    assert out_of_range_item.quality == 50
    assert following_item.sell_in == 4
    assert following_item.quality == 9
    assert "expect item quality to be between 0 and 50" in caplog.text
    assert "had a quality of 53 before update, its quality has been updated to 50" in caplog.text


def test_sulfuras_quality_must_be_80_and_violation_is_logged(caplog):
    valid_sulfuras = Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)
    invalid_sulfuras = Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=75)
    following_item = Item("ordinary item", sell_in=5, quality=10)

    with caplog.at_level("WARNING", logger="gilded_rose"):
        GildedRose(
            [valid_sulfuras, invalid_sulfuras, following_item]
        ).update_quality()

    assert valid_sulfuras.sell_in == 0
    assert valid_sulfuras.quality == 80
    assert invalid_sulfuras.sell_in == 0
    assert invalid_sulfuras.quality == 75
    assert following_item.sell_in == 4
    assert following_item.quality == 9
    assert "Items of type SulfurasStrategy expect item quality to be 80" in caplog.text
    assert "had a quality of 75 before update, its quality has been updated to 75" in caplog.text


def test_sulfuras_strategy_does_not_raise_for_valid_quality():
    item = Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)

    SulfurasStrategy().update(item)

    assert item.sell_in == 0
    assert item.quality == 80
