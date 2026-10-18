from fontTools.diff.color import red_start

from src.radiation import calculate_IR_emitted_power,calculate_cmb_absorbed_power, calculate_abs_sun_power, calculate_abs_IR_earth_power, calculate_abs_albedo_power
from math import pi, sin, cos


def calculate_net_power(human, environment, scenario_choice, current_time):
    #wird bei allen Leistungsgleichungen gebraucht
    P_metabolic_power = human.metabolic_power
    P_cmb = calculate_cmb_absorbed_power(human, environment)
    P_IR = calculate_IR_emitted_power(human)
    #Berechnung A_pro hier um ein Circular import zu vermeiden
    A_pro = decide_projizierte_surface_area(human, environment, current_time)
    #Aufteilung der 4 Fälle

    if scenario_choice == "interstellar":
        # Leistungsgleichung
        P_net = P_metabolic_power+ P_cmb - P_IR
        return P_net

    elif scenario_choice == "sun":
        P_sun = calculate_abs_sun_power(environment, human, A_pro)

        P_net = P_metabolic_power+ P_cmb - P_IR+ P_sun
        return P_net

    elif scenario_choice == "earth":
        P_earth = calculate_abs_IR_earth_power(environment, human, A_pro)

        P_net = P_metabolic_power + P_cmb - P_IR + P_earth
        return P_net

    elif scenario_choice == "sun_earth": #sun+earth
        P_sun = calculate_abs_sun_power(environment, human, A_pro)
        P_earth = calculate_abs_IR_earth_power(environment, human, A_pro)
        P_albedo = calculate_abs_albedo_power(environment, human, A_pro)

        P_net = P_metabolic_power + P_cmb - P_IR + P_earth +P_sun + P_albedo
        return P_net


def calculate_temperature_change(human, environment, scenario_choice, current_time):

    # Temperaturänderung bestimmen
    spec_heat_capacity = human.specific_heat_capacity
    mass = human.mass
    P_net = calculate_net_power(human, environment, scenario_choice, current_time)

    dT_dt = P_net / (spec_heat_capacity* mass)
    return dT_dt

def euler_step(human, environment, time_step, scenario_choice, current_time):

    # neue Temperatur numerisch bestimmen (1 Schritt)
    dT_dt = calculate_temperature_change(human, environment, scenario_choice, current_time)
    T_old = human.temperature
    T_new = T_old + dT_dt * time_step
    return T_new

def run_simulation(human, environment, time_step, duration, scenario_choice):

    # Schleife für die gewünschte Anzahl an durchläufen
    number_of_steps = int(duration / time_step)
    times = [0]
    temperatures = [human.temperature]

    for i in range(number_of_steps):

        current_time = i * time_step

        T_new = euler_step(human, environment, time_step, scenario_choice, current_time)
        human.temperature = T_new

        new_time = (i + 1) * time_step
        times.append(new_time)
        temperatures.append(human.temperature)

    return times, temperatures

def calculate_rotated_projizierte_surface_area(human, environment, time):

    A_pro_front = human.front_projizierte_surface_area
    A_pro_side = human.side_projizierte_surface_area
    rotation_period = environment.rotation_period
    sim_time = time
    #Rotationswinkel berechnen
    rot_angle= 2 * pi * sim_time / rotation_period
    #Zeitabhängig Projizierte Fläche
    A_pro_t = A_pro_front * abs(cos(rot_angle)) + A_pro_side * abs(sin(rot_angle))
    return A_pro_t

def decide_projizierte_surface_area(human, environment, current_time):

    if environment.rotation_period is None:
        A_pro = human.front_projizierte_surface_area

    elif environment.rotation_period > 0:
        A_pro = calculate_rotated_projizierte_surface_area(human, environment, current_time)

    else:
        raise ValueError("Die Zahl muss größer 0 sein!")

    return A_pro


def calculate_net_power_at_r(human, environment, distance, scenario_choice):

    if scenario_choice == "sun":
        environment.sun_distance = distance

    elif scenario_choice == "earth":
        environment.earth_distance = distance


    P_net = calculate_net_power(
        human,
        environment,
        scenario_choice,
        current_time=0
        )

    return P_net

def find_ableitung_von_Pr(human, environment, current_distance, scenario_choice):

    h=0.001 # AE zu groß führt zu ungenauem Ergebnis, zu klein zu Rundungsfehlern
    r = current_distance
    P_r_plus_h = calculate_net_power_at_r(human, environment, r+h, scenario_choice)
    P_r_minus_h = calculate_net_power_at_r(human, environment, r-h, scenario_choice)
    dP_dr = (P_r_plus_h-P_r_minus_h)/(2*h)

    return dP_dr

def newton_step(human, environment, current_distance, scenario_choice):

    P_0 = calculate_net_power_at_r(human, environment , current_distance, scenario_choice)
    P_1 = find_ableitung_von_Pr(human, environment,  current_distance, scenario_choice)

    if abs(P_1) < 1e-12: # Division durch 0 bzw sehr kleinen Wert verhindern
        return None

    new_distance = current_distance - P_0 / P_1

    return new_distance

def itteration_newton(human,environment, scenario_choice):

    toleranz = 1e-6
    max_schritte = 100
    schritte = 0
    current_distance = get_distance(environment, scenario_choice)
    original_distance = current_distance # um später wieder den ursprünglichen Sonnen/Erdabstand zurück zusetzten

    while max_schritte > schritte:

        r_neu = newton_step(human, environment, current_distance, scenario_choice)
        r_alt = current_distance # r_alt wird nicht gebraucht, aber für die Übersicht benutzt

        if r_neu is None: # Wert kommt aus Newton step. Ist None bei Division durch 0 bzw sehr kleinen Wert
            #print("Newtonverfahren führt nicht zum Ergebnis: Es sollte auf Bisektionsverfarhen geändert werden")
            set_distance(environment, scenario_choice, original_distance)
            return None


        if r_neu <= 0: # Um negative Werte zu verhindern bei funktionen mit mehreren Nullstellen (physikalisch nicht möglich)
            #print("Newtonverfahren führt nicht zum Ergebnis: Es sollte auf Bisektionsverfarhen geändert werden")
            set_distance(environment, scenario_choice, original_distance)
            return None

        fehler = abs(r_neu-r_alt)

        if fehler <= toleranz:
            r_alt = r_neu
            break

        r_alt = r_neu
        current_distance = r_alt
        schritte = schritte + 1

    if schritte == max_schritte:
        #print("Newtonverfahren führt nicht zum Ergebnis: Es sollte auf Bisektionsverfarhen geändert werden")
        set_distance(environment, scenario_choice, original_distance)
        return None

    set_distance(environment, scenario_choice, original_distance)

    return r_alt

def Bisektionsverfahren(human, environment, scenario_choice):

    #Originaldistanz speichern
    original_distance = get_distance(environment, scenario_choice)
    #Intervall finden
    r_0 = original_distance
    P_net_0 = calculate_net_power_at_r(human, environment, r_0, scenario_choice) # Leistungswert bei r_0
    max_steps = 100
    steps = 0


    if P_net_0 > 0: # Leistung größer 0, Abstand vergrößern
        r_1 = r_0 * 1.2
        while max_steps > steps:
            P_net_1 = calculate_net_power_at_r(human, environment, r_1, scenario_choice)
            if P_net_1 < 0: # Leistung kleiner 0, kann für Bisektion verwendet werden
                break
            r_1 = r_1 * 1.2
            steps = steps + 1

        if max_steps == steps:
            set_distance(environment, scenario_choice, original_distance)
            return None

    elif P_net_0 < 0: # Leistung kleiner 0, Abstand verringern
        r_1 = r_0* 0.8

        while max_steps > steps:
            P_net_1 = calculate_net_power_at_r(human, environment, r_1, scenario_choice)
            if P_net_1 > 0:
                break
            r_1 = r_1 * 0.8
            steps = steps + 1

        if max_steps == steps:
            set_distance(environment, scenario_choice, original_distance)
            return None

    elif P_net_0 == 0: # nur für den unwahrscheinlichen Volltreffer
        print("Dein Startwert ist die Entfernung!")
        return r_0

    #Schleife der Schritte
    toleranz = 1e-6
    max_schritte = 100
    schritte = 0

    while max_schritte > schritte: # kein extra Abbruchkriteriumschritte, da Pythongenauigkeit vor 100 Schritten erreicht.(Also Toleranzfehler)

        r_0, r_1 = bisection_step(human, environment, r_0, r_1, scenario_choice)

        fehler = abs(r_1 - r_0)
        if fehler <= toleranz:
            r_NST = (r_1 + r_0)/2
            set_distance(environment, scenario_choice, original_distance)
            return r_NST

        schritte = schritte + 1

    set_distance(environment, scenario_choice, original_distance)
    return r_0


def bisection_step(human, environment, r_0, r_1, scenario_choice):
    r_mid = (r_0 + r_1) / 2
    P_net_0 = calculate_net_power_at_r(human, environment, r_0, scenario_choice)
    P_net_mid = calculate_net_power_at_r(human, environment, r_mid, scenario_choice)

    if P_net_0 * P_net_mid > 0:
        return r_mid, r_1

    elif P_net_0 * P_net_mid < 0:
        return r_0, r_mid

    elif P_net_mid == 0: #r_mid ist dann die Nullstelle
        return r_mid, r_mid

def find_equilibrium_distance(human, environment, scenario_choice):

    if scenario_choice == "interstellar":
        return None

    if scenario_choice == 'sun_earth':
        return find_equilibrium_curve(environment,human)

    r = itteration_newton(human, environment, scenario_choice)

    if r is None:
        r = Bisektionsverfahren(human, environment, scenario_choice)

    return r

def get_distance(environment, scenario_choice):

    if scenario_choice == "sun":
        current_distance = environment.sun_distance

    elif scenario_choice == "earth":
        current_distance = environment.earth_distance


    return current_distance

def set_distance(environment, scenario_choice, distance):


    if scenario_choice == "sun":
        environment.sun_distance = distance

    elif scenario_choice == "earth":
        environment.earth_distance = distance


def find_equilibrium_curve(environment,human):

    #Ursprungswerte festhalten
    original_distance_sun = environment.sun_distance
    original_distance_earth = environment.earth_distance

    #startwert 0.95 * R bei Psun=0
    R_von_Psun_0 = find_equilibrium_distance(human, environment, "sun")
    R_start = 0.95 * R_von_Psun_0

    #Endwert Erdabstand auf (Erdradius+100km) festsetzen, dann Sonnenabstand für p=0 bestimmen *1.2
    environment.earth_distance = 6471
    environment.sun_distance = 2
    r_0 = environment.sun_distance
    P_net_start = calculate_net_power(human, environment, 'sun_earth', 1)

    max_steps = 100
    steps = 0
    nullstelle_eingeklammert = False

    if P_net_start > 0:  # Leistung größer 0, Abstand vergrößern
        r_1 = r_0 * 1.2

        while max_steps > steps:
            environment.sun_distance = r_1
            P_net_1 = calculate_net_power(human, environment, 'sun_earth', 1)
            if P_net_1 <= 0:  # Leistung kleiner 0, kann für Bisektion verwendet werden
                nullstelle_eingeklammert = True
                break
            r_1 = r_1 * 1.2
            steps = steps + 1

    elif P_net_start < 0:  # Leistung kleiner 0, Abstand verringern
        r_1 = r_0 * 0.8

        while max_steps > steps:
            environment.sun_distance = r_1
            P_net_1 = calculate_net_power(human, environment, 'sun_earth', 1)
            if P_net_1 >= 0:
                nullstelle_eingeklammert = True
                break
            r_1 = r_1 * 0.8
            steps = steps + 1
    # Abstand für Bisection eingeschlossen mit r_0 und r_1 zur bestimmung von R_end
    if not nullstelle_eingeklammert:
        raise ValueError("Sonnen-Nullstelle konnte nicht eingeklammert werden")
    print("r_0:", r_0)
    print("P_net bei r_0:", P_net_start)
    print("r_1:", r_1)
    print("P_net bei r_1:", P_net_1)
    print("Schritte:", steps)

    # Schleife der Schritte
    toleranz = 1e-6
    max_schritte = 100
    schritte = 0
    r_end = None

    while max_schritte > schritte:  # kein extra Abbruchkriteriumschritte, da Pythongenauigkeit vor 100 Schritten erreicht.(Also Toleranzfehler)

        r_0, r_1 = bisection_step_2D(human, environment, r_0, r_1, 'sun')

        fehler = abs(r_1 - r_0)
        if fehler <= toleranz:
            r_NST = (r_1 + r_0) / 2
            r_end = 1.1 * r_NST
            #set_distance(environment, scenario_choice, original_distance) original daten schon gespeichert
            break

        schritte = schritte + 1

    if r_end is None:
        raise ValueError("Sonnen-Bisektion hat nicht konvergiert")

    #Kurve erstellen
    Kurvenwerte = []

    #Schrittweite bestimmen für 50 Messpunkte
    delta_r = (r_end-R_start)/49

    #aktueller_Sonnenabstand = R_start
    environment.sun_distance = R_start

    for i in range(50):

        aktuell_Sonnenabstand = R_start + i * delta_r
        environment.sun_distance = aktuell_Sonnenabstand
        print("Aktueller Sonnenabstand:", aktuell_Sonnenabstand)

        #für aktuellen Sonnenabstand Erdabstand finden
        environment.earth_distance = 6471
        r_0 = environment.earth_distance

        P_net_start_erd = calculate_net_power(human, environment, 'sun_earth', 1)
        if P_net_start_erd == 0:
            Kurvenwerte.append((aktuell_Sonnenabstand, r_0))
            continue
        # Abstand für Bisection eingeschlossen mit r_0 und r_1
        max_steps = 100
        steps = 0
        nullstelle_eingeklammert = False


        if P_net_start_erd > 0:  # Leistung größer 0, Abstand vergrößern
            r_1 = r_0 * 1.2

            while max_steps > steps:
                environment.earth_distance = r_1
                P_net_1 = calculate_net_power(human, environment, 'sun_earth', 1)
                if P_net_1 <= 0:  # Leistung kleiner 0, kann für Bisektion verwendet werden
                    nullstelle_eingeklammert = True
                    break
                r_1 = r_1 * 1.2
                steps = steps + 1

        elif P_net_start_erd < 0:  # Leistung kleiner 0, Abstand verringern
            r_1 = r_0 * 0.8

            while max_steps > steps:
                environment.earth_distance = r_1
                P_net_1 = calculate_net_power(human, environment, 'sun_earth', 1)
                if P_net_1 >= 0:
                    nullstelle_eingeklammert = True
                    break
                r_1 = r_1 * 0.8
                steps = steps + 1

        if not nullstelle_eingeklammert:
            Kurvenwerte.append((aktuell_Sonnenabstand, None))
            continue

        # Schleife der Schritte
        toleranz = 1e-3
        max_schritte = 100
        schritte = 0
        r_NST_erd = None

        while max_schritte > schritte:  # kein extra Abbruchkriteriumschritte, da Pythongenauigkeit vor 100 Schritten erreicht.(Also Toleranzfehler)

            r_0, r_1 = bisection_step_2D(human, environment, r_0, r_1, 'earth')

            fehler = abs(r_1 - r_0)
            if fehler <= toleranz:
                r_NST_erd = (r_1 + r_0) / 2
                break

            schritte = schritte + 1

        Kurvenwerte.append((aktuell_Sonnenabstand, r_NST_erd))


    environment.sun_distance = original_distance_sun
    environment.earth_distance = original_distance_earth

    return Kurvenwerte

def bisection_step_2D(human, environment, r_0, r_1, flexibel_var):

    r_mid = (r_0 + r_1) / 2

    if flexibel_var == "sun":
        environment.sun_distance = r_0

    elif flexibel_var == "earth":
        environment.earth_distance = r_0

    P_net_0 = calculate_net_power(human, environment, 'sun_earth',1)

    if flexibel_var == "sun":
        environment.sun_distance = r_mid

    elif flexibel_var == "earth":
        environment.earth_distance = r_mid

    P_net_mid = calculate_net_power(human, environment, 'sun_earth',1)

    if P_net_0 == 0:
        return r_0, r_0

    elif P_net_0 * P_net_mid > 0:
        return r_mid, r_1

    elif P_net_0 * P_net_mid < 0:
        return r_0, r_mid

    elif P_net_mid == 0:  # r_mid ist dann die Nullstelle
        return r_mid, r_mid

















# def find_R_end_sun_earth():
#
#     environment.earth_distance = 6471
#     r_0 = 1 #AE
#     P_net_0 = calculate_net_power(human, environment,'sun', 1)  # Leistungswert bei r_0
#     max_steps = 100
#     steps = 0
#
#     if P_net_0 > 0: # Leistung größer 0, Abstand vergrößern
#         r_1 = r_0 * 1.2
#         while max_steps > steps:
#             P_net_1 = calculate_net_power_at_r(human, environment, r_1, "sun")
#             if P_net_1 < 0: # Leistung kleiner 0, kann für Bisektion verwendet werden
#                 break
#             r_1 = r_1 * 1.2
#             steps = steps + 1
#
#     elif P_net_0 < 0: # Leistung kleiner 0, Abstand verringern
#         r_1 = r_0* 0.8
#
#         while max_steps > steps:
#             P_net_1 = calculate_net_power_at_r(human, environment, r_1, "sun")
#             if P_net_1 > 0:
#                 break
#             r_1 = r_1 * 0.8
#             steps = steps + 1
#
#     elif P_net_0 == 0: # nur für den unwahrscheinlichen Volltreffer
#         print("Dein Startwert ist die Entfernung!")
#         return r_0
#
#         # Schleife der Schritte
#         toleranz = 1e-6
#         max_schritte = 100
#         schritte = 0
#
#     while max_schritte > schritte:  # kein extra Abbruchkriteriumschritte, da Pythongenauigkeit vor 100 Schritten erreicht.(Also Toleranzfehler)
#
#         r_0, r_1 = bisection_step(human, environment, r_0, r_1, "sun")
#
#         fehler = abs(r_1 - r_0)
#         if fehler <= toleranz:
#             r_NST = (r_1 + r_0) / 2
#             #set_distance(environment, scenario_choice, original_distance)
#             return r_NST
#
#         schritte = schritte + 1
#
#     #set_distance(environment, scenario_choice, original_distance)
#     return r_0

