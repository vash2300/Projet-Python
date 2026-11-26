"""Joueur : sa voiture et sa progression dans la course."""


class Joueur:
    """Un joueur de la course : sa voiture et où il en est.

    Les blocs du circuit (model/block.py) ne connaissent que la voiture :
    ils appellent car.progress.pass_checkpoint(...) et
    car.progress.cross_finish(...). Le joueur s'enregistre donc dans
    l'attribut progress de sa voiture, pour que les blocs le trouvent.

    Attributes
    ----------

    """

    def __init__(self, numero: int, car, pos_depart: tuple[float, float]):
        """Crée le joueur et le relie à sa voiture.

        Parameters
        ----------
        numero : int
            Numéro du joueur (1 ou 2).
        car : Car
            Voiture du joueur.
        start_position : tuple[float, float]
            Centre de la case de départ, en pixels. Sert de point de
            réapparition tant qu'aucun point de passage n'a été franchi.
        """
        self.numero = numero
        self.car = car
        self.laps = 0
        self.next_checkpoint = 0
        self.last_checkpoint = pos_depart
        self.current_tile = None

        # Les blocs passent par la voiture pour trouver le joueur
        car.progress = self


    def pass_checkpoint(self, index: int, position: tuple[float, float]) -> None:
        """Valide un point de passage (appelée par un bloc 'C').

        Les points se franchissent dans l'ordre a, b, c... Un point ne
        compte que si c'est le prochain attendu. Il devient alors le
        nouveau point de réapparition.
        """
        if index == self.next_checkpoint:
            self.next_checkpoint += 1
            self.last_checkpoint = position

    def cross_finish(self, nb_checkpoint: int) -> None:
        """Passage sur la ligne d'arrivée (appelée par un bloc 'L').

        Le tour compte seulement si tous les points de passage ont été
        franchis. On repart alors de zéro pour le tour suivant.
        """
        if self.next_checkpoint == nb_checkpoint:
            self.laps += 1
            self.next_checkpoint = 0