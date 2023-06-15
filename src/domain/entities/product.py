class Product:
    def __init__(self, name, variations):
        self.name = name
        self.variation = None
        self.variations = variations

    def choose_variation(self, variation):
        variation_exists = variation.strip() in self.variations
        if not variation_exists:
            raise ValueError("Invalid variation")
        self.variation = variation

    def __repr__(self) -> str:  # pragma: no cover
        return str({"name": self.name, "variation": self.variation})
