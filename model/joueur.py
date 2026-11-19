class Joueur:
    """Joueur : sa voiture et sa progression dans la course.

    La progression, c'est le nombre de tours terminés, les points de
    passage franchis pendant le tour en cours et la position où la
    voiture réapparaît si elle tombe dans le vide.
    """

    def __init__(self, numero_joueur: int, car, start_position: tuple[float, float]):
        """Crée le joueur numero(1 ou 2) avec sa voiture.

        `start_position` (en pixels) sert de point de réapparition tant qu'aucun point de passage n'a été franchi.
        """
        self.numero = numero_joueur
        self.car = car
        self.laps: int = 0
        self.checkpoints: set[int] = set()   # index franchis pendant ce tour
        self.last_checkpoint: tuple[float, float] = start_position
        self.current_tile = None             # case où se trouve la voiture

    def point_passage(self, indice: int, position: tuple[float, float]) -> None:
        """Enregistre le point de passage `indice` et en fait le nouveau
        point de réapparition."""
        self.checkpoints.add(indice)
        self.last_checkpoint = position

    def tous_les_checkpoints(self, n_checkpoints: int) -> bool:
        """Vrai si les `n_checkpoints` points de passage du circuit ont
        été franchis pendant ce tour."""
        return len(self.checkpoints) >= n_checkpoints

    def tour_termine(self, position: tuple[float, float]) -> None:
        """Termine un tour : +1 tour, on repart de zéro pour les points de
        passage, et la ligne d'arrivée devient le point de réapparition."""
        self.laps += 1
        self.checkpoints.clear()
        self.last_checkpoint = position
