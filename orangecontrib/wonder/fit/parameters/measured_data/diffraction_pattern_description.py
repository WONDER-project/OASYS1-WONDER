import numpy

import orangecontrib.wonder.util.congruence as congruence
from orangecontrib.wonder.util.fit_utilities import Utilities

from orangecontrib.wonder.fit.parameters.fit_parameter import ParametersList, FitParameter, Boundary, PARAM_HWMAX, PARAM_HWMIN
from orangecontrib.wonder.fit.parameters.measured_data.reflection import Reflection

class DiffractionPatternDescription(ParametersList):

    def __init__(self, phases=[]):
        self.phases = phases
        self.reflections_of_phases = [[]]*len(phases)

    def add_reflection(self, phase_index, reflection):
        self.reflections_of_phases[phase_index].append(reflection)

        self.update_reflection(phase_index, -1)

    def set_reflection(self, phase_index, reflection_index, reflection):
        self.reflections_of_phases[phase_index][reflection_index] = reflection

        self.update_reflection(phase_index, reflection_index)

    def get_reflections_count(self, phase_index):
        return len(self.reflections_of_phases[phase_index])

    def get_reflection(self, phase_index, reflection_index):
        return self.reflections_of_phases[phase_index][reflection_index]

    def get_reflections(self, phase_index):
        return numpy.array(self.reflections_of_phases[phase_index])

    def update_reflection(self, phase_index, reflection_index):
        reflection = self.reflections_of_phases[phase_index][reflection_index]
        reflection.d_spacing = self.get_d_spacing(phase_index, reflection.h, reflection.k, reflection.l)

    def update_reflections(self, phase_index):
        for reflection_index in range(self.get_reflections_count(phase_index)): self.update_reflection(phase_index, reflection_index)

    def existing_reflection(self, phase_index, h, k, l):
        for reflection in self.reflections_of_phases[phase_index]:
            if reflection.h == h and reflection.k == k and reflection.l == l:
                return reflection

        return None

    def get_s_list(self, phase_index):
        return numpy.array([self.get_s(phase_index, reflection.h, reflection.k, reflection.l) for reflection in self.reflections_of_phases[phase_index]])

    def get_hkl_list(self, phase_index):
        return numpy.array([str(reflection.h) + str(reflection.k) + str(reflection.l) for reflection in self.reflections_of_phases[phase_index]])

    def get_s(self, phase_index, h, k, l):
        return self.phases[phase_index].get_s(h, k, l)

    def get_d_spacing(self, phase_index, h, k, l):
        return self.phases[phase_index].get_d_spacing(h, k, l)

    def parse_reflections(self, text, phase_index=1, progressive=""):
        congruence.checkEmptyString(text, "Reflections")

        lines = text.splitlines()

        reflections = []

        phase_index_str = str(phase_index) + "_"

        for i in range(len(lines)):
            congruence.checkEmptyString(lines[i], "Reflections: line " + str(i+1))

            if not lines[i].strip().startswith("#"):
                data = lines[i].strip().split(",")

                if len(data) < 4: raise ValueError("Reflections, malformed line: " + str(i+1))

                h = int(data[0].strip())
                k = int(data[1].strip())
                l = int(data[2].strip())

                if ":=" in data[3].strip():
                    intensity_data = data[3].strip().split(":=")

                    if len(intensity_data) == 2:
                        intensity_name = intensity_data[0].strip()
                        function_value = intensity_data[1].strip()
                    else:
                        intensity_name = None
                        function_value = data[3].strip()

                    if intensity_name is None:
                        intensity_name = Reflection.get_parameters_prefix() + phase_index_str + progressive + "I" + str(h) + str(k) + str(l)
                    elif not intensity_name.startswith(Reflection.get_parameters_prefix()):
                        intensity_name = Reflection.get_parameters_prefix() + phase_index_str + progressive + intensity_name

                    reflection = Reflection(h, k, l, intensity=FitParameter(parameter_name=intensity_name,
                                                                            function=True,
                                                                            function_value=function_value))
                else:
                    intensity_data = data[3].strip().split()

                    if len(intensity_data) == 2:
                        intensity_name = intensity_data[0].strip()
                        intensity_value = float(intensity_data[1])
                    else:
                        intensity_name = None
                        intensity_value = float(data[3])

                    boundary = None
                    fixed = False

                    if len(data) > 4:
                        min_value = PARAM_HWMIN
                        max_value = PARAM_HWMAX

                        for j in range(4, len(data)):
                            boundary_data = data[j].strip().split()

                            if boundary_data[0] == "min": min_value = float(boundary_data[1].strip())
                            elif boundary_data[0] == "max": max_value = float(boundary_data[1].strip())
                            elif boundary_data[0] == "fixed": fixed = True

                        if not fixed:
                            if min_value != PARAM_HWMIN or max_value != PARAM_HWMAX:
                                boundary = Boundary(min_value=min_value, max_value=max_value)
                            else:
                                boundary = Boundary()

                    if intensity_name is None:
                        intensity_name = Reflection.get_parameters_prefix() + phase_index_str + progressive + "I" + str(h) + str(k) + str(l)
                    elif not intensity_name.startswith(Reflection.get_parameters_prefix()):
                        intensity_name = Reflection.get_parameters_prefix() + phase_index_str + progressive + intensity_name


                    reflection = Reflection(h, k, l, intensity=FitParameter(parameter_name=intensity_name,
                                                                            value=intensity_value,
                                                                            fixed=fixed,
                                                                            boundary=boundary))
                reflections.append(reflection)

        self.reflections_of_phases[phase_index] = reflections
        self.update_reflections(phase_index)

    def get_congruence_check(self, wavelength, min_value, max_value, limit_is_s=True):
        excluded_reflections = [[]]*len(self.reflections_of_phases)

        if wavelength <= 0: raise ValueError("Wavelenght should be a positive number")
        if max_value <= 0: raise ValueError("Max Value should be a positive number")

        if not limit_is_s:
            s_min = Utilities.s(numpy.radians(min_value/2), wavelength) # 2THETA MIN VALUE!
            s_max = Utilities.s(numpy.radians(max_value/2), wavelength) # 2THETA MAX VALUE!
        else:
            s_min = min_value
            s_max = max_value

        for phase_index in range(len(self.reflections_of_phases)):
            excluded_reflections_of_phase = []

            for reflection in self.reflections_of_phases[phase_index]:
                s_hkl = Utilities.s_hkl(self.a.value, reflection.h, reflection.k, reflection.l)

                if s_hkl < s_min or s_hkl > s_max: excluded_reflections_of_phase.append(reflection)

            if len(excluded_reflections_of_phase) == 0: excluded_reflections_of_phase = None

            excluded_reflections[phase_index] = excluded_reflections_of_phase

        return excluded_reflections




