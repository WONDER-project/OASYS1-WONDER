import sys, copy

from PyQt5.QtWidgets import QMessageBox, QApplication

from orangewidget.settings import Setting
from orangewidget import gui as orangegui
from orangewidget.widget import OWAction

from orangecontrib.wonder.widgets.gui.ow_generic_widget import OWGenericWidget
from orangecontrib.wonder.util.gui_utility import gui, ConfirmDialog
from orangecontrib.wonder.fit.parameters.fit_global_parameters import FitGlobalParameters
from orangecontrib.wonder.fit.parameters.instrument.instrumental_parameters import Caglioti


class OWInstrumentalProfile(OWGenericWidget):
    name = "Instrumental Profile"
    description = "Define Instrumental Profile Parameters"
    icon = "icons/instrumental_profile.png"
    priority = 12

    want_main_area = False

    use_single_parameter_set = Setting(0)

    U = Setting([0.0])
    V = Setting([0.0])
    W = Setting([0.0])
    U_fixed = Setting([0])
    V_fixed = Setting([0])
    W_fixed = Setting([0])
    U_has_min = Setting([0])
    V_has_min = Setting([0])
    W_has_min = Setting([0])
    U_min = Setting([0.0])
    V_min = Setting([0.0])
    W_min = Setting([0.0])
    U_has_max = Setting([0])
    V_has_max = Setting([0])
    W_has_max = Setting([0])
    U_max = Setting([0.0])
    V_max = Setting([0.0])
    W_max = Setting([0.0])
    U_function = Setting([0])
    V_function = Setting([0])
    W_function = Setting([0])
    U_function_value = Setting([""])
    V_function_value = Setting([""])
    W_function_value = Setting([""])
    a = Setting([0.0])
    b = Setting([0.0])
    c = Setting([0.0])
    a_fixed = Setting([0])
    b_fixed = Setting([0])
    c_fixed = Setting([0])
    a_has_min = Setting([0])
    b_has_min = Setting([0])
    c_has_min = Setting([0])
    a_min = Setting([0.0])
    b_min = Setting([0.0])
    c_min = Setting([0.0])
    a_has_max = Setting([0])
    b_has_max = Setting([0])
    c_has_max = Setting([0])
    a_max = Setting([0.0])
    b_max = Setting([0.0])
    c_max = Setting([0.0])
    a_function = Setting([0])
    b_function = Setting([0])
    c_function = Setting([0])
    a_function_value = Setting([""])
    b_function_value = Setting([""])
    c_function_value = Setting([""])

    inputs = [("Fit Global Parameters", FitGlobalParameters, 'set_data')]
    outputs = [("Fit Global Parameters", FitGlobalParameters)]

    def __init__(self):
        super().__init__(show_automatic_box=True)

        main_box = gui.widgetBox(self.controlArea,
                                 "Instrumental Profile", orientation="vertical",
                                 width=self.CONTROL_AREA_WIDTH - 10, height=600)

        button_box = gui.widgetBox(main_box,
                                   "", orientation="horizontal",
                                   width=self.CONTROL_AREA_WIDTH - 25)

        gui.button(button_box, self, "Send Instrumental Profile", height=40, callback=self.send_intrumental_profile)

        orangegui.comboBox(main_box, self, "use_single_parameter_set", label="Use single set of Parameters", labelWidth=350, orientation="horizontal",
                           items=["No", "Yes"], callback=self.set_use_single_parameter_set, sendSelectedValue=False)

        orangegui.separator(main_box)

        self.instrumental_tabs = gui.tabWidget(main_box)

        self.set_use_single_parameter_set(on_init=True)

        runaction = OWAction("Send Background", self)
        runaction.triggered.connect(self.send_intrumental_profile)
        self.addAction(runaction)

        orangegui.rubber(self.controlArea)

    def set_use_single_parameter_set(self, on_init=False, recycle=True):
        self.instrumental_tabs.clear()
        self.instrumental_box_array = []

        dimension = len(self.U) if self.fit_global_parameters is None else self.fit_global_parameters.measured_dataset.get_diffraction_patterns_number()

        for index in range(1 if self.use_single_parameter_set == 1 else dimension):
            instrumental_tab = gui.createTabPage(self.instrumental_tabs, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, index, self.use_single_parameter_set==1))

            if index < len(self.U) and recycle:  # keep the existing
                instrumental_box = InstrumentalProfileBox(widget=self,
                                                          parent=instrumental_tab,
                                                          index=index,
                                                          U=self.U[index],
                                                          V=self.V[index],
                                                          W=self.W[index],
                                                          a=self.a[index],
                                                          b=self.b[index],
                                                          c=self.c[index],
                                                          U_fixed=self.U_fixed[index],
                                                          V_fixed=self.V_fixed[index],
                                                          W_fixed=self.W_fixed[index],
                                                          a_fixed=self.a_fixed[index],
                                                          b_fixed=self.b_fixed[index],
                                                          c_fixed=self.c_fixed[index],
                                                          U_has_min=self.U_has_min[index],
                                                          V_has_min=self.V_has_min[index],
                                                          W_has_min=self.W_has_min[index],
                                                          a_has_min=self.a_has_min[index],
                                                          b_has_min=self.b_has_min[index],
                                                          c_has_min=self.c_has_min[index],
                                                          U_min=self.U_min[index],
                                                          V_min=self.V_min[index],
                                                          W_min=self.W_min[index],
                                                          a_min=self.a_min[index],
                                                          b_min=self.b_min[index],
                                                          c_min=self.c_min[index],
                                                          U_has_max=self.U_has_max[index],
                                                          V_has_max=self.V_has_max[index],
                                                          W_has_max=self.W_has_max[index],
                                                          a_has_max=self.a_has_max[index],
                                                          b_has_max=self.b_has_max[index],
                                                          c_has_max=self.c_has_max[index],
                                                          U_max=self.U_max[index],
                                                          V_max=self.V_max[index],
                                                          W_max=self.W_max[index],
                                                          a_max=self.a_max[index],
                                                          b_max=self.b_max[index],
                                                          c_max=self.c_max[index],
                                                          U_function=self.U_function[index],
                                                          V_function=self.V_function[index],
                                                          W_function=self.W_function[index],
                                                          a_function=self.a_function[index],
                                                          b_function=self.b_function[index],
                                                          c_function=self.c_function[index],
                                                          U_function_value=self.U_function_value[index],
                                                          V_function_value=self.V_function_value[index],
                                                          W_function_value=self.W_function_value[index],
                                                          a_function_value=self.a_function_value[index],
                                                          b_function_value=self.b_function_value[index],
                                                          c_function_value=self.c_function_value[index])
            else:
                instrumental_box = InstrumentalProfileBox(widget=self, parent=instrumental_tab, index=index)

            self.instrumental_box_array.append(instrumental_box)

            if not on_init: self.dumpSettings()

    def send_intrumental_profile(self):
        try:
            if not self.fit_global_parameters is None:
                self.dumpSettings()

                self.fit_global_parameters.set_instrumental_parameters([self.instrumental_box_array[index].send_instrumental_profile() for index in range(len(self.U))])
                self.fit_global_parameters.regenerate_parameters()

                self.send("Fit Global Parameters", self.fit_global_parameters)

        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 str(e),
                                 QMessageBox.Ok)

            if self.IS_DEVELOP: raise e

    def __check_data_congruence(self, instrumental_parameters):
        if (len(instrumental_parameters) == 1 and self.use_single_parameter_set == 0) or (len(instrumental_parameters) > 1 and self.use_single_parameter_set == 1):
            raise ValueError("Previous Chebyshev parameters are incongruent with the current choice of using a single set")

    def set_data(self, data):
        if not data is None:
            try:
                self.fit_global_parameters = data.duplicate()

                diffraction_patterns = self.fit_global_parameters.measured_dataset.diffraction_patterns
                if diffraction_patterns is None: raise ValueError("No Diffraction Pattern in input data!")

                instrumental_parameters = self.fit_global_parameters.get_instrumental_parameters(Caglioti.__name__)

                if self.use_single_parameter_set == 0:  # NO
                    if instrumental_parameters is None:
                        if len(diffraction_patterns) != len(self.instrumental_box_array):
                            self.set_use_single_parameter_set(recycle=ConfirmDialog.confirmed(message="Number of Diffraction Patterns changed:\ndo you want to use the existing data where possible?\n\nIf yes, check for possible incongruences", title="Warning"))
                        else:
                            self.set_use_single_parameter_set(True)
                    else:
                        self.__check_data_congruence(instrumental_parameters)

                        tabs_to_remove = len(self.U) - len(instrumental_parameters)

                        if tabs_to_remove > 0:
                            for index in range(tabs_to_remove):
                                self.instrumental_tabs.removeTab(-1)
                                self.instrumental_box_array.pop()

                        for diffraction_pattern_index in range(len(instrumental_parameters)):
                            instrumental_parameters_item = self.fit_global_parameters.get_instrumental_parameters_item(Caglioti.__name__, diffraction_pattern_index)

                            if diffraction_pattern_index < len(self.U):
                                self.instrumental_tabs.setTabText(diffraction_pattern_index,
                                                               OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, diffraction_pattern_index, False))

                                instrumental_box = self.instrumental_box_array[diffraction_pattern_index]
                                if not instrumental_parameters_item is None: instrumental_box.set_data(instrumental_parameters_item)
                            else:
                                instrumental_box = InstrumentalProfileBox(widget=self,
                                                                          parent=gui.createTabPage(self.instrumental_tabs, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, index, False)),
                                                                          index=diffraction_pattern_index)

                                if not instrumental_parameters_item is None: instrumental_box.set_data(instrumental_parameters_item)

                                self.instrumental_box_array.append(instrumental_box)
                else:
                    if instrumental_parameters is None:
                        self.set_use_single_parameter_set(True)
                    else:
                        self.__check_data_congruence(instrumental_parameters)

                        instrumental_parameters_item = self.fit_global_parameters.get_instrumental_parameters_item(Caglioti.__name__, 0)

                        self.instrumental_tabs.setTabText(0, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, 0, True))
                        if not instrumental_parameters_item is None: self.instrumental_box_array[0].set_data(instrumental_parameters_item)

                self.dumpSettings()

                if self.is_automatic_run:
                    self.send_intrumental_profile()

            except Exception as e:
                QMessageBox.critical(self, "Error",
                                     str(e),
                                     QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def dumpSettings(self):
        self.dump_U()
        self.dump_V()
        self.dump_W()
        self.dump_a()
        self.dump_b()
        self.dump_c()

    def dump_U(self):
        bkp_U = copy.deepcopy(self.U)
        bkp_U_fixed = copy.deepcopy(self.U_fixed)
        bkp_U_has_min = copy.deepcopy(self.U_has_min)
        bkp_U_min = copy.deepcopy(self.U_min)
        bkp_U_has_max = copy.deepcopy(self.U_has_max)
        bkp_U_max = copy.deepcopy(self.U_max)
        bkp_U_function = copy.deepcopy(self.U_function)
        bkp_U_function_value = copy.deepcopy(self.U_function_value)

        try:
            self.U = []
            self.U_fixed = []
            self.U_has_min = []
            self.U_min = []
            self.U_has_max = []
            self.U_max = []
            self.U_function = []
            self.U_function_value = []

            for index in range(len(self.instrumental_box_array)):
                self.U.append(self.instrumental_box_array[index].U)
                self.U_fixed.append(self.instrumental_box_array[index].U_fixed)
                self.U_has_min.append(self.instrumental_box_array[index].U_has_min)
                self.U_min.append(self.instrumental_box_array[index].U_min)
                self.U_has_max.append(self.instrumental_box_array[index].U_has_max)
                self.U_max.append(self.instrumental_box_array[index].U_max)
                self.U_function.append(self.instrumental_box_array[index].U_function)
                self.U_function_value.append(self.instrumental_box_array[index].U_function_value)
        except Exception as e:
            self.U = copy.deepcopy(bkp_U)
            self.U_fixed = copy.deepcopy(bkp_U_fixed)
            self.U_has_min = copy.deepcopy(bkp_U_has_min)
            self.U_min = copy.deepcopy(bkp_U_min)
            self.U_has_max = copy.deepcopy(bkp_U_has_max)
            self.U_max = copy.deepcopy(bkp_U_max)
            self.U_function = copy.deepcopy(bkp_U_function)
            self.U_function_value = copy.deepcopy(bkp_U_function_value)

            if self.IS_DEVELOP: raise e

    def dump_V(self):
        bkp_V = copy.deepcopy(self.V)
        bkp_V_fixed = copy.deepcopy(self.V_fixed)
        bkp_V_has_min = copy.deepcopy(self.V_has_min)
        bkp_V_min = copy.deepcopy(self.V_min)
        bkp_V_has_max = copy.deepcopy(self.V_has_max)
        bkp_V_max = copy.deepcopy(self.V_max)
        bkp_V_function = copy.deepcopy(self.V_function)
        bkp_V_function_value = copy.deepcopy(self.V_function_value)

        try:
            self.V = []
            self.V_fixed = []
            self.V_has_min = []
            self.V_min = []
            self.V_has_max = []
            self.V_max = []
            self.V_function = []
            self.V_function_value = []

            for index in range(len(self.instrumental_box_array)):
                self.V.append(self.instrumental_box_array[index].V)
                self.V_fixed.append(self.instrumental_box_array[index].V_fixed)
                self.V_has_min.append(self.instrumental_box_array[index].V_has_min)
                self.V_min.append(self.instrumental_box_array[index].V_min)
                self.V_has_max.append(self.instrumental_box_array[index].V_has_max)
                self.V_max.append(self.instrumental_box_array[index].V_max)
                self.V_function.append(self.instrumental_box_array[index].V_function)
                self.V_function_value.append(self.instrumental_box_array[index].V_function_value)
        except Exception as e:
            self.V = copy.deepcopy(bkp_V)
            self.V_fixed = copy.deepcopy(bkp_V_fixed)
            self.V_has_min = copy.deepcopy(bkp_V_has_min)
            self.V_min = copy.deepcopy(bkp_V_min)
            self.V_has_max = copy.deepcopy(bkp_V_has_max)
            self.V_max = copy.deepcopy(bkp_V_max)
            self.V_function = copy.deepcopy(bkp_V_function)
            self.V_function_value = copy.deepcopy(bkp_V_function_value)

            if self.IS_DEVELOP: raise e

    def dump_W(self):
        bkp_W = copy.deepcopy(self.W)
        bkp_W_fixed = copy.deepcopy(self.W_fixed)
        bkp_W_has_min = copy.deepcopy(self.W_has_min)
        bkp_W_min = copy.deepcopy(self.W_min)
        bkp_W_has_max = copy.deepcopy(self.W_has_max)
        bkp_W_max = copy.deepcopy(self.W_max)
        bkp_W_function = copy.deepcopy(self.W_function)
        bkp_W_function_value = copy.deepcopy(self.W_function_value)

        try:
            self.W = []
            self.W_fixed = []
            self.W_has_min = []
            self.W_min = []
            self.W_has_max = []
            self.W_max = []
            self.W_function = []
            self.W_function_value = []

            for index in range(len(self.instrumental_box_array)):
                self.W.append(self.instrumental_box_array[index].W)
                self.W_fixed.append(self.instrumental_box_array[index].W_fixed)
                self.W_has_min.append(self.instrumental_box_array[index].W_has_min)
                self.W_min.append(self.instrumental_box_array[index].W_min)
                self.W_has_max.append(self.instrumental_box_array[index].W_has_max)
                self.W_max.append(self.instrumental_box_array[index].W_max)
                self.W_function.append(self.instrumental_box_array[index].W_function)
                self.W_function_value.append(self.instrumental_box_array[index].W_function_value)
        except Exception as e:
            self.W = copy.deepcopy(bkp_W)
            self.W_fixed = copy.deepcopy(bkp_W_fixed)
            self.W_has_min = copy.deepcopy(bkp_W_has_min)
            self.W_min = copy.deepcopy(bkp_W_min)
            self.W_has_max = copy.deepcopy(bkp_W_has_max)
            self.W_max = copy.deepcopy(bkp_W_max)
            self.W_function = copy.deepcopy(bkp_W_function)
            self.W_function_value = copy.deepcopy(bkp_W_function_value)

            if self.IS_DEVELOP: raise e

    def dump_a(self):
        bkp_a = copy.deepcopy(self.a)
        bkp_a_fixed = copy.deepcopy(self.a_fixed)
        bkp_a_has_min = copy.deepcopy(self.a_has_min)
        bkp_a_min = copy.deepcopy(self.a_min)
        bkp_a_has_max = copy.deepcopy(self.a_has_max)
        bkp_a_max = copy.deepcopy(self.a_max)
        bkp_a_function = copy.deepcopy(self.a_function)
        bkp_a_function_value = copy.deepcopy(self.a_function_value)

        try:
            self.a = []
            self.a_fixed = []
            self.a_has_min = []
            self.a_min = []
            self.a_has_max = []
            self.a_max = []
            self.a_function = []
            self.a_function_value = []

            for index in range(len(self.instrumental_box_array)):
                self.a.append(self.instrumental_box_array[index].a)
                self.a_fixed.append(self.instrumental_box_array[index].a_fixed)
                self.a_has_min.append(self.instrumental_box_array[index].a_has_min)
                self.a_min.append(self.instrumental_box_array[index].a_min)
                self.a_has_max.append(self.instrumental_box_array[index].a_has_max)
                self.a_max.append(self.instrumental_box_array[index].a_max)
                self.a_function.append(self.instrumental_box_array[index].a_function)
                self.a_function_value.append(self.instrumental_box_array[index].a_function_value)
        except Exception as e:
            self.a = copy.deepcopy(bkp_a)
            self.a_fixed = copy.deepcopy(bkp_a_fixed)
            self.a_has_min = copy.deepcopy(bkp_a_has_min)
            self.a_min = copy.deepcopy(bkp_a_min)
            self.a_has_max = copy.deepcopy(bkp_a_has_max)
            self.a_max = copy.deepcopy(bkp_a_max)
            self.a_function = copy.deepcopy(bkp_a_function)
            self.a_function_value = copy.deepcopy(bkp_a_function_value)

            if self.IS_DEVELOP: raise e

    def dump_b(self):
        bkp_b = copy.deepcopy(self.b)
        bkp_b_fixed = copy.deepcopy(self.b_fixed)
        bkp_b_has_min = copy.deepcopy(self.b_has_min)
        bkp_b_min = copy.deepcopy(self.b_min)
        bkp_b_has_max = copy.deepcopy(self.b_has_max)
        bkp_b_max = copy.deepcopy(self.b_max)
        bkp_b_function = copy.deepcopy(self.b_function)
        bkp_b_function_value = copy.deepcopy(self.b_function_value)

        try:
            self.b = []
            self.b_fixed = []
            self.b_has_min = []
            self.b_min = []
            self.b_has_max = []
            self.b_max = []
            self.b_function = []
            self.b_function_value = []

            for index in range(len(self.instrumental_box_array)):
                self.b.append(self.instrumental_box_array[index].b)
                self.b_fixed.append(self.instrumental_box_array[index].b_fixed)
                self.b_has_min.append(self.instrumental_box_array[index].b_has_min)
                self.b_min.append(self.instrumental_box_array[index].b_min)
                self.b_has_max.append(self.instrumental_box_array[index].b_has_max)
                self.b_max.append(self.instrumental_box_array[index].b_max)
                self.b_function.append(self.instrumental_box_array[index].b_function)
                self.b_function_value.append(self.instrumental_box_array[index].b_function_value)
        except Exception as e:
            self.b = copy.deepcopy(bkp_b)
            self.b_fixed = copy.deepcopy(bkp_b_fixed)
            self.b_has_min = copy.deepcopy(bkp_b_has_min)
            self.b_min = copy.deepcopy(bkp_b_min)
            self.b_has_max = copy.deepcopy(bkp_b_has_max)
            self.b_max = copy.deepcopy(bkp_b_max)
            self.b_function = copy.deepcopy(bkp_b_function)
            self.b_function_value = copy.deepcopy(bkp_b_function_value)

            if self.IS_DEVELOP: raise e

    def dump_c(self):
        bkp_c = copy.deepcopy(self.c)
        bkp_c_fixed = copy.deepcopy(self.c_fixed)
        bkp_c_has_min = copy.deepcopy(self.c_has_min)
        bkp_c_min = copy.deepcopy(self.c_min)
        bkp_c_has_max = copy.deepcopy(self.c_has_max)
        bkp_c_max = copy.deepcopy(self.c_max)
        bkp_c_function = copy.deepcopy(self.c_function)
        bkp_c_function_value = copy.deepcopy(self.c_function_value)

        try:
            self.c = []
            self.c_fixed = []
            self.c_has_min = []
            self.c_min = []
            self.c_has_max = []
            self.c_max = []
            self.c_function = []
            self.c_function_value = []

            for index in range(len(self.instrumental_box_array)):
                self.c.append(self.instrumental_box_array[index].c)
                self.c_fixed.append(self.instrumental_box_array[index].c_fixed)
                self.c_has_min.append(self.instrumental_box_array[index].c_has_min)
                self.c_min.append(self.instrumental_box_array[index].c_min)
                self.c_has_max.append(self.instrumental_box_array[index].c_has_max)
                self.c_max.append(self.instrumental_box_array[index].c_max)
                self.c_function.append(self.instrumental_box_array[index].c_function)
                self.c_function_value.append(self.instrumental_box_array[index].c_function_value)
        except Exception as e:
            self.c = copy.deepcopy(bkp_c)
            self.c_fixed = copy.deepcopy(bkp_c_fixed)
            self.c_has_min = copy.deepcopy(bkp_c_has_min)
            self.c_min = copy.deepcopy(bkp_c_min)
            self.c_has_max = copy.deepcopy(bkp_c_has_max)
            self.c_max = copy.deepcopy(bkp_c_max)
            self.c_function = copy.deepcopy(bkp_c_function)
            self.c_function_value = copy.deepcopy(bkp_c_function_value)

            if self.IS_DEVELOP: raise e

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QVBoxLayout
from orangecontrib.wonder.util.gui_utility import InnerBox


class InstrumentalProfileBox(InnerBox):
    U = 0.0
    V = 0.0
    W = 0.0
    a = 0.0
    b = 0.0
    c = 0.0

    U_fixed = 0
    V_fixed = 0
    W_fixed = 0
    a_fixed = 0
    b_fixed = 0
    c_fixed = 0

    U_has_min = 0
    V_has_min = 0
    W_has_min = 0
    a_has_min = 0
    b_has_min = 0
    c_has_min = 0

    U_min = 0.0
    V_min = 0.0
    W_min = 0.0
    a_min = 0.0
    b_min = 0.0
    c_min = 0.0

    U_has_max = 0
    V_has_max = 0
    W_has_max = 0
    a_has_max = 0
    b_has_max = 0
    c_has_max = 0

    U_max = 0.0
    V_max = 0.0
    W_max = 0.0
    a_max = 0.0
    b_max = 0.0
    c_max = 0.0

    U_function = 0
    V_function = 0
    W_function = 0
    a_function = 0
    b_function = 0
    c_function = 0

    U_function_value = ""
    V_function_value = ""
    W_function_value = ""
    a_function_value = ""
    b_function_value = ""
    c_function_value = ""


    widget = None
    is_on_init = True

    parameter_functions = {}

    index = 0

    def __init__(self,
                 widget=None,
                 parent=None,
                 index=0,
                 U=0.0,
                 V=0.0,
                 W=0.0,
                 a=0.0,
                 b=0.0,
                 c=0.0,
                 U_fixed=0,
                 V_fixed=0,
                 W_fixed=0,
                 a_fixed=0,
                 b_fixed=0,
                 c_fixed=0,
                 U_has_min=0,
                 V_has_min=0,
                 W_has_min=0,
                 a_has_min=0,
                 b_has_min=0,
                 c_has_min=0,
                 U_min=0.0,
                 V_min=0.0,
                 W_min=0.0,
                 a_min=0.0,
                 b_min=0.0,
                 c_min=0.0,
                 U_has_max=0,
                 V_has_max=0,
                 W_has_max=0,
                 a_has_max=0,
                 b_has_max=0,
                 c_has_max=0,
                 U_max=0.0,
                 V_max=0.0,
                 W_max=0.0,
                 a_max=0.0,
                 b_max=0.0,
                 c_max=0.0,
                 U_function=0,
                 V_function=0,
                 W_function=0,
                 a_function=0,
                 b_function=0,
                 c_function=0,
                 U_function_value="",
                 V_function_value="",
                 W_function_value="",
                 a_function_value="",
                 b_function_value="",
                 c_function_value=""):
        super(InstrumentalProfileBox, self).__init__()

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.setFixedWidth(widget.CONTROL_AREA_WIDTH - 35)
        self.setFixedHeight(500)

        self.widget = widget
        self.index = index

        self.U = U
        self.V = V
        self.W = W
        self.a = a
        self.b = b
        self.c = c

        self.U_fixed = U_fixed
        self.V_fixed = V_fixed
        self.W_fixed = W_fixed
        self.a_fixed = a_fixed
        self.b_fixed = b_fixed
        self.c_fixed = c_fixed

        self.U_has_min = U_has_min
        self.V_has_min = V_has_min
        self.W_has_min = W_has_min
        self.a_has_min = a_has_min
        self.b_has_min = b_has_min
        self.c_has_min = c_has_min

        self.U_min = U_min
        self.V_min = V_min
        self.W_min = W_min
        self.a_min = a_min
        self.b_min = b_min
        self.c_min = c_min

        self.U_has_max = U_has_max
        self.V_has_max = V_has_max
        self.W_has_max = W_has_max
        self.a_has_max = a_has_max
        self.b_has_max = b_has_max
        self.c_has_max = c_has_max

        self.U_max = U_max
        self.V_max = V_max
        self.W_max = W_max
        self.a_max = a_max
        self.b_max = b_max
        self.c_max = c_max

        self.U_function = U_function
        self.V_function = V_function
        self.W_function = W_function
        self.a_function = a_function
        self.b_function = b_function
        self.c_function = c_function

        self.U_function_value = U_function_value
        self.V_function_value = V_function_value
        self.W_function_value = W_function_value
        self.a_function_value = a_function_value
        self.b_function_value = b_function_value
        self.c_function_value = c_function_value


        self.CONTROL_AREA_WIDTH = widget.CONTROL_AREA_WIDTH

        parent.layout().addWidget(self)
        container = self

        caglioti_box_1 = gui.widgetBox(container, "Caglioti's FWHM", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 55)
        caglioti_box_2 = gui.widgetBox(container, "Caglioti's \u03b7", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 55)

        OWGenericWidget.create_box_in_widget(self, caglioti_box_1, "U", add_callback=True, trim=70)
        OWGenericWidget.create_box_in_widget(self, caglioti_box_1, "V", add_callback=True, trim=70)
        OWGenericWidget.create_box_in_widget(self, caglioti_box_1, "W", add_callback=True, trim=70)
        OWGenericWidget.create_box_in_widget(self, caglioti_box_2, "a", add_callback=True, trim=70)
        OWGenericWidget.create_box_in_widget(self, caglioti_box_2, "b", add_callback=True, trim=70)
        OWGenericWidget.create_box_in_widget(self, caglioti_box_2, "c", add_callback=True, trim=70)

        self.is_on_init = False

    def after_change_workspace_units(self):
        pass

    def set_index(self, index):
        self.index = index

    def callback_U(self):
        if not self.is_on_init: self.widget.dump_U()

    def callback_V(self):
        if not self.is_on_init: self.widget.dump_V()

    def callback_W(self):
        if not self.is_on_init: self.widget.dump_W()

    def callback_a(self):
        if not self.is_on_init: self.widget.dump_a()

    def callback_b(self):
        if not self.is_on_init: self.widget.dump_b()

    def callback_c(self):
        if not self.is_on_init: self.widget.dump_c()

    def after_change_workspace_units(self):
        pass

    def set_index(self, index):
        self.index = index

    def get_parameters_prefix(self):
        return Caglioti.get_parameters_prefix() + self.get_parameter_progressive()

    def get_parameter_progressive(self):
        return str(self.index + 1) + "_"

    def set_data(self, instrumental_parameter):
        OWGenericWidget.populate_fields_in_widget(self, "U", instrumental_parameter.U, value_only=True)
        OWGenericWidget.populate_fields_in_widget(self, "V", instrumental_parameter.V, value_only=True)
        OWGenericWidget.populate_fields_in_widget(self, "W", instrumental_parameter.W, value_only=True)
        OWGenericWidget.populate_fields_in_widget(self, "a", instrumental_parameter.a, value_only=True)
        OWGenericWidget.populate_fields_in_widget(self, "b", instrumental_parameter.b, value_only=True)
        OWGenericWidget.populate_fields_in_widget(self, "c", instrumental_parameter.c, value_only=True)

    def send_instrumental_profile(self):
        return Caglioti(U=OWGenericWidget.populate_parameter_in_widget(self, "U", self.get_parameters_prefix()),
                        V=OWGenericWidget.populate_parameter_in_widget(self, "V", self.get_parameters_prefix()),
                        W=OWGenericWidget.populate_parameter_in_widget(self, "W", self.get_parameters_prefix()),
                        a=OWGenericWidget.populate_parameter_in_widget(self, "a", self.get_parameters_prefix()),
                        b=OWGenericWidget.populate_parameter_in_widget(self, "b", self.get_parameters_prefix()),
                        c=OWGenericWidget.populate_parameter_in_widget(self, "c", self.get_parameters_prefix()))


if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = OWInstrumentalProfile()
    ow.show()
    a.exec_()
    ow.saveSettings()
