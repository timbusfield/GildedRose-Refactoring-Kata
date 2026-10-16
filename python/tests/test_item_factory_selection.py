import pytest

from gilded_rose import (
    AgedBrieStrategy,
    BackstagePassStrategy,
    ConjuredItemStrategy,
    GeneralItemStrategy,
    ItemStrategyResolver,
    SulfurasStrategy,
)


def assert_strategy(item_name, expected_strategy):
    strategy = ItemStrategyResolver.get_strategy(item_name)

    assert type(strategy) is expected_strategy


@pytest.mark.parametrize(
    "item_name",
    [
        pytest.param("Aged Brie", id="canonical-name"),
        pytest.param("aged brie", id="lowercase"),
        pytest.param("aGEdbRIe", id="mixed-case"),
        pytest.param("aged brie (french)", id="french-suffix"),
        pytest.param("french aged brie", id="french-prefix"),
    ],
)
def test_aged_brie_matches(item_name):
    assert_strategy(item_name, AgedBrieStrategy)


@pytest.mark.parametrize(
    "item_name",
    [
        pytest.param("age db rie", id="internal-spaces"),
        pytest.param("brie", id="partial-name"),
        pytest.param("camembert", id="different-cheese"),
    ],
)
def test_aged_brie_non_matches_use_generic_strategy(item_name):
    assert_strategy(item_name, GeneralItemStrategy)


@pytest.mark.parametrize(
    "item_name",
    [
        pytest.param("Sulfuras, Hand of Ragnaros", id="canonical-name"),
        pytest.param("suLFURAS - HOR", id="mixed-case-abbreviation"),
        pytest.param("sulfuras", id="short-name"),
    ],
)
def test_sulfuras_matches(item_name):
    assert_strategy(item_name, SulfurasStrategy)


@pytest.mark.parametrize(
    "item_name",
    [
        pytest.param("Sulfurous", id="similar-word"),
        pytest.param("sulf URAS", id="internal-space"),
    ],
)
def test_sulfuras_non_matches_use_generic_strategy(item_name):
    assert_strategy(item_name, GeneralItemStrategy)


@pytest.mark.parametrize(
    "item_name",
    [
        pytest.param(
            "Backstage passes to a TAFKAL80ETC concert",
            id="canonical-name",
        ),
        pytest.param("backSTAGePassES", id="mixed-case"),
        pytest.param("passes for backstage", id="reversed-words"),
        pytest.param("backstage pass - VIP", id="vip-suffix"),
        pytest.param("back stage passes", id="spaces-between-words"),
    ],
)
def test_backstage_passes_matches(item_name):
    assert_strategy(item_name, BackstagePassStrategy)


@pytest.mark.parametrize(
    "item_name",
    [
        pytest.param("passess", id="misspelling"),
        pytest.param("stage pass", id="partial-name"),
        pytest.param("backstage pas", id="truncated-name"),
        pytest.param("back stage pas ses", id="split-final-word"),
    ],
)
def test_backstage_passes_non_matches_use_generic_strategy(item_name):
    assert_strategy(item_name, GeneralItemStrategy)


@pytest.mark.parametrize(
    "item_name",
    [
        pytest.param("Conjured", id="canonical-name"),
        pytest.param("conJUred", id="mixed-case"),
        pytest.param("Conjured Mana Cake", id="mana-cake-suffix"),
        pytest.param("conjured - ITEM", id="item-suffix"),
    ],
)
def test_conjured_matches(item_name):
    assert_strategy(item_name, ConjuredItemStrategy)


@pytest.mark.parametrize(
    "item_name",
    [
        pytest.param("conjure", id="truncated-name"),
        pytest.param("conjure RED", id="similar-words"),
        pytest.param("conjur ed", id="internal-space"),
    ],
)
def test_conjured_non_matches_use_generic_strategy(item_name):
    assert_strategy(item_name, GeneralItemStrategy)


@pytest.mark.parametrize(
    "item_name",
    [
        pytest.param("Generic", id="generic-name"),
        pytest.param("Something", id="unrecognized-name"),
        pytest.param("A", id="single-character"),
        pytest.param("", id="empty-name"),
        pytest.param("   ", id="whitespace-only"),
    ],
)
def test_generic_names_use_generic_strategy(item_name):
    assert_strategy(item_name, GeneralItemStrategy)


@pytest.mark.parametrize(
    "item_name, expected_strategy",
    [
        pytest.param(
            "Backstage passes to conjured brie",
            BackstagePassStrategy,
            id="backstage-before-conjured",
        ),
        pytest.param(
            "Conjured backstage passes",
            ConjuredItemStrategy,
            id="conjured-before-backstage",
        ),
        pytest.param(
            "Conjured brie",
            ConjuredItemStrategy,
            id="conjured-before-brie",
        ),
        pytest.param(
            "backstage passess to sulfuras",
            BackstagePassStrategy,
            id="backstage-and-sulfuras",
        ),
        pytest.param(
            "Sulfuras backstage passess",
            BackstagePassStrategy,
            id="sulfuras-before-backstage",
        ),
        pytest.param(
            "Sulfuras backstage passess",
            BackstagePassStrategy,
            id="duplicate-sulfuras-before-backstage",
        ),
        pytest.param(
            "Conjured aged brie",
            ConjuredItemStrategy,
            id="conjured-before-aged-brie",
        ),
    ],
)
def test_conflicting_names_follow_expected_precedence(
    item_name,
    expected_strategy,
):
    assert_strategy(item_name, expected_strategy)
