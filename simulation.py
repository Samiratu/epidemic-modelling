from person import *
from disease import *
from aluLib import *
from random import *

# Constants for drawing
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
BAR_HEIGHT = 80
BAR_Y_COORD = 300
LEGEND_SIZE = 30
LEGEND_OFFSET = 250
LEGEND_TEXT_OFFSET = 210

# user
disease_name = input("What is the disease you are simulating: ")
original_population_size = int(input("What is the total population you are simulating: "))
immune_count = int(input("What is the total number of immune people: "))
original_infected = int(input("What is the total number of infected people: "))
infected_count = original_infected
deceased_count = 0
susceptible_count = original_population_size - immune_count - infected_count - deceased_count
rate_of_infection = int(input("Enter the infection rate: "))
rate_of_recovery = int(input("Enter the rate of recovery of the disease: "))
rate_of_lethality = int(input("Enter the rate of lethality of the disease: "))
target_duration = int(input("How many days do you wand to run the simulation: "))
disease = Disease(disease_name, rate_of_infection, rate_of_recovery, rate_of_lethality)

CONTACT_NUMBER = 10
# Keep track of how many days it's been
day_count = 0
# population list
population = []
R0 = 0

def assign_population():
    for i in range(immune_count):
        population.append(1)
    for x in range(infected_count):
        population.append(2)
    for y in range(susceptible_count):
        population.append(3)


assign_population()
# print(population)

file = open("population.csv", 'w')
file.writelines("Total Population, Susceptible, Infected, Immune, Dead" + '\n')
file.close()
# You won't need to change this function, it will display a visual summary of each population


def draw_status():
    clear()
    set_font_size(24)
    draw_text("Total population is: " + str(immune_count + infected_count + susceptible_count), 10, 30)

    draw_text("Simulation has been running for " + str(day_count) + " days", 10, 75)

    # Figure out how large we should make each population
    susceptible_width = (susceptible_count / original_population_size) * WINDOW_WIDTH
    infected_width = (infected_count / original_population_size) * WINDOW_WIDTH
    immune_width = (immune_count / original_population_size) * WINDOW_WIDTH
    dead_width = (deceased_count / original_population_size) * WINDOW_WIDTH

    # Start with susceptible
    set_fill_color(0, 1, 0)
    # Draw the bar
    if susceptible_count != 0:
        draw_rectangle(0, BAR_Y_COORD, susceptible_width, BAR_HEIGHT)
    # Draw the legend:
    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 30, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Susceptible', WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 60)

    # Draw infected
    set_fill_color(1, 0, 0)
    if infected_count != 0:
        draw_rectangle(susceptible_width, BAR_Y_COORD, infected_width, BAR_HEIGHT)

    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 75, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Infected', WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 105)

    # Draw immune
    set_fill_color(0, 0, 1)
    if immune_count != 0:
        draw_rectangle(susceptible_width + infected_width, BAR_Y_COORD, immune_width, BAR_HEIGHT)

    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 120, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Immune', WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 150)

    # Draw diseased
    set_fill_color(0.2, 0.7, 0.7)
    if deceased_count != 0:
        draw_rectangle(susceptible_width + infected_width + immune_width, BAR_Y_COORD, dead_width, BAR_HEIGHT)

    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 165, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Dead', WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 195)


def check_the_infected():
    global immune_count
    global infected_count
    global deceased_count, susceptible_count
    # checking if infected recovered
    for x in range(len(population)):
        person = Person(population[x], disease)
        if population[x] == 2:
            if person.has_recovered():
                population[x] = 1
                infected_count -= 1
                immune_count += 1
                susceptible_count = original_population_size - immune_count - infected_count - deceased_count
            # checking if infected person died.
            elif person.has_died():
                population[x] = 0
                infected_count -= 1
                deceased_count += 1
                susceptible_count = original_population_size - immune_count - infected_count - deceased_count


def check_the_susceptible():
    global infected_count
    global susceptible_count
    # checking if susceptile got infected after meeting an infected person
    for x in range(len(population)):
        person = Person(population[x], disease)
        if person.is_susceptible():
            person_to_meet = Person(population[randint(0, len(population) - 1)], disease)
            if person.is_infected(person_to_meet):
                population[x] = 2

                infected_count += 1
                susceptible_count = original_population_size - immune_count - infected_count - deceased_count


def write_csv():
    # writing down the values of each population into a csv file.
    file = open("population.csv", 'a')
    results = str(original_population_size) + ',' + str(susceptible_count) + ',' + str(infected_count) + ',' + str(immune_count) + ',' + str(deceased_count) + '\n'
    file.writelines(results)
    file.close()


def generate_final_report():
    global R0
    simulating = False
    if day_count == target_duration:
        simulating = True
        percentage_survived = (susceptible_count + immune_count + infected_count) / original_population_size
        print("The percentage of people that survived is " + str(percentage_survived * 100))

    if day_count == 20:
        difference = original_infected - (infected_count + deceased_count)
        R0 = difference / original_infected

    if simulating:
        print("The R0 value is " + str(R0))
        if R0 >= 1:
            print("The disease is an Epidermic")
        else:
            print("The disease is not an Epidermic")


def main():
    global day_count
    # Draws the visual representation
    draw_status()

    # Loop over the infected population to determine if they could recover or pass away
    check_the_infected()

    # Loop over the healthy population to determine if they can catch the disease
    check_the_susceptible()

    # Update our output CSV
    write_csv()

    day_count += 1
    print(original_population_size,susceptible_count, immune_count, infected_count, deceased_count)

    # End the simulation once we reach the set target.
    generate_final_report()
    if day_count == target_duration:
        cs1_quit()


start_graphics(main, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, framerate=1)
