import matplotlib.pyplot as plt
import numpy as np

def plot_elevation_and_water(heights):
    n = len(heights)
    left_max = [0] * n
    right_max = [0] * n
    water_trapped = 0
    
    # Calculate left and right max for each bar
    left_max[0] = heights[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], heights[i])
        
    right_max[n - 1] = heights[n - 1]
    for i in range(n-2, -1, -1):
        right_max[i] = max(right_max[i + 1], heights[i])
    
    # Calculate water levels and trapped water
    water_level = [0] * n
    for i in range(n):
        water_height = min(left_max[i], right_max[i])
        water_level[i] = water_height
        water_trapped += max(0, water_height - heights[i])
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(range(n), heights, color='black')
    for i in range(n):
        if water_level[i] > heights[i]:
            ax.bar(i, water_level[i]-heights[i], bottom=heights[i], color='blue')
    
    ax.set_xlabel('Index')
    ax.set_ylabel('Height/Water Level')
    ax.set_title("Water Volume Trapped: "+ str(water_trapped))
    plt.xticks(range(n))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()


input1 = [0,1,0,2,1,0,1,3,2,1,2,1]
plot_elevation_and_water(input1)

input2 = [4,2,0,3,2,5]
plot_elevation_and_water(input2)

input3 = [0,0,1,0,2,0]
plot_elevation_and_water(input3)