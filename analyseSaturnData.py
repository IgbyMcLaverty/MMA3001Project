import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics

if __name__ == "__main__":
    """

    groundTemps = []
    groundPressures = []

    for i in range(0,201):
        frame = pd.read_csv(f"saturnSims/Without_Airbrakes/SATURN_dataframe_{i}.csv")
        groundTemps.append(frame['air_temperature'][0])
        groundPressures.append(frame['air_pressure'][0])
        print(f"progess: {(i/201)*100:.0f}%",end='\r')
    print("Finished")
    print(f"ground temp: mean {statistics.mean(groundTemps):.2f} sd: {statistics.stdev(groundTemps)}")
    print(f"ground pressure: mean {statistics.mean(groundPressures):.2f} sd: {statistics.stdev(groundPressures)}")

    plt.scatter(groundTemps,groundPressures,)
    plt.xlabel("groundTemps")
    plt.ylabel("groundPressures")
    plt.show()

    for i in range(0,10):
        frame = pd.read_csv(f"saturnSims/Without_Airbrakes/SATURN_dataframe_{i}.csv")
        plt.plot(frame['altitude_barometric'],frame['air_temperature'])
    plt.xlabel("altitude")
    plt.ylabel("air temperature")
    plt.title("Air Temperature Vs Altitude")

    plt.show()

    for i in range(0,10):
        frame = pd.read_csv(f"saturnSims/Without_Airbrakes/SATURN_dataframe_{i}.csv")
        plt.plot(frame['altitude_barometric'],frame['air_pressure'])
    plt.xlabel("altitude")
    plt.ylabel("air pressure")
    plt.title("Air Pressure Vs Altitude")

    plt.show()

    """

    i = 87
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    fig.suptitle(f"analysis for frame {i}", fontsize=16)

    frame = pd.read_csv(f"saturnSims/Without_Airbrakes/SATURN_dataframe_{i}.csv")
    #acc = frame['altitude_barometric'].diff().diff()

    ax = axes[0]
    #ax.plot(frame['time'][0:2000],frame['aerodynamic_pitch'][0:2000],label="aero pitch")
    ax.plot(frame['time'][0:2000],frame['pitch'][0:2000],label="true pitch")
    ax.set_xlabel("Time(s)")
    ax.set_ylabel("Pitch(degrees)")
    ax.set_title("Pitch vs Time")
    ax.legend()

    ax = axes[1]
    ax.plot(frame['time'],frame['altitude_barometric'],label="altitude")
    ax.set_xlabel("time")
    ax.set_ylabel("altitude")
    ax.set_title("altitude vs time")
    ax.legend()

    plt.tight_layout()
    plt.show()
