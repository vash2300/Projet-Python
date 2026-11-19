class Joueur:
    """Joueur : sa voiture et sa progression dans la course.

    La progression, c'est le nombre de tours terminés, les points de
    passage franchis pendant le tour en cours et la position où la
    voiture réapparaît si elle tombe dans le vide.
    """
    def __init__(self, numero_joueur , car, start_position: tuple[float, float]):
        """Crée le joueur numero(1 ou 2) avec sa voiture.

        `start_position` (en pixels) sert de point de réapparition tant qu'aucun point de passage n'a été franchi.
        """
        self.numero = numero_joueur
        self.car = car
        self.laps: int = 0
        self.checkpoints = set()   # index franchis pendant ce tour
        self.last_checkpoint = start_position
        self.current_tile = None             # case où se trouve la voiture

    #chaque point de passage franchis et le point de réapparition sont enregistrés
    def point_passage(self, indice: int, position: tuple[float, float]):
        """Enregistre le point de passage `indice` et en fait le nouveau
        point de réapparition."""
        self.checkpoints.add(indice)
        self.last_checkpoint = position 

    #verifier si tous les points de passage ont été franchis
    def tous_les_checkpoints(self, n_checkpoints) -> bool:
        """Vrai si les `n_checkpoints` points de passage du circuit ont
        été franchis pendant ce tour."""
        return len(self.checkpoints) >= n_checkpoints

    #quand un tour est terminé, le nombre de tours est incrémenté et les points de passage sont réinitialisés
    def tour_termine(self, position: tuple[float, float]):
        """Termine un tour : +1 tour, on repart de zéro pour les points de
        passage, et la ligne d'arrivée devient le point de réapparition."""
        self.laps += 1
        self.checkpoints.clear()
        self.last_checkpoint = position
