from src.human import Human
from src.environment import Environment
from src.plots import plot_temperatures, plot_equilibrium_curve
from src.simulation import run_simulation, find_equilibrium_distance

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

def get_rotation_input():
    while True:
        rotation_choice = input("Soll Rotation aktivierte werden? Geben Sie 0 zum deaktivieren und 1 zum aktivierender Rotation ein!\nAuswahl: ")

        if rotation_choice == "0":
            print("Rotation deaktiviert!")
            return None #nur zur übersicht, nicht notwendig

        elif rotation_choice == "1":
            print("Rotation aktiviert!")
            period_time = get_float_input("Geben Sie die Zeit pro Umdrehung in Sekunden an! ", 0)
            return period_time

        else:
            print("Geben Sie 0 der 1 ein!")





# Es müssen immer beide Werte übergeben werden, auch wenn sie nicht gebraucht werden.
sun_distance = None
earth_distance = None
# muss auch für den Interstellarfall inistalisiert sein
period_time = None

while True:
    choice = input("wählen Sie das Scenario:\n1:Interstellarer Raum\n2:Interplanetarer Raum\n3:Erdorbit\n4:Erdorbit mit Sonneneinfluss\nAuswahl:")

    if choice == "1":
        scenario_choice = "interstellar"
        break

    elif choice == "2":
        scenario_choice = "sun"
        sun_distance = get_float_input("Geben Sie den Abstand zur Sonne in AE ein! ", 0)
        period_time = get_rotation_input()
        break

    elif choice == "3":
        scenario_choice = "earth"
        earth_distance = get_float_input("Geben Sie den Abstand zum Erdmittelpunkt in km ein! ", 6471)
        period_time = get_rotation_input()
        break

    elif choice == "4":
        scenario_choice = "sun_earth"
        sun_distance = get_float_input("Geben Sie den Abstand zur Sonne in AE ein! ", 0)
        earth_distance = get_float_input("Geben Sie den Abstand zum Erdmittelpunkt in km ein! ", 6471)
        period_time = get_rotation_input()
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
    rotation_period = period_time, # in Sekunden für eine volle Umdrehung
)

if scenario_choice == "interstellar":
    print("Interstellarer Raum: Kein Gleichgewichtsabstand zu berechnen.")

elif scenario_choice == "sun_earth":
    equilibrium_distance = find_equilibrium_distance(astronaut, environment, scenario_choice)
    plot_equilibrium_curve(equilibrium_distance)
    print('Die Gleichgewichtskurve ist ohne Rotation!')

else:
    equilibrium_distance = find_equilibrium_distance(astronaut, environment, scenario_choice)
    print(f"Der Gleichgewichtsabstand beträgt: {equilibrium_distance}\nDer Gleichgewichtsabstand ist ohne Rotation")

times, temperatures = run_simulation(astronaut, environment, 1, 21600, scenario_choice)

plot_temperatures(times, temperatures)

print(f"Endtemperatur: {temperatures[-1]:.5f} K")


