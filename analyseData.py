import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics

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
