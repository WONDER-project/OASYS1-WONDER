from orangecontrib.wonder.fit.parameters.fit_parameter import ParametersList
from orangecontrib.wonder.fit.parameters.measured_data.line_profile import LineProfile

class MeasuredDataset(ParametersList):

    diffraction_patterns = None

    incident_radiations = None
    phases = None
    line_profiles = None

    initialized = False

    def __init__(self,
                 diffraction_patterns = None,
                 incident_radiations = None,
                 phases = None,
                 line_profiles = None):
        self.phases = phases
        self.diffraction_patterns = diffraction_patterns
        self.incident_radiations = incident_radiations
        self.line_profiles = line_profiles
        self.initialized = False

    @classmethod
    def initialize_with_diffraction_pattern(cls, diffraction_patterns=[]):
        if diffraction_patterns is None: raise ValueError("Diffraction Patterns is None")
        if not isinstance(diffraction_patterns, list): raise ValueError("Diffraction Patterns is not a list")
        if len(diffraction_patterns) < 1: raise ValueError("Diffraction Patterns list is empty")

        dataset = MeasuredDataset(diffraction_patterns=diffraction_patterns)

        diffraction_patterns_number = dataset.get_diffraction_patterns_number()

        dataset.incident_radiations = [None] * diffraction_patterns_number
        dataset.line_profiles = [None] * diffraction_patterns_number
        dataset.initialized = True

        return dataset

    def set_phases(self, phases=None):
        if phases is None: raise ValueError("Phases is None")
        if not isinstance(phases, list): raise ValueError("Phases is not a list")
        if len(phases) < 1: raise ValueError("Phases list is empty")

        self.phases=phases

        diffraction_patterns_number = self.get_diffraction_patterns_number()

        if self.initialized and diffraction_patterns_number > 0:
            for diffraction_pattern_index in range(diffraction_patterns_number):
                self.line_profiles[diffraction_pattern_index] = LineProfile(self.phases)

    def get_diffraction_patterns_number(self):
        return 0 if self.diffraction_patterns is None else len(self.diffraction_patterns)

    def get_phases_number(self):
        return 0 if self.phases is None else len(self.phases)

    def duplicate(self):
        if self.diffraction_patterns is None: diffraction_patterns = None
        else:
            dimension = len(self.diffraction_patterns)
            diffraction_patterns = [None]*dimension
            for index in range(dimension):
                diffraction_patterns[index] = self.diffraction_patterns[index].duplicate()

        if self.incident_radiations is None: incident_radiations = None
        else:
            dimension = len(self.incident_radiations)
            incident_radiations = [None]*dimension
            for index in range(dimension):
                incident_radiations[index] = self.incident_radiations[index].duplicate()

        if self.phases is None: phases = None
        else:
            dimension = len(self.phases)
            phases = [None]*dimension
            for index in range(dimension):
                phases[index] = self.phases[index].duplicate()

        if self.line_profiles is None: line_profiles = None
        else:
            dimension = len(self.line_profiles)
            line_profiles = [None]*dimension
            for index in range(dimension):
                line_profiles[index] = self.line_profiles[index].duplicate()

        dataset = MeasuredDataset(diffraction_patterns=diffraction_patterns,
                                  incident_radiations=incident_radiations,
                                  phases=phases,
                                  line_profiles=line_profiles)

        dataset.initialized = self.initialized

        return dataset

