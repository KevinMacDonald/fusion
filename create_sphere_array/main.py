# velvet glyph matrix

import adsk.core, adsk.fusion, adsk.cam, traceback

def create_sphere(root_comp, radius):
    # Create sketch on XZ plane
    xz_plane = root_comp.xZConstructionPlane
    sketch = root_comp.sketches.add(xz_plane)
    sketch.name = "SphereProfile"

    # Semicircle arc
    arc = sketch.sketchCurves.sketchArcs.addByThreePoints(
        adsk.core.Point3D.create(-radius, 0, 0),
        adsk.core.Point3D.create(0, radius, 0),
        adsk.core.Point3D.create(radius, 0, 0)
    )

    # Close profile with line
    sketch.sketchCurves.sketchLines.addByTwoPoints(
        arc.endSketchPoint,
        arc.startSketchPoint
    )

    # Axis for revolve
    axis_line = sketch.sketchCurves.sketchLines.addByTwoPoints(
        adsk.core.Point3D.create(-radius, 0, 0),
        adsk.core.Point3D.create(radius, 0, 0)
    )

    # Create profile and revolve
    prof = sketch.profiles.item(0)
    revolves = root_comp.features.revolveFeatures
    rev_input = revolves.createInput(prof, axis_line, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    rev_input.setAngleExtent(False, adsk.core.ValueInput.createByReal(360))
    sphere = revolves.add(rev_input)

    return sphere.bodies.item(0)

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        root_comp = design.rootComponent

        # Parameters
        radius = 10.0  # interpreted as 10 cm under cm units
        clearance = 2.0
        spacing = 2 * radius + clearance  # center-to-center spacing

        x_count = 3
        y_count = 3
        z_count = 3

        # Create sphere
        sphere_body = create_sphere(root_comp, radius)

        # First pattern: X and Y directions
        x_axis = root_comp.xConstructionAxis
        y_axis = root_comp.yConstructionAxis

        pattern_feats = root_comp.features.rectangularPatternFeatures
        input_entities = adsk.core.ObjectCollection.create()
        input_entities.add(sphere_body)

        pattern_input_xy = pattern_feats.createInput(
            input_entities,
            x_axis,
            adsk.core.ValueInput.createByReal(x_count),
            adsk.core.ValueInput.createByReal(spacing),
            adsk.fusion.PatternDistanceType.SpacingPatternDistanceType
        )

        pattern_input_xy.setDirectionTwo(
            y_axis,
            adsk.core.ValueInput.createByReal(y_count),
            adsk.core.ValueInput.createByReal(spacing)
        )

        pattern_xy = pattern_feats.add(pattern_input_xy)

        # Second pattern: Z direction
        z_axis = root_comp.zConstructionAxis
        input_entities_z = adsk.core.ObjectCollection.create()
        for i in range(pattern_xy.bodies.count):
            input_entities_z.add(pattern_xy.bodies.item(i))

        pattern_input_z = pattern_feats.createInput(
            input_entities_z,
            z_axis,
            adsk.core.ValueInput.createByReal(z_count),
            adsk.core.ValueInput.createByReal(spacing),
            adsk.fusion.PatternDistanceType.SpacingPatternDistanceType
        )

        pattern_feats.add(pattern_input_z)

        ui.messageBox("3D sphere array created with nested patterns.")

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))