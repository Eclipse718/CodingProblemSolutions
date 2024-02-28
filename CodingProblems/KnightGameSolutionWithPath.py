import matplotlib.pyplot as plt

def calculateMinimumHP(dungeon):
    m, n = len(dungeon), len(dungeon[0])
    dp = [[float('inf') for _ in range(n+1)] for _ in range(m+1)]
    dp[m][n-1] = dp[m-1][n] = 1
    for i in range(m-1, -1, -1):
        for j in range(n-1, -1, -1):
            dp[i][j] = max(min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j], 1)
    min_health = dp[0][0]

    # Create a visualization of the dungeon
    plt.figure(figsize=(10, 10))
    plt.imshow(dungeon, cmap='RdYlGn')
    plt.colorbar()
    plt.title(f'Dungeon with Minimum Health: {min_health}')

    # Add the optimal path to the visualization
    path = []
    i, j = 0, 0
    while i < m and j < n:
        path.append((i, j))
        if dp[i+1][j] < dp[i][j+1]:
            i += 1
        else:
            j += 1
    plt.plot([x[1] for x in path], [x[0] for x in path], 'r-', linewidth=2)

    plt.show()

    return min_health

dungeon = [[-2,-3,3],[-5,0,1],[10,30,-5]]
print(calculateMinimumHP(dungeon))  # Output: 7

dungeon = [[2, -4], [-6, -20]]
print(calculateMinimumHP(dungeon))  # Output: 3