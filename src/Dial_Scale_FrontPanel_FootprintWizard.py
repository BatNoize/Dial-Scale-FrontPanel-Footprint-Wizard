import math

# from __future__ import division
import FootprintWizardBase  # Import der speziellen Hilfs-Bibliothek
import pcbnew

from dial_scale import (calc_polygon_scale,
                        create_handle,
                        create_lin_dial_scale_grid,
                        create_log_dial_scale_grid,
                        log_to_file,
                        calc_splitted_poly)

# from src.dial_scale import linspace

# --- Meta data ---
__author__ = "Stefan H (BatNoize)"
__date__ = "2025-08-28"
# -----------------------------


class Dial_Scale_FrontPanel_FootprintWizard(FootprintWizardBase.FootprintWizard):  # noqa
    """
    Customized dial scale frontpanel footprints.
    Users can input various parameters in the dialog to define the characteristics  # noqa
    of the dial scale, such as hole configuration,
    tick marks, arc fill, center handle, and help circle for orientation.
    """

    # Diese Lambda-Funktionen sind eine kompakte Art,
    #   die Metadaten zu definieren
    GetName = lambda self: "Dial Scale Footprint Wizard (BatNoize)"  # noqa
    # GetDescription = lambda self: Dial_Scale_FrontPanel_FootprintWizard.__doc__  # noqa
    GetDescription = lambda self: 'Customized dial scale frontpanel footprints.'  # noqa
    GetReferencePrefix = lambda self: "Dial_Scale"  # noqa
    # GetValue = lambda self: "Dial_Scale"  # noqa
    GetValue = lambda self: self.module.Value().GetText()  # noqa

    def GenerateParameterList(self):
        """
        Definiert die Parameter, die der Benutzer im Dialog eingeben kann.
        """
        # Wir gruppieren alle Parameter unter unterschiedlichen Gruppen
        self.AddParam("Hole", "active", self.uBool, True)
        self.AddParam("Hole", "hole_radius", self.uMM, 3.75, min_value=0.05)
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

        self.AddParam("Tick_Marks_log", "active_Major", self.uBool, False)
        self.AddParam("Tick_Marks_log", "active_Minor", self.uBool, False),
        self.AddParam("Tick_Marks_log", "line_width_Major", self.uMM, 0.2, min_value=0.01)  # noqa
        self.AddParam("Tick_Marks_log", "line_width_Minor", self.uMM, 0.15, min_value=0.01)  # noqa
        self.AddParam("Tick_Marks_log", "inner_radius_Major", self.uMM, 5.5)
        self.AddParam("Tick_Marks_log", "outer_radius_Major", self.uMM, 8)
        self.AddParam("Tick_Marks_log", "start_angle", self.uFloat, -150)
        self.AddParam("Tick_Marks_log", "stop_angle", self.uFloat, 150)
        self.AddParam("Tick_Marks_log", "inner_radius_Minor", self.uMM, 5.5)
        self.AddParam("Tick_Marks_log", "outer_radius_Minor", self.uMM, 7.2)
        self.AddParam("Tick_Marks_log", "num_Major_Ticks", self.uInteger, 10)
        self.AddParam("Tick_Marks_log", "num_Minor_Ticks", self.uInteger, 10)
        self.AddParam("Tick_Marks_log", "invert_scale", self.uBool, False)
        self.AddParam("Tick_Marks_log", "log_Minor", self.uBool, True)
        self.AddParam("Tick_Marks_log", "skip_Minor_Ticks_by_degree", self.uFloat, 2, min_value=0.0)  # noqa

        self.AddParam("Arc_Fill", "active", self.uBool, False)
        self.AddParam("Arc_Fill", "filled", self.uBool, False)
        self.AddParam("Arc_Fill", "inner_radius", self.uMM, 6.5)
        self.AddParam("Arc_Fill", "outer_radius", self.uMM, 8.5)
        self.AddParam("Arc_Fill", "start_radius_offset", self.uMM, 0.5)
        self.AddParam("Arc_Fill", "start_angle", self.uFloat, -150)
        self.AddParam("Arc_Fill", "stop_angle", self.uFloat, 150)
        self.AddParam("Arc_Fill", "polygon_verticies", self.uInteger, 6)
        self.AddParam("Arc_Fill", "line_width", self.uMM, 0.1)

        self.AddParam("Arc_Splitted_Fill", "active", self.uBool, False)
        self.AddParam("Arc_Splitted_Fill", "filled", self.uBool, True)
        self.AddParam("Arc_Splitted_Fill", "start_inner_radius", self.uMM, 6.5)
        self.AddParam("Arc_Splitted_Fill", "stop_inner_radius", self.uMM, 6.5)
        self.AddParam("Arc_Splitted_Fill", "start_outer_radius", self.uMM, 7.0)
        self.AddParam("Arc_Splitted_Fill", "stop_outer_radius", self.uMM, 8.5)
        self.AddParam("Arc_Splitted_Fill", "start_angle", self.uFloat, -150)
        self.AddParam("Arc_Splitted_Fill", "stop_angle", self.uFloat, 150)
        self.AddParam("Arc_Splitted_Fill", "num_Major_Ticks", self.uInteger, 11, min_value=2)  # noqa
        self.AddParam("Arc_Splitted_Fill", "distance", self.uMM, 0.2)  # noqa
        self.AddParam("Arc_Splitted_Fill", "polygon_verticies", self.uInteger, 30, min_value=2)  # noqa
        self.AddParam("Arc_Splitted_Fill", "line_width", self.uMM, 0.0)

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
        Alle Werte aus den Parametern sind bereits
        in KiCad-internen Einheiten (nm).
        """
        # 1. Parameter auslesen
        # Die Struktur ist self.parameters[gruppen_name][parameter_name]
        show_lin_major_ticks = self.parameters["Tick_Marks"]["active_Major"]
        show_lin_minor_ticks = self.parameters["Tick_Marks"]["active_Minor"]  # noqa
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

        show_log_major_ticks = self.parameters["Tick_Marks_log"]["active_Major"]  # noqa
        show_log_minor_ticks = self.parameters["Tick_Marks_log"]["active_Minor"]  # noqa
        inner_radius_log = self.parameters["Tick_Marks_log"]["inner_radius_Major"]  # noqa
        outer_radius_log = self.parameters["Tick_Marks_log"]["outer_radius_Major"]  # noqa
        start_angle_log = self.parameters["Tick_Marks_log"]["start_angle"]*math.pi/180  # noqa
        stop_angle_log = self.parameters["Tick_Marks_log"]["stop_angle"]*math.pi/180  # noqa
        inner_radius_minor_log = self.parameters["Tick_Marks_log"]["inner_radius_Minor"]  # noqa
        outer_radius_minor_log = self.parameters["Tick_Marks_log"]["outer_radius_Minor"]  # noqa
        num_major_lines_log = self.parameters["Tick_Marks_log"]["num_Major_Ticks"]  # noqa
        num_minor_lines_log = self.parameters["Tick_Marks_log"]["num_Minor_Ticks"]  # noqa
        invert_log_scale = self.parameters["Tick_Marks_log"]["invert_scale"]
        log_minor_ticks = self.parameters["Tick_Marks_log"]["log_Minor"]
        line_width_major_log = self.parameters["Tick_Marks_log"]["line_width_Major"]  # noqa
        line_width_minor_log = self.parameters["Tick_Marks_log"]["line_width_Minor"]  # noqa
        skip_minor_Ticks_by_degree = self.parameters["Tick_Marks_log"]["skip_Minor_Ticks_by_degree"]*math.pi/180  # noqa

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

        acr_spl_show = self.parameters["Arc_Splitted_Fill"]["active"]
        acr_spl_filled = self.parameters["Arc_Splitted_Fill"]["filled"]
        acr_spl_start_inner_radius = self.parameters["Arc_Splitted_Fill"]["start_inner_radius"]  # noqa
        acr_spl_stop_inner_radius = self.parameters["Arc_Splitted_Fill"]["stop_inner_radius"]  # noqa
        acr_spl_start_outer_radius = self.parameters["Arc_Splitted_Fill"]["start_outer_radius"]  # noqa
        acr_spl_stop_outer_radius = self.parameters["Arc_Splitted_Fill"]["stop_outer_radius"]  # noqa
        acr_spl_start_angle_deg = self.parameters["Arc_Splitted_Fill"]["start_angle"]  # noqa
        acr_spl_stop_angle_deg = self.parameters["Arc_Splitted_Fill"]["stop_angle"]  # noqa
        acr_spl_num_Major_Ticks = self.parameters["Arc_Splitted_Fill"]["num_Major_Ticks"]  # noqa
        acr_spl_face_counts = self.parameters["Arc_Splitted_Fill"]["polygon_verticies"]  # noqa
        acr_spl_distance = self.parameters["Arc_Splitted_Fill"]["distance"] / 2
        acr_spl_line_width = self.parameters["Arc_Splitted_Fill"]["line_width"]

        show_center_handle = self.parameters["Center_Handle"]["active"]  # noqa
        line_width_handle = self.parameters["Center_Handle"]["line_width"]
        inner_radius_handle = self.parameters["Center_Handle"]["inner_radius"]
        outer_radius_handle = self.parameters["Center_Handle"]["outer_radius"]
        angle_handle = self.parameters["Center_Handle"]["angle"]*math.pi/180

        help_circle = self.parameters["help"]["active"]
        help_radius = self.parameters["help"]["circle_radius"]
        help_line_width = self.parameters["help"]["line_width"]

        self.draw.SetLayer(pcbnew.F_SilkS)
        major_lin_intervals, minor_lin_intervals = create_lin_dial_scale_grid(inner_radius,  # noqa
                                                                             outer_radius,  # noqa
                                                                             inner_radius_subdivider,  # noqa
                                                                             outer_radius_subdivider,  # noqa
                                                                             start_angle,  # noqa
                                                                             stop_angle,  # noqa
                                                                             num_radial_lines,  # noqa
                                                                             num_subdivision_lines)  # noqa

        major_log_intervals, minor_log_intervals = create_log_dial_scale_grid(inner_radius=inner_radius_log,  # noqa
                                                                              outer_radius=outer_radius_log,  # noqa
                                                                              inner_radius_subdivider=inner_radius_minor_log,  # noqa
                                                                              outer_radius_subdivider=outer_radius_minor_log,  # noqa
                                                                              start_angle=start_angle_log,  # noqa
                                                                              stop_angle=stop_angle_log,  # noqa
                                                                              num_lines=num_major_lines_log,  # noqa
                                                                              num_subdivisions=num_minor_lines_log,  # noqa
                                                                              invert=invert_log_scale,  # noqa
                                                                              log_sub_ticks=log_minor_ticks,  # noqa
                                                                              skip_sub_divider_for_angle_limit=skip_minor_Ticks_by_degree,  # noqa
                                                                              show_print=False  # noqa
                                                                              )

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

        if show_lin_major_ticks:
            self.draw.SetLayer(pcbnew.F_SilkS)
            self.draw.SetLineThickness(line_width_main)
            for current_line in major_lin_intervals:
                start_x = current_line[0][0]
                start_y = current_line[0][1]
                end_x = current_line[1][0]
                end_y = current_line[1][1]
                self.draw.Line(start_x, start_y, end_x, end_y)
            log_to_file("show_radials")
            log_to_file(major_lin_intervals)

        if show_lin_minor_ticks:
            self.draw.SetLayer(pcbnew.F_SilkS)
            self.draw.SetLineThickness(line_width_subdivision)
            for current_line in minor_lin_intervals:
                start_x = current_line[0][0]
                start_y = current_line[0][1]
                end_x = current_line[1][0]
                end_y = current_line[1][1]
                self.draw.Line(start_x, start_y, end_x, end_y)

        if show_log_major_ticks:
            self.draw.SetLayer(pcbnew.F_SilkS)
            self.draw.SetLineThickness(line_width_major_log)
            for current_line in major_log_intervals:
                start_x = current_line[0][0]
                start_y = current_line[0][1]
                end_x = current_line[1][0]
                end_y = current_line[1][1]
                self.draw.Line(start_x, start_y, end_x, end_y)

        if show_log_minor_ticks:
            self.draw.SetLayer(pcbnew.F_SilkS)
            self.draw.SetLineThickness(line_width_minor_log)
            for current_line in minor_log_intervals:
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

        if acr_spl_show:
            self.draw.SetLayer(pcbnew.F_SilkS)
            self.draw.SetLineThickness(poly_line_width)
            poly_points_array = calc_splitted_poly(start_inner_radius=acr_spl_start_inner_radius,  # noqa
                                                   end_inner_radius=acr_spl_stop_inner_radius,  # noqa
                                                   start_outer_radius=acr_spl_start_outer_radius,  # noqa
                                                   end_outer_radius=acr_spl_stop_outer_radius,  # noqa
                                                   start_angle_deg=acr_spl_start_angle_deg,  # noqa
                                                   end_angle_deg=acr_spl_stop_angle_deg,  # noqa
                                                   segment_counts=acr_spl_num_Major_Ticks,  # noqa
                                                   face_counts=acr_spl_face_counts,  # noqa
                                                   distance=acr_spl_distance)

            for poly_points in poly_points_array:
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
                polygon_umriss.SetWidth(int(acr_spl_line_width))
                if acr_spl_filled:
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
