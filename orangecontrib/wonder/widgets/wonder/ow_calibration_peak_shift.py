import sys, copy

from PyQt5.QtWidgets import QMessageBox, QApplication

from orangewidget.settings import Setting
from orangewidget import gui as orangegui
from orangewidget.widget import OWAction

from orangecontrib.wonder.widgets.gui.ow_generic_widget import OWGenericWidget
from orangecontrib.wonder.util.gui_utility import gui, ConfirmDialog
from orangecontrib.wonder.fit.parameters.fit_global_parameters import FitGlobalParameters
from orangecontrib.wonder.fit.parameters.instrument.instrumental_parameters import Lab6TanCorrection


class OWCalibrationPeakShift(OWGenericWidget):
    name = "Calibration Peak Shift"
    description = "Calibration Peak Shift"
    icon = "icons/calibration_peak_shift.png"
    priority = 13

    want_main_area = False

    use_single_parameter_set = Setting(0)

    ax = Setting([0.0])
    bx = Setting([0.0])
    cx = Setting([0.0])
    dx = Setting([0.0])
    ex = Setting([0.0])
    ax_fixed = Setting([0])
    bx_fixed = Setting([0])
    cx_fixed = Setting([0])
    dx_fixed = Setting([0])
    ex_fixed = Setting([0])
    ax_has_min = Setting([0])
    bx_has_min = Setting([0])
    cx_has_min = Setting([0])
    dx_has_min = Setting([0])
    ex_has_min = Setting([0])
    ax_min = Setting([0.0])
    bx_min = Setting([0.0])
    cx_min = Setting([0.0])
    dx_min = Setting([0.0])
    ex_min = Setting([0.0])
    ax_has_max = Setting([0])
    bx_has_max = Setting([0])
    cx_has_max = Setting([0])
    dx_has_max = Setting([0])
    ex_has_max = Setting([0])
    ax_max = Setting([0.0])
    bx_max = Setting([0.0])
    cx_max = Setting([0.0])
    dx_max = Setting([0.0])
    ex_max = Setting([0.0])
    ax_function = Setting([0])
    bx_function = Setting([0])
    cx_function = Setting([0])
    dx_function = Setting([0])
    ex_function = Setting([0])
    ax_function_value = Setting([""])
    bx_function_value = Setting([""])
    cx_function_value = Setting([""])
    dx_function_value = Setting([""])
    ex_function_value = Setting([""])

    inputs = [("Fit Global Parameters", FitGlobalParameters, 'set_data')]
    outputs = [("Fit Global Parameters", FitGlobalParameters)]

    def __init__(self):
        super().__init__(show_automatic_box=True)

        main_box = gui.widgetBox(self.controlArea,
                                 "LaB6 Tan Correction", orientation="vertical",
                                 width=self.CONTROL_AREA_WIDTH - 10, height=600)

        button_box = gui.widgetBox(main_box,
                                   "", orientation="horizontal",
                                   width=self.CONTROL_AREA_WIDTH - 25)

        gui.button(button_box, self, "Send Peak Shift", height=40, callback=self.send_peak_shift)

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

        dimension = len(self.ax) if self.fit_global_parameters is None else self.fit_global_parameters.measured_dataset.get_diffraction_patterns_number()

        for index in range(1 if self.use_single_parameter_set == 1 else dimension):
            peak_shift_tab = gui.createTabPage(self.peak_shift_tabs, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, index, self.use_single_parameter_set==1))

            if index < len(self.ax) and recycle:  # keep the existing
                peak_shift_box = CalibrationPeakShiftBox(widget=self,
                                                          parent=peak_shift_tab,
                                                          index=index,
                                                          ax=self.ax[index],
                                                          bx=self.bx[index],
                                                          cx=self.cx[index],
                                                          dx=self.dx[index],
                                                          ex=self.ex[index],
                                                          ax_fixed=self.ax_fixed[index],
                                                          bx_fixed=self.bx_fixed[index],
                                                          cx_fixed=self.cx_fixed[index],
                                                          dx_fixed=self.dx_fixed[index],
                                                          ex_fixed=self.ex_fixed[index],
                                                          ax_has_min=self.ax_has_min[index],
                                                          bx_has_min=self.bx_has_min[index],
                                                          cx_has_min=self.cx_has_min[index],
                                                          dx_has_min=self.dx_has_min[index],
                                                          ex_has_min=self.ex_has_min[index],
                                                          ax_min=self.ax_min[index],
                                                          bx_min=self.bx_min[index],
                                                          cx_min=self.cx_min[index],
                                                          dx_min=self.dx_min[index],
                                                          ex_min=self.ex_min[index],
                                                          ax_has_max=self.ax_has_max[index],
                                                          bx_has_max=self.bx_has_max[index],
                                                          cx_has_max=self.cx_has_max[index],
                                                          dx_has_max=self.dx_has_max[index],
                                                          ex_has_max=self.ex_has_max[index],
                                                          ax_max=self.ax_max[index],
                                                          bx_max=self.bx_max[index],
                                                          cx_max=self.cx_max[index],
                                                          dx_max=self.dx_max[index],
                                                          ex_max=self.ex_max[index],
                                                          ax_function=self.ax_function[index],
                                                          bx_function=self.bx_function[index],
                                                          cx_function=self.cx_function[index],
                                                          dx_function=self.dx_function[index],
                                                          ex_function=self.ex_function[index],
                                                          ax_function_value=self.ax_function_value[index],
                                                          bx_function_value=self.bx_function_value[index],
                                                          cx_function_value=self.cx_function_value[index],
                                                          dx_function_value=self.dx_function_value[index],
                                                          ex_function_value=self.ex_function_value[index])
            else:
                peak_shift_box = CalibrationPeakShiftBox(widget=self, parent=peak_shift_tab, index=index)

            self.peak_shift_box_array.append(peak_shift_box)

            if not on_init: self.dumpSettings()

    def send_peak_shift(self):
        try:
            if not self.fit_global_parameters is None:
                self.dumpSettings()

                self.fit_global_parameters.set_shift_parameters([self.peak_shift_box_array[index].send_peak_shift() for index in range(len(self.ax))])
                self.fit_global_parameters.regenerate_parameters()

                self.send("Fit Global Parameters", self.fit_global_parameters)

        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 str(e),
                                 QMessageBox.Ok)

            if self.IS_DEVELOP: raise e

    def __check_data_congruence(self, shift_parameters):
        if (len(shift_parameters) == 1 and self.use_single_parameter_set == 0) or (len(shift_parameters) > 1 and self.use_single_parameter_set == 1):
            raise ValueError("Previous Shift parameters are incongruent with the current choice of using a single set")

    def set_data(self, data):
        if not data is None:
            try:
                self.fit_global_parameters = data.duplicate()

                diffraction_patterns = self.fit_global_parameters.measured_dataset.diffraction_patterns
                if diffraction_patterns is None: raise ValueError("No Diffraction Pattern in input data!")

                shift_parameters = self.fit_global_parameters.get_shift_parameters(Lab6TanCorrection.__name__)

                if self.use_single_parameter_set == 0:  # NO
                    if shift_parameters is None:
                        if len(diffraction_patterns) != len(self.peak_shift_box_array):
                            self.set_use_single_parameter_set(recycle=ConfirmDialog.confirmed(message="Number of Diffraction Patterns changed:\ndo you want to use the existing data where possible?\n\nIf yes, check for possible incongruences", title="Warning"))
                        else:
                            self.set_use_single_parameter_set(True)
                    else:
                        tabs_to_remove = len(self.ax) - len(shift_parameters)

                        if tabs_to_remove > 0:
                            for index in range(tabs_to_remove):
                                self.peak_shift_tabs.removeTab(-1)
                                self.peak_shift_box_array.pop()

                        for diffraction_pattern_index in range(len(shift_parameters)):
                            shift_parameters_item = self.fit_global_parameters.get_shift_parameters_item(Lab6TanCorrection.__name__, diffraction_pattern_index)



                            if diffraction_pattern_index < len(self.ax):
                                self.peak_shift_tabs.setTabText(diffraction_pattern_index, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, diffraction_pattern_index, False))
                                peak_shift_box = self.peak_shift_box_array[diffraction_pattern_index]

                            else:
                                peak_shift_box = CalibrationPeakShiftBox(widget=self,
                                                                         parent=gui.createTabPage(self.peak_shift_tabs, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, diffraction_pattern_index, False)),
                                                                         index=diffraction_pattern_index)
                                self.peak_shift_box_array.append(peak_shift_box)

                            if not shift_parameters_item is None: peak_shift_box.set_data(shift_parameters_item)
                else:
                    if shift_parameters is None:
                        self.set_use_single_parameter_set(True)
                    else:
                        self.__check_data_congruence(shift_parameters)

                        shift_parameters_item = self.fit_global_parameters.get_shift_parameters_item(Lab6TanCorrection.__name__, 0)

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
        self.dump_ax()
        self.dump_bx()
        self.dump_cx()
        self.dump_dx()
        self.dump_ex()

    def dump_ax(self):
        bkp_ax = copy.deepcopy(self.ax)
        bkp_ax_fixed = copy.deepcopy(self.ax_fixed)
        bkp_ax_has_min = copy.deepcopy(self.ax_has_min)
        bkp_ax_min = copy.deepcopy(self.ax_min)
        bkp_ax_has_max = copy.deepcopy(self.ax_has_max)
        bkp_ax_max = copy.deepcopy(self.ax_max)
        bkp_ax_function = copy.deepcopy(self.ax_function)
        bkp_ax_function_value = copy.deepcopy(self.ax_function_value)

        try:
            self.ax = []
            self.ax_fixed = []
            self.ax_has_min = []
            self.ax_min = []
            self.ax_has_max = []
            self.ax_max = []
            self.ax_function = []
            self.ax_function_value = []

            for index in range(len(self.peak_shift_box_array)):
                self.ax.append(self.peak_shift_box_array[index].ax)
                self.ax_fixed.append(self.peak_shift_box_array[index].ax_fixed)
                self.ax_has_min.append(self.peak_shift_box_array[index].ax_has_min)
                self.ax_min.append(self.peak_shift_box_array[index].ax_min)
                self.ax_has_max.append(self.peak_shift_box_array[index].ax_has_max)
                self.ax_max.append(self.peak_shift_box_array[index].ax_max)
                self.ax_function.append(self.peak_shift_box_array[index].ax_function)
                self.ax_function_value.append(self.peak_shift_box_array[index].ax_function_value)
        except Exception as e:
            self.ax = copy.deepcopy(bkp_ax)
            self.ax_fixed = copy.deepcopy(bkp_ax_fixed)
            self.ax_has_min = copy.deepcopy(bkp_ax_has_min)
            self.ax_min = copy.deepcopy(bkp_ax_min)
            self.ax_has_max = copy.deepcopy(bkp_ax_has_max)
            self.ax_max = copy.deepcopy(bkp_ax_max)
            self.ax_function = copy.deepcopy(bkp_ax_function)
            self.ax_function_value = copy.deepcopy(bkp_ax_function_value)

            if self.IS_DEVELOP: raise e

    def dump_bx(self):
        bkp_bx = copy.deepcopy(self.bx)
        bkp_bx_fixed = copy.deepcopy(self.bx_fixed)
        bkp_bx_has_min = copy.deepcopy(self.bx_has_min)
        bkp_bx_min = copy.deepcopy(self.bx_min)
        bkp_bx_has_max = copy.deepcopy(self.bx_has_max)
        bkp_bx_max = copy.deepcopy(self.bx_max)
        bkp_bx_function = copy.deepcopy(self.bx_function)
        bkp_bx_function_value = copy.deepcopy(self.bx_function_value)

        try:
            self.bx = []
            self.bx_fixed = []
            self.bx_has_min = []
            self.bx_min = []
            self.bx_has_max = []
            self.bx_max = []
            self.bx_function = []
            self.bx_function_value = []

            for index in range(len(self.peak_shift_box_array)):
                self.bx.append(self.peak_shift_box_array[index].bx)
                self.bx_fixed.append(self.peak_shift_box_array[index].bx_fixed)
                self.bx_has_min.append(self.peak_shift_box_array[index].bx_has_min)
                self.bx_min.append(self.peak_shift_box_array[index].bx_min)
                self.bx_has_max.append(self.peak_shift_box_array[index].bx_has_max)
                self.bx_max.append(self.peak_shift_box_array[index].bx_max)
                self.bx_function.append(self.peak_shift_box_array[index].bx_function)
                self.bx_function_value.append(self.peak_shift_box_array[index].bx_function_value)
        except Exception as e:
            self.bx = copy.deepcopy(bkp_bx)
            self.bx_fixed = copy.deepcopy(bkp_bx_fixed)
            self.bx_has_min = copy.deepcopy(bkp_bx_has_min)
            self.bx_min = copy.deepcopy(bkp_bx_min)
            self.bx_has_max = copy.deepcopy(bkp_bx_has_max)
            self.bx_max = copy.deepcopy(bkp_bx_max)
            self.bx_function = copy.deepcopy(bkp_bx_function)
            self.bx_function_value = copy.deepcopy(bkp_bx_function_value)

            if self.IS_DEVELOP: raise e

    def dump_cx(self):
        bkp_cx = copy.deepcopy(self.cx)
        bkp_cx_fixed = copy.deepcopy(self.cx_fixed)
        bkp_cx_has_min = copy.deepcopy(self.cx_has_min)
        bkp_cx_min = copy.deepcopy(self.cx_min)
        bkp_cx_has_max = copy.deepcopy(self.cx_has_max)
        bkp_cx_max = copy.deepcopy(self.cx_max)
        bkp_cx_function = copy.deepcopy(self.cx_function)
        bkp_cx_function_value = copy.deepcopy(self.cx_function_value)

        try:
            self.cx = []
            self.cx_fixed = []
            self.cx_has_min = []
            self.cx_min = []
            self.cx_has_max = []
            self.cx_max = []
            self.cx_function = []
            self.cx_function_value = []

            for index in range(len(self.peak_shift_box_array)):
                self.cx.append(self.peak_shift_box_array[index].cx)
                self.cx_fixed.append(self.peak_shift_box_array[index].cx_fixed)
                self.cx_has_min.append(self.peak_shift_box_array[index].cx_has_min)
                self.cx_min.append(self.peak_shift_box_array[index].cx_min)
                self.cx_has_max.append(self.peak_shift_box_array[index].cx_has_max)
                self.cx_max.append(self.peak_shift_box_array[index].cx_max)
                self.cx_function.append(self.peak_shift_box_array[index].cx_function)
                self.cx_function_value.append(self.peak_shift_box_array[index].cx_function_value)
        except Exception as e:
            self.cx = copy.deepcopy(bkp_cx)
            self.cx_fixed = copy.deepcopy(bkp_cx_fixed)
            self.cx_has_min = copy.deepcopy(bkp_cx_has_min)
            self.cx_min = copy.deepcopy(bkp_cx_min)
            self.cx_has_max = copy.deepcopy(bkp_cx_has_max)
            self.cx_max = copy.deepcopy(bkp_cx_max)
            self.cx_function = copy.deepcopy(bkp_cx_function)
            self.cx_function_value = copy.deepcopy(bkp_cx_function_value)

            if self.IS_DEVELOP: raise e

    def dump_dx(self):
        bkp_dx = copy.deepcopy(self.dx)
        bkp_dx_fixed = copy.deepcopy(self.dx_fixed)
        bkp_dx_has_min = copy.deepcopy(self.dx_has_min)
        bkp_dx_min = copy.deepcopy(self.dx_min)
        bkp_dx_has_max = copy.deepcopy(self.dx_has_max)
        bkp_dx_max = copy.deepcopy(self.dx_max)
        bkp_dx_function = copy.deepcopy(self.dx_function)
        bkp_dx_function_value = copy.deepcopy(self.dx_function_value)

        try:
            self.dx = []
            self.dx_fixed = []
            self.dx_has_min = []
            self.dx_min = []
            self.dx_has_max = []
            self.dx_max = []
            self.dx_function = []
            self.dx_function_value = []

            for index in range(len(self.peak_shift_box_array)):
                self.dx.append(self.peak_shift_box_array[index].dx)
                self.dx_fixed.append(self.peak_shift_box_array[index].dx_fixed)
                self.dx_has_min.append(self.peak_shift_box_array[index].dx_has_min)
                self.dx_min.append(self.peak_shift_box_array[index].dx_min)
                self.dx_has_max.append(self.peak_shift_box_array[index].dx_has_max)
                self.dx_max.append(self.peak_shift_box_array[index].dx_max)
                self.dx_function.append(self.peak_shift_box_array[index].dx_function)
                self.dx_function_value.append(self.peak_shift_box_array[index].dx_function_value)
        except Exception as e:
            self.dx = copy.deepcopy(bkp_dx)
            self.dx_fixed = copy.deepcopy(bkp_dx_fixed)
            self.dx_has_min = copy.deepcopy(bkp_dx_has_min)
            self.dx_min = copy.deepcopy(bkp_dx_min)
            self.dx_has_max = copy.deepcopy(bkp_dx_has_max)
            self.dx_max = copy.deepcopy(bkp_dx_max)
            self.dx_function = copy.deepcopy(bkp_dx_function)
            self.dx_function_value = copy.deepcopy(bkp_dx_function_value)

            if self.IS_DEVELOP: raise e

    def dump_ex(self):
        bkp_ex = copy.deepcopy(self.ex)
        bkp_ex_fixed = copy.deepcopy(self.ex_fixed)
        bkp_ex_has_min = copy.deepcopy(self.ex_has_min)
        bkp_ex_min = copy.deepcopy(self.ex_min)
        bkp_ex_has_max = copy.deepcopy(self.ex_has_max)
        bkp_ex_max = copy.deepcopy(self.ex_max)
        bkp_ex_function = copy.deepcopy(self.ex_function)
        bkp_ex_function_value = copy.deepcopy(self.ex_function_value)

        try:
            self.ex = []
            self.ex_fixed = []
            self.ex_has_min = []
            self.ex_min = []
            self.ex_has_max = []
            self.ex_max = []
            self.ex_function = []
            self.ex_function_value = []

            for index in range(len(self.peak_shift_box_array)):
                self.ex.append(self.peak_shift_box_array[index].ex)
                self.ex_fixed.append(self.peak_shift_box_array[index].ex_fixed)
                self.ex_has_min.append(self.peak_shift_box_array[index].ex_has_min)
                self.ex_min.append(self.peak_shift_box_array[index].ex_min)
                self.ex_has_max.append(self.peak_shift_box_array[index].ex_has_max)
                self.ex_max.append(self.peak_shift_box_array[index].ex_max)
                self.ex_function.append(self.peak_shift_box_array[index].ex_function)
                self.ex_function_value.append(self.peak_shift_box_array[index].ex_function_value)
        except Exception as e:
            self.ex = copy.deepcopy(bkp_ex)
            self.ex_fixed = copy.deepcopy(bkp_ex_fixed)
            self.ex_has_min = copy.deepcopy(bkp_ex_has_min)
            self.ex_min = copy.deepcopy(bkp_ex_min)
            self.ex_has_max = copy.deepcopy(bkp_ex_has_max)
            self.ex_max = copy.deepcopy(bkp_ex_max)
            self.ex_function = copy.deepcopy(bkp_ex_function)
            self.ex_function_value = copy.deepcopy(bkp_ex_function_value)

            if self.IS_DEVELOP: raise e

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QVBoxLayout
from orangecontrib.wonder.util.gui_utility import InnerBox


class CalibrationPeakShiftBox(InnerBox):
    widget = None
    is_on_init = True

    parameter_functions = {}

    index = 0

    def __init__(self,
                 widget=None,
                 parent=None,
                 index=0,
                 ax=0.0,
                 bx=0.0,
                 cx=0.0,
                 dx=0.0,
                 ex=0.0,
                 ax_fixed=0,
                 bx_fixed=0,
                 cx_fixed=0,
                 dx_fixed=0,
                 ex_fixed=0,
                 ax_has_min=0,
                 bx_has_min=0,
                 cx_has_min=0,
                 dx_has_min=0,
                 ex_has_min=0,
                 ax_min=0.0,
                 bx_min=0.0,
                 cx_min=0.0,
                 dx_min=0.0,
                 ex_min=0.0,
                 ax_has_max=0,
                 bx_has_max=0,
                 cx_has_max=0,
                 dx_has_max=0,
                 ex_has_max=0,
                 ax_max=0.0,
                 bx_max=0.0,
                 cx_max=0.0,
                 dx_max=0.0,
                 ex_max=0.0,
                 ax_function=0,
                 bx_function=0,
                 cx_function=0,
                 dx_function=0,
                 ex_function=0,
                 ax_function_value="",
                 bx_function_value="",
                 cx_function_value="",
                 dx_function_value="",
                 ex_function_value=""):
        super(CalibrationPeakShiftBox, self).__init__()

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.setFixedWidth(widget.CONTROL_AREA_WIDTH - 35)
        self.setFixedHeight(500)

        self.widget = widget
        self.index = index

        self.ax = ax
        self.bx = bx
        self.cx = cx
        self.dx = dx
        self.ex = ex

        self.ax_fixed = ax_fixed
        self.bx_fixed = bx_fixed
        self.cx_fixed = cx_fixed
        self.dx_fixed = dx_fixed
        self.ex_fixed = ex_fixed

        self.ax_has_min = ax_has_min
        self.bx_has_min = bx_has_min
        self.cx_has_min = cx_has_min
        self.dx_has_min = dx_has_min
        self.ex_has_min = ex_has_min

        self.ax_min = ax_min
        self.bx_min = bx_min
        self.cx_min = cx_min
        self.dx_min = dx_min
        self.ex_min = ex_min

        self.ax_has_max = ax_has_max
        self.bx_has_max = bx_has_max
        self.cx_has_max = cx_has_max
        self.dx_has_max = dx_has_max
        self.ex_has_max = ex_has_max

        self.ax_max = ax_max
        self.bx_max = bx_max
        self.cx_max = cx_max
        self.dx_max = dx_max
        self.ex_max = ex_max

        self.ax_function = ax_function
        self.bx_function = bx_function
        self.cx_function = cx_function
        self.dx_function = dx_function
        self.ex_function = ex_function

        self.ax_function_value = ax_function_value
        self.bx_function_value = bx_function_value
        self.cx_function_value = cx_function_value
        self.dx_function_value = dx_function_value
        self.ex_function_value = ex_function_value

        self.CONTROL_AREA_WIDTH = widget.CONTROL_AREA_WIDTH

        parent.layout().addWidget(self)
        container = self

        OWGenericWidget.create_box_in_widget(self, container, "ax", add_callback=True)
        OWGenericWidget.create_box_in_widget(self, container, "bx", add_callback=True)
        OWGenericWidget.create_box_in_widget(self, container, "cx", add_callback=True)
        OWGenericWidget.create_box_in_widget(self, container, "dx", add_callback=True)
        OWGenericWidget.create_box_in_widget(self, container, "ex", add_callback=True)

        self.is_on_init = False

    def after_change_workspace_units(self):
        pass

    def set_index(self, index):
        self.index = index

    def callback_ax(self):
        if not self.is_on_init: self.widget.dump_ax()

    def callback_bx(self):
        if not self.is_on_init: self.widget.dump_bx()

    def callback_cx(self):
        if not self.is_on_init: self.widget.dump_cx()

    def callback_dx(self):
        if not self.is_on_init: self.widget.dump_dx()

    def callback_ex(self):
        if not self.is_on_init: self.widget.dump_ex()

    def after_change_workspace_units(self):
        pass

    def set_index(self, index):
        self.index = index

    def get_parameters_prefix(self):
        return Lab6TanCorrection.get_parameters_prefix() + self.get_parameter_progressive()

    def get_parameter_progressive(self):
        return str(self.index + 1) + "_"

    def set_data(self, shift_parameters):
        OWGenericWidget.populate_fields_in_widget(self, "ax", shift_parameters.ax, value_only=True)
        OWGenericWidget.populate_fields_in_widget(self, "bx", shift_parameters.bx, value_only=True)
        OWGenericWidget.populate_fields_in_widget(self, "cx", shift_parameters.cx, value_only=True)
        OWGenericWidget.populate_fields_in_widget(self, "dx", shift_parameters.dx, value_only=True)
        OWGenericWidget.populate_fields_in_widget(self, "ex", shift_parameters.ex, value_only=True)

    def send_peak_shift(self):
        return Lab6TanCorrection(ax=OWGenericWidget.populate_parameter_in_widget(self, "ax", self.get_parameters_prefix()),
                                 bx=OWGenericWidget.populate_parameter_in_widget(self, "bx", self.get_parameters_prefix()),
                                 cx=OWGenericWidget.populate_parameter_in_widget(self, "cx", self.get_parameters_prefix()),
                                 dx=OWGenericWidget.populate_parameter_in_widget(self, "dx", self.get_parameters_prefix()),
                                 ex=OWGenericWidget.populate_parameter_in_widget(self, "ex", self.get_parameters_prefix()))


if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = OWCalibrationPeakShift()
    ow.show()
    a.exec_()
    ow.saveSettings()
