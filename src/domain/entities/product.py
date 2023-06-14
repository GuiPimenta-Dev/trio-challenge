class Product:
    def __init__(self, name, variations):
        self.name = name
        self._variations = variations

    @property
    def variations(self):
        return self._variations

    def has_variation(self, variation):
        return variation in self._variations
