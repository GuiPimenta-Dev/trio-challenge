from src.domain.entities.product import Product


def test_if_product_has_variation():
    latte = Product("Latte", ["Pumpkin Spice", "Vanilla", "Hazelnut"])

    assert latte.has_variation("Pumpkin Spice") is True
    assert latte.has_variation("Vanilla") is True
    assert latte.has_variation("Hazelnut") is True
    assert latte.has_variation("Caramel") is False
