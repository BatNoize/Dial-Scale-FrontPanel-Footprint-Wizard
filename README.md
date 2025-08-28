# The Dial Scale Footprint Wizard

**The Dial Scale Footprint Wizard** is a tool that allows users to generate customized dial scale footprints for KiCad.

## Examples

![Example usage](docs/Example_2.png)


![Example usage](docs/Demo.gif)

## Usage
Users can input various parameters in the dialog to define the characteristics of the dial scale, such as hole configuration, tick marks, arc fill, center handle, and help circle for orientation. The wizard groups the parameters under different categories for easy navigation and customization.

Here is an overview of the parameters that can be defined in the dialog:
### Hole:
- ``Active``: Enable or disable the hole feature.
- ``Hole Radius``: Specify the radius of the hole.
- ``Pad Radius``: Set the radius of the pad around the hole.
- ``Plated``: Choose whether the hole should be plated or not.
### Tick Marks:
- ``Active Major``: Enable or disable major tick marks.
- ``Active Minor``: Enable or disable minor tick marks.
- ``Line Width Major``: Set the line width for major tick marks.
- ``Line Width Minor``: Set the line width for minor tick marks.
- ``Inner Radius Major``: Define the inner radius for major tick marks.
- ``Outer Radius Major``: Define the outer radius for major tick marks.
- ``Start Angle``: Specify the starting angle for the tick marks.
- ``Stop Angle``: Specify the stopping angle for the tick marks.
- ``Inner Radius Minor``: Define the inner radius for minor tick marks.
- ``Outer Radius Minor``: Define the outer radius for minor tick marks.
- ``Num Major Ticks``: Set the number of major tick marks.
- ``Num Minor Ticks``: Set the number of minor tick marks.
### Arc Fill:
- ``Active``: Enable or disable the arc fill feature.
- ``Filled``: Choose whether the arc should be filled or not.
- ``Inner Radius``: Specify the inner radius of the arc.
- ``Outer Radius``: Specify the outer radius of the arc.
- ``Start Radius Offset``: Specify the start radius offset.
- ``Start Angle``: Specify the starting angle for the arc.
- ``Stop Angle``: Specify the stopping angle for the arc.
- ``Polygon Vertices``: Set the number of vertices for the polygon.
- ``Line Width``: Set the line width for the arc fill.
### Center Handle:
- ``Active``: Enable or disable the center handle feature.
- ``Line Width``: Set the line width for the center handle.
- ``Inner Radius``: Define the inner radius for the center handle.
- ``Outer Radius``: Define the outer radius for the center handle.
- ``Angle``: Specify the angle for the center handle.
### Help:
- ``Active``: Enable or disable the help feature.
- ``Circle Radius``: Specify the radius of the help circle.
- ``Line Width``: Set the line width for the help features.

The BuildThisFootprint function generates the geometry of the footprint based on the defined parameters. It creates the dial scale with features such as radial lines, tick marks, arc fill, center handle, and help circle. The wizard provides a user-friendly interface for designing and customizing dial scale footprints for PCB layouts.