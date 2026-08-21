from plotter import plot_points

def bresenham_circle(xc, yc, r):
    points = []

    def plot_octants(x, y):
        points.extend([
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x),
            (xc + y, yc - x), (xc - y, yc - x),
        ])

    x = 0
    y = r
    d = 3 - 2 * r
    plot_octants(x, y)

    while y >= x:
        x += 1
        if d > 0:
            y -= 1
            d += 4 * (x - y) + 10
        else:
            d += 4 * x + 6
        plot_octants(x, y)

    return points

def run():
    xc = int(input("center x: "))
    yc = int(input("center y: "))
    r = int(input("radius: "))
    points = bresenham_circle(xc, yc, r)
    plot_points(points, title="Bresenham Circle", grid_size=(r + 5) * 2)

if __name__ == "__main__":
    run()