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

from orangecontrib.wonder.fit.parameters.fit_parameter import ParametersList

class Caglioti(ParametersList):
    U = None
    V = None
    W = None
    a = None
    b = None
    c = None

    @classmethod
    def get_parameters_prefix(cls):
        return "caglioti_"

    def __init__(self, U, V, W, a, b, c):
        super(Caglioti, self).__init__()

        self.U = U
        self.V = V
        self.W = W
        self.a = a
        self.b = b
        self.c = c

class Lab6TanCorrection(ParametersList):
    ax = None
    bx = None
    cx = None
    dx = None
    ex = None

    @classmethod
    def get_parameters_prefix(cls):
        return "lab6_tancorrection_"

    def __init__(self, ax, bx, cx, dx, ex):
        super(Lab6TanCorrection, self).__init__()

        self.ax = ax
        self.bx = bx
        self.cx = cx
        self.dx = dx
        self.ex = ex

class ZeroError(ParametersList):
    shift = None

    @classmethod
    def get_parameters_prefix(cls):
        return "zero_error_"

    def __init__(self, shift):
        super(ZeroError, self).__init__()

        self.shift = shift

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

class Beampath:
    PRIMARY = 0
    SECONDARY = 1

    @classmethod
    def tuple(cls):
        return ["Primary", "Secondary"]

class LorentzFormula:
    S_Shkl = 0
    Shkl_Shkl = 1

    @classmethod
    def tuple(cls):
        return ["1/[s\u22c5s(hkl)]", "1/s(hkl)\u00b2"]

class PolarizationParameters(ParametersList):
    use_lorentz_factor = False
    lorentz_formula = LorentzFormula.Shkl_Shkl
    use_polarization_factor = False
    beampath = Beampath.PRIMARY
    degree_of_polarization = 0.5
    twotheta_mono = None

    def __init__(self,
                 use_lorentz_factor = False,
                 lorentz_formula = LorentzFormula.Shkl_Shkl,
                 use_polarization_factor=False,
                 beampath = Beampath.PRIMARY,
                 degree_of_polarization=0.0,
                 twotheta_mono=None):
        self.use_lorentz_factor = use_lorentz_factor
        self.lorentz_formula = lorentz_formula
        self.use_polarization_factor = use_polarization_factor
        self.beampath = beampath
        self.degree_of_polarization = degree_of_polarization
        self.twotheta_mono = twotheta_mono

        if degree_of_polarization < 0: self.degree_of_polarization = 0.0
        elif degree_of_polarization> 1: self.degree_of_polarization = 1.0

    @classmethod
    def get_parameters_prefix(cls):
        return "lp_"


class InstrumentalParameters(ParametersList):
    def __init__(self,
                 instrumental_profile_parameters = {},
                 shift_parameters = {}):
        self.instrumental_profile_parameters = instrumental_profile_parameters
        self.shift_parameters = shift_parameters

    # INSTRUMENTAL -------------------------------

    def get_instrumental_profile_parameters(self, key):
        return ParametersList.get_dict_parameters(self.instrumental_profile_parameters, key)

    def get_instrumental_profile_parameters_item(self, key, diffraction_pattern_index):
        return ParametersList.get_dict_parameters_item(self.instrumental_profile_parameters, key, diffraction_pattern_index)

    def set_instrumental_profile_parameters(self, instrumental_profile_parameters):
        if self.instrumental_profile_parameters is None: self.instrumental_profile_parameters = {}
        ParametersList.set_dict_parameters(self.instrumental_profile_parameters, instrumental_profile_parameters)

    # SHIFT -------------------------------

    def get_shift_parameters(self, key):
        return ParametersList.get_dict_parameters(self.shift_parameters, key)

    def get_shift_parameters_item(self, key, diffraction_pattern_index):
        return ParametersList.get_dict_parameters_item(self.shift_parameters, key, diffraction_pattern_index)

    def set_shift_parameters(self, shift_parameters):
        if self.shift_parameters is None: self.shift_parameters = {}
        ParametersList.set_dict_parameters(self.shift_parameters, shift_parameters)

