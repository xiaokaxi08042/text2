import random
import copy
import codecs


class Genetic_alg:
    def __init__(self, weights, support_points, threshold):
        self.weights = weights
        self.support_points = support_points
        self.threshold = threshold
        self.size = len(weights)
        self.populations = []

    def construct_populations(self, times):
        local_populations = []
        local_populations.append([0 for i in range(self.size)])
        for k in range(times):
            chromosome = []
            for i in range(self.size):
                chromosome.append(random.randint(0, 1))
            local_populations.append(chromosome)
        self.selection(local_populations)

    def Mating(self, times=10):
        local_chromosomes = []
        self.populations.sort(key=lambda each: self.compute_points(each), reverse=True)
        total_points = 0
        for each in self.populations:
            total_points += self.compute_points(each)
        for i in range(times):
            father = random.randint(0, total_points)
            mother = random.randint(0, total_points)
            father_chromosome, mother_chromosome = self.Crossover(father, mother)
            local_chromosomes.append(father_chromosome)
            local_chromosomes.append(mother_chromosome)
        self.selection(local_chromosomes)

    def Crossover(self, father, mother):
        father_chromosome = copy.deepcopy(self.populations[-1])
        mother_chromosome = copy.deepcopy(self.populations[-1])
        # bug
        for each in self.populations:
            if self.compute_points(each) > father:
                father_chromosome = each
            else:
                father -= self.compute_points(each)
        for each in self.populations:
            if self.compute_points(each) > mother:
                mother_chromosome = each
            else:
                mother -= self.compute_points(each)
        mating_points = random.randint(0, self.size - 1)
        while mating_points < self.size:
            father_chromosome[mating_points], mother_chromosome[mating_points] \
                = mother_chromosome[mating_points], father_chromosome[mating_points]
            mating_points += 1
        return self.Mutation(father_chromosome, 20), self.Mutation(mother_chromosome, 20)

    def Mutation(self, chromosome, times=1):
        tmp = copy.deepcopy(chromosome)
        for i in range(times):
            mutation_point = random.randint(0, self.size - 1)
            tmp[mutation_point] = 1 - tmp[mutation_point]
        return tmp

    def selection(self, chromosomes):
        local_chromosomes = set()
        for each in chromosomes:
            tmp = self.compute_weights(each)
            if tmp <= self.threshold:
                local_chromosomes.add(' '.join([str(value) for value in each]))
        for each in local_chromosomes:
            self.populations.append([int(value) for value in each.split(' ')])

    def compute_weights(self, chromosome):
        tmp = 0
        for i in range(len(chromosome)):
            if chromosome[i] == 1:
                tmp += self.weights[i]
        return tmp

    def compute_points(self, chromosome):
        tmp = 0
        for i in range(len(chromosome)):
            if chromosome[i] == 1:
                tmp += self.support_points[i]
        return tmp

    def final_result(self):
        self.populations.sort(key=lambda each: self.compute_points(each), reverse=True)
        return self.populations[0]


def evaluation(weights, points, threshold):
    result = [0 for i in range(threshold + 1)]
    size = len(weights)
    for i in range(size):
        if i == 0:
            continue
        j = threshold
        while j > 0:
            if j >= weights[i]:
                result[j] = max(result[j], result[j - weights[i]] + points[i])
            j -= 1
    return max(result)

if __name__ == '__main__':
    with codecs.open('beibao3.txt', 'r') as f:
        first = 1
        weights = []
        points = []
        weights.append(0)
        points.append(0)
        threshold = 0
        for each in f.readlines():
            each = each.strip('\n')
            array = each.split(' ')
            if first:
                threshold = int(array[0])
                first = 0
            else:
                weights.append(int(array[0]))
                points.append(int(array[1]))
    alg = Genetic_alg(weights, points, threshold)
    alg.construct_populations(1000)
    alg.Mating(10000)
    print(alg.final_result())
    print('Points:' + str(alg.compute_points(alg.final_result())))
    print('Weights:' + str(alg.compute_weights(alg.final_result())))
    print(points)
    print(evaluation(weights, points, threshold))
