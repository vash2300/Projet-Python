class Bloc:
    """Bloc posé sur une case du circuit : départ ("1", "2"),
    point de passage ("C"), ligne d'arrivée ("L") ou boost ("B")."""

    def __init__(self, effet: str, position: tuple[float, float], index: int | None = None):
        """`effet` : lettre du bloc. `position` : centre de la case en pixels.
        `index` : numéro du point de passage (seulement pour "C")."""
        self.effet = effet
        self.position = position
        self.index = index
