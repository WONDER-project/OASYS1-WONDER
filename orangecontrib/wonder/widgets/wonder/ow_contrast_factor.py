import sys, copy

from PyQt5.QtWidgets import QMessageBox, QApplication


from orangewidget.settings import Setting
from orangewidget import gui as orangegui
from orangewidget.widget import OWAction

from orangecontrib.wonder.widgets.gui.ow_generic_widget import OWGenericWidget
from orangecontrib.wonder.util.gui_utility import gui
from orangecontrib.wonder.util import congruence
from orangecontrib.wonder.fit.parameters.fit_parameter import FitParameter
from orangecontrib.wonder.fit.parameters.fit_global_parameters import FitGlobalParameters
from orangecontrib.wonder.fit.parameters.microstructure.constrast_factor import calculate_A_B_coefficients
from orangecontrib.wonder.fit.parameters.microstructure.strain import KrivoglazWilkensModel
from orangecontrib.wonder.fit.parameters.measured_data.phase import Phase

class OWContrastFactor(OWGenericWidget):

    name = "Contrast Factor Calculator"
    description = "Contrast Factor Calculator"
    icon = "icons/contrast_factor.png"
    priority = 18

    want_main_area = False

    active = Setting([1])
    c11    = Setting([24.65])
    c12    = Setting([13.45])
    c44    = Setting([2.87])

    inputs = [("Fit Global Parameters", FitGlobalParameters, 'set_data')]
    outputs = [("Fit Global Parameters", FitGlobalParameters)]

    def __init__(self):
        super().__init__(show_automatic_box=True)

        main_box = gui.widgetBox(self.controlArea,
                                 "Constrast Factor Calculator Parameters", orientation="vertical",
                                 width=self.CONTROL_AREA_WIDTH - 10, height=600)

        button_box = gui.widgetBox(main_box,
                                   "", orientation="horizontal",
                                   width=self.CONTROL_AREA_WIDTH-25)

        gui.button(button_box, self, "Send Constrast Factor A/B Parameters", height=40, callback=self.send_contrast_factors_a_b)

        self.strains_tabs = gui.tabWidget(main_box)
        self.strains_box_array = []

        for index in range(len(self.c11)):
            strain_box = StrainBox(widget=self,
                                   parent=gui.createTabPage(self.strains_tabs, Phase.get_default_name(index)),
                                   index = index,
                                   active = self.active[index],
                                   c11=self.c11[index],
                                   c12=self.c12[index],
                                   c44=self.c44[index])

            self.strains_box_array.append(strain_box)

        runaction = OWAction("Send Strain", self)
        runaction.triggered.connect(self.send_contrast_factors_a_b)
        self.addAction(runaction)

        orangegui.rubber(self.controlArea)

    def set_data(self, data):
        if not data is None:
            try:
                self.fit_global_parameters = data.duplicate()

                if self.fit_global_parameters.measured_dataset is None:
                    raise ValueError("Calculation is not possibile, Measured Dataset is missing")

                if self.fit_global_parameters.measured_dataset.phases is None:
                    raise ValueError("Calculation is not possibile, Phases are missing")

                if not self.fit_global_parameters.strain_parameters is None:
                    raise Exception("This widget should be put BEFORE the strain model widget")

                phases = self.fit_global_parameters.measured_dataset.phases

                if phases is None: raise ValueError("No Phases in input data!")

                tabs_to_remove = len(self.c11) - len(phases)

                if tabs_to_remove > 0:
                    for index in range(tabs_to_remove):
                        self.strains_tabs.removeTab(-1)
                        self.strains_box_array.pop()

                for phase_index in range(len(phases)):
                    if phase_index < len(self.c11):
                        self.strains_tabs.setTabText(phase_index, phases[phase_index].get_name(phase_index))
                    else:
                        self.strains_box_array.append(StrainBox(widget=self,
                                                                parent=gui.createTabPage(self.strains_tabs, phases[phase_index].get_name(phase_index)),
                                                                index=phase_index,
                                                                active=0))

                self.dumpSettings()

                if self.is_automatic_run:
                    self.send_contrast_factors_a_b()

            except Exception as e:
                QMessageBox.critical(self, "Error",
                                     str(e),
                                     QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def send_contrast_factors_a_b(self):
        try:
            if not self.fit_global_parameters is None:
                self.dumpSettings()

                self.fit_global_parameters.set_strain_parameters([self.strains_box_array[index].get_strain_parameters() for index in range(len(self.strains_box_array))])
                self.fit_global_parameters.evaluate_functions()

                self.fit_global_parameters.regenerate_parameters()

                self.send("Fit Global Parameters", self.fit_global_parameters)
        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 str(e),
                                 QMessageBox.Ok)

            if self.IS_DEVELOP: raise e

    ##############################
    # SINGLE FIELDS SIGNALS
    ##############################

    def dumpSettings(self):
        self.dump_active()
        self.dump_c11()
        self.dump_c12()
        self.dump_c44()

    def dump_active(self):
        bkp_active = copy.deepcopy(self.active)

        try:
            self.active = []

            for index in range(len(self.strains_box_array)):
                self.active.append(self.strains_box_array[index].active)
        except Exception as e:
            self.active = copy.deepcopy(bkp_active)

            if self.IS_DEVELOP: raise e

    def dump_c11(self):
        bkp_c11 = copy.deepcopy(self.c11)

        try:
            self.c11 = []

            for index in range(len(self.strains_box_array)):
                self.c11.append(self.strains_box_array[index].c11)
        except Exception as e:
            self.c11 = copy.deepcopy(bkp_c11)

            if self.IS_DEVELOP: raise e

    def dump_c12(self):
        bkp_c12 = copy.deepcopy(self.c12)

        try:
            self.c12 = []

            for index in range(len(self.strains_box_array)):
                self.c12.append(self.strains_box_array[index].c12)
        except Exception as e:
            self.c12 = copy.deepcopy(bkp_c12)

            if self.IS_DEVELOP: raise e

    def dump_c44(self):
        bkp_c44 = copy.deepcopy(self.c44)

        try:
            self.c44 = []

            for index in range(len(self.strains_box_array)):
                self.c44.append(self.strains_box_array[index].c44)
        except Exception as e:
            self.c44 = copy.deepcopy(bkp_c44)

            if self.IS_DEVELOP: raise e
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
from orangecontrib.wonder.util.gui_utility import InnerBox

class StrainBox(InnerBox):
    active = 1
    c11    = 0.0
    c12    = 0.0
    c44    = 0.0

    widget = None
    is_on_init = True

    parameter_functions = {}

    index = 0

    def __init__(self,
                 widget=None,
                 parent=None,
                 index=0,
                 active=1,
                 c11=0.0,
                 c12=0.0,
                 c44=0.0):
        super(StrainBox, self).__init__()

        self.widget = widget

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.setFixedWidth(widget.CONTROL_AREA_WIDTH - 35)
        self.setFixedHeight(300)

        self.index = index

        self.active = active
        self.c11 = c11
        self.c12 = c12
        self.c44 = c44

        self.CONTROL_AREA_WIDTH = widget.CONTROL_AREA_WIDTH - 45

        parent.layout().addWidget(self)
        container = self

        self.cb_active = orangegui.comboBox(container, self, "active", label="Active", items=["No", "Yes"], callback=self.set_active, orientation="horizontal")

        self.main_box = gui.widgetBox(container, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 10)

        contrast_factor_box = gui.widgetBox(self.main_box, "Elastic Constants", orientation="vertical", height=300, width=self.CONTROL_AREA_WIDTH - 10)

        gui.lineEdit(contrast_factor_box, self, "c11", "c11", labelWidth=90, valueType=float, callback=widget.dump_c11)
        gui.lineEdit(contrast_factor_box, self, "c12", "c12", labelWidth=90, valueType=float, callback=widget.dump_c12)
        gui.lineEdit(contrast_factor_box, self, "c44", "c44", labelWidth=90, valueType=float, callback=widget.dump_c44)

        text_area_box = gui.widgetBox(contrast_factor_box, "Calculation Result", orientation="vertical", height=160, width=self.CONTROL_AREA_WIDTH - 20)

        self.text_area = gui.textArea(height=120, width=self.CONTROL_AREA_WIDTH - 40, readOnly=True)
        self.text_area.setText("")

        text_area_box.layout().addWidget(self.text_area)

        self.set_active()

        self.is_on_init = False

    def after_change_workspace_units(self):
        pass

    def set_index(self, index):
        self.index = index

    def set_active(self):
        self.main_box.setEnabled(self.active == 1)

        if not self.is_on_init: self.widget.dump_active()

    def get_parameters_prefix(self):
        return KrivoglazWilkensModel.get_parameters_prefix() + self.get_parameter_progressive()

    def get_parameter_progressive(self):
        return str(self.index + 1) + "_"

    def get_strain_parameters(self):
        if self.active == 0:
            return None
        else:
            congruence.checkStrictlyPositiveNumber(self.c11, "c11")
            congruence.checkStrictlyPositiveNumber(self.c12, "c12")
            congruence.checkStrictlyPositiveNumber(self.c44, "c44")

            symmetry = self.widget.fit_global_parameters.measured_dataset.get_phase(self.index).symmetry

            Ae, Be, As, Bs = calculate_A_B_coefficients(self.c11, self.c12, self.c44, symmetry)

            text = "Ae = " + str(Ae) + "\n"
            text += "Be = " + str(Be) + "\n"
            text += "As = " + str(As) + "\n"
            text += "Bs = " + str(Bs) + "\n"

            self.text_area.setText(text)

            return KrivoglazWilkensModel(Ae=FitParameter(parameter_name=self.get_parameters_prefix() + "Ae", value=Ae, fixed=True),
                                         Be=FitParameter(parameter_name=self.get_parameters_prefix() + "Be", value=Be, fixed=True),
                                         As=FitParameter(parameter_name=self.get_parameters_prefix() + "As", value=As, fixed=True),
                                         Bs=FitParameter(parameter_name=self.get_parameters_prefix() + "Bs", value=Bs, fixed=True))

if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = OWContrastFactor()
    ow.show()
    a.exec_()
    ow.saveSettings()
