from ant_colony_system import parse_input, ant_colony_system
from ant_colony_system import calculate_distances
from ant_colony_system import plot_pheromone_matrix, initialize_pheromone_matrix


def main_ant_colony_system():
    num_ants = 20
    alpha = 1
    beta = 2
    q0 = 0.9
    p = 0.1
    evaporation_rate = 0.001
    max_iterations = 100

    # Parse input
    cities = parse_input("tsp.txt")
    distances = calculate_distances(cities)

    # Run ACS
    (best_solution, best_solution_length, route_lengths, runtime,
     pheromone_matrix)= ant_colony_system(num_ants, alpha, beta, q0, p,
                                        evaporation_rate, cities, distances,
                                        max_iterations)

    print("Best solution:", best_solution)
    print("Best solution length:", best_solution_length)
    print("Runtime:", runtime, "seconds")

    # Calculate average route value
    average_route_value = sum(route_lengths) / len(route_lengths)
    print("Average route value over iterations:", average_route_value)

    # Plot pheromone matrix for the best solution
    plot_pheromone_matrix(pheromone_matrix, cities)


if __name__ == "__main__":
    main_ant_colony_system()

