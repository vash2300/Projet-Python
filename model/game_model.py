from constants import GameState, GRID_ROWS, GRID_COLS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None
        self.noms_circuits: list[str] = ["Anneau", "Désert"] # a remplacer par une liste de circuits réels
        self.index_selection: int = 0

    def circuit_suivant(self) -> None:
        """Sélectionne le circuit suivant (revient au premier après le dernier)."""
        if self.index_selection < len(self.noms_circuits) - 1: #eviter l'index out of range
            self.index_selection += 1
        else:
            self.index_selection = 0

    def circuit_precedent(self) -> None:
        """Sélectionne le circuit précédent (va au dernier avant le premier)."""
        if self.index_selection > 0: #eviter l'index out of range
            self.index_selection -= 1
        else:
            self.index_selection = len(self.noms_circuits) - 1

    def load_circuit(self) -> None:
        grid = [[RoadTile(col=col_idx, row=row_idx)
                for row_idx in range(GRID_COLS)] for col_idx in range(GRID_ROWS)]
        self.circuit = Circuit(grid=grid)
        self.spawn_car()

    def spawn_car(self) -> None:
        self.car = Car(7, 1)

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        self.car.update_position()
