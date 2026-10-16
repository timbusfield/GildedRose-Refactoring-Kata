"""Comprison of original and refactored code.

This code compares the result of applying update_quality() to
- Item 1: An Aged Brie with quality 45 amd sell_in of 20 (days)
- Item 2: An Aged Brie with quality 45 amd sell_in of 0 (days)

It demonstrates that both the original code (renamed to OriginalGildedRose here)
and the refactored code have the same result

- Item 1 has its quality increased to 46
- Item 2 has its quality increased to 47

"""

import logging
import re
from abc import ABC, abstractmethod
from typing import ClassVar

logger = logging.getLogger(__name__)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class ItemUpdateStrategy(ABC):
    def update(self, item):
        previous_quality = item.quality
        self._update(item)
        self._validate_quality(item, previous_quality)

    @abstractmethod
    def _update(self, item):
        pass

    def _validate_quality(self, item, previous_quality):
        pass


class QualityBoundedItemStrategy(ItemUpdateStrategy):
    MINIMUM_QUALITY = 0
    MAXIMUM_QUALITY = 50

    def _validate_quality(self, item, previous_quality):
        if not self.MINIMUM_QUALITY <= previous_quality <= self.MAXIMUM_QUALITY:
            message = (
                f"Items of type {type(self).__name__} expect item quality to be between "
                f"{self.MINIMUM_QUALITY} and {self.MAXIMUM_QUALITY}; "
                f"the item {item.name!r} had a quality of {previous_quality} before update, "
                f"its quality has been updated to {item.quality}."
            )
            raise ValueError(message)

    def _keep_quality_within_limits(self, item):
        item.quality = max(
            self.MINIMUM_QUALITY, min(self.MAXIMUM_QUALITY, item.quality)
        )


class RateBasedItemStrategy(QualityBoundedItemStrategy):
    quality_multiplier: ClassVar[int]

    def _update(self, item):
        item.sell_in -= 1
        base_rate = 2 if item.sell_in < 0 else 1
        item.quality += base_rate * self.quality_multiplier
        self._keep_quality_within_limits(item)


class GeneralItemStrategy(RateBasedItemStrategy):
    quality_multiplier = -1


class AgedBrieStrategy(RateBasedItemStrategy):
    quality_multiplier = 1


class ConjuredItemStrategy(RateBasedItemStrategy):
    quality_multiplier = -2


class BackstagePassStrategy(QualityBoundedItemStrategy):
    def _update(self, item):
        item.sell_in -= 1

        if item.sell_in < 0:
            item.quality = 0
        elif item.sell_in < 5:
            item.quality += 3
        elif item.sell_in < 10:
            item.quality += 2
        else:
            item.quality += 1

        self._keep_quality_within_limits(item)


class SulfurasStrategy(ItemUpdateStrategy):
    SULFURAS_QUALITY = 80

    def _update(self, item):
        # Legendary item: never decreases in quality, never has to be sold
        pass

    def _validate_quality(self, item, previous_quality):
        if item.quality != self.SULFURAS_QUALITY:
            message = (
                "Items of type SulfurasStrategy expect item quality to be "
                f"{self.SULFURAS_QUALITY}; the item {item.name!r} "
                f"had a quality of {previous_quality} before update, "
                f"its quality has been updated to {item.quality}."
            )
            raise ValueError(message)


class ItemStrategyResolver:
    _PATTERNS: ClassVar[tuple[tuple[re.Pattern[str], ItemUpdateStrategy], ...]] = (
        # Conjured must start the name, giving it priority in mixed names.
        (
            re.compile(r"^\s*conjured\b", re.IGNORECASE),
            ConjuredItemStrategy(),
        ),
        # Match backstage before passes or passes before backstage, allowing
        # optional spaces within "backstage" and the tested pass spellings.
        (
            re.compile(
                r"(?:\bback\s*stage\s*pass(?:es|ess)?\b"
                r"|\bpass(?:es|ess)?\b.*\bback\s*stage\b)",
                re.IGNORECASE,
            ),
            BackstagePassStrategy(),
        ),
        # Match the Sulfuras word anywhere, but not similar words like "Sulfurous".
        (re.compile(r"\bsulfuras\b", re.IGNORECASE), SulfurasStrategy()),
        # Match the "aged brie" phrase with optional spacing and any casing.
        (
            re.compile(
                r"\baged\s*brie\b",
                re.IGNORECASE,
            ),
            AgedBrieStrategy(),
        ),
    )
    _DEFAULT_STRATEGY: ClassVar[ItemUpdateStrategy] = GeneralItemStrategy()

    @classmethod
    def get_strategy(cls, item_name: str) -> ItemUpdateStrategy:
        for pattern, strategy in cls._PATTERNS:
            if pattern.search(item_name):
                return strategy
        return cls._DEFAULT_STRATEGY


class OriginalGildedRose:
    def __init__(self, items):
        self.items = items
        self._strategies = {}

    def update_quality(self):
        for item in self.items:
            # check already assessed names
            strategy = self._strategies.get(item.name)
            if strategy is None:
                # generate strategy for name if doesn't exist
                strategy = ItemStrategyResolver.get_strategy(item.name)
                self._strategies[item.name] = strategy
            try:
                strategy.update(item)
            except ValueError as error:
                logger.warning(
                    "Updated the item %r; though the following warning was encountered: %s",
                    item,
                    error,
                )


class GildedRose:
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if (
                item.name != "Aged Brie"
                and item.name != "Backstage passes to a TAFKAL80ETC concert"
            ):
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item.quality = item.quality - 1
            elif item.quality < 50:
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
                elif item.quality < 50:
                    item.quality = item.quality + 1


from copy import deepcopy

if __name__ == "__main__":
    ORIGINAL_QUALITY = 45
    test_items = [
        Item(name="Aged Brie", sell_in=20, quality=ORIGINAL_QUALITY),
        Item(name="Aged Brie", sell_in=0, quality=ORIGINAL_QUALITY),
    ]

    test_items_a = deepcopy(test_items)
    test_items_b = deepcopy(test_items)

    original_gilded_rose = OriginalGildedRose(test_items_a)
    original_gilded_rose.update_quality()

    gilded_rose = GildedRose(test_items_b)
    gilded_rose.update_quality()

    for label, original, updated in [
        ("Original GildedRose", test_items, test_items_a),
        ("Refactored GildedRose", test_items, test_items_b),
    ]:
        print(f"\n\n{label}")
        for i, (before, after) in enumerate(zip(original, updated), start=1):
            change = after.quality - before.quality
            direction = "+" if change >= 0 else ""
            print(
                f"  Item {i} ({before.name}, sell_in={before.sell_in}): "
                f"quality {before.quality} → {after.quality} "
                f"({direction}{change})"
            )
