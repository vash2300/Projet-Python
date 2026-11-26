"""Terrains du jeu : route, herbe, terre, glace et vide.

Chaque terrain influence la dynamique des voitures (traction, seuil de
dérapage, frottements en dérapage). La classe `Terrain` est abstraite :
on ne peut instancier que ses sous-classes.
"""
from abc import ABC, abstractmethod

from constants import TERRAIN_STATS, TERRAIN_COLORS


class Terrain(ABC):
    """Classe abstraite représentant un type de terrain.

    Attributes
    ----------
    traction : float
        Facilité à accélérer / freiner sur ce terrain (1.0 = maximale).
    drift_threshold : float
        Angle (radians) entre orientation et vitesse au-delà duquel la
        voiture dérape. Plus il est grand, plus il est difficile de déraper.
    drift_friction : float
        Proportion de vitesse perdue par frame pendant un dérapage.
    """

    def __init__(self, traction: float, drift_threshold: float,
                 drift_friction: float):
        """Initialise les propriétés physiques du terrain.

        Parameters
        ----------
        traction : float
            Coefficient de traction.
        drift_threshold : float
            Seuil de déclenchement du dérapage.
        drift_friction : float
            Frottement appliqué pendant un dérapage.
        """
        self.traction = traction
        self.drift_threshold = drift_threshold
        self.drift_friction = drift_friction

    @abstractmethod
    def get_color(self) -> tuple[int, int, int]:
        """Retourne la couleur RVB utilisée pour dessiner le terrain."""
        pass

    def on_car_enter(self, car) -> None:
        """Appelée quand une voiture se trouve sur ce terrain.

        Par défaut, un terrain n'a pas d'effet particulier : seules les
        sous-classes qui en ont un (comme `Void`) surchargent cette méthode.

        Parameters
        ----------
        car : Car
            La voiture présente sur le terrain.
        """
        pass

    @staticmethod
    def from_char(char: str) -> "Terrain":
        """Crée un terrain à partir de son caractère dans un fichier circuit.

        Parameters
        ----------
        char : str
            'R' (route), 'G' (herbe), 'D' (terre), 'I' (glace) ou 'V' (vide).

        Returns
        -------
        Terrain
            Une nouvelle instance du terrain correspondant.

        Raises
        ------
        ValueError
            Si le caractère ne correspond à aucun terrain.
        """
        classes = {"R": Road, "G": Grass, "D": Dirt, "I": Ice, "V": Void}
        if char not in classes:
            raise ValueError(f"Terrain inconnu : '{char}'")
        return classes[char]()


class Road(Terrain):
    """Route : traction élevée, difficile de déraper, gros frottements."""

    def __init__(self):
        traction, threshold, friction = TERRAIN_STATS["road"]
        Terrain.__init__(self, traction, threshold, friction)

    def get_color(self) -> tuple[int, int, int]:
        return TERRAIN_COLORS["road"]


class Grass(Terrain):
    """Herbe : traction moyenne, facile de déraper, frottements importants."""

    def __init__(self):
        traction, threshold, friction = TERRAIN_STATS["grass"]
        Terrain.__init__(self, traction, threshold, friction)

    def get_color(self) -> tuple[int, int, int]:
        return TERRAIN_COLORS["grass"]


class Dirt(Terrain):
    """Terre : traction moyenne, très facile de déraper, frottements moyens."""

    def __init__(self):
        traction, threshold, friction = TERRAIN_STATS["dirt"]
        Terrain.__init__(self, traction, threshold, friction)

    def get_color(self) -> tuple[int, int, int]:
        return TERRAIN_COLORS["dirt"]


class Ice(Terrain):
    """Glace : faible traction, dérapage quasi permanent, presque sans frottement."""

    def __init__(self):
        traction, threshold, friction = TERRAIN_STATS["ice"]
        Terrain.__init__(self, traction, threshold, friction)

    def get_color(self) -> tuple[int, int, int]:
        return TERRAIN_COLORS["ice"]


class Void(Terrain):
    """Vide : la voiture est téléportée à son dernier point de passage."""

    def __init__(self):
        traction, threshold, friction = TERRAIN_STATS["void"]
        Terrain.__init__(self, traction, threshold, friction)

    def get_color(self) -> tuple[int, int, int]:
        return TERRAIN_COLORS["void"]

    def on_car_enter(self, car) -> None:
        """Surcharge : renvoie la voiture à son dernier point de passage."""
        car.respawn()
