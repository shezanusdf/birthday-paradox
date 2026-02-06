import random
import datetime
import streamlit as st


def get_birthdays(number_of_birthdays):
    birthdays = []
    for i in range(number_of_birthdays):
        start_of_year = datetime.date(2001, 1, 1)

        random_number_of_days = datetime.timedelta(random.randint(0, 364))
        birthday = start_of_year + random_number_of_days
        birthdays.append(birthday)

    return birthdays


def get_match(birthdays):
    if len(birthdays) == len(set(birthdays)):
        return None

    for a, birthdayA in enumerate(birthdays):
        for birthdayB in birthdays[a + 1:]:
            if birthdayA == birthdayB:
                return birthdayA

    return None


MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')


st.title("Birthday Paradox Simulator")


st.write('''The Birthday Paradox shows that in a group of N people, the odds
that two of them have matching birthdays is tremendously high.
This program does a monte carlo simulation (i.e repeated random 
simulations) to explore this concept.''')


# ---- SESSION STATE INITIALIZATION ----
if "generated" not in st.session_state:
    st.session_state.generated = False

if "sim_started" not in st.session_state:
    st.session_state.sim_started = False

if "birthdays" not in st.session_state:
    st.session_state.birthdays = []


# ---- USER INPUT ----
numBDays = st.number_input(
    "How many birthdays shall I generate? (max : 100)",
    min_value=1,
    max_value=100,
    value=23
)


# ---- GENERATE BIRTHDAYS ----
if st.button("Generate Birthdays"):

    st.session_state.birthdays = get_birthdays(numBDays)
    st.session_state.generated = True
    st.session_state.sim_started = False


# ---- DISPLAY GENERATED BIRTHDAYS ----
if st.session_state.generated:

    st.write(f"Here are {numBDays} birthdays:")

    birthday_output = []
    for birthday in st.session_state.birthdays:
        month_name = MONTHS[birthday.month - 1]
        dateText = f"{month_name} {birthday.day}"
        birthday_output.append(dateText)

    st.write(", ".join(birthday_output))


    # CHECK FOR MATCH
    match = get_match(st.session_state.birthdays)

    if match is not None:
        month_name = MONTHS[match.month - 1]
        dateText = f"{month_name} {match.day}"
        st.write(f"In this simulation, multiple people have a birthday on {dateText}")
    else:
        st.write("In this simulation, there are no matching birthdays")


    st.write(f"Generating {numBDays} random birthdays 100,000 times...")
    st.write("Press button below to begin...")


    # ---- START SIMULATION BUTTON ----
    if st.button("Begin 100,000 Simulations"):
        st.session_state.sim_started = True


# ---- RUN SIMULATION ----
if st.session_state.sim_started:

    st.write("Let's run another 100,000 simulations.")

    simMatch = 0

    progress_text = st.empty()
    progress_bar = st.progress(0)

    for i in range(100_000):

        birthdays = get_birthdays(numBDays)

        if get_match(birthdays) is not None:
            simMatch += 1

        if i % 10_000 == 0 and i != 0:
            progress_text.write(f"{i} simulations run...")
            progress_bar.progress(i / 100_000)

    progress_bar.progress(1.0)

    st.write("100,000 simulations run.")

    probability = round(simMatch / 100_000 * 100, 2)

    st.write(f"Out of 100,000 simulations of {numBDays} people, there was a")
    st.write(f"matching bday in that group {simMatch} times. This means")
    st.write(f"that {numBDays} people have a {probability}% chance of")
    st.write("having a matching birthday in their group.")
    st.write("That's probably more than you would think!")
