import pcbnew
import math
import numpy as np
import FootprintWizardBase  # Import der speziellen Hilfs-Bibliothek

# --- Meta data ---
__author__ = "Stefan H (BatNoize)"
__version__ = "0.0.5"
__date__ = "2025-08-28"
# -----------------------------


def create_cartesian_grid(inner_radius,
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
    winkel_aussen = np.linspace(startwinkel_rad, endwinkel_rad, face_counts+1)
    winkel_innen = np.linspace(endwinkel_rad, startwinkel_rad, face_counts+1)
    log_to_file(winkel_aussen)
    log_to_file(winkel_innen)

    # Koordinaten für das Polygon berechnen
    r_step = (outer_radius-r_start_offset - inner_radius)/face_counts
    log_to_file(r_step)
    print(len(winkel_aussen))
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

# import os
# from datetime import datetime


def log_to_file(message, log_file=r"~/kicad_debug_log.txt", add_timestamp=True):
#    """
#    Schreibt eine Nachricht in eine Log-Datei.##

#    Args:
#        message (str): Die Nachricht, die geloggt werden soll.
#        log_file (str): Der Pfad zur Log-Datei.
#        add_timestamp (bool): Wenn True, wird ein Zeitstempel vorangestellt.
#    """
#    try:
#        # Den aktuellen Zeitstempel im Format JJJJ-MM-TT HH:MM:SS erstellen
#        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#        # Die finale Log-Nachricht zusammenbauen
#        log_entry = f"{timestamp} - {message}" if add_timestamp else message
#
#        # Die Datei im 'append'-Modus ('a') öffnen.
#        # Das 'with'-Statement stellt sicher, dass die Datei immer korrekt geschlossen wird.
#        with open(log_file, 'a', encoding='utf-8') as f:
#            f.write(log_entry + "\n") # "\n" für einen Zeilenumbruch

#    except IOError as e:
#        # Falls die Datei nicht geschrieben werden kann (z.B. wegen fehlender Rechte),
#        # wird eine Fehlermeldung auf der Konsole ausgegeben.
#        print(f"!! FEHLER: Konnte nicht in die Log-Datei schreiben: {e}")
    pass


class Dial_Scale_FrontPanel_FootprintWizard(FootprintWizardBase.FootprintWizard):  # noqa
    """
    Customized dial scale frontpanel footprints.
    Users can input various parameters in the dialog to define the characteristics
    of the dial scale, such as hole configuration,
    tick marks, arc fill, center handle, and help circle for orientation.
    """

    # Diese Lambda-Funktionen sind eine kompakte Art,
    #   die Metadaten zu definieren
    GetName = lambda self: "Dial Scale Footprint Wizard (BatNoize)"
    GetDescription = lambda self: Dial_Scale_FrontPanel_FootprintWizard.__doc__
    GetReferencePrefix = lambda self: "Dial_Scale"
    GetValue = lambda self: "Polygon_Line"


    def GenerateParameterList(self):
        """
        Definiert die Parameter, die der Benutzer im Dialog eingeben kann.
        """
        # Wir gruppieren alle Parameter unter unterschiedlichen Gruppen
        self.AddParam("Hole", "active", self.uBool, True)
        self.AddParam("Hole", "hole_radius", self.uMM, 2, min_value=0.05)
        self.AddParam("Hole", "pad_radius", self.uMM, 0.1, min_value=0.01)
        self.AddParam("Hole", "plated", self.uBool, False)

        self.AddParam("Tick_Marks", "active_Major", self.uBool, True)
        self.AddParam("Tick_Marks", "active_Minor", self.uBool, False),
        self.AddParam("Tick_Marks", "line_width_Major", self.uMM, 0.2, min_value=0.01)  # noqa
        self.AddParam("Tick_Marks", "line_width_Minor", self.uMM, 0.15, min_value=0.01)  # noqa
        self.AddParam("Tick_Marks", "inner_radius_Major", self.uMM, 5.5)
        self.AddParam("Tick_Marks", "outer_radius_Major", self.uMM, 8)
        self.AddParam("Tick_Marks", "start_angle", self.uFloat, -150)
        self.AddParam("Tick_Marks", "stop_angle", self.uFloat, 150)
        self.AddParam("Tick_Marks", "inner_radius_Minor", self.uMM, 5.5)
        self.AddParam("Tick_Marks", "outer_radius_Minor", self.uMM, 7.2)
        self.AddParam("Tick_Marks", "num_Major_Ticks", self.uInteger, 11)
        self.AddParam("Tick_Marks", "num_Minor_Ticks", self.uInteger, 4)

        self.AddParam("Arc_Fill", "active", self.uBool, False)
        self.AddParam("Arc_Fill", "filled", self.uBool, False)
        self.AddParam("Arc_Fill", "inner_radius", self.uMM, 6.5)
        self.AddParam("Arc_Fill", "outer_radius", self.uMM, 8.5)
        self.AddParam("Arc_Fill", "start_radius_offset", self.uMM, 0.5)
        self.AddParam("Arc_Fill", "start_angle", self.uFloat, -150)
        self.AddParam("Arc_Fill", "stop_angle", self.uFloat, 150)
        self.AddParam("Arc_Fill", "polygon_verticies", self.uInteger, 6)
        self.AddParam("Arc_Fill", "line_width", self.uMM, 0.1)

        self.AddParam("Center_Handle", "active", self.uBool, False)
        self.AddParam("Center_Handle", "line_width", self.uMM, 0.1, min_value=0.01)  # noqa
        self.AddParam("Center_Handle", "inner_radius", self.uMM, 0)
        self.AddParam("Center_Handle", "outer_radius", self.uMM, 10)
        self.AddParam("Center_Handle", "angle", self.uFloat, 180)

        self.AddParam("help", "active", self.uBool, True)
        self.AddParam("help", "circle_radius", self.uMM, 10)
        self.AddParam("help", "line_width", self.uMM, 0.05, min_value=0.01)

    def BuildThisFootprint(self):
        """
        Erstellt die Geometrie des Footprints.
        Die Hilfs-Bibliothek stellt ein 'self.draw' Objekt zur Verfügung.
        Alle Werte aus den Parametern sind bereits in KiCad-internen Einheiten (nm).
        """
        # 1. Parameter auslesen
        # Die Struktur ist self.parameters[gruppen_name][parameter_name]
        show_radials = self.parameters["Tick_Marks"]["active_Major"]
        show_radial_subdivision = self.parameters["Tick_Marks"]["active_Minor"]  # noqa
        inner_radius = self.parameters["Tick_Marks"]["inner_radius_Major"]
        outer_radius = self.parameters["Tick_Marks"]["outer_radius_Major"]
        start_angle = self.parameters["Tick_Marks"]["start_angle"]*math.pi/180
        stop_angle = self.parameters["Tick_Marks"]["stop_angle"]*math.pi/180
        inner_radius_subdivider = self.parameters["Tick_Marks"]["inner_radius_Minor"]  # noqa
        outer_radius_subdivider = self.parameters["Tick_Marks"]["outer_radius_Minor"]  # noqa
        num_radial_lines = self.parameters["Tick_Marks"]["num_Major_Ticks"]
        num_subdivision_lines = self.parameters["Tick_Marks"]["num_Minor_Ticks"]  # noqa
        line_width_main = self.parameters["Tick_Marks"]["line_width_Major"]
        line_width_subdivision = self.parameters["Tick_Marks"]["line_width_Minor"]  # noqa

        hole_show = self.parameters["Hole"]["active"]
        hole_radius = self.parameters["Hole"]["hole_radius"]
        hole_pad_radius = self.parameters["Hole"]["pad_radius"]
        hole_pad_plated = self.parameters["Hole"]["plated"]

        poly_show = self.parameters["Arc_Fill"]["active"]
        poly_filled = self.parameters["Arc_Fill"]["filled"]
        poly_inner_radius = self.parameters["Arc_Fill"]["inner_radius"]
        poly_outer_radius = self.parameters["Arc_Fill"]["outer_radius"]
        poly_start_radius_offset = self.parameters["Arc_Fill"]["start_radius_offset"]  # noqa
        poly_start_angle = self.parameters["Arc_Fill"]["start_angle"]*math.pi/180  # noqa
        poly_stop_angle = self.parameters["Arc_Fill"]["stop_angle"]*math.pi/180  # noqa
        poly_polygon_verticies = self.parameters["Arc_Fill"]["polygon_verticies"]  # noqa
        poly_line_width = self.parameters["Arc_Fill"]["line_width"]

        show_center_handle = self.parameters["Center_Handle"]["active"]  # noqa
        line_width_handle = self.parameters["Center_Handle"]["line_width"]
        inner_radius_handle = self.parameters["Center_Handle"]["inner_radius"]
        outer_radius_handle = self.parameters["Center_Handle"]["outer_radius"]
        angle_handle = self.parameters["Center_Handle"]["angle"]*math.pi/180

        help_circle = self.parameters["help"]["active"]
        help_radius = self.parameters["help"]["circle_radius"]
        help_line_width = self.parameters["help"]["line_width"]

        self.draw.SetLayer(pcbnew.F_SilkS)
        main_intervals, sub_intervals = create_cartesian_grid(inner_radius,
                                                              outer_radius,
                                                              inner_radius_subdivider,  # noqa
                                                              outer_radius_subdivider,  # noqa
                                                              start_angle,
                                                              stop_angle,
                                                              num_radial_lines,
                                                              num_subdivision_lines)  # noqa

        if hole_show:
            # Radius übergane unterschiedet sich ein bisschen
            #    von andereen Methoden.
            pad = pcbnew.PAD(self.module)
            pad.SetSize(pcbnew.VECTOR2I_MM((hole_pad_radius/5e5), (hole_pad_radius/5e5)))  # noqa
            pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
            if hole_pad_plated:
                pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
                pad.SetLayerSet(pad.PTHMask())
            else:
                pad.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
                pad.SetLayerSet(pad.UnplatedHoleMask())
            pad.SetDrillSize(pcbnew.VECTOR2I_MM((hole_radius/5e5), (hole_radius/5e5)))  # noqa
            self.module.Add(pad)

        if show_radials:
            self.draw.SetLayer(pcbnew.F_SilkS)
            self.draw.SetLineThickness(line_width_main)
            for current_line in main_intervals:
                start_x = current_line[0][0]
                start_y = current_line[0][1]
                end_x = current_line[1][0]
                end_y = current_line[1][1]
                self.draw.Line(start_x, start_y, end_x, end_y)
            log_to_file("show_radials")
            log_to_file(main_intervals)

        if show_radial_subdivision:
            self.draw.SetLayer(pcbnew.F_SilkS)
            self.draw.SetLineThickness(line_width_subdivision)
            for current_line in sub_intervals:
                start_x = current_line[0][0]
                start_y = current_line[0][1]
                end_x = current_line[1][0]
                end_y = current_line[1][1]
                self.draw.Line(start_x, start_y, end_x, end_y)

        if poly_show:
            self.draw.SetLayer(pcbnew.F_SilkS)
            self.draw.SetLineThickness(poly_line_width)
            poly_points = calc_polygon_scale(poly_inner_radius,
                                             poly_outer_radius,
                                             poly_start_radius_offset,
                                             poly_start_angle,
                                             poly_stop_angle,
                                             poly_polygon_verticies)

            log_to_file("show_poly")
            log_to_file(poly_points)
            log_to_file(type(poly_points[0][0]))

            punkte_in_mm = poly_points
            # Eine realistische Grenze, z.B. 1 Meter = 1000 mm
            MAX_COORD_MM = 1000
            punkte_kicad = []
            for x, y in punkte_in_mm:
                # Prüfe, ob die Zahlen gültig (nicht inf, nicht nan)
                #      und im Rahmen sind
                if math.isfinite(x) and math.isfinite(y) and abs(x) < MAX_COORD_MM and abs(y) < MAX_COORD_MM:  # noqa
                    punkte_kicad.append(pcbnew.VECTOR2I_MM(x, y))
                else:
                    # fehlerhafte werte korrigieren
                    punkte_kicad.append(pcbnew.VECTOR2I_MM(x/1e6, y/1e6))

            # Wichtig: Dies ist für grafische Elemente,
            #        nicht für Kupferflächen!
            polygon_umriss = pcbnew.PCB_SHAPE()
            # 5. Eigenschaften des Objekts festlegen
            polygon_umriss.SetShape(pcbnew.SHAPE_T_POLY)
            polygon_umriss.SetLayer(pcbnew.F_SilkS)  # Vorderer Siebdruck
            polygon_umriss.SetWidth(int(poly_line_width))
            if poly_filled:
                polygon_umriss.SetFilled(True)  # Füllung aktivieren
            else:
                polygon_umriss.SetFilled(False)
            # 6. Dem Objekt die Eckpunkte zuweisen
            polygon_umriss.SetPolyPoints(punkte_kicad)

            # 7. Das fertige Objekt zum Board hinzufügen
            self.module.Add(polygon_umriss)

        self.draw.SetLineThickness(help_line_width)

        if show_center_handle:
            self.draw.SetLayer(pcbnew.F_SilkS)
            self.draw.SetLineThickness(line_width_handle)
            handle = create_handle(inner_radius_handle,
                                   outer_radius_handle,
                                   angle_handle)
            start_x = handle[0][0]
            start_y = handle[0][1]
            end_x = handle[1][0]
            end_y = handle[1][1]
            self.draw.Line(start_x, start_y, end_x, end_y)

        if help_circle:
            self.draw.SetLayer(pcbnew.Dwgs_User)
            self.draw.SetLineThickness(help_line_width)
            self.draw.Circle(0, 0, help_radius)

        self.draw.SetLayer(pcbnew.F_SilkS)
        self.draw.SetLineThickness(0.15)

        # Standard-Textelemente hinzufügen
        # Die Platzierung und Größe wird hier automatisch gehandhabt
        text_offset = 10.0e6 + self.GetTextSize() * 0.6
        log_to_file(f"text_offset {text_offset}")
        self.draw.Reference(0, -text_offset, self.GetTextSize())
        self.draw.Value(0, text_offset, self.GetTextSize())

    def CheckParameters(self):
        """
        Optionale Methode zur Überprüfung der Benutzereingaben.
        """
        pass


# Registriert den Wizard bei KiCad
Dial_Scale_FrontPanel_FootprintWizard().register()
