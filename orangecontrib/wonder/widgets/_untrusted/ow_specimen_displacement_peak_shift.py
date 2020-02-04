import sys, copy

from PyQt5.QtWidgets import QMessageBox, QApplication

from orangewidget.settings import Setting
from orangewidget import gui as orangegui
from orangewidget.widget import OWAction

from orangecontrib.wonder.widgets.gui.ow_generic_widget import OWGenericWidget
from orangecontrib.wonder.util.gui_utility import gui, ConfirmDialog
from orangecontrib.wonder.util import congruence
from orangecontrib.wonder.fit.parameters.fit_global_parameters import FitGlobalParameters
from orangecontrib.wonder.fit.parameters.instrument.instrumental_parameters import SpecimenDisplacement


class OWSpecimenDisplacementPeakShift(OWGenericWidget):

    name = "Specimen Displacement Peak Shift"
    description = "Specimen Displacement Peak Shift"
    icon = "icons/specimen_displacement_peak_shift.png"
    priority = 15

    want_main_area = False

    use_single_parameter_set = Setting(0)

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
        super().__init__(show_automatic_box=True)

        main_box = gui.widgetBox(self.controlArea,
                                 "Specimen Displacement", orientation="vertical",
                                 width=self.CONTROL_AREA_WIDTH - 10, height=600)

        button_box = gui.widgetBox(main_box,
                                   "", orientation="horizontal",
                                   width=self.CONTROL_AREA_WIDTH - 25)

        gui.button(button_box, self, "Send Specimen Displacement", height=40, callback=self.send_peak_shift)

        orangegui.comboBox(main_box, self, "use_single_parameter_set", label="Use single set of Parameters", labelWidth=350, orientation="horizontal",
                           items=["No", "Yes"], callback=self.set_use_single_parameter_set, sendSelectedValue=False)

        orangegui.separator(main_box)

        self.peak_shift_tabs = gui.tabWidget(main_box)

        self.set_use_single_parameter_set(on_init=True)

        runaction = OWAction("Send Peak Shift", self)
        runaction.triggered.connect(self.send_peak_shift)
        self.addAction(runaction)

        orangegui.rubber(self.controlArea)

    def set_use_single_parameter_set(self, on_init=False, recycle=True):
        self.peak_shift_tabs.clear()
        self.peak_shift_box_array = []

        dimension = len(self.displacement) if self.fit_global_parameters is None else self.fit_global_parameters.measured_dataset.get_diffraction_patterns_number()

        for index in range(1 if self.use_single_parameter_set == 1 else dimension):
            peak_shift_tab = gui.createTabPage(self.peak_shift_tabs, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, index, self.use_single_parameter_set==1))

            if index < len(self.displacement) and recycle:  # keep the existing
                peak_shift_box = SpecimenDisplacementPeakShiftBox(widget=self,
                                                                  parent=peak_shift_tab,
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
            else:
                peak_shift_box = SpecimenDisplacementPeakShiftBox(widget=self, parent=peak_shift_tab, index=index)

            self.peak_shift_box_array.append(peak_shift_box)

            if not on_init: self.dumpSettings()

    def send_peak_shift(self):
        try:
            if not self.fit_global_parameters is None:
                self.dumpSettings()

                self.fit_global_parameters.set_shift_parameters([self.peak_shift_box_array[index].send_peak_shift() for index in range(len(self.displacement))])
                self.fit_global_parameters.regenerate_parameters()

                self.send("Fit Global Parameters", self.fit_global_parameters)

        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 str(e),
                                 QMessageBox.Ok)

            if self.IS_DEVELOP: raise e

    def __check_data_congruence(self, shift_parameters):
        if (len(shift_parameters) == 1 and self.use_single_parameter_set == 0) or (len(shift_parameters) > 1 and self.use_single_parameter_set == 1):
            raise ValueError("Previous Specimen Displacement parameters are incongruent with the current choice of using a single set")

    def set_data(self, data):
        if not data is None:
            try:
                self.fit_global_parameters = data.duplicate()

                diffraction_patterns = self.fit_global_parameters.measured_dataset.diffraction_patterns
                if diffraction_patterns is None: raise ValueError("No Diffraction Pattern in input data!")

                shift_parameters = self.fit_global_parameters.get_shift_parameters(SpecimenDisplacement.__name__)

                if self.use_single_parameter_set == 0:  # NO
                    if shift_parameters is None:
                        if len(diffraction_patterns) != len(self.peak_shift_box_array):
                            self.set_use_single_parameter_set(recycle=ConfirmDialog.confirmed(message="Number of Diffraction Patterns changed:\ndo you want to use the existing data where possible?\n\nIf yes, check for possible incongruences", title="Warning"))
                        else:
                            self.set_use_single_parameter_set(True)
                    else:
                        #self.__check_data_congruence(shift_parameters)

                        tabs_to_remove = len(self.displacement) - len(shift_parameters)

                        if tabs_to_remove > 0:
                            for index in range(tabs_to_remove):
                                self.peak_shift_tabs.removeTab(-1)
                                self.peak_shift_box_array.pop()

                        for diffraction_pattern_index in range(len(shift_parameters)):
                            shift_parameters_item = self.fit_global_parameters.get_shift_parameters_item(SpecimenDisplacement.__name__, diffraction_pattern_index)

                            if diffraction_pattern_index < len(self.displacement):
                                self.peak_shift_tabs.setTabText(diffraction_pattern_index,
                                                               OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, diffraction_pattern_index, False))

                                peak_shift_box = self.peak_shift_box_array[diffraction_pattern_index]
                            else:
                                peak_shift_box = SpecimenDisplacementPeakShiftBox(widget=self,
                                                                                  parent=gui.createTabPage(self.peak_shift_tabs, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, diffraction_pattern_index, False)),
                                                                                  index=diffraction_pattern_index)
                                self.peak_shift_box_array.append(peak_shift_box)

                            if not shift_parameters_item is None: peak_shift_box.set_data(shift_parameters_item)
                else:
                    if shift_parameters is None:
                        self.set_use_single_parameter_set(True)
                    else:
                        self.__check_data_congruence(shift_parameters)

                        shift_parameters_item = self.fit_global_parameters.get_shift_parameters_item(SpecimenDisplacement.__name__, 0)

                        self.peak_shift_tabs.setTabText(0, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, 0, True))
                        if not shift_parameters_item is None: self.peak_shift_box_array[0].set_data(shift_parameters_item)

                self.dumpSettings()

                if self.is_automatic_run:
                    self.send_peak_shift()

            except Exception as e:
                QMessageBox.critical(self, "Error",
                                     str(e),
                                     QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def dumpSettings(self):
        self.dump_goniometer_radius()
        self.dump_displacement()

    def dump_goniometer_radius(self):
        bkp_goniometer_radius = copy.deepcopy(self.goniometer_radius)

        try:
            self.goniometer_radius = []

            for index in range(len(self.peak_shift_box_array)):
                self.goniometer_radius.append(self.peak_shift_box_array[index].goniometer_radius)
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

            for index in range(len(self.peak_shift_box_array)):
                self.displacement.append(self.peak_shift_box_array[index].displacement)
                self.displacement_fixed.append(self.peak_shift_box_array[index].displacement_fixed)
                self.displacement_has_min.append(self.peak_shift_box_array[index].displacement_has_min)
                self.displacement_min.append(self.peak_shift_box_array[index].displacement_min)
                self.displacement_has_max.append(self.peak_shift_box_array[index].displacement_has_max)
                self.displacement_max.append(self.peak_shift_box_array[index].displacement_max)
                self.displacement_function.append(self.peak_shift_box_array[index].displacement_function)
                self.displacement_function_value.append(self.peak_shift_box_array[index].displacement_function_value)
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

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QDoubleValidator
from orangecontrib.wonder.util.gui_utility import InnerBox


class SpecimenDisplacementPeakShiftBox(InnerBox):
    widget = None
    is_on_init = True

    parameter_functions = {}

    index = 0

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
        super(SpecimenDisplacementPeakShiftBox, self).__init__()

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.setFixedWidth(widget.CONTROL_AREA_WIDTH - 35)
        self.setFixedHeight(500)

        self.widget = widget
        self.index = index

        self.goniometer_radius = goniometer_radius
        self.displacement = displacement
        self.displacement_fixed = displacement_fixed
        self.displacement_has_min = displacement_has_min
        self.displacement_min = displacement_min
        self.displacement_has_max = displacement_has_max
        self.displacement_max = displacement_max
        self.displacement_function = displacement_function
        self.displacement_function_value = displacement_function_value

        self.CONTROL_AREA_WIDTH = widget.CONTROL_AREA_WIDTH

        parent.layout().addWidget(self)
        container = self

        gui.lineEdit(container, self, "goniometer_radius", "Goniometer Radius [m]", labelWidth=300, valueType=float, validator=QDoubleValidator(), callback=widget.dump_goniometer_radius)
        orangegui.separator(container)
        OWGenericWidget.create_box_in_widget(self, container, "displacement", add_callback=True)

        self.is_on_init = False

    def after_change_workspace_units(self):
        pass

    def set_index(self, index):
        self.index = index

    def callback_displacement(self):
        if not self.is_on_init: self.widget.dump_displacement()

    def after_change_workspace_units(self):
        pass

    def set_index(self, index):
        self.index = index

    def get_parameters_prefix(self):
        return SpecimenDisplacement.get_parameters_prefix() + self.get_parameter_progressive()

    def get_parameter_progressive(self):
        return str(self.index + 1) + "_"

    def set_data(self, shift_parameters):
        self.goniometer_radius = shift_parameters.goniometer_radius

        displacement = shift_parameters.displacement.duplicate()
        displacement.rescale(1e6)  # to um

        OWGenericWidget.populate_fields_in_widget(self, "displacement", displacement, value_only=True)

    def send_peak_shift(self):
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