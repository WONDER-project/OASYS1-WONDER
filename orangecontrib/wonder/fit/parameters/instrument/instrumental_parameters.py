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

import copy
from orangecontrib.wonder.fit.parameters.fit_parameter import ParametersList


class InstrumentalParameters(ParametersList):
    def __init__(self,
                 incident_radiations = None,
                 instrumental_profile_parameters = {},
                 shift_parameters = {}):
        self.incident_radiations = incident_radiations
        self.instrumental_profile_parameters = instrumental_profile_parameters
        self.shift_parameters = shift_parameters

    def get_incident_radiations_item(self, diffraction_pattern_index):
        try:    return self.incident_radiations[0 if len(self.incident_radiations) == 1 else diffraction_pattern_index]
        except: return None

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

    def duplicate(self):
        incident_radiations = ParametersList.duplicate_attributes_list(self.incident_radiations)
        instrumental_profile_parameters = copy.deepcopy(self.instrumental_profile_parameters)
        shift_parameters = copy.deepcopy(self.shift_parameters)

        return InstrumentalParameters(incident_radiations, instrumental_profile_parameters, shift_parameters)
