"""Circuit : grille de cases chargée depuis un fichier texte.

Format d'un fichier circuit :

    # ligne de commentaire
    name: Prairie
    laps: 3
    start_angle: 0
    ---
    G. G. Gb G. ...

Après la ligne '---', chaque ligne est une rangée de cases séparées par
des espaces. Une case s'écrit avec deux caractères : le terrain puis le bloc.
    Terrain : R route, G herbe, D terre, I glace, V vide
    Bloc    : . aucun, 1 / 2 départs, L arrivée, B boost,
              a b c ... points de passage (dans l'ordre)
"""
import os

from constants import TILE_SIZE, CIRCUITS_DIR
from model.tile import Tile
from model.terrain import Terrain
from model.block import (
    Block, StartBlock, CheckpointBlock, FinishLineBlock
)


class Circuit:
    """Grille 2D de cases avec ses règles de course.

    Attributes
    ----------
    grid : list[list[Tile]]
        Les cases, indexées par grid[row][col].
    rows : int
        Nombre de lignes.
    cols : int
        Nombre de colonnes.
    name : str
        Nom du circuit.
    nb_laps : int
        Nombre de tours à effectuer pour gagner.
    start_angle : float
        Direction de départ des voitures en degrés (0 = vers la droite,
        90 = vers le haut, convention trigonométrique).
    nb_checkpoints : int
        Nombre de points de passage (calculé à partir de la grille).
    starts : dict[int, tuple[int, int]]
        Case de départ (col, row) de chaque joueur (calculé).
    """

    def __init__(self, grid: list[list[Tile]], name: str = "Sans nom",
                 nb_laps: int = 3, start_angle: float = 0.0):
        """
        Parameters
        ----------
        grid : list[list[Tile]]
            Les cases du circuit.
        name : str
            Nom du circuit.
        nb_laps : int
            Nombre de tours.
        start_angle : float
            Direction de départ en degrés.

        Raises
        ------
        ValueError
            Si les blocs de la grille sont incohérents (voir
            `__analyse_blocks`).
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        self.name = name
        self.nb_laps = nb_laps
        self.start_angle = start_angle
        self.nb_checkpoints = 0
        self.starts: dict[int, tuple[int, int]] = {}
        self.__analyse_blocks()

    def __analyse_blocks(self) -> None:
        """Parcourt la grille pour remplir `starts` et `nb_checkpoints`.

        Vérifie aussi que le circuit est jouable.

        Raises
        ------
        ValueError
            Si un départ est dupliqué ou manquant, si les points de passage
            ne sont pas numérotés 0, 1, 2... sans trou, ou s'il n'y a pas
            de ligne d'arrivée.
        """
        checkpoint_indexes = set()
        has_finish_line = False

        for row in self.grid:
            for tile in row:
                block = tile.block
                if isinstance(block, StartBlock):
                    if block.player_id in self.starts:
                        raise ValueError(
                            f"Départ du joueur {block.player_id} en double")
                    self.starts[block.player_id] = (tile.col, tile.row)
                elif isinstance(block, CheckpointBlock):
                    checkpoint_indexes.add(block.index)
                elif isinstance(block, FinishLineBlock):
                    has_finish_line = True

        if sorted(self.starts) != [1, 2]:
            raise ValueError("Il faut un départ '1' et un départ '2'")
        if not has_finish_line:
            raise ValueError("Il faut au moins un bloc d'arrivée 'L'")
        if not checkpoint_indexes:
            raise ValueError("Il faut au moins un point de passage")
        if checkpoint_indexes != set(range(len(checkpoint_indexes))):
            raise ValueError(
                "Les points de passage doivent être a, b, c... sans trou")

        self.nb_checkpoints = len(checkpoint_indexes)

    @classmethod
    def from_file(cls, path: str) -> "Circuit":
        """Construit un circuit à partir d'un fichier texte.

        Parameters
        ----------
        path : str
            Chemin du fichier circuit.

        Returns
        -------
        Circuit
            Le circuit chargé.

        Raises
        ------
        ValueError
            Si le fichier est mal formé (message avec ligne et colonne).
        """
        header: dict[str, str] = {}
        grid_lines: list[str] = []
        in_grid = False

        with open(path, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line == "---":
                    in_grid = True
                elif in_grid:
                    grid_lines.append(line)
                else:
                    key, _, value = line.partition(":")
                    header[key.strip()] = value.strip()

        if not grid_lines:
            raise ValueError(f"{path} : aucune grille trouvée après '---'")

        grid = []
        for row_idx, line in enumerate(grid_lines):
            tokens = line.split()
            if row_idx > 0 and len(tokens) != len(grid[0]):
                raise ValueError(
                    f"{path}, ligne {row_idx + 1} de la grille : "
                    f"{len(tokens)} cases au lieu de {len(grid[0])}")
            row = []
            for col_idx, token in enumerate(tokens):
                try:
                    if len(token) != 2:
                        raise ValueError("une case s'écrit avec 2 caractères")
                    terrain = Terrain.from_char(token[0])
                    block = Block.from_char(token[1])
                except ValueError as error:
                    raise ValueError(
                        f"{path}, ligne {row_idx + 1}, colonne "
                        f"{col_idx + 1} : {error}") from error
                row.append(Tile(col_idx, row_idx, terrain, block))
            grid.append(row)

        return cls(
            grid,
            name=header.get("name", os.path.basename(path)),
            nb_laps=int(header.get("laps", 3)),
            start_angle=float(header.get("start_angle", 0)),
        )

    @staticmethod
    def list_files(directory: str = CIRCUITS_DIR) -> list[str]:
        """Liste les fichiers circuits (.txt) d'un dossier, triés par nom.

        Utile pour construire le menu de choix du circuit.

        Parameters
        ----------
        directory : str
            Dossier à explorer.

        Returns
        -------
        list[str]
            Chemins complets des fichiers circuits.
        """
        names = sorted(n for n in os.listdir(directory) if n.endswith(".txt"))
        return [os.path.join(directory, n) for n in names]

    def get_tile(self, col: int, row: int) -> Tile | None:
        """Retourne la case (col, row), ou None si elle est hors de la carte.

        Une valeur None est à traiter comme du vide (l'extérieur de la carte
        est considéré comme du vide).
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> Tile | None:
        """Retourne la case située au pixel (px, py), ou None hors carte."""
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)

    def pixel_width(self) -> int:
        """Largeur du circuit en pixels."""
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        """Hauteur du circuit en pixels."""
        return self.rows * TILE_SIZE
