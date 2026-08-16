import matplotlib.pyplot as plt

def plot_temperatures(times, temperatures):

    plt.plot(times, temperatures)

    plt.xlabel("time [s]")
    plt.ylabel("temperature [K]")

    plt.title("Change in temperature over time")

    plt.show()

