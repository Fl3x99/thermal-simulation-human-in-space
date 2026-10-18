import matplotlib.pyplot as plt

def plot_temperatures(times, temperatures):

    plt.plot(times, temperatures)

    plt.xlabel("time [s]")
    plt.ylabel("temperature [K]")

    plt.title("Change in temperature over time")

    plt.show()

def plot_equilibrium_curve(Kurvenwerte):

    sonnenabstaende = []
    erdabstaende = []
    sonne_gueltig = []
    erde_gueltig = []

    sonne_ungueltig = []
    erde_ungueltig = []

    for sonnenabstand, erdabstand in Kurvenwerte:
        if erdabstand is not None:
            sonnenabstaende.append(sonnenabstand)
            erdabstaende.append(erdabstand)

            if erdabstand >= 6471:
                sonne_gueltig.append(sonnenabstand)
                erde_gueltig.append(erdabstand)
            else:
                sonne_ungueltig.append(sonnenabstand)
                erde_ungueltig.append(erdabstand)


    plt.plot(sonne_gueltig, erde_gueltig, color="green", label="Valid equilibrium")
    plt.plot(sonne_ungueltig, erde_ungueltig, color="red", linestyle="--", label="Outside model domain")

    plt.axhline(y=6471, color="gray", linestyle=":", label="100 km altitude")

    plt.xlabel("Distance to Sun [AU]")
    plt.ylabel("Distance to Earth's center [km]")

    plt.title("Thermal equilibrium curve – Sun and Earth")
    plt.legend()
    plt.grid(True)

    plt.show()