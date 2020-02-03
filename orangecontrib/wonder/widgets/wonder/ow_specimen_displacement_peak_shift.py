import sys, copy

from PyQt5.QtWidgets import QApplication

from orangewidget.settings import Setting
from orangewidget import gui as orangegui

from orangecontrib.wonder.widgets.gui.ow_generic_parameter_widget import OWGenericWidget, OWGenericParameterWidget, ParameterBox
from orangecontrib.wonder.util.gui_utility import gui
from orangecontrib.wonder.util import congruence
from orangecontrib.wonder.fit.parameters.fit_global_parameters import FitGlobalParameters
from orangecontrib.wonder.fit.parameters.instrument.instrumental_parameters import SpecimenDisplacement


class OWSpecimenDisplacementPeakShift(OWGenericParameterWidget):

    name = "Specimen Displacement Peak Shift"
    description = "Specimen Displacement Peak Shift"
    icon = "icons/specimen_displacement_peak_shift.png"
    priority = 15

    want_main_area = False

    goniometer_radius = Setting([1.0])

    displacement = Setting([0.0])
    displacement_fixed = Setting([0])
    displacement_has_min = Setting([0])
    displacement_min = Setting([0.0])
    displacement_has_max = Setting([0])
    displacement_max = Setting([0.0])
    displacement_function = Setting([0])
    displacement_function_value = Setting([""])

    inputs = [("Fit Global Parameters", FitGlobalParameters, 'set_data')]
    outputs = [("Fit Global Parameters", FitGlobalParameters)]

    def __init__(self):
        super().__init__()

    def get_parameter_name(self):
        return "Specimen Displacement"

    def get_current_dimension(self):
        return len(self.displacement)

    def get_parameter_box_instance(self, parameter_tab, index):
        return SpecimenDisplacementPeakShiftBox(widget=self,
                                         parent=parameter_tab,
                                         index=index,
                                         goniometer_radius=self.goniometer_radius[index],
                                         displacement=self.displacement[index],
                                         displacement_fixed=self.displacement_fixed[index],
                                         displacement_has_min=self.displacement_has_min[index],
                                         displacement_min=self.displacement_min[index],
                                         displacement_has_max=self.displacement_has_max[index],
                                         displacement_max=self.displacement_max[index],
                                         displacement_function=self.displacement_function[index],
                                         displacement_function_value=self.displacement_function_value[index])

    def get_empty_parameter_box_instance(self, parameter_tab, index):
        return SpecimenDisplacementPeakShiftBox(widget=self, parent=parameter_tab, index=index)

    def set_parameter(self):
        self.fit_global_parameters.set_shift_parameters([self.get_parameter_box(index).get_peak_shift() for index in range(self.get_current_dimension())])

    def get_parameter_array(self):
        return self.fit_global_parameters.get_shift_parameters(SpecimenDisplacement.__name__)

    def get_parameter_item(self, diffraction_pattern_index):
        return self.fit_global_parameters.get_shift_parameters_item(SpecimenDisplacement.__name__, diffraction_pattern_index)

    def dumpSettings(self):
        self.dump_goniometer_radius()
        self.dump_displacement()

    def dump_goniometer_radius(self):
        bkp_goniometer_radius = copy.deepcopy(self.goniometer_radius)

        try:
            self.goniometer_radius = []

            for parameter_box in self.get_parameter_box_array():
                self.goniometer_radius.append(parameter_box.goniometer_radius)
        except Exception as e:
            self.goniometer_radius = copy.deepcopy(bkp_goniometer_radius)

            if self.IS_DEVELOP: raise  e

    def dump_displacement(self):
        bkp_displacement = copy.deepcopy(self.displacement)
        bkp_displacement_fixed = copy.deepcopy(self.displacement_fixed)
        bkp_displacement_has_min = copy.deepcopy(self.displacement_has_min)
        bkp_displacement_min = copy.deepcopy(self.displacement_min)
        bkp_displacement_has_max = copy.deepcopy(self.displacement_has_max)
        bkp_displacement_max = copy.deepcopy(self.displacement_max)
        bkp_displacement_function = copy.deepcopy(self.displacement_function)
        bkp_displacement_function_value = copy.deepcopy(self.displacement_function_value)

        try:
            self.displacement = []
            self.displacement_fixed = []
            self.displacement_has_min = []
            self.displacement_min = []
            self.displacement_has_max = []
            self.displacement_max = []
            self.displacement_function = []
            self.displacement_function_value = []

            for parameter_box in self.get_parameter_box_array():
                self.displacement.append(parameter_box.displacement)
                self.displacement_fixed.append(parameter_box.displacement_fixed)
                self.displacement_has_min.append(parameter_box.displacement_has_min)
                self.displacement_min.append(parameter_box.displacement_min)
                self.displacement_has_max.append(parameter_box.displacement_has_max)
                self.displacement_max.append(parameter_box.displacement_max)
                self.displacement_function.append(parameter_box.displacement_function)
                self.displacement_function_value.append(parameter_box.displacement_function_value)
        except Exception as e:
            self.displacement = copy.deepcopy(bkp_displacement)
            self.displacement_fixed = copy.deepcopy(bkp_displacement_fixed)
            self.displacement_has_min = copy.deepcopy(bkp_displacement_has_min)
            self.displacement_min = copy.deepcopy(bkp_displacement_min)
            self.displacement_has_max = copy.deepcopy(bkp_displacement_has_max)
            self.displacement_max = copy.deepcopy(bkp_displacement_max)
            self.displacement_function = copy.deepcopy(bkp_displacement_function)
            self.displacement_function_value = copy.deepcopy(bkp_displacement_function_value)

            if self.IS_DEVELOP: raise e

class SpecimenDisplacementPeakShiftBox(ParameterBox):
    def __init__(self,
                 widget=None,
                 parent=None,
                 index=0,
                 goniometer_radius = 1.0,
                 displacement=0.0,
                 displacement_fixed=0,
                 displacement_has_min=0,
                 displacement_min=0.0,
                 displacement_has_max=0,
                 displacement_max=0.0,
                 displacement_function=0,
                 displacement_function_value=""):
        super(SpecimenDisplacementPeakShiftBox, self).__init__(widget=widget,
                                                               parent=parent,
                                                               index=index,
                                                               goniometer_radius=goniometer_radius,
                                                               displacement = displacement,
                                                               displacement_fixed = displacement_fixed,
                                                               displacement_has_min = displacement_has_min,
                                                               displacement_min = displacement_min,
                                                               displacement_has_max = displacement_has_max,
                                                               displacement_max = displacement_max,
                                                               displacement_function = displacement_function,
                                                               displacement_function_value = displacement_function_value)

    def init_fields(self, **kwargs):
        self.goniometer_radius           = kwargs["goniometer_radius"]
        self.displacement                = kwargs["displacement"]
        self.displacement_fixed          = kwargs["displacement_fixed"]
        self.displacement_has_min        = kwargs["displacement_has_min"]
        self.displacement_min            = kwargs["displacement_min"]
        self.displacement_has_max        = kwargs["displacement_has_max"]
        self.displacement_max            = kwargs["displacement_max"]
        self.displacement_function       = kwargs["displacement_function"]
        self.displacement_function_value = kwargs["displacement_function_value"]

    def init_gui(self, container):
        gui.lineEdit(container, self, "goniometer_radius", "Goniometer Radius [m]", labelWidth=300, valueType=float, callback=self.widget.dump_goniometer_radius)
        orangegui.separator(container)
        OWGenericWidget.create_box_in_widget(self, container, "displacement", add_callback=True)

    def callback_displacement(self):
        if not self.is_on_init: self.widget.dump_displacement()

    def get_basic_parameter_prefix(self):
        return SpecimenDisplacement.get_parameters_prefix()

    def set_data(self, shift_parameters):
        self.goniometer_radius = shift_parameters.goniometer_radius

        displacement = shift_parameters.displacement.duplicate()
        displacement.rescale(1e6)  # to um

        OWGenericWidget.populate_fields_in_widget(self, "displacement", displacement, value_only=True)

    def get_peak_shift(self):
        congruence.checkStrictlyPositiveNumber(self.goniometer_radius, "Goniometer Radius")

        displacement = OWGenericWidget.populate_parameter_in_widget(self, "displacement", self.get_parameters_prefix())
        displacement.rescale(1e-6)  # to m

        return SpecimenDisplacement(goniometer_radius=self.goniometer_radius, displacement=displacement)


if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = OWSpecimenDisplacementPeakShift()
    ow.show()
    a.exec_()
    ow.saveSettings()
