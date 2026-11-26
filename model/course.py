"""Course : tours, points de passage et vainqueur."""


class Course:
    """Gère l'état de la course pendant qu'elle se déroule.

    À chaque frame, regarde la case sous chaque voiture. Quand une voiture
    arrive sur une nouvelle case, l'effet de la case est appliqué (terrain
    puis bloc). Le premier joueur qui termine tous les tours gagne.

    Attributes
    ----------
    circuit : Circuit
        Circuit de la course.
    joueurs : list[Joueur]
        Les deux joueurs.
    nb_laps : int
        Nombre de tours à faire pour gagner (lu dans le fichier circuit).
    nb_checkpoints : int
        Nombre de points de passage du circuit.
    winner : Joueur | None
        Le vainqueur, ou None tant que personne n'a gagné.
    """

    def __init__(self, circuit, joueurs: list):
        """Prépare une nouvelle course.

        Parameters
        ----------
        circuit : Circuit
            Circuit chargé depuis son fichier.
        joueurs : list[Joueur]
            Les joueurs, déjà placés sur leurs cases de départ.
        """
        self.circuit = circuit
        self.joueurs = joueurs
        self.nb_laps = circuit.nb_laps
        self.nb_checkpoints = circuit.nb_checkpoints
        self.winner = None

    def update(self) -> None:
        """Avance la course d'une frame, effets des cases, puis vainqueur."""
        if self.winner is not None:
            return
        for joueur in self.joueurs:
            self.check_tile(joueur)
            if joueur.laps >= self.nb_laps and self.winner is None:
                self.winner = joueur

    def check_tile(self, joueur) -> None:
        """Applique l'effet de la case sur laquelle arrive la voiture.

        L'effet n'est appliqué qu'au moment où la voiture change de case :
        à 60 images par seconde, sinon un boost serait déclenché à chaque frame.

        Parameters
        ----------
        joueur : Joueur
            Joueur dont on vérifie la voiture.
        """
        car = joueur.car
        tile = self.circuit.get_tile_at_pixel(car.x, car.y)

        if tile is None:
            # L'extérieur de la carte est considéré comme du vide
            car.respawn()
            joueur.current_tile = None
        elif tile is not joueur.current_tile:
            joueur.current_tile = tile
            tile.on_car_enter(car, self.circuit)

    def winner(self) -> bool:
        """Indique si la course est terminée (un joueur a gagné)."""
        return self.winner is not None