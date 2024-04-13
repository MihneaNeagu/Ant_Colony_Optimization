import random
import numpy as np

class Ant:
    def __init__(self, num_cities, alpha, beta, q0, p, pheromone_matrix, distances):
        self.num_cities = num_cities
        self.alpha = alpha
        self.beta = beta
        self.q0 = q0
        self.p = p
        self.pheromone_matrix = pheromone_matrix
        self.distances = distances
        self.visited = [False] * num_cities
        self.tour = []
        self.tour_length = 0

    def transition_probability(self, current_city, next_city):
        if self.visited[next_city]:
            return 0

        pheromone = self.pheromone_matrix[current_city][next_city]
        distance = self.distances[current_city][next_city]

        if distance == 0:
            return 0

        vision = 1 / distance

        numerator = pheromone ** self.alpha * vision ** self.beta
        denominator = sum((self.pheromone_matrix[current_city][neighbor] ** self.alpha *
                            (1 / self.distances[current_city][neighbor]) ** self.beta)
                            for neighbor in range(self.num_cities) if not self.visited[neighbor])

        return numerator / denominator

    def select_next_city(self, current_city):
        q = random.random()
        if q < self.q0:
            return self.select_next_city_greedy(current_city)
        else:
            return self.select_next_city_probabilistic(current_city)

    def select_next_city_greedy(self, current_city):
        unvisited_cities = [city for city in range(self.num_cities) if not self.visited[city]]
        max_pheromone = float('-inf')
        selected_city = -1
        for city in unvisited_cities:
            pheromone = self.pheromone_matrix[current_city][city] ** self.alpha
            attractiveness = (1.0 / self.distances[current_city][city]) ** self.beta
            if pheromone * attractiveness > max_pheromone:
                max_pheromone = pheromone * attractiveness
                selected_city = city
        return selected_city
    def select_next_city_probabilistic(self, current_city):
        unvisited_cities = [city for city in range(self.num_cities) if not self.visited[city]]
        probabilities = [self.transition_probability(current_city, next_city) for next_city in unvisited_cities]
        selected_city = random.choices(unvisited_cities, weights=probabilities)[0]
        return selected_city
    def find_tour(self, pheromone_matrix):
        start_city = random.randint(0, self.num_cities - 1)
        self.visited[start_city] = True
        self.tour.append(start_city)
        current_city = start_city
        while len(self.tour) < self.num_cities:
            next_city = self.select_next_city(current_city)
            self.visited[next_city] = True
            self.tour.append(next_city)
            self.tour_length += self.distances[current_city][next_city]
            # Local pheromone update rule
            pheromone_matrix[current_city][next_city] = (1 - self.p) * pheromone_matrix[current_city][
                next_city] + self.p * 1
            current_city = next_city
        self.tour_length += self.distances[self.tour[-1]][self.tour[0]]

