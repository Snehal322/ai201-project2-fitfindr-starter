from tools import (
    search_listings,
    suggest_outfit,
    create_fit_card
)

from utils.data_loader import (
    get_example_wardrobe,
    get_empty_wardrobe
)


def test_search_returns_results():

    results = search_listings(
        "vintage graphic tee",
        size=None,
        max_price=50
    )

    assert isinstance(results, list)
    assert len(results) > 0


def test_search_empty_results():

    results = search_listings(
        "designer ballgown",
        size="XXS",
        max_price=5
    )

    assert results == []


def test_search_price_filter():

    results = search_listings(
        "jacket",
        size=None,
        max_price=10
    )

    assert all(
        item["price"] <= 10
        for item in results
    )


def test_suggest_outfit_empty_wardrobe():

    result = suggest_outfit(
        {
            "title": "Vintage Tee",
            "category": "tops",
            "colors": ["black"],
            "style_tags": ["vintage"]
        },
        get_empty_wardrobe()
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_suggest_outfit_example_wardrobe():

    result = suggest_outfit(
        {
            "title": "Vintage Tee",
            "category": "tops",
            "colors": ["black"],
            "style_tags": ["vintage"]
        },
        get_example_wardrobe()
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_fit_card_empty_outfit():

    result = create_fit_card(
        "",
        {
            "title": "Vintage Tee",
            "price": 20,
            "platform": "depop"
        }
    )

    assert "unable" in result.lower()


def test_fit_card_generation():

    result = create_fit_card(
        "Pair it with wide-leg jeans and chunky sneakers.",
        {
            "title": "Vintage Tee",
            "price": 20,
            "platform": "depop"
        }
    )

    assert isinstance(result, str)
    assert len(result) > 0