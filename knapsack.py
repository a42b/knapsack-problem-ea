import random
import matplotlib.pyplot as plt


def load_knapsack_instance(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    n, capacity = map(int, lines[0].strip().split())
    items = [tuple(map(int, line.strip().split())) for line in lines[1:]]
    return n, capacity, items


def fitness(individual, items, capacity):
    total_value = 0
    total_weight = 0
    for gene, (value, weight) in zip(individual, items):
        if gene:
            total_value += value
            total_weight += weight
    if total_weight > capacity:
        return 0
    return total_value


def initialize_population(pop_size, items, capacity):
    population = []
    for _ in range(pop_size):
        individual = [0] * len(items)
        indices = list(range(len(items)))
        random.shuffle(indices)
        total_weight = 0
        for i in indices:
            value, weight = items[i]
            if total_weight + weight <= capacity:
                individual[i] = 1
                total_weight += weight
        population.append(individual)
    return population


def tournament_selection(population, fitnesses, tournament_size=3):
    selected = random.sample(list(zip(population, fitnesses)), tournament_size)
    return max(selected, key=lambda x: x[1])[0]

def crossover(p1, p2):
    child1 = [p1[i] if random.random() < 0.5 else p2[i] for i in range(len(p1))]
    child2 = [p2[i] if random.random() < 0.5 else p1[i] for i in range(len(p1))]
    return child1, child2

def mutate(individual, mutation_rate):
    return [bit if random.random() > mutation_rate else 1 - bit for bit in individual]


def evolutionary_algorithm(filename, generations=200, pop_size=100, crossover_rate=0.8, mutation_rate=None):
    n, capacity, items = load_knapsack_instance(filename)
    if mutation_rate is None:
        mutation_rate = 1 / n 

    population = initialize_population(pop_size, items, capacity)
    fitness_history = []

    for generation in range(generations):
        fitnesses = [fitness(ind, items, capacity) for ind in population]
        new_population = []

        best_ind = max(zip(population, fitnesses), key=lambda x: x[1])[0]
        new_population.append(best_ind)

        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)

            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:]

            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            new_population.extend([child1, child2])

        population = new_population[:pop_size]
        best_fitness = max([fitness(ind, items, capacity) for ind in population])
        fitness_history.append(best_fitness)
        if generation % 10 == 0 or generation == generations - 1:
            print(f"Generation {generation}: Best Fitness = {best_fitness}")

    final_fitnesses = [fitness(ind, items, capacity) for ind in population]
    best_idx = final_fitnesses.index(max(final_fitnesses))
    best_individual = population[best_idx]
    total_weight = sum(weight for bit, (value, weight) in zip(best_individual, items) if bit)


    print("\nBest solution found:")
    print("Total value:", final_fitnesses[best_idx])
    print("Total weight:", total_weight)

    plt.plot(fitness_history)
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.title("Fitness over Generations")
    plt.grid(True)
    plt.show()

    return final_fitnesses[best_idx], best_individual

if __name__ == "__main__":
    filename = "input_1000.txt" 
    evolutionary_algorithm(filename, generations=250, pop_size=500)
