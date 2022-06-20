from time import time
from typing import List
import numpy as np

class Optimizer:
    def __init__(self, populationSize, epochs, probMut, probCross, strongestToStay, blocks, sheet) -> None:
        self.populationSize = populationSize
        self.epochs = epochs
        self.probCross = probCross
        self.probMut = probMut 
        self.blocks = blocks
        self.sheet = sheet
        self.population = []
        self.strongestToStay = strongestToStay
        self.chosenFromPopulation = []

    def createPopulation(self):
        for i in range(self.populationSize - 6):
            temp = np.arange(0, len(self.blocks))
            np.random.shuffle(temp)
            self.population.append({
                'genotype' : list(temp) + [int(np.round(i)) for i in np.random.rand(len(self.blocks))],
                'id': i,
                'fitnessFunction': 0
            })
        
        self.population.append({
            'genotype': [block.id for block in sorted(self.blocks, reverse=True, key=lambda x:x.area)] \
                + [int(np.round(i)) for i in np.random.rand(len(self.blocks))],
            'id': i+1,
            'fitnessFunction': 0
        })
        self.population.append({
            'genotype': [block.id for block in sorted(self.blocks, reverse=True, key=lambda x:x.width)] \
                + [int(np.round(i)) for i in np.random.rand(len(self.blocks))],
            'id': i+2,
            'fitnessFunction': 0
        })
        self.population.append({
            'genotype': [block.id for block in sorted(self.blocks, reverse=True, key=lambda x:x.height)] \
                + [int(np.round(i)) for i in np.random.rand(len(self.blocks))],
            'id': i+3,
            'fitnessFunction': 0
        })
        self.population.append({
            'genotype': [block.id for block in sorted(self.blocks, reverse=True, key=lambda x:x.perimeter)] \
                + [int(np.round(i)) for i in np.random.rand(len(self.blocks))],
            'id': i+4,
            'fitnessFunction': 0
        })
        self.population.append({
            'genotype': [block.id for block in sorted(self.blocks, reverse=True, key=lambda x:x.maxWidthHeight)] + \
                [int(np.round(i)) for i in np.random.rand(len(self.blocks))],
            'id': i+5,
            'fitnessFunction': 0
        })
        self.population.append({'genotype': [block.id for block in sorted(self.blocks, reverse=True, key=lambda x:x.diagonalWidthHeight)] + \
            [int(np.round(i)) for i in np.random.rand(len(self.blocks))],
            'id': i+6,
            'fitnessFunction': 0
        })

    def fitnessFunction(self, genotype):
        return self.sheet.measureUsedArea(genotype.copy(), self.blocks.copy())

    def rouletteProb(self, fitnessVal, fitnessSum):
        return fitnessVal/fitnessSum

    def select(self,end = False):
        for i in range(self.populationSize):
            self.population[i]["fitnessFunction"] = self.fitnessFunction(self.population[i]["genotype"])
        
        self.population = [chromosome for chromosome in self.population if chromosome["fitnessFunction"]!=np.inf]
        print(self.population)
        print("\n\n\n\n\n")
        self.population.sort(key=lambda x: x["fitnessFunction"])
        if end:
            return
        self.chosenFromPopulation = self.population[:self.strongestToStay].copy()
        # print(0,self.chosenFromPopulation)
        # for i in range(len(self.chosenFromPopulation)):
        #     self.chosenFromPopulation[i]["fitnessFunction"] = self.fitnessFunction(self.chosenFromPopulation[i]["genotype"])
        # print(1,self.chosenFromPopulation)
        sumFitnessFunction = sum([val["fitnessFunction"] for val in self.chosenFromPopulation])
        # print(2,self.chosenFromPopulation)
        for i in range(len(self.chosenFromPopulation)):
            self.chosenFromPopulation[i]["rouletteProb"] = self.rouletteProb(self.chosenFromPopulation[i]["fitnessFunction"], sumFitnessFunction)
        
        


    def mutate(self, genotype) -> List:
        if np.random.rand() <= self.probMut:
            idxToSwap = np.random.choice(len(genotype) // 2, 2, replace=False)
            genotype[idxToSwap[0]], genotype[idxToSwap[1]] = genotype[idxToSwap[1]], genotype[idxToSwap[0]]
        if np.random.rand() <= self.probMut:
            idxToSwap = np.random.choice(len(genotype) // 2, 2, replace=False) + 4
            genotype[idxToSwap[0]], genotype[idxToSwap[1]] = genotype[idxToSwap[1]], genotype[idxToSwap[0]]
        return genotype

    def cross(self, genotypeA, genotypeB, cutIdx = [1,2]) -> List:
        off1 = genotypeA[:len(self.blocks)]
        idx = [genotypeA.index(genotypeB[cutIdx[0]]), genotypeA.index(genotypeB[cutIdx[1]])]
        if genotypeA[:3]==[0, 2, 1] and genotypeB[:3]==[2, 0, 1]:
            print()
        off1[idx[0]] = "H"
        off1[idx[1]] = "H"
        pos = set(cutIdx) - {idx[0], idx[1]} # indexy cyfr
        if idx[0] != cutIdx[0] and idx[0] != cutIdx[1]:
            x = list(pos)[0]
            off1[idx[0]], off1[x] = off1[x], off1[idx[0]]
            pos -= {x}
        if idx[1] != cutIdx[0] and idx[1] != cutIdx[1]:
            x = list(pos)[0]
            off1[idx[1]], off1[x] = off1[x], off1[idx[1]]
            pos -= {x}
        off1[cutIdx[0]], off1[cutIdx[1]] = genotypeB[cutIdx[0]], genotypeB[cutIdx[1]]
        off2 = np.logical_xor(genotypeA[len(self.blocks):],genotypeB[len(self.blocks):], dtype=int)
        if "H" in off1 or len(set(off1)) != len(self.blocks):
            raise ValueError(f"{genotypeA=} {genotypeB=} {off1=}")
        return off1 + list(map(int,off2))

    def start(self):
        self.createPopulation()
        for i in range(self.epochs):
            print(f"Epoch: {i}", end=" ")
            start = time()
            self.select()
            newPopulation = []
            print(self.chosenFromPopulation)
            probab = [val["rouletteProb"] for val in self.chosenFromPopulation]
            print(probab)
            while len(newPopulation) < self.populationSize:
                if 0 < len(self.chosenFromPopulation) < 2:
                    chosenOnes = [self.chosenFromPopulation[0], self.chosenFromPopulation[0]]
                else:
                    chosenOnes = np.random.choice(self.chosenFromPopulation,size=2, replace=False, p=probab)
                newPopulation.append({
                    'id': len(newPopulation),
                    'fitnessFunction': 0,
                    'genotype': self.cross(chosenOnes[0]["genotype"], chosenOnes[1]["genotype"]) if np.random.rand() <= self.probCross else chosenOnes[0]["genotype"]
                })
            print(f"Time: {time()-start}s", end=" ")
            print(f"Population's best: {self.population[0]['fitnessFunction']} {100* self.population[0]['fitnessFunction']/self.sheet.area}%")
            # print(f"{self.population[0]=}")
            self.population = newPopulation.copy()
            self.chosenFromPopulation = []
        self.select(end=True)
        print(f"Best chromosome: {self.population[0]['genotype']} {self.population[0]['fitnessFunction']} {100* self.population[0]['fitnessFunction']/self.sheet.area}%")