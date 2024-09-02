import matplotlib.pyplot as plt
import mcoloring
import sys

sys.setrecursionlimit(1500)  # Sets a higher recursion limit but may lead to stack overflow


if __name__ == "__main__":
    coloring3 = []
    variations=[[],[],[]]
    validColors=[]

    triangles = []
    pts = []
    count = 0

    print("Enter test number:")
    test_number = int(input())
    test_number = str(test_number)

    # Read the triangle vertices from triangle file generated from PolyTriangulation
    with open("./tests/triangles_" + test_number + ".txt", "r") as f:
        for line in f:
            vertices = line.strip().split()
            triangle = []
            for vertex in vertices:
                x, y = map(float, vertex.split(','))
                triangle.append((x, y, count))  # Adding an index for each vertex
                pts.append([x, y, count])
                count += 1
            triangles.append(triangle)

    adj_matrix = [[0 for __ in range(count)] for _ in range(count)]

    for triangle in triangles:
        a, b, c = triangle
        adj_matrix[a[2]][b[2]] = 1
        adj_matrix[b[2]][a[2]] = 1
        adj_matrix[b[2]][c[2]] = 1
        adj_matrix[c[2]][b[2]] = 1
        adj_matrix[c[2]][a[2]] = 1
        adj_matrix[a[2]][c[2]] = 1

    g = mcoloring.Graph(count)
    g.graph = adj_matrix
    m = 3
    coloring = g.graphColouring(m)

    i = 0
    rgbCount = [0, 0, 0]
    for c in coloring:
        coloring3.append(c)
        rgbCount[c - 1] += 1
        variations[c - 1].append([i, pts[i][:2]])
        i += 1
    rgbMin = min(rgbCount)
    for i in range(len(rgbCount)):
        if rgbCount[i] == rgbMin:
            validColors.append(i)
    currVariationDisplayed = 0
    guardSelected = 0

    plt_points = []
    
    # Print number of guards
    num_guards = len(variations[1])
    print(num_guards)

    # Export the coordinates of the vertex where the guard should be
    with open("./guard_position.txt", "w+") as f:
        for coord in variations[1]:
            x, y = coord[1][0], coord[1][1]
            coord_str = str(x) + " " + str(y) + "\n"
            f.write(coord_str)
            
            # For plotting later
            plt_points.append((x, y))

    # Display on pyplot
    plot1 = plt.figure(1)
    plt_colors = ['black', 'blue', 'green']

    # Plot edges of triangle
    edges = []
    for triangle in triangles:
        for i in range(2):
            x_values = [triangle[i][0], triangle[i+1][0]]
            y_values = [triangle[i][1], triangle[i+1][1]]
            plt.plot(x_values, y_values, '-', color=plt_colors[i])
        x_values = [triangle[2][0], triangle[0][0]]
        y_values = [triangle[2][1], triangle[0][1]]
        plt.plot(x_values, y_values, '-', color=plt_colors[2])
    
    # Plot points of guard
    x_values = [point[0] for point in plt_points]
    y_values = [point[1] for point in plt_points]
    plt.scatter(x_values, y_values, color='red', marker='o') 

    # Set labels for graph    
    plt.xlabel('X-position')
    plt.ylabel('Y-position')
    plt.title('Plot of triangulation and guard positions')
    plt.grid(True)

    # Set equal scaling for both axes
    plt.gca().set_aspect('equal', adjustable='box')

    plt.show()

            