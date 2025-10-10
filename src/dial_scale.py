import math


def create_lin_dial_scale_grid(inner_radius,
                               outer_radius,
                               inner_radius_subdivider,
                               outer_radius_subdivider,
                               start_angle,
                               stop_angle,
                               num_lines,
                               num_subdivisions):

    main_intervals = []
    sub_intervals = []

    for i in range(num_lines):
        angle = start_angle + (stop_angle - start_angle) * i / (num_lines - 1)
        x1 = round(inner_radius * math.cos(angle), 10)
        y1 = round(inner_radius * math.sin(angle), 10)
        x2 = round(outer_radius * math.cos(angle), 10)
        y2 = round(outer_radius * math.sin(angle), 10)
        main_intervals.append([[x1, y1], [x2, y2]])

        if i < num_lines - 1:
            for j in range(1, num_subdivisions + 1):
                sub_angle = start_angle + (stop_angle - start_angle) * (i + j / (num_subdivisions + 1)) / (num_lines - 1)  # noqa
                sub_x1 = round(inner_radius_subdivider * math.cos(sub_angle), 10)  # noqa
                sub_y1 = round(inner_radius_subdivider * math.sin(sub_angle), 10)  # noqa
                sub_x2 = round(outer_radius_subdivider * math.cos(sub_angle), 10)  # noqa
                sub_y2 = round(outer_radius_subdivider * math.sin(sub_angle), 10)  # noqa
                sub_intervals.append([[sub_x1, sub_y1], [sub_x2, sub_y2]])

    return main_intervals, sub_intervals


def create_handle(inner_radius, outer_radius, angle):
    x1 = round(inner_radius * math.cos(angle), 10)
    y1 = round(inner_radius * math.sin(angle), 10)
    x2 = round(outer_radius * math.cos(angle), 10)
    y2 = round(outer_radius * math.sin(angle), 10)
    return [[x1, y1], [x2, y2]]


def create_log_dial_scale_grid(inner_radius,
                               outer_radius,
                               inner_radius_subdivider,
                               outer_radius_subdivider,
                               start_angle, stop_angle,
                               num_lines,
                               num_subdivisions,
                               invert,
                               log_sub_ticks,
                               skip_sub_divider_for_angle_limit,
                               show_print=False
                               ):
    main_intervals = []
    sub_intervals = []
    log_angles = logspace(start_angle, stop_angle, num_lines, invert)
    if show_print: print(log_angles)  # noqa
    for i, angle in enumerate(log_angles):
        # angle = start_angle + (stop_angle - start_angle) * i / (num_lines - 1)  # noqa
        x1 = round(inner_radius * math.cos(angle), 10)
        y1 = round(inner_radius * math.sin(angle), 10)
        x2 = round(outer_radius * math.cos(angle), 10)
        y2 = round(outer_radius * math.sin(angle), 10)
        main_intervals.append([[x1, y1], [x2, y2]])
        if i < len(log_angles) - 1:
            # print(f"angle difference {abs(log_angles[i] - log_angles[i+1])}")
            if show_print:
                print(f"add subdivider between {log_angles[i]} {log_angles[i+1]}")  # noqa
            if log_sub_ticks:
                if show_print:
                    print("Log Minor Ticks")
                log_sub_angles = logspace(log_angles[i],
                                          log_angles[i+1],
                                          num_subdivisions,
                                          invert)
            else:
                if show_print:
                    print("Lin Minor Ticks")
                log_sub_angles = linspace(log_angles[i],
                                          log_angles[i+1],
                                          num_subdivisions
                                          )
            # print(log_sub_angles)
            # print(f"log_sub_angles {log_sub_angles}")
            if (abs(log_angles[i] - log_angles[i+1]) <= skip_sub_divider_for_angle_limit):  # noqa
                if show_print: print("Skip anlge too small")  # noqa
                continue
            for j, sub_angle in enumerate(log_sub_angles):
                if (abs(sub_angle - log_angles[i]) <= skip_sub_divider_for_angle_limit):  # ToDo  # noqa
                    if show_print: print(f"1. Skip {j} {sub_angle} {abs(log_angles[i] - log_angles[i+1])}")  # noqa
                    continue
                if j == 0:
                    if show_print: print(f"2. Skip 0 {log_sub_angles[j]}")  # noqa
                    continue
                if (abs(sub_angle - log_angles[i+1]) <= skip_sub_divider_for_angle_limit): # ToDo  # noqa
                    if show_print: print(f"3. Skip {j} {sub_angle} {abs(log_angles[i] - log_angles[i+1])}")  # noqa
                    continue

                # if j-1 >= len(log_sub_angles):
                #     print(f"Skip {j+1} at {log_sub_angles[j]}")
                #     continue
                # if j >= len(log_sub_angles)-1:
                #     print(f"Stop at {log_sub_angles[j]}")
                #     continue

                sub_x1 = round(inner_radius_subdivider * math.cos(sub_angle), 10)  # noqa
                sub_y1 = round(inner_radius_subdivider * math.sin(sub_angle), 10)  # noqa
                sub_x2 = round(outer_radius_subdivider * math.cos(sub_angle), 10)  # noqa
                sub_y2 = round(outer_radius_subdivider * math.sin(sub_angle), 10)  # noqa
                sub_intervals.append([[sub_x1, sub_y1], [sub_x2, sub_y2]])

    return main_intervals, sub_intervals


# ####################################################
# # Tick Masrks Version > 0.1.0 ######################
# ####################################################


def calc_major_tick_marks(start_inner_radius: float = 5,
                          stop_inner_radius: float = 5,
                          start_outer_radius: float = 5.2,
                          stop_outer_radius: float = 8,
                          start_angle: float = -150,
                          stop_angle: float = 150,
                          num_major_ticks: int = 10
                          ):
    major_angles = linspace(start_angle, stop_angle, num_major_ticks)

    major_tick_marks = []
    for angle in major_angles:

        sub_inner_r = _r_of_phi(start_radius=start_inner_radius,
                                end_radius=stop_inner_radius,
                                start_angle_deg=start_angle,
                                end_angle_deg=stop_angle,
                                angle=angle)
        sub_outer_r = _r_of_phi(start_radius=start_outer_radius,
                                end_radius=stop_outer_radius,
                                start_angle_deg=start_angle,
                                end_angle_deg=stop_angle,
                                angle=angle)

        x_inner = sub_inner_r * math.cos(angle * math.pi / 180)
        y_inner = sub_inner_r * math.sin(angle * math.pi / 180)

        x_outer = sub_outer_r * math.cos(angle * math.pi / 180)
        y_outer = sub_outer_r * math.sin(angle * math.pi / 180)

        line = [[x_inner, y_inner], [x_outer, y_outer]]
        major_tick_marks.append(line)
    return major_tick_marks


def calc_fullrange_minor_tick_marks(start_inner_radius: float = 5,
                                    stop_inner_radius: float = 5,
                                    start_outer_radius: float = 5.2,
                                    stop_outer_radius: float = 8,
                                    start_angle: float = -150,
                                    stop_angle: float = 150,
                                    num_major_ticks: int = 10,
                                    num_minor_ticks: int = 2,
                                    skip_major_pos=True
                                    ):
    major_angles = linspace(start_angle, stop_angle, num_major_ticks)

    minor_angels = []
    for i in range(len(major_angles)-1):
        minor_angels_part = linspace(major_angles[i], major_angles[i+1], num_minor_ticks+2)  # noqa
        if skip_major_pos:
            minor_angels_part.pop(-1)
            minor_angels_part.pop(0)
        minor_angels.append(minor_angels_part)

    minor_start_angle = minor_angels[0][0]
    minor_stop_angle = minor_angels[-1][-1]

    minor_tick_marks = []
    for sub_group in minor_angels:
        minor_group_sub_ticks = []
        for angle in sub_group:
            sub_inner_r = _r_of_phi(start_radius=start_inner_radius,
                                    end_radius=stop_inner_radius,
                                    start_angle_deg=minor_start_angle,
                                    end_angle_deg=minor_stop_angle,
                                    angle=angle)

            sub_outer_r = _r_of_phi(start_radius=start_outer_radius,
                                    end_radius=stop_outer_radius,
                                    start_angle_deg=minor_start_angle,
                                    end_angle_deg=minor_stop_angle,
                                    angle=angle)

            x_inner = sub_inner_r * math.cos(angle * math.pi / 180)
            y_inner = sub_inner_r * math.sin(angle * math.pi / 180)

            x_outer = sub_outer_r * math.cos(angle * math.pi / 180)
            y_outer = sub_outer_r * math.sin(angle * math.pi / 180)
            line = [[x_inner, y_inner], [x_outer, y_outer]]

            minor_group_sub_ticks.append(line)
        minor_tick_marks = minor_tick_marks + minor_group_sub_ticks
    return minor_tick_marks


def calc_sep_minor_tick_marks(start_inner_radius: float = 5,
                              stop_inner_radius: float = 5,
                              start_outer_radius: float = 5.2,
                              stop_outer_radius: float = 8,
                              start_angle: float = -150,
                              stop_angle: float = 150,
                              num_major_ticks: int = 10,
                              num_minor_ticks: int = 2,
                              skip_major_pos=True
                              ):
    major_angles = linspace(start_angle, stop_angle, num_major_ticks)

    sub_angle_group = []
    for i in range(len(major_angles)-1):
        sub_angle_group.append([major_angles[i], major_angles[i+1]])

    minor_tick_marks = []
    for sub_group in sub_angle_group:
        minor_angels = []
        # print(sub_group)
        minor_start_angle = sub_group[0]
        minor_stop_angle = sub_group[1]
        # print(minor_start_angle, minor_stop_angle)

        minor_angels_part = linspace(minor_start_angle, minor_stop_angle, num_minor_ticks + 2)  # noqa
        if skip_major_pos:
            minor_angels_part.pop(-1)
            minor_angels_part.pop(0)
        minor_angels.append(minor_angels_part)
        # print("minor_angels",minor_angels)
        minor_group_sub_ticks = []
        for angle in minor_angels_part:
            sub_inner_r = _r_of_phi(start_radius=start_inner_radius,
                                    end_radius=stop_inner_radius,
                                    start_angle_deg=minor_angels_part[0],
                                    end_angle_deg=minor_angels_part[-1],
                                    angle=angle)

            sub_outer_r = _r_of_phi(start_radius=start_outer_radius,
                                    end_radius=stop_outer_radius,
                                    start_angle_deg=minor_angels_part[0],
                                    end_angle_deg=minor_angels_part[-1],
                                    angle=angle)

            x_inner = sub_inner_r * math.cos(angle * math.pi / 180)
            y_inner = sub_inner_r * math.sin(angle * math.pi / 180)

            x_outer = sub_outer_r * math.cos(angle * math.pi / 180)
            y_outer = sub_outer_r * math.sin(angle * math.pi / 180)
            line = [[x_inner, y_inner], [x_outer, y_outer]]

            minor_group_sub_ticks.append(line)
        minor_tick_marks = minor_tick_marks + minor_group_sub_ticks
    return minor_tick_marks


# ####################################################
# # Polygon ##########################################
# ####################################################

def calc_polygon_scale(inner_radius,
                       outer_radius,
                       r_start_offset,
                       start_angle,
                       stop_angle,
                       face_counts):
    log_to_file("calc_polygon_scale")

    # Winkel in Radiant umrechnen nicht mehr nötig
    startwinkel_rad = start_angle
    endwinkel_rad = stop_angle

    # Winkelwerte für das Polygon berechnen
    winkel_aussen = linspace(startwinkel_rad, endwinkel_rad, face_counts+1)
    winkel_innen = linspace(endwinkel_rad, startwinkel_rad, face_counts+1)
    log_to_file(winkel_aussen)
    log_to_file(winkel_innen)

    # Koordinaten für das Polygon berechnen
    r_step = (outer_radius-r_start_offset - inner_radius)/face_counts
    log_to_file(r_step)
    # print(len(winkel_aussen))
    x_aussen = []
    y_aussen = []

    for i, angle in enumerate(winkel_aussen):
        # print(i, angle, r_aussen-i*r_step)
        x_aussen.append((inner_radius+r_start_offset+i*r_step) * math.cos(angle))  # noqa
        y_aussen.append((inner_radius+r_start_offset+i*r_step) * math.sin(angle))  # noqa

    x_innen = []
    y_innen = []
    for i, angle in enumerate(winkel_innen):
        x_innen.append(inner_radius * math.cos(angle))
        y_innen.append(inner_radius * math.sin(angle))

    poly = []
    for i in range(len(x_innen)):
        poly.append((float(x_innen[i]), float(y_innen[i])))
    for i in range(len(x_aussen)):
        poly.append((float(x_aussen[i]), float(y_aussen[i])))
    poly.append((float(x_innen[0]), float(y_innen[0])))
    return poly


def linspace(start, stop, steps: int) -> list:
    step_size = (stop-start)/(steps-1)
    # print(step_size)
    lin_array = []
    for i in range(steps):
        # print(i, i*step_size+start)
        lin_array.append(i*step_size+start)
    return lin_array


def logspace(start, stop, steps, invert=False):
    log_array = []
    dist = stop - start
    for i in range(steps):
        if invert:
            value = start + dist * math.pow(i/(steps-1), 2)
        else:
            value = stop - dist * math.pow(i/(steps-1), 2)
        log_array.append(value)
    return log_array


def calc_rad(angle):
    '''Convert degree to radiant.'''
    return angle * math.pi / 180


# ####################################################
# # Splitted Spiral section
# ####################################################


def _r_of_phi(start_radius: float = 5,
              end_radius: float = 8,
              start_angle_deg: float = -135,
              end_angle_deg: float = 135,
              angle: float = 0) -> list[float]:
    '''
    Parameters
    ----------
    start_radius : float
        Radius of start angle (`start_angle_deg`). Default 5.
    end_radius : float
        Radius of end angle (`end_angle_deg`). Default 8.
    start_angle_deg : float
        Start angle in degree. Default -135.
    end_angle_deg : float
        End angle in degree Default 135.
    angle : float
        Angle (theta) where radius should be calculated.

    Return:
    -------
        r_(angle)
    '''
    # $r(θ)=a⋅θ+b$
    start_angle_rad = start_angle_deg * math.pi / 180
    end_angle_rad = end_angle_deg * math.pi / 180
    theta = angle * math.pi / 180
    r = (start_radius - end_radius)/(start_angle_rad - end_angle_rad) * (theta - start_angle_rad) + start_radius  # noqa
    return r


def calc_spiral(start_radius: float = 5,
                end_radius: float = 8,
                start_angle_deg: float = -135,
                end_angle_deg: float = 135,
                segment_counts: float = 30) -> list[list[float], list[float]]:
    """
    Generates the x and y coordinate points for an Archimedean spiral
       between a start and end angle.

    The function calculates a series of points that lie along
       the defined spiral section.

    Parameters
    ----------
    start_radius : float
        The radius at the start angle (`start_angle_deg`). Default is 5.
    end_radius : float
        The radius at the end angle (`end_angle_deg`). Default is 8.
    start_angle_deg : float
        The start angle in degrees. Default is -135.
    end_angle_deg : float
        The end angle in degrees. Default is 135.
    segment_counts : int, optional
        The number of segments (points) to be generated between
          the start and end angles.
        A higher number results in a smoother curve. Default is 30.

    Returns
    -------
    list of list of float
        A list containing two sublists:
        - The first sublist contains the x-coordinates of the spiral points.
        - The second sublist contains the y-coordinates of the spiral points.
        Format: [[x1, x2, ..., xN], [y1, y2, ..., yN]]

    Notes
    -----
    This function depends on an externally defined function
      called `_r_of_phi(r_s, r_e, phi_s, phi_e, phi)`,
    which calculates the radius `r` for a specific angle `phi`.
    It is assumed that `linspace` and `math` have been imported.
    """
    angles = linspace(start_angle_deg, end_angle_deg, segment_counts)
    rads = []
    # angles = []
    for angle in angles:
        r = _r_of_phi(start_radius=start_radius,
                      end_radius=end_radius,
                      start_angle_deg=start_angle_deg,
                      end_angle_deg=end_angle_deg,
                      angle=angle)
        rads.append(r)
        # angles.append(angle)

    x_archi = []
    y_archi = []
    for i, r in enumerate(rads):
        x_archi.append(r*math.cos(angles[i] * math.pi / 180))
        y_archi.append(r*math.sin(angles[i] * math.pi / 180))

    return [x_archi, y_archi]


def _calculate_error(x_s, y_s, x1, y1):
    """
    Calculates the Euclidean distance error between two points in a 2D space.

    Parameters
    ----------
    x_s : float
        The x-coordinate of the starting point.
    y_s : float
        The y-coordinate of the starting point.
    x1 : float
        The x-coordinate of the target point.
    y1 : float
        The y-coordinate of the target point.

    Returns
    -------
    float
        The Euclidean distance error between the starting point (x_s, y_s)
            and the target point (x1, y1).

    Notes
    -----
    This function uses the Euclidean distance formula to calculate the error.
    It is assumed that `math` module has been imported.
    """
    error = math.sqrt((x1 - x_s)**2 + (y1 - y_s)**2)
    return error


def _find_intersection(start_radius: float = 5,
                       end_radius: float = 8,
                       start_angle_deg: float = -135,
                       end_angle_deg: float = 135,
                       angle: float = 0,
                       d: float = 0.5,
                       initial_guess: float = 0,
                       epsilon=0.001):
    """
    Find the intersection point between a spiral curve and a straight line.

    Parameters:
    - start_radius: The starting radius of the spiral curve.
    - end_radius: The ending radius of the spiral curve.
    - start_angle_deg: The starting angle of the spiral curve in degrees.
    - end_angle_deg: The ending angle of the spiral curve in degrees.
    - angle: The angle of the straight line in degrees.
    - d: The distance of the straight line from the origin.
    - initial_guess: The initial guess for the intersection angle.
    - epsilon: The error tolerance for convergence (default is 0.001).

    Returns:
    - Tuple containing the intersection angle, x and y coordinates of
        the spiral curve at the intersection point,
        and x and y coordinates of the straight line at the intersection point.
    """
    # 1. Initialization
    search_angle = initial_guess
    delta = 1
    r = _r_of_phi(start_radius=start_radius,
                  end_radius=end_radius,
                  start_angle_deg=start_angle_deg,
                  end_angle_deg=end_angle_deg,
                  angle=search_angle)
    # x, y of the spiral
    x_s = r*math.cos(search_angle * math.pi / 180)
    y_s = r*math.sin(search_angle * math.pi / 180)
    # Take x_s as x1, not necessary but to differentiate
    #    from the line of the spiral
    x1 = x_s
    y1 = math.tan(angle * math.pi / 180) * x1 + (d/math.cos(angle * math.pi / 180))  # noqa
    # print(x1, y1)

    # Calculate the error of the initial guess
    error_actual = _calculate_error(x_s, y_s, x1, y1)

    # The sign that determines the direction of the approximation
    sign = 1.0
    # 2. Iteration loop
    for i in range(300):
        if abs(error_actual) <= epsilon:
            return search_angle, x_s, y_s, x1, y1

        # 3. Calculate the next test value
        test_angle = search_angle + (sign * delta)
        r = _r_of_phi(start_radius=start_radius,
                      end_radius=end_radius,
                      start_angle_deg=start_angle_deg,
                      end_angle_deg=end_angle_deg,
                      angle=test_angle)
        x_s = r*math.cos(test_angle * math.pi / 180)
        y_s = r*math.sin(test_angle * math.pi / 180)
        x1 = x_s
        y1 = math.tan(angle * math.pi / 180) * x1 + (d/math.cos(angle * math.pi / 180))  # noqa

        error_new = _calculate_error(x_s, y_s, x1, y1)

        if error_new < error_actual:
            # Error decreased: Good direction!
            # Take the new value as the current value
            search_angle = test_angle
            error_actual = error_new

        else:
            # Error increased: Wrong direction!
            # a) Return to the previous (better) value
            # (current value remains unchanged)
            # b) Change the direction (sign)
            sign *= -1
            # print("direction change")

            # c) Reduce the step size (delta) for finer search
            # This is the main tool against oscillations.
            delta /= 2.0

            if delta < epsilon * 0.000001:
                # Delta has become too small, stop the search
                # print(f"\nAbort: Delta {delta} too small in {i} iterations. Error: {error_actual:.6f}")  # noqa
                return test_angle, x_s, y_s, x1, y1

        # print(f"angle {(search_angle):.2f} {test_angle} error:  {error_new:.8f} {error_actual:.8f}, {sign} {delta}")  # noqa

    return test_angle, x_s, y_s, x1, y1


def _calc_segmented_angles(start_radius,
                           end_radius,
                           start_angle_deg,
                           end_angle_deg,
                           distance,
                           angle_steps
                           ):
    segment_angles = []
    for i, angle in enumerate(angle_steps):
        # print()
        if i == 0:
            segment_angles.append(angle)
        elif i == len(angle_steps)-1:
            segment_angles.append(angle)
        else:
            # print("m,", i % 2, angle)
            anlge_m1 = _find_intersection(start_radius=start_radius,
                                          end_radius=end_radius,
                                          start_angle_deg=start_angle_deg,
                                          end_angle_deg=end_angle_deg,
                                          angle=angle,
                                          d=-distance,
                                          initial_guess=angle)[0]
            anlge_p1 = _find_intersection(start_radius=start_radius,
                                          end_radius=end_radius,
                                          start_angle_deg=start_angle_deg,
                                          end_angle_deg=end_angle_deg,
                                          angle=angle,
                                          d=distance,
                                          initial_guess=angle)[0]

            segment_angles.append(anlge_m1)
            segment_angles.append(anlge_p1)
    start_stop_segment_angles = []
    for i in range(int(len(segment_angles) / 2)):
        start_stop_segment_angles.append([segment_angles[i * 2], segment_angles[i * 2 + 1]])  # noqa
    return start_stop_segment_angles


def calc_splitted_poly(start_inner_radius: float = 5,
                       end_inner_radius: float = 5,
                       start_outer_radius: float = 6,
                       end_outer_radius: float = 8,
                       start_angle_deg: float = -135,
                       end_angle_deg: float = 135,
                       segment_counts: int = 10,
                       face_counts: int = 30,
                       distance: float = 0.2):
    angle_steps = linspace(start_angle_deg, end_angle_deg, segment_counts)
    inner_start_stop_angles = _calc_segmented_angles(start_radius=start_inner_radius,  # noqa
                                                     end_radius=end_inner_radius,  # noqa
                                                     start_angle_deg=start_angle_deg,  # noqa
                                                     end_angle_deg=end_angle_deg,  # noqa
                                                     distance=distance,
                                                     angle_steps=angle_steps)

    outer_start_stop_angles = _calc_segmented_angles(start_radius=start_outer_radius,  # noqa
                                                     end_radius=end_outer_radius,  # noqa
                                                     start_angle_deg=start_angle_deg,  # noqa
                                                     end_angle_deg=end_angle_deg,  # noqa
                                                     distance=distance,
                                                     angle_steps=angle_steps)

    polys = []
    for i in range(len(inner_start_stop_angles)):
        r_s = _r_of_phi(start_radius=start_inner_radius,
                        end_radius=end_inner_radius,
                        start_angle_deg=start_angle_deg,
                        end_angle_deg=end_angle_deg,
                        angle=inner_start_stop_angles[i][0])
        r_e = _r_of_phi(start_radius=start_inner_radius,
                        end_radius=end_inner_radius,
                        start_angle_deg=start_angle_deg,
                        end_angle_deg=end_angle_deg,
                        angle=inner_start_stop_angles[i][1])
        x_innen, y_innen = calc_spiral(start_radius=r_s,
                                       end_radius=r_e,
                                       start_angle_deg=inner_start_stop_angles[i][0],  # noqa
                                       end_angle_deg=inner_start_stop_angles[i][1],  # noqa
                                       segment_counts=face_counts)

        r_s = _r_of_phi(start_radius=start_outer_radius,
                        end_radius=end_outer_radius,
                        start_angle_deg=start_angle_deg,
                        end_angle_deg=end_angle_deg,
                        angle=outer_start_stop_angles[i][0])
        r_e = _r_of_phi(start_radius=start_outer_radius,
                        end_radius=end_outer_radius,
                        start_angle_deg=start_angle_deg,
                        end_angle_deg=end_angle_deg,
                        angle=outer_start_stop_angles[i][1])
        x_aussen, y_aussen = calc_spiral(start_radius=r_s,
                                         end_radius=r_e,
                                         start_angle_deg=outer_start_stop_angles[i][0],  # noqa
                                         end_angle_deg=outer_start_stop_angles[i][1],  # noqa
                                         segment_counts=face_counts)

        poly = []
        for j in range(len(x_innen)):
            poly.append((float(x_innen[j]), float(y_innen[j])))
        for j in range(len(x_aussen)):
            poly.append((float(x_aussen[len(x_aussen)-j-1]), float(y_aussen[len(y_aussen)-j-1])))  # noqa
        poly.append((float(x_innen[0]), float(y_innen[0])))

        polys.append(poly)
    return polys


def log_to_file(message, log_file=r"~/kicad_debug_log.txt", add_timestamp=True):  # noqa
    """
    Schreibt eine Nachricht in eine Log-Datei.##

    Args:
        message (str): Die Nachricht, die geloggt werden soll.
        log_file (str): Der Pfad zur Log-Datei.
        add_timestamp (bool): Wenn True, wird ein Zeitstempel vorangestellt.
    """
    pass
#    try:
#        # Den aktuellen Zeitstempel im Format JJJJ-MM-TT HH:MM:SS erstellen
#        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        # Die finale Log-Nachricht zusammenbauen
#        log_entry = f"{timestamp} - {message}" if add_timestamp else message
#        # Die Datei im 'append'-Modus ('a') öffnen.
#        # Das 'with'-Statement stellt sicher,
#        #       dass die Datei immer korrekt geschlossen wird.
#        with open(log_file, 'a', encoding='utf-8') as f:
#            f.write(log_entry + "\n") # "\n" für einen Zeilenumbruch
#    except IOError as e:
#        # Falls die Datei nicht geschrieben werden kann
#        #      (z.B. wegen fehlender Rechte),
#        # wird eine Fehlermeldung auf der Konsole ausgegeben.
#        print(f"!! FEHLER: Konnte nicht in die Log-Datei schreiben: {e}")
