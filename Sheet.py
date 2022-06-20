import numpy as np

class Sheet:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.area = width * height
        self.usedWidth = 0
        self.usedHeight = 0
        self.currentHeight = 0
        self.currentWidth = 0
        self.positions = []
        self.lineWidths= []

    def measureUsedArea(self, genotype, blocks):
        blocks.sort(key=lambda x: x.id)
        self.reset_sim()
        temp = []
        for i in range(len(blocks)):
            currentGen = genotype[i]
            currentOrinent = genotype[i+len(blocks)]
            currentBlock = blocks[currentGen]
            if currentBlock.orientation != currentOrinent:
                currentBlock.flip()
            if currentBlock.width + self.currentWidth <= self.width:
                # mieści się na szerokość
                if currentBlock.height + self.currentHeight <= self.height:
                    # mieści się na wysokość
                    currentBlock.update(nPos=(self.currentWidth, self.currentHeight))                    
                    self.usedWidth += currentBlock.width
                    if currentBlock.height > self.usedHeight:
                        self.usedHeight = currentBlock.height
                    self.currentWidth += currentBlock.width
                    temp.append(currentGen)
                else:
                    # nie miesci się na wysokość
                    return np.inf
            else:
                self.positions.append(temp)
                temp = []
                # nie miesci się na szerokość
                if currentBlock.height + self.currentHeight + self.usedHeight <= self.height:
                    # mieści się na wysokość
                    self.currentHeight = self.usedHeight
                    self.usedHeight = 0
                    self.lineWidths.append(self.currentWidth)
                    self.currentWidth = 0
                    if currentBlock.width + self.currentWidth <= self.width:
                        currentBlock.update(nPos=(self.currentWidth, self.currentHeight))                    
                        self.usedWidth += currentBlock.width
                        if currentBlock.height > self.usedHeight:
                            self.usedHeight = currentBlock.height
                        self.currentWidth += currentBlock.width
                        temp.append(currentGen)
                    else:
                        # nie miesci się na długość
                        return np.inf
                else:
                    return np.inf
        self.positions.append(temp)
        if len(self.lineWidths) == 0:
            self.lineWidths.append(self.currentWidth)
        return max(self.lineWidths) * (self.currentHeight+ self.usedHeight)

    def reset_sim(self):
        self.usedWidth = 0
        self.usedHeight = 0
        self.currentHeight = 0
        self.currentWidth = 0
        self.positions = []
        self.lineWidths= []

if __name__ == '__main__':
    from Block import Block
    sheet = Sheet(10, 10)
    blocks = [Block(0, [0,0], 3, 3),Block(1, [0,0], 5, 3),Block(2, [0,0], 3, 5)]
    print(sheet.measureUsedArea([2,0,1,0,0,0],blocks), sheet.positions)