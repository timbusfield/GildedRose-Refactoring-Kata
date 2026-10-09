

import re
from abc import ABC, abstractmethod
from typing import ClassVar

MINIMUM_QUALITY = 0
MAXIMUM_QUALITY = 50

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

class ItemUpdateStrategy(ABC):
    @abstractmethod
    def update(self, item):
        pass

class QualityBoundedItemStrategy(ItemUpdateStrategy):
    def _keep_quality_within_limits(self, item):
        item.quality = max(MINIMUM_QUALITY, min(MAXIMUM_QUALITY, item.quality))


class RateBasedItemStrategy(QualityBoundedItemStrategy):
    quality_multiplier: ClassVar[int]

    def update(self, item):
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
    def update(self, item):
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
    def update(self, item):
        # Legendary item: never decreases in quality, never has to be sold
        pass


class ItemStrategyResolver:
    _PATTERNS: ClassVar[
        tuple[tuple[re.Pattern[str], ItemUpdateStrategy], ...]
    ] = (
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



class GildedRose:

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            strategy = ItemStrategyResolver.get_strategy(item.name)
            strategy.update(item)
