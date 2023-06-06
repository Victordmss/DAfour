## DAfour
Development of a Connect 4 Game software for the Applied System Software course at the Riga University of Technology (RTU)

### Link for the report:
[Link](https://docs.google.com/document/d/1wj8dWIFPc39VEJFcaQ2we9zuJyPB9k3uuMuU6C9DiXs/edit?usp=sharing) for the report

### Group Members
- Victor Demessance - 230ADB010
- Artur Henrique Allen Santos - 230ADB012
- Sevda Imanigheshlaghchaei - 230ADB033
- Ahmad Foroughi - 230ADB034

## How to Run
1. Clone the repository
```bash
$ git clone https://github.com/Victordmss/DAfour
```
2. Go to the project folder
```bash
$ cd DAfour
```
3. Create a virtual environment
```bash
$ python3 -m venv venv
```
4. Activate the virtual environment
```bash
$ source venv/bin/activate
```
5. Install the requirements
```bash
$ pip install -r requirements.txt
```
6. Run the game
```bash
$ python3 main.py
```

## User Manual

![](resources/image/launching_background.png)

The first thing to do is to click on the screen to start the game. The user has the choice to click on any part of the screen.

![image](https://github.com/Victordmss/DAfour/assets/86049841/d60281e2-89dd-4eb3-86ee-7a6be98ec374)

The user arrives on the game screen. He can move the mouse to see directly the position of the piece he is going to play. Moreover, he can see the color of the piece thanks to the preview at the top of the board. Finally, the user can choose to click on the reset button to restart the game on the start screen.

![image](https://github.com/Victordmss/DAfour/assets/86049841/689f6106-86e6-41e9-af8e-349bc2a37445)

As the game progresses, the cells on the board fill up. If a move is victorious, the screen refreshes showing the winner (1 for the red player, always starting, and 2 for the yellow). The user can then look at the board to check this but cannot play any more. Finally, he can press the reset button to return to the start screen.

![image](https://github.com/Victordmss/DAfour/assets/86049841/61561f82-227f-47b1-836f-15b43f357bbf)

