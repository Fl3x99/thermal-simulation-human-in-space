from src.radiation import calculate_IR_emitted_power,calculate_cmb_absorbed_power


def calculate_net_power(human, environment):

    #Leistungsgleichung
    P_metabolic_power = human.metabolic_power
    P_cmb = calculate_cmb_absorbed_power(human, environment)
    P_IR = calculate_IR_emitted_power(human)

    P_net = P_metabolic_power+ P_cmb - P_IR
    return P_net


def calculate_temperature_change(human, environment):

    # Temperaturänderung bestimmen
    spec_heat_capacity = human.specific_heat_capacity
    mass = human.mass
    P_net = calculate_net_power(human, environment)

    dT_dt = P_net / (spec_heat_capacity* mass)
    return dT_dt

def euler_step(human, environment, time_step):

    # neue Temperatur numerisch bestimmen (1 Schritt)
    dT_dt = calculate_temperature_change(human, environment)
    T_old = human.temperature
    T_new = T_old + dT_dt * time_step
    return T_new

def run_simulation(human, environment, time_step, duration):

    # Schleife für die gewünschte Anzahl an durchläufen
    number_of_steps = int(duration / time_step)
    times = [0]
    temperatures = [human.temperature]

    for i in range(number_of_steps):
        T_new = euler_step(human, environment, time_step)
        human.temperature = T_new

        current_time = (i + 1) * time_step
        times.append(current_time)
        temperatures.append(human.temperature)

    return times, temperatures