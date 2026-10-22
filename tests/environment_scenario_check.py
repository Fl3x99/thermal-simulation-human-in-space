from src.human import Human
from src.environment import Environment
from src.simulation import run_simulation, decide_projizierte_surface_area
from src.plots import plot_temperatures

from src.radiation import calculate_I_sun_distance, calculate_abs_sun_power
from src.simulation import calculate_net_power

sun_distance = 1       # AE
earth_distance = None  # Keine Erde
scenario_choice = "sun"

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
    rotation_period = None, # in Sekunden für eine volle Umdrehung
)

I_r = calculate_I_sun_distance(environment)
print(f"Sonnenintensität: {I_r:.5f} W/m^2 bei einem Abstand von {environment.sun_distance:.1f} AE")
A_pro = decide_projizierte_surface_area(astronaut, environment, 0)
P_sun = calculate_abs_sun_power(environment, astronaut, A_pro)
print(f"Sonnenleistung ist: {P_sun:.5f} W")
P_net = calculate_net_power(astronaut, environment, scenario_choice, 0)
print(f"Die Gesamtenergiebilanz ist: {P_net:.5f} W")

times, temperatures = run_simulation(astronaut, environment, 60, 21600, scenario_choice)

plot_temperatures(times, temperatures)

I_r = calculate_I_sun_distance(environment)
print(f"Sonnenintensität: {I_r:.5f} W/m^2 bei einem Abstand von {environment.sun_distance:.1f} AE")
A_pro = decide_projizierte_surface_area(astronaut, environment, 0)
P_sun = calculate_abs_sun_power(environment, astronaut, A_pro)
print(f"Sonnenleistung ist: {P_sun:.5f} W")
P_net = calculate_net_power(astronaut, environment, scenario_choice, 0)
print(f"Die Gesamtenergiebilanz ist: {P_net:.5f} W")