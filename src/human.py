from math import pi


class Human:
    def __init__(self, mass, temperature, specific_heat_capacity, metabolic_power, emissivity_ir, absorptivity_sun ,
                 absorptivity_ir, head_radius, torso_height, torso_width, torso_depth, arm_length, arm_radius,
                 leg_length, leg_radius):
        # Parameter übergeben
        self.mass = mass
        self.temperature = temperature
        self.specific_heat_capacity = specific_heat_capacity
        self.metabolic_power = metabolic_power
        self.emissivity_ir = emissivity_ir
        self.absorptivity_sun = absorptivity_sun
        self.absorptivity_ir = absorptivity_ir
        self.head_radius = head_radius
        self.torso_height = torso_height
        self.torso_width = torso_width
        self.torso_depth = torso_depth
        self.arm_length = arm_length
        self.arm_radius = arm_radius
        self.leg_length = leg_length
        self.leg_radius = leg_radius
        # Oberfläche berechnen
        self.calculate_total_surface_area()
        # projizierte Frontaloberfläche berechnen
        self.calculate_projizierte_surface_area()

    def calculate_total_surface_area(self):
        head_surface = 4*pi*self.head_radius**2
        torso_surface = 2*(self.torso_height*self.torso_width+self.torso_height*self.torso_depth+self.torso_width*self.torso_depth)
        arm_surface = pi*self.arm_radius**2+2*pi*self.arm_radius*self.arm_length
        leg_surface = pi*self.leg_radius**2+2*pi*self.leg_radius*self.leg_length

        self.total_surface_area = head_surface+torso_surface+2*arm_surface+2*leg_surface


    def calculate_projizierte_surface_area(self): # Frontal
        pro_head_surface = pi*self.head_radius**2 #pi*r^2
        pro_torso_surface = self.torso_height*self.torso_width # Höhe*Breite
        pro_arm_surface = self.arm_length*2*self.arm_radius #l*2*r
        pro_leg_surface = self.leg_length*2*self.leg_radius # l*2*r

        self.front_projizierte_surface_area = pro_head_surface+pro_torso_surface+2*pro_arm_surface+2*pro_leg_surface
