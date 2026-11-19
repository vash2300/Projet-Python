from constants import GameState, GRID_ROWS, GRID_COLS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None
        self.cars: list[Car] = []
        self.noms_circuits = ["Anneau", "Désert", "Montagne"] # a remplacer par une liste de circuits réelsgit
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
        """Crée les deux voitures côte à côte.
        self.car reste la voiture du joueur 1, car le contrôleur l'utilise
        encore ; self.cars contient les deux voitures.
        """
        #a remplacer par la position de départ du circuit, ici c'est juste un exemple
        self.car = Car(7, 1)
        self.cars = [self.car, Car(8, 1, couleur=(50, 110, 230))] # couleur de la voiture du joueur 2

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        for car in self.cars:
            car.update_position()
