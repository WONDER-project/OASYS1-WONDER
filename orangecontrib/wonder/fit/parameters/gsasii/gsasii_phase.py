from orangecontrib.wonder.util.fit_utilities import Symmetry

from orangecontrib.wonder.fit.parameters.measured_data.phase import Phase

class GSASIIPhase(Phase):

    cif_file = None

    @classmethod
    def get_parameters_prefix(cls):
        return "gsasii_phase"

    def __init__(self, a, b, c, alpha, beta, gamma, symmetry=Symmetry.SIMPLE_CUBIC, cif_file=None, gsas_reflections_list=None, intensity_scale_factor=None):
        super(GSASIIPhase, self).__init__(a, b, c, alpha, beta, gamma, symmetry=symmetry, use_structure=True, formula=None, intensity_scale_factor=intensity_scale_factor)

        self.cif_file = cif_file
        self.gsas_reflections_list = gsas_reflections_list


