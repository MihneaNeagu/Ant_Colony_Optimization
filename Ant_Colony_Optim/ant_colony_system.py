import math
import random
from ant import Ant
import numpy as np
import matplotlib.pyplot as plt
import time


class City:
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y


def initialize_pheromone_matrix(num_cities):
    pheromone_matrix = np.ones((num_cities, num_cities))  # Initialize pheromone matrix with ones
    return pheromone_matrix


def parse_input(filename):
    cities = []
    with open(filename, 'r') as file:
        lines = file.readlines()[6:-1]
        for line in lines:
            parts = line.split()
            city = City(int(parts[0]), int(parts[1]), int(parts[2]))
            cities.append(city)
    return cities


def euclidean_distance(city1, city2):
    xd = city1.x - city2.x
    yd = city1.y - city2.y
    return round(math.sqrt(xd ** 2 + yd ** 2))


def calculate_distances(cities):
    num_cities = len(cities)
    distances = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            distance = euclidean_distance(cities[i], cities[j])
            distances[i][j] = distance
            distances[j][i] = distance
    return distances


def update_pheromone(pheromone_matrix, ants, evaporation_rate, p, L_plus):
    num_cities = len(pheromone_matrix)
    # Evaporation
    pheromone_matrix *= (1 - evaporation_rate)
    # Pheromone deposit
    for ant in ants:
        for i in range(len(ant.tour) - 1):
            city1, city2 = ant.tour[i], ant.tour[i + 1]
            delta_tau = 1 / L_plus if ant.tour_length == L_plus else 0
            pheromone_matrix[city1][city2] += p * delta_tau


def ant_colony_system(num_ants, alpha, beta, q0, p, evaporation_rate, cities, distances, max_iterations):
    for _ in range(10):
        num_cities = len(cities)
        pheromone_matrix = initialize_pheromone_matrix(num_cities)
        best_solution = None
        best_solution_length = float('inf')
        route_lengths = []

        start_time = time.time()

        for iteration in range(max_iterations):
            ants = [Ant(num_cities, alpha, beta, q0, p, pheromone_matrix, distances) for _ in range(num_ants)]
            for ant in ants:
                ant.find_tour(pheromone_matrix)
                if ant.tour_length < best_solution_length:
                    best_solution = ant.tour
                    best_solution_length = ant.tour_length
            route_lengths.append(best_solution_length)
            update_pheromone(pheromone_matrix, ants, evaporation_rate, p, best_solution_length)

        end_time = time.time()
        runtime = end_time - start_time

        return best_solution, best_solution_length, route_lengths, runtime, pheromone_matrix


def plot_pheromone_matrix(pheromone_matrix, cities):
    num_cities = len(cities)
    plt.figure(figsize=(10, 8))
    plt.imshow(pheromone_matrix, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Pheromone Level')
    plt.xticks(range(num_cities), [city.number for city in cities], rotation=45)
    plt.yticks(range(num_cities), [city.number for city in cities])
    plt.xlabel('To City')
    plt.ylabel('From City')
    plt.title('Pheromone Matrix')
    plt.show()

