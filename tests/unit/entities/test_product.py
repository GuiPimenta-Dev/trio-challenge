import pytest

from src.domain.entities.product import Product


def test_if_variation_is_chosen_correctly():
    latte = Product("Latte", ["Pumpkin Spice", "Vanilla", "Hazelnut"])

    latte.choose_variation("Vanilla")

    assert latte.variation == "Vanilla"


def test_if_an_error_is_raised_if_variation_is_not_found():
    latte = Product("Latte", ["Pumpkin Spice", "Vanilla", "Hazelnut"])

    with pytest.raises(ValueError) as excinfo:
        latte.choose_variation("invalid_variation")

    assert "Invalid variation" in str(excinfo.value)
