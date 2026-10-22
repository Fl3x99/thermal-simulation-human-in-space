from math import pi

from src.human import Human


astronaut = Human(
    mass=90,
    temperature=310.15,
    specific_heat_capacity=3500,
    metabolic_power=100,
    emissivity_ir=0.98,
    absorptivity_sun=0.7,
    absorptivity_ir=0.98,
    head_radius=0.12,
    torso_height=0.65,
    torso_width=0.42,
    torso_depth=0.24,
    arm_length=0.63,
    arm_radius=0.05,
    leg_length=0.93,
    leg_radius=0.075,
)

head_volume = (4 / 3) * pi * astronaut.head_radius**3

torso_volume = (
    astronaut.torso_height
    * astronaut.torso_width
    * astronaut.torso_depth
)

arm_volume = pi * astronaut.arm_radius**2 * astronaut.arm_length
leg_volume = pi * astronaut.leg_radius**2 * astronaut.leg_length

total_volume = (
    head_volume
    + torso_volume
    + 2 * arm_volume
    + 2 * leg_volume
)

density = astronaut.mass / total_volume

print(f"Gesamtoberfläche: {astronaut.total_surface_area:.3f} m²")
print(f"Gesamtvolumen: {total_volume:.3f} m³")
print(f"Mittlere Dichte: {density:.1f} kg/m³")
#Öberfläche größer als eines Menschen-Quader als Torso keine gute Annahme Zylinder echt besser
#Volumen zu groß
#Dichte zu gering