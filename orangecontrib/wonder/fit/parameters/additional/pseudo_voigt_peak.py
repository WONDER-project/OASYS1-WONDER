#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #########################################################################
# Copyright (c) 2020, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2020. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# #########################################################################

import numpy

from orangecontrib.wonder.fit.parameters.fit_parameter import ParametersList, FitParameter, Boundary, PARAM_HWMAX, PARAM_HWMIN
from oasys.widgets import congruence


class SpuriousPeaks(ParametersList):
    def __init__(self, number_of_peaks=1):
        self.pseudo_voigt_peaks = [] * number_of_peaks

    def parse_peaks(self, text, diffraction_pattern_index=0):
        try:
            congruence.checkEmptyString(text, "Reflections")
            empty = False
        except:
            empty = True

        pseudo_voigt_peaks = []

        if not empty:
            lines = text.splitlines()

            for line_index in range(len(lines)):
                pseudo_voigt_peak = PseudoVoigtPeak.parse_peak(line=lines[line_index],
                                                               line_index=line_index,
                                                               diffraction_pattern_index=diffraction_pattern_index)

                if not pseudo_voigt_peak is None: pseudo_voigt_peaks.append(pseudo_voigt_peak)

        self.pseudo_voigt_peaks = pseudo_voigt_peaks

    def get_pseudo_voigt_peaks_number(self):
        return len(self.pseudo_voigt_peaks)

    def get_pseudo_voigt_peak(self, peak_index):
        return self.pseudo_voigt_peaks[peak_index]

    def get_pseudo_voigt_peaks(self):
        return numpy.array(self.pseudo_voigt_peaks)

class PseudoVoigtPeak():
    @classmethod
    def get_parameters_prefix(cls):
        return "pv_"

    def __init__(self, twotheta_0=None, eta=None, fwhm=None, intensity=None):
        self.twotheta_0 = twotheta_0
        self.eta = eta
        self.fwhm = fwhm
        self.intensity = intensity

    def __str__(self):
        return ("--" if self.twotheta_0 is None else str(self.twotheta_0)) + ", " + \
               ("--" if self.eta is None else str(self.eta)) + ", " + \
               ("--" if self.fwhm is None else str(self.fwhm)) + ", " + \
               ("--" if self.intensity is None else str(self.intensity))

    def to_row(self):
        if not self.twotheta_0 is None and not self.eta is None and not self.fwhm is None and not self.intensity is None:
            return self.twotheta_0.to_parameter_on_row() + ", " + \
                   self.eta.to_parameter_on_row() + ", " + \
                   self.fwhm.to_parameter_on_row() + ", " + \
                   self.intensity.to_parameter_on_row()
        else:
            return ""

    def get_pseudo_voigt_peak(self, twotheta):
        tths = (2 * (twotheta - self.twotheta_0.value) / self.fwhm.value) ** 2
        pis = numpy.pi * self.fwhm.value / 2

        lorentzian = 1 / (pis * (1 + tths))
        gaussian = numpy.sqrt(numpy.pi * numpy.log(2)) * numpy.exp(-numpy.log(2) * tths) / pis

        return self.intensity.value * (((1 - self.eta.value) * gaussian) + (self.eta.value * lorentzian))

    @classmethod
    def parse_peak(cls, line, line_index=0, diffraction_pattern_index=0):
        try:
            congruence.checkEmptyString(line, "Pseudo-Voigt Peak")
        except:
            return None

        if line.strip().startswith("#"):
            return None
        else:
            parameter_prefix = PseudoVoigtPeak.get_parameters_prefix() + str(diffraction_pattern_index + 1) + "_" + str(line_index+1) + "_"

            line_id = "(d.p. " + str(diffraction_pattern_index+1) +", line " + str(line_index+1) + ")"

            psuedo_voigt_peak = PseudoVoigtPeak()

            data = line.strip().split(",")

            if len(data) < 4: raise ValueError("Pseudo-Voigt Peak, malformed line: " + str(line_index+1))

            try:
                twotheta_0 = FitParameter.parse_parameter_on_row(data[0], parameter_prefix, "twotheta0")
                eta        = FitParameter.parse_parameter_on_row(data[1], parameter_prefix, "eta")
                fwhm       = FitParameter.parse_parameter_on_row(data[2], parameter_prefix, "fwhm")
                intensity  = FitParameter.parse_parameter_on_row(data[3], parameter_prefix, "intensity")
            except:
                raise "Row " + line_id + " is malformed"

            if not twotheta_0.function:
                congruence.checkStrictlyPositiveAngle(twotheta_0.value, "2\u03b80 " + line_id)
                if twotheta_0.boundary.is_free(): twotheta_0.boundary = Boundary(min_value=0.0)

            if not eta.function:
                if not 0.0 < eta.value < 1.0: raise ValueError("\u03b7 " + line_id + " must be between 0 and 1")
                if eta.boundary.is_free(): eta.boundary = Boundary(min_value=0.0, max_value=1.0)

            if not fwhm.function:
                congruence.checkStrictlyPositiveNumber(fwhm.value, "fwhm " + line_id)
                if fwhm.boundary.is_free(): fwhm.boundary = Boundary(min_value=0.0)

            if not intensity.function:
                congruence.checkStrictlyPositiveNumber(intensity.value, "intensity " + line_id)
                if intensity.boundary.is_free():  intensity.boundary  = Boundary(min_value=0.0)

            psuedo_voigt_peak.twotheta_0 = twotheta_0
            psuedo_voigt_peak.eta        = eta
            psuedo_voigt_peak.fwhm       = fwhm
            psuedo_voigt_peak.intensity  = intensity

            return psuedo_voigt_peak

if __name__ == "__main__":

    peak = PseudoVoigtPeak.parse_peak("10 fixed, eta_mio 0.2 min 0.0 max 1.0, := ciccio, 20")
    print (peak)
