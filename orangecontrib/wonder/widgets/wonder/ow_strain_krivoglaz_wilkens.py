import sys, copy

from PyQt5.QtWidgets import QMessageBox, QApplication

from orangewidget.settings import Setting
from orangewidget import gui as orangegui
from orangewidget.widget import OWAction

from orangecontrib.wonder.widgets.gui.ow_generic_widget import OWGenericWidget
from orangecontrib.wonder.util.gui_utility import gui
from orangecontrib.wonder.util import congruence
from orangecontrib.wonder.fit.parameters.fit_global_parameters import FitGlobalParameters
from orangecontrib.wonder.fit.parameters.microstructure.strain import KrivoglazWilkensModel
from orangecontrib.wonder.fit.parameters.measured_data.phase import Phase

class OWStrainKW(OWGenericWidget):

    name = "Krivoglaz-Wilkens Strain"
    description = "Define Krivoglaz-Wilkens Strain"
    icon = "icons/strain.png"
    priority = 19

    want_main_area =  False

    active = Setting([1])

    rho = Setting([0.0])
    rho_fixed = Setting([0])
    rho_has_min = Setting([1])
    rho_min = Setting([0.0])
    rho_has_max = Setting([0])
    rho_max = Setting([0.0])
    rho_function = Setting([0])
    rho_function_value = Setting([""])

    Re = Setting([0.0])
    Re_fixed = Setting([0])
    Re_has_min = Setting([1])
    Re_min = Setting([0.0])
    Re_has_max = Setting([0])
    Re_max = Setting([0.0])
    Re_function = Setting([0])
    Re_function_value = Setting([""])

    Ae = Setting([0.0])
    Ae_fixed = Setting([1])
    Ae_has_min = Setting([0])
    Ae_min = Setting([0.0])
    Ae_has_max = Setting([0])
    Ae_max = Setting([0.0])
    Ae_function = Setting([0])
    Ae_function_value = Setting([""])

    Be = Setting([0.0])
    Be_fixed = Setting([1])
    Be_has_min = Setting([0])
    Be_min = Setting([0.0])
    Be_has_max = Setting([0])
    Be_max = Setting([0.0])
    Be_function = Setting([0])
    Be_function_value = Setting([""])

    As = Setting([0.0])
    As_fixed = Setting([1])
    As_has_min = Setting([0])
    As_min = Setting([0.0])
    As_has_max = Setting([0])
    As_max = Setting([0.0])
    As_function = Setting([0])
    As_function_value = Setting([""])

    Bs = Setting([0.0])
    Bs_fixed = Setting([1])
    Bs_has_min = Setting([0])
    Bs_min = Setting([0.0])
    Bs_has_max = Setting([0])
    Bs_max = Setting([0.0])
    Bs_function = Setting([0])
    Bs_function_value = Setting([""])

    mix = Setting([0.5])
    mix_fixed = Setting([0])
    mix_has_min = Setting([1])
    mix_min = Setting([0.0])
    mix_has_max = Setting([1])
    mix_max = Setting([1.0])
    mix_function = Setting([0])
    mix_function_value = Setting([""])

    b = Setting([0.0])
    b_fixed = Setting([0])
    b_has_min = Setting([0])
    b_min = Setting([0.0])
    b_has_max = Setting([0])
    b_max = Setting([0.0])
    b_function = Setting([1])
    b_function_value = Setting(["phase_1_a*sqrt(3)/2"])

    inputs = [("Fit Global Parameters", FitGlobalParameters, 'set_data')]
    outputs = [("Fit Global Parameters", FitGlobalParameters)]

    def __init__(self):
        super().__init__(show_automatic_box=True)

        main_box = gui.widgetBox(self.controlArea,
                                 "Strain", orientation="vertical",
                                 width=self.CONTROL_AREA_WIDTH - 10, height=600)

        button_box = gui.widgetBox(main_box,
                                   "", orientation="horizontal",
                                   width=self.CONTROL_AREA_WIDTH-25)

        gui.button(button_box,  self, "Send Strain", height=40, callback=self.send_strains)

        self.strains_tabs = gui.tabWidget(main_box)
        self.strains_box_array = []

        for index in range(len(self.rho)):
            strain_box = StrainBox(widget=self,
                                   parent=gui.createTabPage(self.strains_tabs, Phase.get_default_name(index)),
                                   index=index,
                                   active=self.active[index],
                                   rho=self.rho[index],
                                   rho_fixed=self.rho_fixed[index],
                                   rho_has_min=self.rho_has_min[index],
                                   rho_min=self.rho_min[index],
                                   rho_has_max=self.rho_has_max[index],
                                   rho_max=self.rho_max[index],
                                   rho_function=self.rho_function[index],
                                   rho_function_value=self.rho_function_value[index],
                                   Re=self.Re[index],
                                   Re_fixed=self.Re_fixed[index],
                                   Re_has_min=self.Re_has_min[index],
                                   Re_min=self.Re_min[index],
                                   Re_has_max=self.Re_has_max[index],
                                   Re_max=self.Re_max[index],
                                   Re_function=self.Re_function[index],
                                   Re_function_value=self.Re_function_value[index],
                                   Ae=self.Ae[index],
                                   Ae_fixed=self.Ae_fixed[index],
                                   Ae_has_min=self.Ae_has_min[index],
                                   Ae_min=self.Ae_min[index],
                                   Ae_has_max=self.Ae_has_max[index],
                                   Ae_max=self.Ae_max[index],
                                   Ae_function=self.Ae_function[index],
                                   Ae_function_value=self.Ae_function_value[index],
                                   Be=self.Be[index],
                                   Be_fixed=self.Be_fixed[index],
                                   Be_has_min=self.Be_has_min[index],
                                   Be_min=self.Be_min[index],
                                   Be_has_max=self.Be_has_max[index],
                                   Be_max=self.Be_max[index],
                                   Be_function=self.Be_function[index],
                                   Be_function_value=self.Be_function_value[index],
                                   As=self.As[index],
                                   As_fixed=self.As_fixed[index],
                                   As_has_min=self.As_has_min[index],
                                   As_min=self.As_min[index],
                                   As_has_max=self.As_has_max[index],
                                   As_max=self.As_max[index],
                                   As_function=self.As_function[index],
                                   As_function_value=self.As_function_value[index],
                                   Bs=self.Bs[index],
                                   Bs_fixed=self.Bs_fixed[index],
                                   Bs_has_min=self.Bs_has_min[index],
                                   Bs_min=self.Bs_min[index],
                                   Bs_has_max=self.Bs_has_max[index],
                                   Bs_max=self.Bs_max[index],
                                   Bs_function=self.Bs_function[index],
                                   Bs_function_value=self.Bs_function_value[index],
                                   mix=self.mix[index],
                                   mix_fixed=self.mix_fixed[index],
                                   mix_has_min=self.mix_has_min[index],
                                   mix_min=self.mix_min[index],
                                   mix_has_max=self.mix_has_max[index],
                                   mix_max=self.mix_max[index],
                                   mix_function=self.mix_function[index],
                                   mix_function_value=self.mix_function_value[index],
                                   b=self.b[index],
                                   b_fixed=self.b_fixed[index],
                                   b_has_min=self.b_has_min[index],
                                   b_min=self.b_min[index],
                                   b_has_max=self.b_has_max[index],
                                   b_max=self.b_max[index],
                                   b_function=self.b_function[index],
                                   b_function_value=self.b_function_value[index])

            self.strains_box_array.append(strain_box)

        runaction = OWAction("Send Strain", self)
        runaction.triggered.connect(self.send_strains)
        self.addAction(runaction)

        orangegui.rubber(self.controlArea)

    def set_data(self, data):
        if not data is None:
            try:
                self.fit_global_parameters = data.duplicate()
                    
                phases = self.fit_global_parameters.measured_dataset.phases

                if phases is None: raise ValueError("No Phases in input data!")

                if not self.fit_global_parameters.strain_parameters is None:
                    if not isinstance(self.fit_global_parameters.get_strain_parameters(0), KrivoglazWilkensModel):
                        raise Exception("Only 1 Strain Model is allowed in a line of fit: it should be branched before")

                tabs_to_remove = len(self.rho) - len(phases)

                if tabs_to_remove > 0:
                    for index in range(tabs_to_remove):
                        self.strains_tabs.removeTab(-1)
                        self.strains_box_array.pop()

                for phase_index in range(len(phases)):
                    if not self.fit_global_parameters.strain_parameters is None:
                        strain_parameters = self.fit_global_parameters.get_strain_parameters(phase_index)
                    else:
                        strain_parameters = None

                    if phase_index < len(self.rho):
                        self.strains_tabs.setTabText(phase_index, phases[phase_index].get_name(phase_index))
                        strain_box = self.strains_box_array[phase_index]

                        if not strain_parameters is None:
                            strain_box.set_data(strain_parameters)
                    else:
                        strain_box = StrainBox(widget=self,
                                               parent=gui.createTabPage(self.strains_tabs, phases[phase_index].get_name(phase_index)),
                                               index=phase_index,
                                               active=0)

                        if not strain_parameters is None:
                            strain_box.set_data(strain_parameters)

                        self.strains_box_array.append(strain_box)

                self.dumpSettings()

                if self.is_automatic_run:
                    self.send_strains()

            except Exception as e:
                QMessageBox.critical(self, "Error",
                                     str(e),
                                     QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def send_strains(self):
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
        self.dump_rho()
        self.dump_Re()
        self.dump_Ae()
        self.dump_Be()
        self.dump_As()
        self.dump_Bs()
        self.dump_mix()
        self.dump_b()

    def dump_active(self):
        bkp_active = copy.deepcopy(self.active)

        try:
            self.active = []

            for index in range(len(self.strains_box_array)):
                self.active.append(self.strains_box_array[index].active)
        except Exception as e:
            self.active = copy.deepcopy(bkp_active)

            if self.IS_DEVELOP: raise e

    def dump_rho(self):
        bkp_rho = copy.deepcopy(self.rho)
        bkp_rho_fixed = copy.deepcopy(self.rho_fixed)
        bkp_rho_has_min = copy.deepcopy(self.rho_has_min)
        bkp_rho_min = copy.deepcopy(self.rho_min)
        bkp_rho_has_max = copy.deepcopy(self.rho_has_max)
        bkp_rho_max = copy.deepcopy(self.rho_max)
        bkp_rho_function = copy.deepcopy(self.rho_function)
        bkp_rho_function_value = copy.deepcopy(self.rho_function_value)

        try:
            self.rho = []
            self.rho_fixed = []
            self.rho_has_min = []
            self.rho_min = []
            self.rho_has_max = []
            self.rho_max = []
            self.rho_function = []
            self.rho_function_value = []

            for index in range(len(self.strains_box_array)):
                self.rho.append(self.strains_box_array[index].rho)
                self.rho_fixed.append(self.strains_box_array[index].rho_fixed)
                self.rho_has_min.append(self.strains_box_array[index].rho_has_min)
                self.rho_min.append(self.strains_box_array[index].rho_min)
                self.rho_has_max.append(self.strains_box_array[index].rho_has_max)
                self.rho_max.append(self.strains_box_array[index].rho_max)
                self.rho_function.append(self.strains_box_array[index].rho_function)
                self.rho_function_value.append(self.strains_box_array[index].rho_function_value)
        except Exception as e:
            self.rho = copy.deepcopy(bkp_rho)
            self.rho_fixed = copy.deepcopy(bkp_rho_fixed)
            self.rho_has_min = copy.deepcopy(bkp_rho_has_min)
            self.rho_min = copy.deepcopy(bkp_rho_min)
            self.rho_has_max = copy.deepcopy(bkp_rho_has_max)
            self.rho_max = copy.deepcopy(bkp_rho_max)
            self.rho_function = copy.deepcopy(bkp_rho_function)
            self.rho_function_value = copy.deepcopy(bkp_rho_function_value)

            if self.IS_DEVELOP: raise e

    def dump_Re(self):
        bkp_Re = copy.deepcopy(self.Re)
        bkp_Re_fixed = copy.deepcopy(self.Re_fixed)
        bkp_Re_has_min = copy.deepcopy(self.Re_has_min)
        bkp_Re_min = copy.deepcopy(self.Re_min)
        bkp_Re_has_max = copy.deepcopy(self.Re_has_max)
        bkp_Re_max = copy.deepcopy(self.Re_max)
        bkp_Re_function = copy.deepcopy(self.Re_function)
        bkp_Re_function_value = copy.deepcopy(self.Re_function_value)

        try:
            self.Re = []
            self.Re_fixed = []
            self.Re_has_min = []
            self.Re_min = []
            self.Re_has_max = []
            self.Re_max = []
            self.Re_function = []
            self.Re_function_value = []

            for index in range(len(self.strains_box_array)):
                self.Re.append(self.strains_box_array[index].Re)
                self.Re_fixed.append(self.strains_box_array[index].Re_fixed)
                self.Re_has_min.append(self.strains_box_array[index].Re_has_min)
                self.Re_min.append(self.strains_box_array[index].Re_min)
                self.Re_has_max.append(self.strains_box_array[index].Re_has_max)
                self.Re_max.append(self.strains_box_array[index].Re_max)
                self.Re_function.append(self.strains_box_array[index].Re_function)
                self.Re_function_value.append(self.strains_box_array[index].Re_function_value)
        except Exception as e:
            self.Re = copy.deepcopy(bkp_Re)
            self.Re_fixed = copy.deepcopy(bkp_Re_fixed)
            self.Re_has_min = copy.deepcopy(bkp_Re_has_min)
            self.Re_min = copy.deepcopy(bkp_Re_min)
            self.Re_has_max = copy.deepcopy(bkp_Re_has_max)
            self.Re_max = copy.deepcopy(bkp_Re_max)
            self.Re_function = copy.deepcopy(bkp_Re_function)
            self.Re_function_value = copy.deepcopy(bkp_Re_function_value)

            if self.IS_DEVELOP: raise e

    def dump_Ae(self):
        bkp_Ae = copy.deepcopy(self.Ae)
        bkp_Ae_fixed = copy.deepcopy(self.Ae_fixed)
        bkp_Ae_has_min = copy.deepcopy(self.Ae_has_min)
        bkp_Ae_min = copy.deepcopy(self.Ae_min)
        bkp_Ae_has_max = copy.deepcopy(self.Ae_has_max)
        bkp_Ae_max = copy.deepcopy(self.Ae_max)
        bkp_Ae_function = copy.deepcopy(self.Ae_function)
        bkp_Ae_function_value = copy.deepcopy(self.Ae_function_value)

        try:
            self.Ae = []
            self.Ae_fixed = []
            self.Ae_has_min = []
            self.Ae_min = []
            self.Ae_has_max = []
            self.Ae_max = []
            self.Ae_function = []
            self.Ae_function_value = []

            for index in range(len(self.strains_box_array)):
                self.Ae.append(self.strains_box_array[index].Ae)
                self.Ae_fixed.append(self.strains_box_array[index].Ae_fixed)
                self.Ae_has_min.append(self.strains_box_array[index].Ae_has_min)
                self.Ae_min.append(self.strains_box_array[index].Ae_min)
                self.Ae_has_max.append(self.strains_box_array[index].Ae_has_max)
                self.Ae_max.append(self.strains_box_array[index].Ae_max)
                self.Ae_function.append(self.strains_box_array[index].Ae_function)
                self.Ae_function_value.append(self.strains_box_array[index].Ae_function_value)
        except Exception as e:
            self.Ae = copy.deepcopy(bkp_Ae)
            self.Ae_fixed = copy.deepcopy(bkp_Ae_fixed)
            self.Ae_has_min = copy.deepcopy(bkp_Ae_has_min)
            self.Ae_min = copy.deepcopy(bkp_Ae_min)
            self.Ae_has_max = copy.deepcopy(bkp_Ae_has_max)
            self.Ae_max = copy.deepcopy(bkp_Ae_max)
            self.Ae_function = copy.deepcopy(bkp_Ae_function)
            self.Ae_function_value = copy.deepcopy(bkp_Ae_function_value)

            if self.IS_DEVELOP: raise e

    def dump_Be(self):
        bkp_Be = copy.deepcopy(self.Be)
        bkp_Be_fixed = copy.deepcopy(self.Be_fixed)
        bkp_Be_has_min = copy.deepcopy(self.Be_has_min)
        bkp_Be_min = copy.deepcopy(self.Be_min)
        bkp_Be_has_max = copy.deepcopy(self.Be_has_max)
        bkp_Be_max = copy.deepcopy(self.Be_max)
        bkp_Be_function = copy.deepcopy(self.Be_function)
        bkp_Be_function_value = copy.deepcopy(self.Be_function_value)

        try:
            self.Be = []
            self.Be_fixed = []
            self.Be_has_min = []
            self.Be_min = []
            self.Be_has_max = []
            self.Be_max = []
            self.Be_function = []
            self.Be_function_value = []

            for index in range(len(self.strains_box_array)):
                self.Be.append(self.strains_box_array[index].Be)
                self.Be_fixed.append(self.strains_box_array[index].Be_fixed)
                self.Be_has_min.append(self.strains_box_array[index].Be_has_min)
                self.Be_min.append(self.strains_box_array[index].Be_min)
                self.Be_has_max.append(self.strains_box_array[index].Be_has_max)
                self.Be_max.append(self.strains_box_array[index].Be_max)
                self.Be_function.append(self.strains_box_array[index].Be_function)
                self.Be_function_value.append(self.strains_box_array[index].Be_function_value)
        except Exception as e:
            self.Be = copy.deepcopy(bkp_Be)
            self.Be_fixed = copy.deepcopy(bkp_Be_fixed)
            self.Be_has_min = copy.deepcopy(bkp_Be_has_min)
            self.Be_min = copy.deepcopy(bkp_Be_min)
            self.Be_has_max = copy.deepcopy(bkp_Be_has_max)
            self.Be_max = copy.deepcopy(bkp_Be_max)
            self.Be_function = copy.deepcopy(bkp_Be_function)
            self.Be_function_value = copy.deepcopy(bkp_Be_function_value)

            if self.IS_DEVELOP: raise e

    def dump_As(self):
        bkp_As = copy.deepcopy(self.As)
        bkp_As_fixed = copy.deepcopy(self.As_fixed)
        bkp_As_has_min = copy.deepcopy(self.As_has_min)
        bkp_As_min = copy.deepcopy(self.As_min)
        bkp_As_has_max = copy.deepcopy(self.As_has_max)
        bkp_As_max = copy.deepcopy(self.As_max)
        bkp_As_function = copy.deepcopy(self.As_function)
        bkp_As_function_value = copy.deepcopy(self.As_function_value)

        try:
            self.As = []
            self.As_fixed = []
            self.As_has_min = []
            self.As_min = []
            self.As_has_max = []
            self.As_max = []
            self.As_function = []
            self.As_function_value = []

            for index in range(len(self.strains_box_array)):
                self.As.append(self.strains_box_array[index].As)
                self.As_fixed.append(self.strains_box_array[index].As_fixed)
                self.As_has_min.append(self.strains_box_array[index].As_has_min)
                self.As_min.append(self.strains_box_array[index].As_min)
                self.As_has_max.append(self.strains_box_array[index].As_has_max)
                self.As_max.append(self.strains_box_array[index].As_max)
                self.As_function.append(self.strains_box_array[index].As_function)
                self.As_function_value.append(self.strains_box_array[index].As_function_value)
        except Exception as e:
            self.As = copy.deepcopy(bkp_As)
            self.As_fixed = copy.deepcopy(bkp_As_fixed)
            self.As_has_min = copy.deepcopy(bkp_As_has_min)
            self.As_min = copy.deepcopy(bkp_As_min)
            self.As_has_max = copy.deepcopy(bkp_As_has_max)
            self.As_max = copy.deepcopy(bkp_As_max)
            self.As_function = copy.deepcopy(bkp_As_function)
            self.As_function_value = copy.deepcopy(bkp_As_function_value)

            if self.IS_DEVELOP: raise e

    def dump_Bs(self):
        bkp_Bs = copy.deepcopy(self.Bs)
        bkp_Bs_fixed = copy.deepcopy(self.Bs_fixed)
        bkp_Bs_has_min = copy.deepcopy(self.Bs_has_min)
        bkp_Bs_min = copy.deepcopy(self.Bs_min)
        bkp_Bs_has_max = copy.deepcopy(self.Bs_has_max)
        bkp_Bs_max = copy.deepcopy(self.Bs_max)
        bkp_Bs_function = copy.deepcopy(self.Bs_function)
        bkp_Bs_function_value = copy.deepcopy(self.Bs_function_value)

        try:
            self.Bs = []
            self.Bs_fixed = []
            self.Bs_has_min = []
            self.Bs_min = []
            self.Bs_has_max = []
            self.Bs_max = []
            self.Bs_function = []
            self.Bs_function_value = []

            for index in range(len(self.strains_box_array)):
                self.Bs.append(self.strains_box_array[index].Bs)
                self.Bs_fixed.append(self.strains_box_array[index].Bs_fixed)
                self.Bs_has_min.append(self.strains_box_array[index].Bs_has_min)
                self.Bs_min.append(self.strains_box_array[index].Bs_min)
                self.Bs_has_max.append(self.strains_box_array[index].Bs_has_max)
                self.Bs_max.append(self.strains_box_array[index].Bs_max)
                self.Bs_function.append(self.strains_box_array[index].Bs_function)
                self.Bs_function_value.append(self.strains_box_array[index].Bs_function_value)
        except Exception as e:
            self.Bs = copy.deepcopy(bkp_Bs)
            self.Bs_fixed = copy.deepcopy(bkp_Bs_fixed)
            self.Bs_has_min = copy.deepcopy(bkp_Bs_has_min)
            self.Bs_min = copy.deepcopy(bkp_Bs_min)
            self.Bs_has_max = copy.deepcopy(bkp_Bs_has_max)
            self.Bs_max = copy.deepcopy(bkp_Bs_max)
            self.Bs_function = copy.deepcopy(bkp_Bs_function)
            self.Bs_function_value = copy.deepcopy(bkp_Bs_function_value)

            if self.IS_DEVELOP: raise e

    def dump_mix(self):
        bkp_mix = copy.deepcopy(self.mix)
        bkp_mix_fixed = copy.deepcopy(self.mix_fixed)
        bkp_mix_has_min = copy.deepcopy(self.mix_has_min)
        bkp_mix_min = copy.deepcopy(self.mix_min)
        bkp_mix_has_max = copy.deepcopy(self.mix_has_max)
        bkp_mix_max = copy.deepcopy(self.mix_max)
        bkp_mix_function = copy.deepcopy(self.mix_function)
        bkp_mix_function_value = copy.deepcopy(self.mix_function_value)

        try:
            self.mix = []
            self.mix_fixed = []
            self.mix_has_min = []
            self.mix_min = []
            self.mix_has_max = []
            self.mix_max = []
            self.mix_function = []
            self.mix_function_value = []

            for index in range(len(self.strains_box_array)):
                self.mix.append(self.strains_box_array[index].mix)
                self.mix_fixed.append(self.strains_box_array[index].mix_fixed)
                self.mix_has_min.append(self.strains_box_array[index].mix_has_min)
                self.mix_min.append(self.strains_box_array[index].mix_min)
                self.mix_has_max.append(self.strains_box_array[index].mix_has_max)
                self.mix_max.append(self.strains_box_array[index].mix_max)
                self.mix_function.append(self.strains_box_array[index].mix_function)
                self.mix_function_value.append(self.strains_box_array[index].mix_function_value)
        except Exception as e:
            self.mix = copy.deepcopy(bkp_mix)
            self.mix_fixed = copy.deepcopy(bkp_mix_fixed)
            self.mix_has_min = copy.deepcopy(bkp_mix_has_min)
            self.mix_min = copy.deepcopy(bkp_mix_min)
            self.mix_has_max = copy.deepcopy(bkp_mix_has_max)
            self.mix_max = copy.deepcopy(bkp_mix_max)
            self.mix_function = copy.deepcopy(bkp_mix_function)
            self.mix_function_value = copy.deepcopy(bkp_mix_function_value)

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

            for index in range(len(self.strains_box_array)):
                self.b.append(self.strains_box_array[index].b)
                self.b_fixed.append(self.strains_box_array[index].b_fixed)
                self.b_has_min.append(self.strains_box_array[index].b_has_min)
                self.b_min.append(self.strains_box_array[index].b_min)
                self.b_has_max.append(self.strains_box_array[index].b_has_max)
                self.b_max.append(self.strains_box_array[index].b_max)
                self.b_function.append(self.strains_box_array[index].b_function)
                self.b_function_value.append(self.strains_box_array[index].b_function_value)
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


from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
from orangecontrib.wonder.util.gui_utility import InnerBox


class StrainBox(InnerBox):
    active = 1
    rho = 0.0
    rho_fixed = 0
    rho_has_min = 1
    rho_min = 0.0
    rho_has_max = 0
    rho_max = 0.0
    rho_function = 0
    rho_function_value = ""
    Re = 0.0
    Re_fixed = 0
    Re_has_min = 1
    Re_min = 0.0
    Re_has_max = 0
    Re_max = 0.0
    Re_function = 0
    Re_function_value = ""
    Ae = 0.0
    Ae_fixed = 1
    Ae_has_min = 0
    Ae_min = 0.0
    Ae_has_max = 0
    Ae_max = 0.0
    Ae_function = 0
    Ae_function_value = ""
    Be = 0.0
    Be_fixed = 1
    Be_has_min = 0
    Be_min = 0.0
    Be_has_max = 0
    Be_max = 0.0
    Be_function = 0
    Be_function_value = ""
    As = 0.0
    As_fixed = 1
    As_has_min = 0
    As_min = 0.0
    As_has_max = 0
    As_max = 0.0
    As_function = 0
    As_function_value = ""
    Bs = 0.0
    Bs_fixed = 1
    Bs_has_min = 0
    Bs_min = 0.0
    Bs_has_max = 0
    Bs_max = 0.0
    Bs_function = 0
    Bs_function_value = ""
    mix = 0.5
    mix_fixed = 0
    mix_has_min = 1
    mix_min = 0.0
    mix_has_max = 1
    mix_max = 1.0
    mix_function = 0
    mix_function_value = ""
    b = 0.0
    b_fixed = 0
    b_has_min = 0
    b_min = 0.0
    b_has_max = 0
    b_max = 0.0
    b_function = 1
    b_function_value = "phase_1_a*sqrt([3/2"

    widget = None
    is_on_init = True

    parameter_functions = {}

    index = 0

    def __init__(self,
                 widget=None,
                 parent=None,
                 index=0,
                 active=1,
                 rho = 0.0,
                 rho_fixed = 0,
                 rho_has_min = 1,
                 rho_min = 0.0,
                 rho_has_max = 0,
                 rho_max = 0.0,
                 rho_function = 0,
                 rho_function_value = "",
                 Re = 0.0,
                 Re_fixed = 0,
                 Re_has_min = 1,
                 Re_min = 0.0,
                 Re_has_max = 0,
                 Re_max = 0.0,
                 Re_function = 0,
                 Re_function_value = "",
                 Ae = 0.0,
                 Ae_fixed = 1,
                 Ae_has_min = 0,
                 Ae_min = 0.0,
                 Ae_has_max = 0,
                 Ae_max = 0.0,
                 Ae_function = 0,
                 Ae_function_value = "",
                 Be = 0.0,
                 Be_fixed = 1,
                 Be_has_min = 0,
                 Be_min = 0.0,
                 Be_has_max = 0,
                 Be_max = 0.0,
                 Be_function = 0,
                 Be_function_value = "",
                 As = 0.0,
                 As_fixed = 1,
                 As_has_min = 0,
                 As_min = 0.0,
                 As_has_max = 0,
                 As_max = 0.0,
                 As_function = 0,
                 As_function_value = "",
                 Bs = 0.0,
                 Bs_fixed = 1,
                 Bs_has_min = 0,
                 Bs_min = 0.0,
                 Bs_has_max = 0,
                 Bs_max = 0.0,
                 Bs_function = 0,
                 Bs_function_value = "",
                 mix = 0.5,
                 mix_fixed = 0,
                 mix_has_min = 1,
                 mix_min = 0.0,
                 mix_has_max = 1,
                 mix_max = 1.0,
                 mix_function = 0,
                 mix_function_value = "",
                 b = 0.0,
                 b_fixed = 0,
                 b_has_min = 0,
                 b_min = 0.0,
                 b_has_max = 0,
                 b_max = 0.0,
                 b_function = 1,
                 b_function_value = "phase_1_a*sqrt(3/2)"):
        super(StrainBox, self).__init__()

        self.widget = widget

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.setFixedWidth(widget.CONTROL_AREA_WIDTH - 35)
        self.setFixedHeight(300)

        self.index = index

        self.active = active
        self.rho = rho
        self.rho_fixed = rho_fixed
        self.rho_has_min = rho_has_min
        self.rho_min = rho_min
        self.rho_has_max = rho_has_max
        self.rho_max = rho_max
        self.rho_function = rho_function
        self.rho_function_value = rho_function_value
        self.Re = Re
        self.Re_fixed = Re_fixed
        self.Re_has_min = Re_has_min
        self.Re_min = Re_min
        self.Re_has_max = Re_has_max
        self.Re_max = Re_max
        self.Re_function = Re_function
        self.Re_function_value = Re_function_value
        self.Ae = Ae
        self.Ae_fixed = Ae_fixed
        self.Ae_has_min = Ae_has_min
        self.Ae_min = Ae_min
        self.Ae_has_max = Ae_has_max
        self.Ae_max = Ae_max
        self.Ae_function = Ae_function
        self.Ae_function_value = Ae_function_value
        self.Be = Be
        self.Be_fixed = Be_fixed
        self.Be_has_min = Be_has_min
        self.Be_min = Be_min
        self.Be_has_max = Be_has_max
        self.Be_max = Be_max
        self.Be_function = Be_function
        self.Be_function_value = Be_function_value
        self.As = As
        self.As_fixed = As_fixed
        self.As_has_min = As_has_min
        self.As_min = As_min
        self.As_has_max = As_has_max
        self.As_max = As_max
        self.As_function = As_function
        self.As_function_value = As_function_value
        self.Bs = Bs
        self.Bs_fixed = Bs_fixed
        self.Bs_has_min = Bs_has_min
        self.Bs_min = Bs_min
        self.Bs_has_max = Bs_has_max
        self.Bs_max = Bs_max
        self.Bs_function = Bs_function
        self.Bs_function_value = Bs_function_value
        self.mix = mix
        self.mix_fixed = mix_fixed
        self.mix_has_min = mix_has_min
        self.mix_min = mix_min
        self.mix_has_max = mix_has_max
        self.mix_max = mix_max
        self.mix_function = mix_function
        self.mix_function_value = mix_function_value
        self.b = b
        self.b_fixed = b_fixed
        self.b_has_min = b_has_min
        self.b_min = b_min
        self.b_has_max = b_has_max
        self.b_max = b_max
        self.b_function = b_function
        self.b_function_value = b_function_value

        self.CONTROL_AREA_WIDTH = widget.CONTROL_AREA_WIDTH - 45

        parent.layout().addWidget(self)
        container = self

        self.cb_active = orangegui.comboBox(container, self, "active", label="Active", items=["No", "Yes"], callback=self.set_active, orientation="horizontal")

        self.main_box = gui.widgetBox(container, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 10)

        OWGenericWidget.create_box_in_widget(self, self.main_box, "rho", add_callback=True, label="\u03c1", min_value=0.0, min_accepted=False, trim=25)
        OWGenericWidget.create_box_in_widget(self, self.main_box, "Re", add_callback=True, min_value=0.0, min_accepted=False, trim=25)
        OWGenericWidget.create_box_in_widget(self, self.main_box, "Ae", add_callback=True, trim=25)
        OWGenericWidget.create_box_in_widget(self, self.main_box, "Be", add_callback=True, trim=25)
        OWGenericWidget.create_box_in_widget(self, self.main_box, "As", add_callback=True, trim=25)
        OWGenericWidget.create_box_in_widget(self, self.main_box, "Bs", add_callback=True, trim=25)
        OWGenericWidget.create_box_in_widget(self, self.main_box, "mix", add_callback=True, min_value=0.0, min_accepted=True, max_value=1.0, max_accepted=True, trim=25)
        OWGenericWidget.create_box_in_widget(self, self.main_box, "b", add_callback=True, min_value=0.0, min_accepted=False, trim=25)

        self.set_active()

        self.is_on_init = False

    def after_change_workspace_units(self):
        pass

    def set_index(self, index):
        self.index = index

    def set_active(self):
        self.main_box.setEnabled(self.active == 1)

        if not self.is_on_init: self.widget.dump_active()

    def callback_rho(self):
        if not self.is_on_init: self.widget.dump_rho()

    def callback_Re(self):
        if not self.is_on_init: self.widget.dump_Re()

    def callback_Ae(self):
        if not self.is_on_init: self.widget.dump_Ae()

    def callback_Be(self):
        if not self.is_on_init: self.widget.dump_Be()

    def callback_As(self):
        if not self.is_on_init: self.widget.dump_As()

    def callback_Bs(self):
        if not self.is_on_init: self.widget.dump_Bs()

    def callback_mix(self):
        if not self.is_on_init: self.widget.dump_mix()

    def callback_b(self):
        if not self.is_on_init: self.widget.dump_b()

    def get_parameters_prefix(self):
        return KrivoglazWilkensModel.get_parameters_prefix() + self.get_parameter_progressive()

    def get_parameter_progressive(self):
        return str(self.index + 1) + "_"

    def set_data(self, strain_parameters):
        if strain_parameters.rho is None and \
                strain_parameters.Re is None and \
                strain_parameters.mix is None and \
                strain_parameters.mix is None:
            OWGenericWidget.populate_fields_in_widget(self, "Ae", strain_parameters.Ae, value_only=False)
            OWGenericWidget.populate_fields_in_widget(self, "Be", strain_parameters.Be, value_only=False)
            OWGenericWidget.populate_fields_in_widget(self, "As", strain_parameters.As, value_only=False)
            OWGenericWidget.populate_fields_in_widget(self, "Bs", strain_parameters.Bs, value_only=False)
        else:
            OWGenericWidget.populate_fields_in_widget(self, "rho", strain_parameters.rho)
            OWGenericWidget.populate_fields_in_widget(self, "Re", strain_parameters.Re)
            OWGenericWidget.populate_fields_in_widget(self, "Ae", strain_parameters.Ae)
            OWGenericWidget.populate_fields_in_widget(self, "Be", strain_parameters.Be)
            OWGenericWidget.populate_fields_in_widget(self, "As", strain_parameters.As)
            OWGenericWidget.populate_fields_in_widget(self, "Bs", strain_parameters.Bs)
            OWGenericWidget.populate_fields_in_widget(self, "mix", strain_parameters.mix)
            OWGenericWidget.populate_fields_in_widget(self, "b", strain_parameters.b)

    def get_strain_parameters(self):
        if self.active == 0: return None
        else:
            if not self.rho_function == 1: congruence.checkStrictlyPositiveNumber(self.rho, "\u03c1")
            if not self.Re_function == 1: congruence.checkStrictlyPositiveNumber(self.Re, "Re")
            if not self.mix_function == 1: congruence.checkPositiveNumber(self.mix, "mix")
            if not self.b_function == 1: congruence.checkStrictlyPositiveNumber(self.b, "b")

            return KrivoglazWilkensModel(rho=OWGenericWidget.populate_parameter_in_widget(self, "rho", self.get_parameters_prefix()),
                                         Re =OWGenericWidget.populate_parameter_in_widget(self, "Re",  self.get_parameters_prefix()),
                                         Ae =OWGenericWidget.populate_parameter_in_widget(self, "Ae",  self.get_parameters_prefix()),
                                         Be =OWGenericWidget.populate_parameter_in_widget(self, "Be",  self.get_parameters_prefix()),
                                         As =OWGenericWidget.populate_parameter_in_widget(self, "As",  self.get_parameters_prefix()),
                                         Bs =OWGenericWidget.populate_parameter_in_widget(self, "Bs",  self.get_parameters_prefix()),
                                         mix=OWGenericWidget.populate_parameter_in_widget(self, "mix", self.get_parameters_prefix()),
                                         b  =OWGenericWidget.populate_parameter_in_widget(self, "b",   self.get_parameters_prefix()))


if __name__ == "__main__":
    a =  QApplication(sys.argv)
    ow = OWStrainKW()
    ow.show()
    a.exec_()
    ow.saveSettings()
