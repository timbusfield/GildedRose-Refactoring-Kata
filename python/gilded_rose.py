

import re
from abc import ABC, abstractmethod
from enum import StrEnum
from typing import ClassVar


class ItemName(StrEnum):
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    AGED_BRIE = "Aged Brie"
    BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
    CONJURED = "Conjured"

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

    def _keep_quality_within_limits(self, item):
        item.quality = max(MINIMUM_QUALITY, min(MAXIMUM_QUALITY, item.quality))

class GeneralItemStrategy(ItemUpdateStrategy):
    def __init__(self, multiplier: int = -1):
        """
        multiplier: 
          -1  => Standard item (degrades by 1, 2)
          +1  => Aged Brie (increases by 1, 2)
          -2  => Conjured item (degrades by 2, 4)
        """
        self.multiplier = multiplier

    def update(self, item):
        item.sell_in -= 1
        
        # Base rate doubles after sell-by date passes
        base_rate = 2 if item.sell_in < 0 else 1
        
        # Apply factor and sign
        item.quality += base_rate * self.multiplier
        self._keep_quality_within_limits(item)

class BackstagePassStrategy(ItemUpdateStrategy):
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


class ItemStrategyFactory:
    _STRATEGIES: ClassVar[dict[str, ItemUpdateStrategy]] = {
        ItemName.AGED_BRIE: GeneralItemStrategy(multiplier=1),
        ItemName.CONJURED: GeneralItemStrategy(multiplier=-2),
        ItemName.BACKSTAGE_PASSES: BackstagePassStrategy(),
        ItemName.SULFURAS: SulfurasStrategy(),
    }
    
    _DEFAULT_STRATEGY = GeneralItemStrategy(multiplier=-1)
    
    _PATTERNS: ClassVar[tuple[tuple[re.Pattern[str], ItemName], ...]] = (
        # Conjured must start the name, giving it priority in mixed names.
        (re.compile(r"^\s*conjured\b", re.IGNORECASE), ItemName.CONJURED),
        # Match backstage before passes or passes before backstage, allowing
        # optional spaces within "backstage" and the tested pass spellings.
        (
            re.compile(
                r"(?:\bback\s*stage\s*pass(?:es|ess)?\b"
                r"|\bpass(?:es|ess)?\b.*\bback\s*stage\b)",
                re.IGNORECASE,
            ),
            ItemName.BACKSTAGE_PASSES,
        ),
        # Match the Sulfuras word anywhere, but not similar words like "Sulfurous".
        (re.compile(r"\bsulfuras\b", re.IGNORECASE), ItemName.SULFURAS),
        # Match the "aged brie" phrase with optional spacing and any casing.
        (
            re.compile(
                r"\baged\s*brie\b",
                re.IGNORECASE,
            ),
            ItemName.AGED_BRIE,
        ),
    )

    @classmethod
    def get_strategy(cls, item_name: str) -> ItemUpdateStrategy:
        for pattern, strategy_name in cls._PATTERNS:
            if pattern.search(item_name):
                return cls._STRATEGIES[strategy_name]
        return cls._DEFAULT_STRATEGY



class GildedRose:

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            strategy = ItemStrategyFactory.get_strategy(item.name)
            strategy.update(item)
