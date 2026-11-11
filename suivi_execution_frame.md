# Exercice 2 – Suivre l'exécution d'une frame

## 1. Objectif
Suivre l'exécution du programme pendant une frame
lorsque le joueur maintient la touche avancer.

## 2. Suivi des appels de méthodes

### Initialisation

| Ordre | Fichier/Classe | Méthode appelée | Appelée depuis | MVC | Rôle |
|---|---|---|---|---|---|
| 1 | main.py | main() | Projet-Python (point de départ) | — | Lance le programme |
| 2 | Pygame | pygame.init() | main() | — | Initialise les modules Pygame |
| 3 | Pygame | pygame.display.set_caption() | main() | — | Définit le titre de la fenêtre |
| 4 | GameController | __init__() | main() via GameController() | Controller | Initialise le contrôleur |
| 5 | Pygame | pygame.display.set_mode() | GameController.__init__() | — | Crée la fenêtre du jeu |
| 6 | Pygame | pygame.time.Clock() | GameController.__init__() | — | Crée l'horloge pour gérer les FPS |
| 7 | GameModel | __init__() | GameController.__init__() via GameModel() | Model | Initialise l'état du jeu, le circuit et la voiture |
| 8 | GameView | __init__() | GameController.__init__() via GameView() | View | Initialise la vue et récupère la fenêtre |
| 9 | Pygame | pygame.font.SysFont() | GameView.__init__() | — | Crée la police d'écriture |
| 10 | InputHandler | __init__() | GameController.__init__() via InputHandler() | Controller | Initialise le gestionnaire des entrées clavier |
| 11 | GameController | run() | main() | Controller | Lance la boucle principale |

### Suivi des frames

**Le suivi d'une frame est valable que dans le cas ou on est en course et le joueur maintient la touche ”avancer”**

| Ordre | Fichier/Classe | Méthode | Appelée depuis | MVC | Rôle |
|---|---|---|---|---|---|
| 1 | GameController | handle_events() | run() | Controller | Récupère et traite les événements |
| 2 | Pygame | pygame.event.get() | handle_events() | — | Récupère les événements en attente |
| 3 | GameController | update() | run() | Controller | Coordonne la mise à jour du jeu |
| 4 | InputHandler | get_inputs() | GameController.update() | Controller | Récupère les touches maintenues |
| 5 | Pygame | pygame.key.get_pressed() | get_inputs() | — | Récupère l'état actuel des touches |
| 6 | GameController | apply_input() | GameController.update() | Controller | Applique les commandes du joueur |
| 7 | Car | accelerate() | GameController.apply_input() | Model | Augmente la vitesse de la voiture |
| 8 | GameModel | update() | GameController.update() | Model | Met à jour la logique du modèle |
| 9 | Car | update_position() | GameModel.update() | Model | Actualise la position de la voiture |
| 10 | GameController | render() | run() | Controller | Demande à la vue d'afficher le jeu |
| 11 | GameView | draw() | GameController.render() | View | Gère l'affichage du jeu |
| 12 | Pygame | screen.fill() | GameView.draw() | — | Efface l'écran avec la couleur de fond |
| 13 | GameView | _draw_racing() | GameView.draw() | View | Dessine le circuit et la voiture |
| 14 | RoadTile | get_sprite() | GameView._draw_racing() | Model | Récupère l'image de chaque case du circuit |
| 15 | Pygame | screen.blit() | GameView._draw_racing() | — | Affiche chaque case du circuit |
| 16 | Car | get_rotated_sprite() | GameView._draw_racing() | Model | Récupère l'image transformée de la voiture et son rectangle |
| 17 | Pygame | pygame.transform.rotate() | Car.get_rotated_sprite() | — | Applique la rotation à l'image de la voiture |
| 18 | Pygame | get_rect() | Car.get_rotated_sprite() | — | Calcule le rectangle de positionnement de la voiture |
| 19 | Pygame | screen.blit() | GameView._draw_racing() | — | Affiche la voiture à sa nouvelle position |
| 20 | Pygame | pygame.display.flip() | GameView.draw() | — | Actualise l'écran |
| 21 | Pygame | clock.tick(FPS) | run() | — | Limite la fréquence d'exécution de la boucle |

## 3. Schéma d'enchaînement des appels

### Initialisation

main.py
└── main()
    ├── pygame.init()
    ├── pygame.display.set_caption()
    ├── GameController()
    │   └── GameController.__init__()
    │       ├── pygame.display.set_mode()
    │       ├── pygame.time.Clock()
    │       ├── GameModel()
    │       │   └── GameModel.__init__()
    │       ├── GameView()
    │       │   └── GameView.__init__()
    │       │       └── pygame.font.SysFont()
    │       └── InputHandler()
    │           └── InputHandler.__init__()
    └── controller.run()

### Suivi d'une frame

GameController.run()
│
├── 1. handle_events()
│   └── pygame.event.get()
│
├── 2. update()
│   ├── InputHandler.get_inputs()
│   │   └── pygame.key.get_pressed()
│   │
│   ├── apply_input()
│   │   └── Car.accelerate()
│   │
│   └── GameModel.update()
│       └── Car.update_position()
│
├── 3. render()
│   └── GameView.draw()
│       ├── screen.fill()
│       │
│       ├── _draw_racing()
│       │   ├── RoadTile.get_sprite() [pour chaque case]
│       │   ├── screen.blit() [pour chaque case]
│       │   ├── Car.get_rotated_sprite()
│       │   │   ├── pygame.transform.rotate()
│       │   │   └── get_rect()
│       │   └── screen.blit() [pour la voiture]
│       │
│       └── pygame.display.flip()
│
└── 4. clock.tick(FPS)

Retour au début du ‘while self.running‘ du ‘controller.run()‘

## 4. Conclusion
À chaque frame, le GameController orchestre le déroulement du jeu en trois grandes étapes. Il commence par récupérer les événements et les entrées du joueur, puis transmet les commandes au modèle (GameModel et Car) afin de mettre à jour la vitesse et la position de la voiture. Enfin, il demande à la vue (GameView) d'afficher le circuit et la voiture avec leurs nouvelles positions. La frame se termine par clock.tick(FPS), qui contrôle la fréquence d'exécution de la boucle. Ce processus se répète tant que le jeu est en cours d'exécution.

**Entrées utilisateur → Mise à jour du modèle → Affichage → Frame suivante.**