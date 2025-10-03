import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        root_comp = design.rootComponent
        spheres = root_comp.features.sphereFeatures

        # Input dialog for all parameters
        input_values = ui.inputBox(
            'Enter radius, x spacing, y spacing, z spacing, x count, y count, z count (comma-separated):',
            'Sphere Array Parameters',
            '1.0, 3.0, 3.0, 3.0, 3, 3, 3'
        )

        # Parse input
        radius_str, x_str, y_str, z_str, xc_str, yc_str, zc_str = [s.strip() for s in input_values.split(',')]
        radius = float(radius_str)
        x_spacing = float(x_str)
        y_spacing = float(y_str)
        z_spacing = float(z_str)
        x_count = int(xc_str)
        y_count = int(yc_str)
        z_count = int(zc_str)

        for i in range(x_count):
            for j in range(y_count):
                for k in range(z_count):
                    center = adsk.core.Point3D.create(
                        i * x_spacing,
                        j * y_spacing,
                        k * z_spacing
                    )
                    input = spheres.createInput(center, adsk.core.ValueInput.createByReal(radius))
                    spheres.add(input)

        ui.messageBox('Sphere array created.')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))