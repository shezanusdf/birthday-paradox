import random, datetime

def get_birthdays(number_of_birthdays) :
    '''Returns a list of random birthday date objects.'''
    birthdays = []
    for i in range(number_of_birthdays) :
        # The year is unimportant for simulation.
        #  As long as all birthdays are in the same year.
        start_of_year = datetime.date(2001,1,1)
        
        # Get a random day in the year.
        random_number_of_days = datetime.timedelta(random.randint(0, 364))
        birthday = start_of_year + random_number_of_days
        birthdays.append(birthday)
    return birthdays

def get_match(birthdays) :
    ''' Returns the dateobj of the bday appearing more than 
    once in the birthday list'''
    if len(birthdays) == len(set(birthdays)) :
        return None # All birthdays are unique, so return None.
    
    # Compare each birthday to every other birthday
    for a, birthdayA in enumerate(birthdays) :
        for b, birthdayB in enumerate(birthdays[a+1:]) :
            if birthdayA == birthdayB :
                return birthdayA # Returns the matching bday
                
#Intro
print('''The Birthday Paradox shows that in a group of N people, the odds
      that two of them have matching birthdays is tremendously high.
      This program does a monte carlo simulation (i.e repeated random 
      siimulations) to explore this concept.''')

# Months
MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

while True :
    print('How many birthdays shall i generate? (max : 100)')
    response = input('> ')
    if response.isdecimal() and (0 < int(response) <= 100):
        numBDays = int(response)
        break # User entered a valid numnber

# Generate and display the bdays
print('here are', numBDays, 'birthdays : ')
birthdays = get_birthdays(numBDays)
for i, birthday in enumerate(birthdays):
    if i != 0 :
        # Displays comma for each bday after the first bday
        print(', ', end='')
    month_name = MONTHS[birthday.month - 1]
    dateText = f"{month_name} {birthday.day}"  
    print(dateText, end = '')

# Determines if two bdays match
match = get_match(birthdays)

# Display the results:
print('In this simulation, ', end='')
if match != None :
    month_name = MONTHS[match.month - 1]
    dateText = f"{month_name} {dateText}"
    print('multiple people have a birthday on', dateText)
else:
    print('There are no matching birthdays')

# Run 100k sims:
print('Generating', numBDays, 'random birthdays 100,000 times..')
input("Press Enter to begin...")

print("Let\'s run another 100,000 simulations.")
simMatch = 0 # How many bdays had matching bdays
for i in range(100_000):
    #Reports on progress every 10,000 sims.
    if i % 10_000 == 0:
        print(i, 'simulations run...')
    birthdays = get_birthdays(numBDays)
    if get_match(birthdays) != None:
        simMatch += 1
        
print("100,000 simulations run.")

# Display simulation results
probability = round(simMatch / 100_000 * 100, 2)
print('out of 100,000 simulations of', numBDays, 'people, there was a')
print('matching bday in that group', simMatch, 'times. This means')
print('that', numBDays, 'people have a', probability, '%','chance of')
print('having a matching birthday in their group.')
print("That's probably more than you would think!")