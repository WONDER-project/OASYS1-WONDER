from orangecontrib.wonder.util.fit_utilities import Symmetry
from orangecontrib.wonder.fit.parameters.fit_parameter import FitParameter

from orangecontrib.wonder.fit.parameters.measured_data.phase import Phase
from orangecontrib.wonder.fit.parameters.gsasii.gsasii_functions import gsasii_load_reflections, gsasii_intensity_factor

class GSASIIPhase(Phase):

    cif_file = None

    @classmethod
    def get_parameters_prefix(cls):
        return "gsasii_phase"

    def __init__(self, a, b, c, alpha, beta, gamma, symmetry=Symmetry.SIMPLE_CUBIC, cif_file=None, intensity_scale_factor=None):
        super(GSASIIPhase, self).__init__(a, b, c, alpha, beta, gamma, symmetry=symmetry, use_structure=True, formula=None, intensity_scale_factor=intensity_scale_factor)

        self.cif_file = cif_file
        self.gsasii_reflections_list = None

    @classmethod
    def init_cube(cls, a0, symmetry=Symmetry.FCC, cif_file=None, intensity_scale_factor=None, progressive = ""):
        if not cls.is_cube(symmetry): raise ValueError("Symmetry doesn't belong to a cubic crystal cell")

        if a0.fixed:
            a = FitParameter(parameter_name=Phase.get_parameters_prefix() + progressive + "a", value=a0.value, fixed=a0.fixed, boundary=a0.boundary)
            b = FitParameter(parameter_name=Phase.get_parameters_prefix() + progressive + "b", value=a0.value, fixed=a0.fixed, boundary=a0.boundary)
            c = FitParameter(parameter_name=Phase.get_parameters_prefix() + progressive + "c", value=a0.value, fixed=a0.fixed, boundary=a0.boundary)
        else:
            a = a0
            b = FitParameter(parameter_name=Phase.get_parameters_prefix() + progressive + "b", function=True, function_value=Phase.get_parameters_prefix() + progressive + "a")
            c = FitParameter(parameter_name=Phase.get_parameters_prefix() + progressive + "c", function=True, function_value=Phase.get_parameters_prefix() + progressive + "a" )

        alpha = FitParameter(parameter_name=Phase.get_parameters_prefix() + progressive + "alpha", value=90, fixed=True)
        beta  = FitParameter(parameter_name=Phase.get_parameters_prefix() + progressive + "beta",  value=90, fixed=True)
        gamma = FitParameter(parameter_name=Phase.get_parameters_prefix() + progressive + "gamma", value=90, fixed=True)

        return GSASIIPhase(a,
                           b,
                           c,
                           alpha,
                           beta,
                           gamma,
                           symmetry=symmetry,
                           cif_file=cif_file,
                           intensity_scale_factor=intensity_scale_factor)

    def set_gsasii_reflections_list(self, gsasii_reflections_list):
        self.gsasii_reflections_list = gsasii_reflections_list

    def get_gsasii_reflections_list(self):
        return self.gsasii_reflections_list
