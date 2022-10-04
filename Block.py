import numpy as np

class Block:
    def __init__(self, id, pos, width, height) -> None:
        self.id = id
        self.pos = pos
        self.width = width
        self.height = height
        self.orientation = 1 if height >= width else 0
        self.area = width * height
        self.perimeter = 2* (width + height)
        self.maxWidthHeight = max(width, height)
        self.diagonal = np.sqrt(width**2 + height**2)
        self.diagonalWidthHeight = self.diagonal+width+height

    def update(self, nPos=None, nOrientation=None):
        if nPos is not None:
            self.pos = nPos
        if nOrientation is not None:
            self.orientation = nOrientation

    def flip(self):
        self.height, self.width = self.width, self.height
        self.orientation = 1 if self.orientation==0 else 0

    def __str__(self) -> str:
        return f"Block:{self.id}, h:{self.height}, w:{self.width}, pos:{self.pos}, orientation:{self.orientation}"
