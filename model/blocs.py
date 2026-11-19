class Bloc:
    """Bloc posé sur une case du circuit : départ ("1", "2"),
    point de passage ("C"), ligne d'arrivée ("L") ou boost ("B").
    effet : lettre du bloc. position : centre de la case en pixels.
    index : numéro du point de passage (seulement pour "C")."""

    def __init__(self, effet: str, position: tuple[float, float], index: int = 0):
        """`effet` : lettre du bloc. `position` : centre de la case en pixels.
        `index` : numéro du point de passage (seulement pour "C")."""
        self.effet = effet
        self.position = position
        self.index = index

    def numero_joueur(self):
        """Pour un bloc de départ, numéro du joueur (1 ou 2) ; sinon None."""
        if self.effet in ("1", "2"):
            return int(self.effet)
        else:
            return None

    def sur_passage(self, Joueur, race):
        """Applique l'effet du bloc quand la voiture du joueur entre sur la case."""
        if self.effet == "C":
            self.point_passage(Joueur)
        elif self.effet == "L":
            self.arrivee(Joueur, race)
        elif self.effet == "B":
            self.boost(Joueur)
        # "1" et "2" (départ) : aucun effet pendant la course

    def point_passage(self, Joueur):
        """Marque ce point de passage comme franchi."""
        Joueur.point_passage(self.index, self.position)

    def arrivee(self, Joueur, race):
        """Valide un tour si tous les points de passage ont été franchis."""
        if Joueur.tous_les_checkpoints(race.n_checkpoints):
            Joueur.tour_termine(self.position)
            race.tour_termine(Joueur)

    def boost(self, Joueur):
        """Active le boost de la voiture."""
        Joueur.car.apply_boost()