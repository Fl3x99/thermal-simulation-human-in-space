from src.human import Human
from src.environment import Environment
from src.simulation import run_simulation, calculate_net_power
from src.plots import plot_temperatures

def get_float_input(prompt, min_value):
    while True:
        try:
            value = float(input(prompt))
            if value > min_value:
                return value
            else:
                print(f"Der Abstand muss größer als: {min_value:.0f}  sein")

        except ValueError:
            print("Geben Sie eine Zahl")


# Es müssen immer beide Werte übergeben werden, auch wenn sie nicht gebraucht werden.
sun_distance = None
earth_distance = None

while True:
    choice = input("wählen Sie das Scenario:\n1:Interstellarer Raum\n2:Interplanetarer Raum\n3:Erdorbit\n4:Erdorbit mit Sonneneinfluss\nAuswahl:")

    if choice == "1":
        scenario_choice = "interstellar"
        break

    elif choice == "2":
        scenario_choice = "sun"
        sun_distance = get_float_input("Geben Sie den Abstand zur Sonne in AE ein! ", 0)
        break

    elif choice == "3":
        scenario_choice = "earth"
        earth_distance = get_float_input("Geben Sie den Abstand zum Erdmittelpunkt in km ein! ", 6471)
        break

    elif choice == "4":
        scenario_choice = "sun_earth"
        sun_distance = get_float_input("Geben Sie den Abstand zur Sonne in AE ein! ", 0)
        earth_distance = get_float_input("Geben Sie den Abstand zum Erdmittelpunkt in km ein! ", 6471)
        break

    else:
        print("Geben Sie eine Zahl zwischen 1 und 4 ein! ")


astronaut = Human(
    mass = 90,
    temperature = 310.15,
    specific_heat_capacity = 3500,
    metabolic_power = 100,
    emissivity_ir = 0.98,
    absorptivity_sun = 0.7,
    absorptivity_ir = 0.98,
    head_radius = 0.12,
    torso_height = 0.65,
    torso_width = 0.42,
    torso_depth = 0.24,
    arm_length = 0.63,
    arm_radius = 0.05,
    leg_length = 0.93,
    leg_radius = 0.075,
    )

environment = Environment(
    sun_distance = sun_distance, #in AE
    earth_distance = earth_distance, # in km
    cmb_temperature = 2.7, # in K
    rotation_period = 60, # in Sekunden für eine volle Umdrehung
)

P_net_start = calculate_net_power(astronaut, environment, scenario_choice)
print(f"Nettoleistung am Anfang: {P_net_start:.2f} W")

times, temperatures = run_simulation(astronaut, environment, 60, 21600, scenario_choice)

plot_temperatures(times, temperatures)


