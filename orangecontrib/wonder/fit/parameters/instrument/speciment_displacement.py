from wonder.fit.parameters.fit_parameter import ParametersList


class SpecimenDisplacement(ParametersList):
    goniometer_radius = 1.0
    displacement = None

    @classmethod
    def get_parameters_prefix(cls):
        return "sd_"

    def __init__(self, goniometer_radius=1.0, displacement=None):
        super(SpecimenDisplacement, self).__init__()

        self.goniometer_radius = goniometer_radius
        self.displacement = displacement
