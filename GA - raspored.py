from random import shuffle, randint

courses = ["Math", "Science", "English", "History", "Art", "Informatics", "Economy", "Data mining"]
teachers = {"Math": ["Mr. Green", "Ms. Brown"],
            "Science": ["Ms. Lee", "Mr. Chen"],
            "English": ["Ms. Johnson", "Mr. Garcia"],
            "History": ["Mr. Wilson", "Ms. Davis"],
            "Art": ["Ms. Jackson", "Mr. Williams"],
            "Informatics": ["Ms. Lee", "Mr. Chen"],
            "Economy": ["Ms. Johnson", "Mr. Garcia"],
            "Data mining": ["Mr. Wilson", "Ms. Davis"]}

teacher_preferences = {"Mr. Green": [1], 
                       "Ms. Brown": [3], 
                       "Ms. Lee": [],
                       "Mr. Chen": [2, 4],
                       "Ms. Johnson": [],
                       "Mr. Garcia": [0],
                       "Mr. Wilson": [],
                       "Ms. Davis": [1, 4], 
                       "Ms. Jackson": [],
                       "Mr. Williams": []}

course_occurrences = {"Math": 4, "Science": 3, "English": 3, "History": 2, "Art": 2, "Informatics": 5, "Economy": 3, "Data mining": 3}

timeslots_per_day = 5
num_days = 5
population_size = 10

def has_conflict(timetable):
    for day in range(num_days):
        for slot in range(timeslots_per_day):
            course = timetable[day][slot]
            for teacher in teachers[course]:
                if day in teacher_preferences[teacher]:
                    return True
    return False

def evaluate_fitness(timetable):
    if has_conflict(timetable):
        return 0
    fitness = timeslots_per_day * num_days
    course_counts = {course: 0 for course in courses}
    daily_occurrences = {course: [0] * num_days for course in courses}
    
    for day in range(num_days):
        for slot in range(timeslots_per_day):
            course = timetable[day][slot]
            if course_counts[course] >= course_occurrences[course]:
                fitness -= 1  
            else:
                course_counts[course] += 1
            daily_occurrences[course][day] += 1
            for teacher in teachers[course]:
                if day in teacher_preferences[teacher]:
                    fitness -= 1  

    for course, counts in daily_occurrences.items():
        for count in counts:
            if count > 2:
                fitness -= 1  
    
    return fitness

def create_timetable():
    timetable = [[None] * timeslots_per_day for _ in range(num_days)]
    course_counts = {course: 0 for course in courses}
    daily_occurrences = {course: [0] * num_days for course in courses}
    
    for course, max_occurrences in course_occurrences.items():
        available_slots = [(day, slot) for day in range(num_days) for slot in range(timeslots_per_day)]
        shuffle(available_slots)
        
        for _ in range(max_occurrences):
            for day, slot in available_slots:
                if daily_occurrences[course][day] < 2 and timetable[day][slot] is None:
                    timetable[day][slot] = course
                    daily_occurrences[course][day] += 1
                    course_counts[course] += 1
                    break

    remaining_courses = [course for course in courses for _ in range(course_occurrences[course] - course_counts[course])]
    shuffle(remaining_courses)
    for day in range(num_days):
        for slot in range(timeslots_per_day):
            if timetable[day][slot] is None:
                timetable[day][slot] = remaining_courses.pop()
    
    return timetable

population = [create_timetable() for _ in range(population_size)]

for generation in range(100):
    new_population = []
    fitness_values = [evaluate_fitness(individual) for individual in population]

    for _ in range(population_size):
        parent1 = population[randint(0, population_size - 1)]
        parent2 = population[randint(0, population_size - 1)]
        parent1_fitness = evaluate_fitness(parent1)
        parent2_fitness = evaluate_fitness(parent2)
        if parent1_fitness > parent2_fitness:
            new_population.append(parent1)
        else:
            new_population.append(parent2)

    for i in range(0, population_size, 2):
        if i + 1 < population_size:
            parent1 = new_population[i]
            parent2 = new_population[i + 1]
            crossover_point = randint(1, timeslots_per_day - 1)
            for day in range(num_days):
                new_population[i][day][crossover_point:], new_population[i + 1][day][crossover_point:] = \
                    new_population[i + 1][day][crossover_point:], new_population[i][day][crossover_point:]

    for i in range(population_size):
        for day in range(num_days):
            if randint(0, 100) < 5:
                index1, index2 = randint(0, timeslots_per_day - 1), randint(0, timeslots_per_day - 1)
                new_population[i][day][index1], new_population[i][day][index2] = \
                    new_population[i][day][index2], new_population[i][day][index1]

    population = new_population

best_timetable = max(population, key=evaluate_fitness)

print("Best Timetable:")
for day in range(num_days):
    print(f"Day {day + 1}:")
    for slot in range(timeslots_per_day):
        course = best_timetable[day][slot]
        print(f"\tSlot {slot + 1}: {course} ({teachers[course][0]})")
