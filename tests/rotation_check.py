from src.human import Human
from src.environment import Environment
from src.simulation import calculate_rotated_projizierte_surface_area
import numpy as np

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
    sun_distance = 1, #in AE
    earth_distance = 42164, # in km
    cmb_temperature = 2.7, # in K
    rotation_period = 60, # in Sekunden für eine volle Umdrehung
)

print(f"Frontfläche: {astronaut.front_projizierte_surface_area:.5f} m²")
print(f"Seitenfläche: {astronaut.side_projizierte_surface_area:.5f} m²")

test_times = np.arange(0, 61)

for time in test_times:
    A_pro = calculate_rotated_projizierte_surface_area(
        astronaut,
        environment,
        time
    )

    print(f"Zeit: {time:5.1f} s | projizierte Fläche: {A_pro:.5f} m²")