import matplotlib.pyplot as plt
from itertools import cycle  # noqa ignore: F401 'itertools.cycle' imported but unused


def plot_line_arrays(interval_grids, show_data=False, title="Tick Marks Dial Scale Demo"):  # noqa
    # Liste von Farben für den Plot
    colors = cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
    # # interval_grids == [[[x11, y12], [x21, y22]],
    #                      [[x31, y32], [x41, y42]],
    #                      [[x11, y12], [x21, y22]],
    #                      [[x31, y32], [x41, y42]]]
    # interval_grids = [Hauptintervalle, gripper]
    # Hauptintervalle=  [[-2.47, -2.47], [-5.65, -5.65]]
    #                   [[-1.08, -3.32], [-2.47, -7.60]]
    #                   [[0.54, -3.45], [1.25, -7.90]]]

    # # gripper= [[-0.0, -0.0], [-8.0, -9.797174393178826e-16]]
    if show_data:
        for i, grid in enumerate(interval_grids):
            print(f"Array of Lines {i}:")
            # Ausgabe der Hauptintervalle
            for interval in grid:
                print(interval)
                pass

    # Plotte das Raster
    fig, ax = plt.subplots()
    for i, grid in enumerate(interval_grids):
        color = next(colors)
        for line in grid:
            ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=color)  # noqa

    ax.set_aspect('equal')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(title)
    plt.grid(True)
    # Y-Achse invertieren. Anzeige wie in KiCad.
    plt.gca().invert_yaxis()
    plt.show()


def plot_poly_x_y(x_line, y_line, dots=True, title="Polygon Scale"):
    # Polygon zeichnen
    plt.fill(x_line, y_line, alpha=0.5)
    # plt.fill(poly, alpha=0.5)

    if dots:
        # Liste mit vordefinierten Farben
        colors = ['blue', 'green', 'purple', 'orange', 'black']
        for i in range(len(x_line)):
            color_index = i % len(colors)
            # # Punkte in verschiedenen Farben plotten
            plt.plot(x_line[i], y_line[i], 'o', color=colors[color_index])

        # Den ersten Punkt als rot markieren
        plt.plot(x_line[0], y_line[0], 'o', color='red')

    # Achsenbeschriftung
    plt.xlabel('X-Achse (mm)')
    plt.ylabel('Y-Achse (mm)')

    # Titel
    plt.title(title)

    # Anzeigen des Plots
    # Gleiche Skalierung für X- und Y-Achse
    plt.axis('equal')
    plt.grid(True)
    # Y-Achse invertieren. Anzeige wie in KiCad.
    plt.gca().invert_yaxis()
    plt.show()


def plot_multi_poly_x_y(xy_lines=[], dots=True, title="Multi Polygon Scales"):  # noqa
    plt.figure(figsize=(8, 8))
    for x_line, y_line in xy_lines:

        plt.fill(x_line, y_line, alpha=0.5)
        if dots:
            colors = ['blue', 'green', 'purple', 'orange', 'black']  # color list  # noqa
            for i in range(len(x_line)):
                color_index = i % len(colors)
                plt.plot(x_line[i], y_line[i], 'o', color=colors[color_index])

            # Den ersten Punkt als rot markieren
            plt.plot(x_line[0], y_line[0], 'o', color='red')

    # Achsenbeschriftung
    plt.xlabel('X-Achse (mm)')
    plt.ylabel('Y-Achse (mm)')

    # Titel
    plt.title(title)

    # Anzeigen des Plots
    plt.axis('equal')  # Gleiche Skalierung für X- und Y-Achse
    plt.grid(True)
    # Y-Achse invertieren. Anzeige wie in KiCad.
    plt.gca().invert_yaxis()
    plt.show()


def xy_array_to_xANDyArray(poly):
    x_line = []
    y_line = []
    for element in poly:
        x_line.append(element[0])
        y_line.append(element[1])
    # xy_lines.append([x_line, y_line])
    return x_line, y_line
