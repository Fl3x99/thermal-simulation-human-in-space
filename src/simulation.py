from src.radiation import calculate_IR_emitted_power,calculate_cmb_absorbed_power, calculate_abs_sun_power, calculate_abs_IR_earth_power, calculate_abs_albedo_power



def calculate_net_power(human, environment, scenario_choice):
    #wird bei allen Leistungsgleichungen gebraucht
    P_metabolic_power = human.metabolic_power
    P_cmb = calculate_cmb_absorbed_power(human, environment)
    P_IR = calculate_IR_emitted_power(human)
    #Aufteilung der 4 Fälle

    if scenario_choice == "interstellar":
        # Leistungsgleichung
        P_net = P_metabolic_power+ P_cmb - P_IR
        return P_net

    elif scenario_choice == "sun":
        P_sun = calculate_abs_sun_power(environment, human)

        P_net = P_metabolic_power+ P_cmb - P_IR+ P_sun
        return P_net

    elif scenario_choice == "earth":
        P_earth = calculate_abs_IR_earth_power(environment, human)

        P_net = P_metabolic_power + P_cmb - P_IR + P_earth
        return P_net

    elif scenario_choice == "sun_earth": #sun+earth
        P_sun = calculate_abs_sun_power(environment, human)
        P_earth = calculate_abs_IR_earth_power(environment, human)
        P_albedo = calculate_abs_albedo_power(environment, human)

        P_net = P_metabolic_power + P_cmb - P_IR + P_earth +P_sun + P_albedo
        return P_net


def calculate_temperature_change(human, environment, scenario_choice):

    # Temperaturänderung bestimmen
    spec_heat_capacity = human.specific_heat_capacity
    mass = human.mass
    P_net = calculate_net_power(human, environment, scenario_choice)

    dT_dt = P_net / (spec_heat_capacity* mass)
    return dT_dt

def euler_step(human, environment, time_step, scenario_choice):

    # neue Temperatur numerisch bestimmen (1 Schritt)
    dT_dt = calculate_temperature_change(human, environment, scenario_choice)
    T_old = human.temperature
    T_new = T_old + dT_dt * time_step
    return T_new

def run_simulation(human, environment, time_step, duration, scenario_choice):

    # Schleife für die gewünschte Anzahl an durchläufen
    number_of_steps = int(duration / time_step)
    times = [0]
    temperatures = [human.temperature]

    for i in range(number_of_steps):
        T_new = euler_step(human, environment, time_step, scenario_choice)
        human.temperature = T_new

        current_time = (i + 1) * time_step
        times.append(current_time)
        temperatures.append(human.temperature)

    return times, temperatures