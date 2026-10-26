from src.human import Human
from src.environment import Environment
from src.simulation import bisection_step, Bisektionsverfahren,itteration_newton, calculate_net_power_at_r

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
    earth_distance =  42164, # in km
    cmb_temperature = 2.7, # in K
    rotation_period = 60, # in Sekunden für eine volle Umdrehung
)

result = Bisektionsverfahren(astronaut, environment, "sun")
print(f"Das Ergebnis bei Startwert: {environment.sun_distance:.2f} AE ist {result:.5f} AE")

environment.sun_distance = 1.5
result = Bisektionsverfahren(astronaut, environment, "sun")
print(f"Das Ergebnis bei Startwert: {environment.sun_distance:.2f} AE ist {result:.5f} AE")

environment.sun_distance = 2
result = Bisektionsverfahren(astronaut, environment, "sun")
print(f"Das Ergebnis bei Startwert: {environment.sun_distance:.2f} AE ist {result:.5f} AE")

environment.sun_distance = 5
result = Bisektionsverfahren(astronaut, environment, "sun")
print(f"Das Ergebnis bei Startwert: {environment.sun_distance:.2f} AE ist {result:.5f} AE")

environment.sun_distance = 0.3
result = Bisektionsverfahren(astronaut, environment, "sun")
print(f"Das Ergebnis bei Startwert: {environment.sun_distance:.2f} AE ist {result:.5f} AE")

# Newton-Verfahren auf verbleibende Nettoleistung prüfen
r_newton = itteration_newton(astronaut, environment, "sun")

print("\nNewton-Test:")
print("Berechneter Abstand:", r_newton, "AU")

if r_newton is not None:
    original_distance = environment.sun_distance

    P_rest = calculate_net_power_at_r(
        astronaut, environment, r_newton, "sun"
    )

    environment.sun_distance = original_distance

    print("Verbleibende Nettoleistung:", P_rest, "W")
else:
    print("Newton-Verfahren nicht konvergiert")