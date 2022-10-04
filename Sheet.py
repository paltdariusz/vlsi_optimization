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
        newBlocks = []
        for i in range(len(blocks)):
            currentGen = genotype[i]
            wantedOrientation = genotype[i+len(blocks)]
            currentBlock = blocks[currentGen]
            if currentBlock.orientation != wantedOrientation:
                currentBlock.flip()
            if currentBlock.width + self.currentWidth <= self.width:
                # mieści się na szerokość
                # if currentBlock.height + self.currentHeight <= self.height:
                    # mieści się na wysokość
                currentBlock.update(nPos=(self.currentWidth, self.currentHeight))                    
                self.usedWidth += currentBlock.width
                if currentBlock.height > self.usedHeight:
                    self.usedHeight = currentBlock.height
                self.currentWidth += currentBlock.width
                temp.append(currentGen)
                # else:
                    # nie miesci się na wysokość
                    # return np.inf, None

            else:
                self.positions.append(temp)
                temp = []
                # nie miesci się na szerokość
                # if currentBlock.height + self.currentHeight + self.usedHeight <= self.height:
                    # mieści się na wysokość
                self.currentHeight += self.usedHeight
                self.usedHeight = 0
                self.lineWidths.append(self.currentWidth)
                self.currentWidth = 0
                # if currentBlock.width + self.currentWidth <= self.width:
                currentBlock.update(nPos=(self.currentWidth, self.currentHeight))                    
                self.usedWidth += currentBlock.width
                if currentBlock.height > self.usedHeight:
                    self.usedHeight = currentBlock.height
                self.currentWidth += currentBlock.width
                temp.append(currentGen)
                #     else:
                #         # nie miesci się na długość
                #         return np.inf, None
                # else:
                #     return np.inf, None
            newBlocks.append(currentBlock)
        self.positions.append(temp)
       
        self.lineWidths.append(self.currentWidth)

        penaltyH = self.height - self.currentHeight+ self.usedHeight
        penaltyW = self.width - max(self.lineWidths) 
        penaltyH = np.abs(penaltyH) if penaltyH < 0 else 0
        penaltyW = np.abs(penaltyW) if penaltyW < 0 else 0
        # + 1000000 * (penaltyW + penaltyH)

        return max(self.lineWidths) * (self.currentHeight+ self.usedHeight) , newBlocks.copy()

    def reset_sim(self):
        self.usedWidth = 0
        self.usedHeight = 0
        self.currentHeight = 0
        self.currentWidth = 0
        self.positions = []
        self.lineWidths= []

if __name__ == '__main__':
    from Block import Block
    sheet = Sheet(200, 200)
    blocks = [
        Block(0, [0,0], 40, 30),
        Block(1, [0,0], 10, 70),
        Block(2, [0,0], 25, 70),
        Block(3, [0,0], 40, 60),
        Block(4, [0,0], 80, 40),
        Block(5, [0,0], 45, 60),
        Block(6, [0,0], 35, 70),
        Block(7, [0,0], 30, 60),
        Block(8, [0,0], 120, 40),
        Block(9, [0,0], 25, 60),
        Block(10, [0,0], 80, 70),
        Block(11, [0,0], 60, 60),
        Block(12, [0,0], 50, 70),
        Block(13, [0,0], 75, 30),
        Block(14, [0,0], 85, 30)]
    x,y = sheet.measureUsedArea([9, 1, 6, 0, 7, 2, 12, 3, 10, 11, 5, 4, 13, 8, 14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],blocks)
    for b in y:
        print(b)
    print(x)