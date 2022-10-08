import numpy as np


class Cube:
    def __init__(self) -> None:
        self.walls = np.full((6, 3, 3), -1)

    def reset(self) -> None:
        for i in range(6):  
            self.walls[i] = np.full((3, 3), i)
    
    def get_color(self, id) -> tuple[int, int, int]:
        return {
            0: (255, 255, 255),  # WHITE
            1: (0, 255, 0),      # GREEN
            2: (255, 0, 0),      # RED
            3: (0, 0, 255),      # BLUE
            4: (255, 165, 0),    # ORANGE
            5: (255, 255, 0)     # YELLOW
        }[self.walls.flat[id]]

    def u(self) -> None:
        self.walls[0] = np.rot90(self.walls[0], k=3)
        self.walls[[1, 2, 3, 4], 0] = self.walls[[2, 3, 4, 1], 0]
        print(self.walls)
        print(self.walls.flatten())

    def r(self) -> None:
        self.walls[2] = np.rot90(self.walls[2], k=3)
        self.walls[[1, 0, 3, 5], :, 2] = self.walls[[5, 1, 0, 3], :, 2]

    def d(self) -> None:
        self.walls[5] = np.rot90(self.walls[5], k=3)    
        self.walls[[1, 2, 3, 4], 2] = self.walls[[4, 1, 2, 3], 2]

    def l(self) -> None:
        self.walls[4] = np.rot90(self.walls[4], k=1)
        self.walls[[1, 0, 3, 5], :, 0] = self.walls[[0, 3, 5, 1], :, 0]
        print(self.walls)
        print(self.walls.flatten())



if __name__ == "__main__":
    cube = Cube()
    cube.reset()
    cube.r()

    print(cube.walls)

