"""Blocs posés sur les cases du circuit.

Un bloc a un effet quand une voiture passe dessus : point de passage,
ligne d'arrivée, boost ou position de départ. La classe `Block` est
abstraite et chaque sous-classe implémente `on_car_enter`.

Contrat avec la partie "Voiture" (attributs/méthodes attendus sur `car`) :
    - car.x, car.y                      : position en pixels
    - car.progress.pass_checkpoint(index, pos)
    - car.progress.cross_finish(nb_checkpoints)
    - car.apply_boost(strength, duration)
"""
from abc import ABC, abstractmethod

from constants import BOOST_STRENGTH, BOOST_DURATION


class Block(ABC):
    """Classe abstraite d'un bloc posé sur une case.

    Attributes
    ----------
    label : str
        Symbole affiché sur le bloc (ex : 'C', 'L', 'B', '1', '2').
    """

    def __init__(self, label: str):
        """Initialise le bloc.

        Parameters
        ----------
        label : str
            Symbole affiché à l'écran.
        """
        self.label = label

    @abstractmethod
    def on_car_enter(self, car, circuit) -> None:
        """Applique l'effet du bloc à une voiture qui passe dessus.

        Parameters
        ----------
        car : Car
            La voiture présente sur le bloc.
        circuit : Circuit
            Le circuit en cours (utile pour connaître le nombre de points
            de passage, retrouver la case, etc.).
        """
        pass

    @staticmethod
    def from_char(char: str) -> "Block | None":
        """Crée un bloc à partir de son caractère dans un fichier circuit.

        Parameters
        ----------
        char : str
            '.' (aucun bloc), '1' ou '2' (départ), 'L' (arrivée),
            'B' (boost) ou une lettre minuscule 'a' à 'z' (point de passage
            numéro 0 à 25).

        Returns
        -------
        Block | None
            Le bloc créé, ou None s'il n'y a pas de bloc ('.').

        Raises
        ------
        ValueError
            Si le caractère ne correspond à aucun bloc.
        """
        if char == ".":
            return None
        if char in ("1", "2"):
            return StartBlock(int(char))
        if char == "L":
            return FinishLineBlock()
        if char == "B":
            return BoostBlock()
        if "a" <= char <= "z":
            return CheckpointBlock(ord(char) - ord("a"))
        raise ValueError(f"Bloc inconnu : '{char}'")


class StartBlock(Block):
    """Position de départ d'un joueur. Sans effet pendant la course."""

    def __init__(self, player_id: int):
        """
        Parameters
        ----------
        player_id : int
            Numéro du joueur (1 ou 2).
        """
        Block.__init__(self, str(player_id))
        self.player_id = player_id

    def on_car_enter(self, car, circuit) -> None:
        """Ne fait rien : ce bloc sert seulement à placer les voitures."""
        pass


class CheckpointBlock(Block):
    """Point de passage : mémorise la progression de la voiture."""

    def __init__(self, index: int):
        """
        Parameters
        ----------
        index : int
            Numéro du point de passage (0 = le premier à franchir).
        """
        Block.__init__(self, "C")
        self.index = index

    def on_car_enter(self, car, circuit) -> None:
        """Valide le point de passage et mémorise le centre de sa case.

        Le centre de la case servira de point de réapparition de la voiture.
        """
        tile = circuit.get_tile_at_pixel(car.x, car.y)
        car.progress.pass_checkpoint(self.index, tile.get_center())


class FinishLineBlock(Block):
    """Ligne d'arrivée : compte un tour si tous les points sont passés."""

    def __init__(self):
        Block.__init__(self, "L")

    def on_car_enter(self, car, circuit) -> None:
        """Demande à la progression de la voiture de valider un tour."""
        car.progress.cross_finish(circuit.nb_checkpoints)


class BoostBlock(Block):
    """Boost : donne un bonus d'accélération temporaire."""

    def __init__(self, strength: float = BOOST_STRENGTH,
                 duration: int = BOOST_DURATION):
        """
        Parameters
        ----------
        strength : float
            Bonus d'accélération.
        duration : int
            Durée du boost en frames.
        """
        Block.__init__(self, "B")
        self.strength = strength
        self.duration = duration

    def on_car_enter(self, car, circuit) -> None:
        """Applique le boost à la voiture."""
        car.apply_boost(self.strength, self.duration)
