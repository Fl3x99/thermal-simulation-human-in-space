from src.human import Human
from src.environment import Environment
from src.simulation import run_simulation
from scipy.integrate import solve_ivp
from src.simulation import calculate_temperature_change

#Mensch erstellen
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

#Umgebung erstellen
environment = Environment(
    sun_distance = 1, #in AE
    earth_distance = None, # in km
    cmb_temperature = 2.7, # in K
    rotation_period = None, # in Sekunden für eine volle Umdrehung
    )
#Testbedingungen
scenario_choice = "sun"
duration = 21600  # 6 Stunden in Sekunden

#Hilfsfunktion, solveip übergibt aktuelle Zeit und Temperatur und brauch Änderungsrate dT_dt
def differential_equation(t, T):
    astronaut.temperature = T[0]

    dT_dt = calculate_temperature_change(
        astronaut, environment, scenario_choice, t
    )

    return [dT_dt]

time_steps = [60, 30, 10, 5, 1, 0.5]
#Schleife für die verschiednen Zeitschritte
for time_step in time_steps:
    astronaut.temperature = 310.15 #zurücksetzen wegen der mehreren Schleifen
    times, temperatures = run_simulation(
        astronaut, environment, time_step, duration, scenario_choice
    )
    print(f"Schrittweite: {time_step} s | Endtemperatur: {temperatures[-1]:.8f} K")

# Vergleichsrechnung mit SciPy (RK45)
astronaut.temperature = 310.15

solution = solve_ivp(
    differential_equation, #Hilfsfunktion
    (0, duration),
    [310.15], #starttemperatur
    method="RK45", #Methode Runge-Kutta-Verfahren
    rtol=1e-10, #relative Tolerant
    atol=1e-12 #absolute Toleranz
)
print(f"RK45-Endtemperatur: {solution.y[0, -1]:.8f} K")
# Ergebnis: Euler konvergiert gegen RK45.
# Bei Halbierung der Schrittweite halbiert sich ungefähr der Fehler.
# Abweichung bei dt = 1 s: ca. 0.000309 K.