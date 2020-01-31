import sys, copy

from PyQt5.QtWidgets import QMessageBox, QApplication

from orangewidget.settings import Setting
from orangewidget import gui as orangegui
from orangewidget.widget import OWAction

from orangecontrib.wonder.widgets.gui.ow_generic_widget import OWGenericWidget
from orangecontrib.wonder.util.gui_utility import gui, ConfirmDialog

from orangecontrib.wonder.fit.parameters.fit_global_parameters import FitGlobalParameters
from orangecontrib.wonder.fit.parameters.instrument.background_parameters import ExpDecayBackground


class OWExpDecayBackground(OWGenericWidget):
    name = "ExpDecay Background"
    description = "Define ExpDecay background"
    icon = "icons/expdecay_background.png"
    priority = 11

    want_main_area = False

    use_single_parameter_set = Setting(0)

    a0 = Setting([0.0])
    b0 = Setting([0.0])
    a1 = Setting([0.0])
    b1 = Setting([0.0])
    a2 = Setting([0.0])
    b2 = Setting([0.0])
    a0_fixed = Setting([0])
    b0_fixed = Setting([0])
    a1_fixed = Setting([0])
    b1_fixed = Setting([0])
    a2_fixed = Setting([0])
    b2_fixed = Setting([0])
    a0_has_min = Setting([0])
    b0_has_min = Setting([0])
    a1_has_min = Setting([0])
    b1_has_min = Setting([0])
    a2_has_min = Setting([0])
    b2_has_min = Setting([0])
    a0_min = Setting([0.0])
    b0_min = Setting([0.0])
    a1_min = Setting([0.0])
    b1_min = Setting([0.0])
    a2_min = Setting([0.0])
    b2_min = Setting([0.0])
    a0_has_max = Setting([0])
    b0_has_max = Setting([0])
    a1_has_max = Setting([0])
    b1_has_max = Setting([0])
    a2_has_max = Setting([0])
    b2_has_max = Setting([0])
    a0_max = Setting([0.0])
    b0_max = Setting([0.0])
    a1_max = Setting([0.0])
    b1_max = Setting([0.0])
    a2_max = Setting([0.0])
    b2_max = Setting([0.0])
    a0_function = Setting([0])
    b0_function = Setting([0])
    a1_function = Setting([0])
    b1_function = Setting([0])
    a2_function = Setting([0])
    b2_function = Setting([0])
    a0_function_value = Setting([""])
    b0_function_value = Setting([""])
    a1_function_value = Setting([""])
    b1_function_value = Setting([""])
    a2_function_value = Setting([""])
    b2_function_value = Setting([""])

    inputs = [("Fit Global Parameters", FitGlobalParameters, 'set_data')]
    outputs = [("Fit Global Parameters", FitGlobalParameters)]

    def __init__(self):
        super().__init__(show_automatic_box=True)

        main_box = gui.widgetBox(self.controlArea,
                                 "Exponential Background", orientation="vertical",
                                 width=self.CONTROL_AREA_WIDTH - 10, height=600)

        button_box = gui.widgetBox(main_box,
                                   "", orientation="horizontal",
                                   width=self.CONTROL_AREA_WIDTH - 25)

        gui.button(button_box, self, "Send Background", height=40, callback=self.send_background)

        orangegui.comboBox(main_box, self, "use_single_parameter_set", label="Use single set of Parameters", labelWidth=350, orientation="horizontal",
                           items=["No", "Yes"], callback=self.set_use_single_parameter_set, sendSelectedValue=False)

        orangegui.separator(main_box)

        self.expdecay_tabs = gui.tabWidget(main_box)

        self.set_use_single_parameter_set(on_init=True)

        runaction = OWAction("Send Background", self)
        runaction.triggered.connect(self.send_background)
        self.addAction(runaction)

        orangegui.rubber(self.controlArea)

    def set_use_single_parameter_set(self, on_init=False, recycle=True):
        self.expdecay_tabs.clear()
        self.expdecay_box_array = []

        dimension = len(self.a0) if self.fit_global_parameters is None else self.fit_global_parameters.measured_dataset.get_diffraction_patterns_number()

        for index in range(1 if self.use_single_parameter_set == 1 else dimension):
            expdecay_tab = gui.createTabPage(self.expdecay_tabs, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, index, self.use_single_parameter_set == 1))

            if index < len(self.a0) and recycle:  # keep the existing
                expdecay_box = ExpDecayBackgroundBox(widget=self,
                                                       parent=expdecay_tab,
                                                       index=index,
                                                       a0=self.a0[index],
                                                       b0=self.b0[index],
                                                       a1=self.a1[index],
                                                       b1=self.b1[index],
                                                       a2=self.a2[index],
                                                       b2=self.b2[index],
                                                       a0_fixed=self.a0_fixed[index],
                                                       b0_fixed=self.b0_fixed[index],
                                                       a1_fixed=self.a1_fixed[index],
                                                       b1_fixed=self.b1_fixed[index],
                                                       a2_fixed=self.a2_fixed[index],
                                                       b2_fixed=self.b2_fixed[index],
                                                       a0_has_min=self.a0_has_min[index],
                                                       b0_has_min=self.b0_has_min[index],
                                                       a1_has_min=self.a1_has_min[index],
                                                       b1_has_min=self.b1_has_min[index],
                                                       a2_has_min=self.a2_has_min[index],
                                                       b2_has_min=self.b2_has_min[index],
                                                       a0_min=self.a0_min[index],
                                                       b0_min=self.b0_min[index],
                                                       a1_min=self.a1_min[index],
                                                       b1_min=self.b1_min[index],
                                                       a2_min=self.a2_min[index],
                                                       b2_min=self.b2_min[index],
                                                       a0_has_max=self.a0_has_max[index],
                                                       b0_has_max=self.b0_has_max[index],
                                                       a1_has_max=self.a1_has_max[index],
                                                       b1_has_max=self.b1_has_max[index],
                                                       a2_has_max=self.a2_has_max[index],
                                                       b2_has_max=self.b2_has_max[index],
                                                       a0_max=self.a0_max[index],
                                                       b0_max=self.b0_max[index],
                                                       a1_max=self.a1_max[index],
                                                       b1_max=self.b1_max[index],
                                                       a2_max=self.a2_max[index],
                                                       b2_max=self.b2_max[index],
                                                       a0_function=self.a0_function[index],
                                                       b0_function=self.b0_function[index],
                                                       a1_function=self.a1_function[index],
                                                       b1_function=self.b1_function[index],
                                                       a2_function=self.a2_function[index],
                                                       b2_function=self.b2_function[index],
                                                       a0_function_value=self.a0_function_value[index],
                                                       b0_function_value=self.b0_function_value[index],
                                                       a1_function_value=self.a1_function_value[index],
                                                       b1_function_value=self.b1_function_value[index],
                                                       a2_function_value=self.a2_function_value[index],
                                                       b2_function_value=self.b2_function_value[index])
            else:
                expdecay_box = ExpDecayBackgroundBox(widget=self, parent=expdecay_tab, index=index)

            self.expdecay_box_array.append(expdecay_box)

            if not on_init: self.dumpSettings()

    def send_background(self):
        try:
            if not self.fit_global_parameters is None:
                self.dumpSettings()

                self.fit_global_parameters.set_background_parameters([self.expdecay_box_array[index].send_background() for index in range(len(self.a0))])
                self.fit_global_parameters.regenerate_parameters()

                self.send("Fit Global Parameters", self.fit_global_parameters)

        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 str(e),
                                 QMessageBox.Ok)

            if self.IS_DEVELOP: raise e

    def __check_data_congruence(self, background_parameters):
        if (len(background_parameters) == 1 and self.use_single_parameter_set == 0) or (len(background_parameters) > 1 and self.use_single_parameter_set == 1):
            raise ValueError("Previous Exponential Decay parameters are incongruent with the current choice of using a single set")

    def set_data(self, data):
        if not data is None:
            try:
                self.fit_global_parameters = data.duplicate()

                diffraction_patterns = self.fit_global_parameters.measured_dataset.diffraction_patterns
                if diffraction_patterns is None: raise ValueError("No Diffraction Pattern in input data!")

                background_parameters = self.fit_global_parameters.get_background_parameters(ExpDecayBackground.__name__)

                if self.use_single_parameter_set == 0:  # NO
                    if background_parameters is None:
                        if len(diffraction_patterns) != len(self.expdecay_box_array):
                            self.set_use_single_parameter_set(recycle=ConfirmDialog.confirmed(message="Number of Diffraction Patterns changed:\ndo you want to use the existing data where possible?\n\nIf yes, check for possible incongruences", title="Warning"))
                        else:
                            self.set_use_single_parameter_set(True)
                    else:
                        # self.__check_data_congruence(background_parameters)

                        tabs_to_remove = len(self.a0) - len(background_parameters)

                        if tabs_to_remove > 0:
                            for index in range(tabs_to_remove):
                                self.expdecay_tabs.removeTab(-1)
                                self.expdecay_box_array.pop()

                        for diffraction_pattern_index in range(len(background_parameters)):
                            background_parameters_item = self.fit_global_parameters.get_background_parameters_item(ExpDecayBackground.__name__, diffraction_pattern_index)

                            if diffraction_pattern_index < len(self.a0):
                                self.expdecay_tabs.setTabText(diffraction_pattern_index,
                                                               OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, diffraction_pattern_index, False))

                                expdecay_box = self.expdecay_box_array[diffraction_pattern_index]
                                if not background_parameters_item is None: expdecay_box.set_data(background_parameters_item)
                            else:
                                expdecay_box = ExpDecayBackgroundBox(widget=self,
                                                                       parent=gui.createTabPage(self.expdecay_tabs, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, diffraction_pattern_index, False)),
                                                                       index=diffraction_pattern_index)

                                if not background_parameters_item is None: expdecay_box.set_data(background_parameters_item)

                                self.expdecay_box_array.append(expdecay_box)
                else:
                    if background_parameters is None:
                        self.set_use_single_parameter_set(True)
                    else:
                        self.__check_data_congruence(background_parameters)

                        background_parameters_item = self.fit_global_parameters.get_background_parameters_item(ExpDecayBackground.__name__, 0)

                        self.expdecay_tabs.setTabText(0, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, 0, True))
                        if not background_parameters_item is None: self.expdecay_box_array[0].set_data(background_parameters_item)

                self.dumpSettings()

                if self.is_automatic_run:
                    self.send_background()

            except Exception as e:
                QMessageBox.critical(self, "Error",
                                     str(e),
                                     QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def dumpSettings(self):
        self.dump_a0()
        self.dump_b0()
        self.dump_a1()
        self.dump_b1()
        self.dump_a2()
        self.dump_b2()

    def dump_a0(self):
        bkp_a0 = copy.deepcopy(self.a0)
        bkp_a0_fixed = copy.deepcopy(self.a0_fixed)
        bkp_a0_has_min = copy.deepcopy(self.a0_has_min)
        bkp_a0_min = copy.deepcopy(self.a0_min)
        bkp_a0_has_max = copy.deepcopy(self.a0_has_max)
        bkp_a0_max = copy.deepcopy(self.a0_max)
        bkp_a0_function = copy.deepcopy(self.a0_function)
        bkp_a0_function_value = copy.deepcopy(self.a0_function_value)

        try:
            self.a0 = []
            self.a0_fixed = []
            self.a0_has_min = []
            self.a0_min = []
            self.a0_has_max = []
            self.a0_max = []
            self.a0_function = []
            self.a0_function_value = []

            for index in range(len(self.expdecay_box_array)):
                self.a0.append(self.expdecay_box_array[index].a0)
                self.a0_fixed.append(self.expdecay_box_array[index].a0_fixed)
                self.a0_has_min.append(self.expdecay_box_array[index].a0_has_min)
                self.a0_min.append(self.expdecay_box_array[index].a0_min)
                self.a0_has_max.append(self.expdecay_box_array[index].a0_has_max)
                self.a0_max.append(self.expdecay_box_array[index].a0_max)
                self.a0_function.append(self.expdecay_box_array[index].a0_function)
                self.a0_function_value.append(self.expdecay_box_array[index].a0_function_value)
        except:
            self.a0 = copy.deepcopy(bkp_a0)
            self.a0_fixed = copy.deepcopy(bkp_a0_fixed)
            self.a0_has_min = copy.deepcopy(bkp_a0_has_min)
            self.a0_min = copy.deepcopy(bkp_a0_min)
            self.a0_has_max = copy.deepcopy(bkp_a0_has_max)
            self.a0_max = copy.deepcopy(bkp_a0_max)
            self.a0_function = copy.deepcopy(bkp_a0_function)
            self.a0_function_value = copy.deepcopy(bkp_a0_function_value)

    def dump_b0(self):
        bkp_b0 = copy.deepcopy(self.b0)
        bkp_b0_fixed = copy.deepcopy(self.b0_fixed)
        bkp_b0_has_min = copy.deepcopy(self.b0_has_min)
        bkp_b0_min = copy.deepcopy(self.b0_min)
        bkp_b0_has_max = copy.deepcopy(self.b0_has_max)
        bkp_b0_max = copy.deepcopy(self.b0_max)
        bkp_b0_function = copy.deepcopy(self.b0_function)
        bkp_b0_function_value = copy.deepcopy(self.b0_function_value)

        try:
            self.b0 = []
            self.b0_fixed = []
            self.b0_has_min = []
            self.b0_min = []
            self.b0_has_max = []
            self.b0_max = []
            self.b0_function = []
            self.b0_function_value = []

            for index in range(len(self.expdecay_box_array)):
                self.b0.append(self.expdecay_box_array[index].b0)
                self.b0_fixed.append(self.expdecay_box_array[index].b0_fixed)
                self.b0_has_min.append(self.expdecay_box_array[index].b0_has_min)
                self.b0_min.append(self.expdecay_box_array[index].b0_min)
                self.b0_has_max.append(self.expdecay_box_array[index].b0_has_max)
                self.b0_max.append(self.expdecay_box_array[index].b0_max)
                self.b0_function.append(self.expdecay_box_array[index].b0_function)
                self.b0_function_value.append(self.expdecay_box_array[index].b0_function_value)
        except:
            self.b0 = copy.deepcopy(bkp_b0)
            self.b0_fixed = copy.deepcopy(bkp_b0_fixed)
            self.b0_has_min = copy.deepcopy(bkp_b0_has_min)
            self.b0_min = copy.deepcopy(bkp_b0_min)
            self.b0_has_max = copy.deepcopy(bkp_b0_has_max)
            self.b0_max = copy.deepcopy(bkp_b0_max)
            self.b0_function = copy.deepcopy(bkp_b0_function)
            self.b0_function_value = copy.deepcopy(bkp_b0_function_value)

    def dump_a1(self):
        bkp_a1 = copy.deepcopy(self.a1)
        bkp_a1_fixed = copy.deepcopy(self.a1_fixed)
        bkp_a1_has_min = copy.deepcopy(self.a1_has_min)
        bkp_a1_min = copy.deepcopy(self.a1_min)
        bkp_a1_has_max = copy.deepcopy(self.a1_has_max)
        bkp_a1_max = copy.deepcopy(self.a1_max)
        bkp_a1_function = copy.deepcopy(self.a1_function)
        bkp_a1_function_value = copy.deepcopy(self.a1_function_value)

        try:
            self.a1 = []
            self.a1_fixed = []
            self.a1_has_min = []
            self.a1_min = []
            self.a1_has_max = []
            self.a1_max = []
            self.a1_function = []
            self.a1_function_value = []

            for index in range(len(self.expdecay_box_array)):
                self.a1.append(self.expdecay_box_array[index].a1)
                self.a1_fixed.append(self.expdecay_box_array[index].a1_fixed)
                self.a1_has_min.append(self.expdecay_box_array[index].a1_has_min)
                self.a1_min.append(self.expdecay_box_array[index].a1_min)
                self.a1_has_max.append(self.expdecay_box_array[index].a1_has_max)
                self.a1_max.append(self.expdecay_box_array[index].a1_max)
                self.a1_function.append(self.expdecay_box_array[index].a1_function)
                self.a1_function_value.append(self.expdecay_box_array[index].a1_function_value)
        except:
            self.a1 = copy.deepcopy(bkp_a1)
            self.a1_fixed = copy.deepcopy(bkp_a1_fixed)
            self.a1_has_min = copy.deepcopy(bkp_a1_has_min)
            self.a1_min = copy.deepcopy(bkp_a1_min)
            self.a1_has_max = copy.deepcopy(bkp_a1_has_max)
            self.a1_max = copy.deepcopy(bkp_a1_max)
            self.a1_function = copy.deepcopy(bkp_a1_function)
            self.a1_function_value = copy.deepcopy(bkp_a1_function_value)

    def dump_b1(self):
        bkp_b1 = copy.deepcopy(self.b1)
        bkp_b1_fixed = copy.deepcopy(self.b1_fixed)
        bkp_b1_has_min = copy.deepcopy(self.b1_has_min)
        bkp_b1_min = copy.deepcopy(self.b1_min)
        bkp_b1_has_max = copy.deepcopy(self.b1_has_max)
        bkp_b1_max = copy.deepcopy(self.b1_max)
        bkp_b1_function = copy.deepcopy(self.b1_function)
        bkp_b1_function_value = copy.deepcopy(self.b1_function_value)

        try:
            self.b1 = []
            self.b1_fixed = []
            self.b1_has_min = []
            self.b1_min = []
            self.b1_has_max = []
            self.b1_max = []
            self.b1_function = []
            self.b1_function_value = []

            for index in range(len(self.expdecay_box_array)):
                self.b1.append(self.expdecay_box_array[index].b1)
                self.b1_fixed.append(self.expdecay_box_array[index].b1_fixed)
                self.b1_has_min.append(self.expdecay_box_array[index].b1_has_min)
                self.b1_min.append(self.expdecay_box_array[index].b1_min)
                self.b1_has_max.append(self.expdecay_box_array[index].b1_has_max)
                self.b1_max.append(self.expdecay_box_array[index].b1_max)
                self.b1_function.append(self.expdecay_box_array[index].b1_function)
                self.b1_function_value.append(self.expdecay_box_array[index].b1_function_value)
        except:
            self.b1 = copy.deepcopy(bkp_b1)
            self.b1_fixed = copy.deepcopy(bkp_b1_fixed)
            self.b1_has_min = copy.deepcopy(bkp_b1_has_min)
            self.b1_min = copy.deepcopy(bkp_b1_min)
            self.b1_has_max = copy.deepcopy(bkp_b1_has_max)
            self.b1_max = copy.deepcopy(bkp_b1_max)
            self.b1_function = copy.deepcopy(bkp_b1_function)
            self.b1_function_value = copy.deepcopy(bkp_b1_function_value)

    def dump_a2(self):
        bkp_a2 = copy.deepcopy(self.a2)
        bkp_a2_fixed = copy.deepcopy(self.a2_fixed)
        bkp_a2_has_min = copy.deepcopy(self.a2_has_min)
        bkp_a2_min = copy.deepcopy(self.a2_min)
        bkp_a2_has_max = copy.deepcopy(self.a2_has_max)
        bkp_a2_max = copy.deepcopy(self.a2_max)
        bkp_a2_function = copy.deepcopy(self.a2_function)
        bkp_a2_function_value = copy.deepcopy(self.a2_function_value)

        try:
            self.a2 = []
            self.a2_fixed = []
            self.a2_has_min = []
            self.a2_min = []
            self.a2_has_max = []
            self.a2_max = []
            self.a2_function = []
            self.a2_function_value = []

            for index in range(len(self.expdecay_box_array)):
                self.a2.append(self.expdecay_box_array[index].a2)
                self.a2_fixed.append(self.expdecay_box_array[index].a2_fixed)
                self.a2_has_min.append(self.expdecay_box_array[index].a2_has_min)
                self.a2_min.append(self.expdecay_box_array[index].a2_min)
                self.a2_has_max.append(self.expdecay_box_array[index].a2_has_max)
                self.a2_max.append(self.expdecay_box_array[index].a2_max)
                self.a2_function.append(self.expdecay_box_array[index].a2_function)
                self.a2_function_value.append(self.expdecay_box_array[index].a2_function_value)
        except:
            self.a2 = copy.deepcopy(bkp_a2)
            self.a2_fixed = copy.deepcopy(bkp_a2_fixed)
            self.a2_has_min = copy.deepcopy(bkp_a2_has_min)
            self.a2_min = copy.deepcopy(bkp_a2_min)
            self.a2_has_max = copy.deepcopy(bkp_a2_has_max)
            self.a2_max = copy.deepcopy(bkp_a2_max)
            self.a2_function = copy.deepcopy(bkp_a2_function)
            self.a2_function_value = copy.deepcopy(bkp_a2_function_value)

    def dump_b2(self):
        bkp_b2 = copy.deepcopy(self.b2)
        bkp_b2_fixed = copy.deepcopy(self.b2_fixed)
        bkp_b2_has_min = copy.deepcopy(self.b2_has_min)
        bkp_b2_min = copy.deepcopy(self.b2_min)
        bkp_b2_has_max = copy.deepcopy(self.b2_has_max)
        bkp_b2_max = copy.deepcopy(self.b2_max)
        bkp_b2_function = copy.deepcopy(self.b2_function)
        bkp_b2_function_value = copy.deepcopy(self.b2_function_value)

        try:
            self.b2 = []
            self.b2_fixed = []
            self.b2_has_min = []
            self.b2_min = []
            self.b2_has_max = []
            self.b2_max = []
            self.b2_function = []
            self.b2_function_value = []

            for index in range(len(self.expdecay_box_array)):
                self.b2.append(self.expdecay_box_array[index].b2)
                self.b2_fixed.append(self.expdecay_box_array[index].b2_fixed)
                self.b2_has_min.append(self.expdecay_box_array[index].b2_has_min)
                self.b2_min.append(self.expdecay_box_array[index].b2_min)
                self.b2_has_max.append(self.expdecay_box_array[index].b2_has_max)
                self.b2_max.append(self.expdecay_box_array[index].b2_max)
                self.b2_function.append(self.expdecay_box_array[index].b2_function)
                self.b2_function_value.append(self.expdecay_box_array[index].b2_function_value)
        except:
            self.b2 = copy.deepcopy(bkp_b2)
            self.b2_fixed = copy.deepcopy(bkp_b2_fixed)
            self.b2_has_min = copy.deepcopy(bkp_b2_has_min)
            self.b2_min = copy.deepcopy(bkp_b2_min)
            self.b2_has_max = copy.deepcopy(bkp_b2_has_max)
            self.b2_max = copy.deepcopy(bkp_b2_max)
            self.b2_function = copy.deepcopy(bkp_b2_function)
            self.b2_function_value = copy.deepcopy(bkp_b2_function_value)


from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QVBoxLayout
from orangecontrib.wonder.util.gui_utility import InnerBox


class ExpDecayBackgroundBox(InnerBox):
    widget = None
    is_on_init = True

    parameter_functions = {}

    index = 0

    def __init__(self,
                 widget=None,
                 parent=None,
                 index=0,
                 a0=0.0,
                 b0=0.0,
                 a1=0.0,
                 b1=0.0,
                 a2=0.0,
                 b2=0.0,
                 a0_fixed=0,
                 b0_fixed=0,
                 a1_fixed=0,
                 b1_fixed=0,
                 a2_fixed=0,
                 b2_fixed=0,
                 a0_has_min=0,
                 b0_has_min=0,
                 a1_has_min=0,
                 b1_has_min=0,
                 a2_has_min=0,
                 b2_has_min=0,
                 a0_min=0.0,
                 b0_min=0.0,
                 a1_min=0.0,
                 b1_min=0.0,
                 a2_min=0.0,
                 b2_min=0.0,
                 a0_has_max=0,
                 b0_has_max=0,
                 a1_has_max=0,
                 b1_has_max=0,
                 a2_has_max=0,
                 b2_has_max=0,
                 a0_max=0.0,
                 b0_max=0.0,
                 a1_max=0.0,
                 b1_max=0.0,
                 a2_max=0.0,
                 b2_max=0.0,
                 a0_function=0,
                 b0_function=0,
                 a1_function=0,
                 b1_function=0,
                 a2_function=0,
                 b2_function=0,
                 a0_function_value="",
                 b0_function_value="",
                 a1_function_value="",
                 b1_function_value="",
                 a2_function_value="",
                 b2_function_value=""):
        super(ExpDecayBackgroundBox, self).__init__()

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.setFixedWidth(widget.CONTROL_AREA_WIDTH - 35)
        self.setFixedHeight(500)

        self.widget = widget
        self.index = index

        self.a0 = a0
        self.b0 = b0
        self.a1 = a1
        self.b1 = b1
        self.a2 = a2
        self.b2 = b2
        self.a0_fixed = a0_fixed
        self.b0_fixed = b0_fixed
        self.a1_fixed = a1_fixed
        self.b1_fixed = b1_fixed
        self.a2_fixed = a2_fixed
        self.b2_fixed = b2_fixed
        self.a0_has_min = a0_has_min
        self.b0_has_min = b0_has_min
        self.a1_has_min = a1_has_min
        self.b1_has_min = b1_has_min
        self.a2_has_min = a2_has_min
        self.b2_has_min = b2_has_min
        self.a0_min = a0_min
        self.b0_min = b0_min
        self.a1_min = a1_min
        self.b1_min = b1_min
        self.a2_min = a2_min
        self.b2_min = b2_min
        self.a0_has_max = a0_has_max
        self.b0_has_max = b0_has_max
        self.a1_has_max = a1_has_max
        self.b1_has_max = b1_has_max
        self.a2_has_max = a2_has_max
        self.b2_has_max = b2_has_max
        self.a0_max = a0_max
        self.b0_max = b0_max
        self.a1_max = a1_max
        self.b1_max = b1_max
        self.a2_max = a2_max
        self.b2_max = b2_max
        self.a0_function = a0_function
        self.b0_function = b0_function
        self.a1_function = a1_function
        self.b1_function = b1_function
        self.a2_function = a2_function
        self.b2_function = b2_function
        self.a0_function_value = a0_function_value
        self.b0_function_value = b0_function_value
        self.a1_function_value = a1_function_value
        self.b1_function_value = b1_function_value
        self.a2_function_value = a2_function_value
        self.b2_function_value = b2_function_value

        self.CONTROL_AREA_WIDTH = widget.CONTROL_AREA_WIDTH

        parent.layout().addWidget(self)
        container = self

        OWGenericWidget.create_box_in_widget(self, container, "a0", add_callback=True, trim=25)
        OWGenericWidget.create_box_in_widget(self, container, "b0", add_callback=True, trim=25)
        OWGenericWidget.create_box_in_widget(self, container, "a1", add_callback=True, trim=25)
        OWGenericWidget.create_box_in_widget(self, container, "b1", add_callback=True, trim=25)
        OWGenericWidget.create_box_in_widget(self, container, "a2", add_callback=True, trim=25)
        OWGenericWidget.create_box_in_widget(self, container, "b2", add_callback=True, trim=25)

        self.is_on_init = False

    def after_change_workspace_units(self):
        pass

    def set_index(self, index):
        self.index = index

    def callback_a0(self):
        if not self.is_on_init: self.widget.dump_a0()

    def callback_b0(self):
        if not self.is_on_init: self.widget.dump_b0()

    def callback_a1(self):
        if not self.is_on_init: self.widget.dump_a1()

    def callback_b1(self):
        if not self.is_on_init: self.widget.dump_b1()

    def callback_a2(self):
        if not self.is_on_init: self.widget.dump_a2()

    def callback_b2(self):
        if not self.is_on_init: self.widget.dump_b2()

    def after_change_workspace_units(self):
        pass

    def set_index(self, index):
        self.index = index

    def get_parameters_prefix(self):
        return ExpDecayBackground.get_parameters_prefix() + self.get_parameter_progressive()

    def get_parameter_progressive(self):
        return str(self.index + 1) + "_"

    def set_data(self, background_parameters):
        OWGenericWidget.populate_fields_in_widget(self, "a0", background_parameters.a0, value_only=True)
        OWGenericWidget.populate_fields_in_widget(self, "b0", background_parameters.b0, value_only=True)
        OWGenericWidget.populate_fields_in_widget(self, "a1", background_parameters.a1, value_only=True)
        OWGenericWidget.populate_fields_in_widget(self, "b1", background_parameters.b1, value_only=True)
        OWGenericWidget.populate_fields_in_widget(self, "a2", background_parameters.a2, value_only=True)
        OWGenericWidget.populate_fields_in_widget(self, "b2", background_parameters.b2, value_only=True)

    def send_background(self):
        return ExpDecayBackground(a0=OWGenericWidget.populate_parameter_in_widget(self, "a0", self.get_parameters_prefix()),
                                   b0=OWGenericWidget.populate_parameter_in_widget(self, "b0", self.get_parameters_prefix()),
                                   a1=OWGenericWidget.populate_parameter_in_widget(self, "a1", self.get_parameters_prefix()),
                                   b1=OWGenericWidget.populate_parameter_in_widget(self, "b1", self.get_parameters_prefix()),
                                   a2=OWGenericWidget.populate_parameter_in_widget(self, "a2", self.get_parameters_prefix()),
                                   b2=OWGenericWidget.populate_parameter_in_widget(self, "b2", self.get_parameters_prefix()))


if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = OWExpDecayBackground()
    ow.show()
    a.exec_()
    ow.saveSettings()
