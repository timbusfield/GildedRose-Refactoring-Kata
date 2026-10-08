

from enum import StrEnum

class ItemName(StrEnum):
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    AGED_BRIE = "Aged Brie"
    BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
    CONJURED = "Conjured"

MINIUM_QUALITY = 0
MAXIMUM_QUALITY = 50

GENERIC_DEGRADE_FACTOR = 1
CONJURED_DEGRADE_FACTOR = 2
PRE_SELL_IN_FACTOR = 1
PAST_SELL_IN_FACTOR = 2


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def _update_sell_in(self, item):
        item.sell_in = item.sell_in - 1

    def _update_degrading_item(self, item, item_type_factor: int = GENERIC_DEGRADE_FACTOR):
        self._update_sell_in(item)
        item_stage_factor = PRE_SELL_IN_FACTOR if item.sell_in >= 0 else PAST_SELL_IN_FACTOR
        item.quality = max(MINIUM_QUALITY, item.quality - (item_type_factor * item_stage_factor))

    def _update_generic_item(self, item):
        self._update_degrading_item(item, GENERIC_DEGRADE_FACTOR)

    def _update_conjured_item(self, item):
        self._update_degrading_item(item, CONJURED_DEGRADE_FACTOR)

    def _update_aged_brie_item(self, item):
        self._update_sell_in(item)
        item.quality = min(MAXIMUM_QUALITY,item.quality+1)

    def _update_backstage_passes(self, item):
        self._update_sell_in(item)
        if item.sell_in < 0:
            item.quality = 0
        else:
            if item.sell_in < 5:
                quality_increase = 3
            elif item.sell_in < 10:
                quality_increase = 2
            else:
                quality_increase = 1
            item.quality = min(MAXIMUM_QUALITY,item.quality+quality_increase)

    def _update_item_quality(self, item):
        match item.name:
            case ItemName.SULFURAS:
                pass

            case ItemName.AGED_BRIE:
                self._update_aged_brie_item(item)

            case ItemName.BACKSTAGE_PASSES:
                self._update_backstage_passes(item)

            case ItemName.CONJURED:
                self._update_conjured_item(item)

    def update_quality(self):
        for item in self.items:
            self._update_item_quality(item)



class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

class OriginalGildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item.quality = item.quality - 1
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality > 0:
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < 50:
                        item.quality = item.quality + 1