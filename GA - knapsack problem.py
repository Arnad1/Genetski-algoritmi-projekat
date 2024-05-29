import random

class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value

items = [
    Item("Bottle", 1, 10),
    Item("Headphones", 0.5, 30),
    Item("Book", 2, 20),
    Item("Hat", 0.2, 5),
    Item("Laptop", 3, 70),
    Item("Camera", 1.5, 50),
    Item("Snacks", 0.8, 15),
    Item("Sunglasses", 0.1, 7),
    Item("Umbrella", 0.7, 12),
    Item("Wallet", 0.3, 25),
]

def fitness(chromosome):
    total_weight = 0
    total_value = 0
    for i, gene in enumerate(chromosome):
        if gene == 1:
            total_weight += items[i].weight
            total_value += items[i].value
    if total_weight > bag_weight:
        return 0
    return total_value

def selection(population):
    selected = []
    for _ in range(population_size):
        contestants = random.sample(population, 2)
        winner = max(contestants, key=fitness)
        selected.append(winner)
    return selected

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 2)
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    return offspring1, offspring2

def mutation(chromosome, mutation_rate):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = flip(chromosome[i])  
    return chromosome

def flip(gene):
    return 1 - gene

bag_weight = 5 
population_size = 100
generations = 50
mutation_rate = 0.01

population = [[random.randint(0, 1) for _ in range(len(items))] for _ in range(population_size)]

for gen in range(generations):
    selected_parents = selection(population)

    offspring = []
    for i in range(0, population_size, 2):
        parent1 = selected_parents[i]
        parent2 = selected_parents[(i + 1) % population_size] 
        offspring1, offspring2 = crossover(parent1, parent2)
        offspring.extend([offspring1, offspring2])

    offspring = [mutation(individual, mutation_rate) for individual in offspring]

    population = selected_parents + offspring

    population = sorted(population, key=fitness, reverse=True)[:population_size]

    best_chromosome = population[0]
    best_value = fitness(best_chromosome)
    print(f"Generation: {gen+1}, Best Value: {best_value}")

best_chromosome = population[0]
best_items = [items[i].name for i, gene in enumerate(best_chromosome) if gene == 1]
total_value = fitness(best_chromosome)
total_weight = sum(items[i].weight for i, gene in enumerate(best_chromosome) if gene == 1)

print(f"\nBest Items: {', '.join(best_items)}")
print(f"Total Value: {total_value}")
print(f"Total Weight: {total_weight}")
