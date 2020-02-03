import sys, copy

from PyQt5.QtWidgets import QMessageBox, QApplication

from orangewidget.settings import Setting
from orangewidget import gui as orangegui
from orangewidget.widget import OWAction

from orangecontrib.wonder.widgets.gui.ow_generic_widget import OWGenericWidget
from orangecontrib.wonder.util.gui_utility import gui, ConfirmDialog
from orangecontrib.wonder.util import congruence
from orangecontrib.wonder.fit.parameters.fit_global_parameters import FitGlobalParameters
from orangecontrib.wonder.fit.parameters.instrument.polarization_parameters import PolarizationParameters, Beampath, LorentzFormula

class OWLorentzPolarization(OWGenericWidget):

    name = "Lorentz-Polarization Factors"
    description = "Define Lorentz-Polarization Factor"
    icon = "icons/lorentz_polarization.png"
    priority = 9

    want_main_area = False

    use_single_parameter_set = Setting(0)

    use_lorentz_factor      = Setting([1])
    lorentz_formula         = Setting([LorentzFormula.Shkl_Shkl])
    use_polarization_factor = Setting([0])
    degree_of_polarization  = Setting([0.0])
    beampath                = Setting([Beampath.PRIMARY])
    use_twotheta_mono       = Setting([1])
    twotheta_mono           = Setting([28.443])

    inputs = [("Fit Global Parameters", FitGlobalParameters, 'set_data')]
    outputs = [("Fit Global Parameters", FitGlobalParameters)]

    def __init__(self):
        super().__init__(show_automatic_box=True)

        main_box = gui.widgetBox(self.controlArea,
                                 "Lorentz-Polarization Factors Setting", orientation="vertical",
                                 width=self.CONTROL_AREA_WIDTH - 10, height=400)

        button_box = gui.widgetBox(main_box,
                                   "", orientation="horizontal",
                                   width=self.CONTROL_AREA_WIDTH-25)

        gui.button(button_box, self, "Send Lorentz-Polarization Parameters", height=40, callback=self.send_lorentz_polarization)

        orangegui.comboBox(main_box, self, "use_single_parameter_set", label="Use single set of Parameters", labelWidth=350, orientation="horizontal",
                           items=["No", "Yes"], callback=self.set_use_single_parameter_set, sendSelectedValue=False)

        orangegui.separator(main_box)

        self.lorentz_polarization_tabs = gui.tabWidget(main_box)

        self.set_use_single_parameter_set(on_init=True)

        runaction = OWAction("Send Lorentz-Polarization Parameters", self)
        runaction.triggered.connect(self.send_lorentz_polarization)
        self.addAction(runaction)

        orangegui.rubber(self.controlArea)

    def set_use_single_parameter_set(self, on_init=False, recycle=True):
        self.lorentz_polarization_tabs.clear()
        self.lorentz_polarization_box_array = []

        dimension = len(self.use_lorentz_factor) if self.fit_global_parameters is None else self.fit_global_parameters.measured_dataset.get_diffraction_patterns_number()

        for index in range(1 if self.use_single_parameter_set == 1 else dimension):
            lorentz_polarization_tab = gui.createTabPage(self.lorentz_polarization_tabs, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, index, self.use_single_parameter_set==1))

            if index < len(self.use_lorentz_factor) and recycle:  # keep the existing
                lorentz_polarization_box = PolarizationParametersBox(widget=self,
                                                                     parent=lorentz_polarization_tab,
                                                                     index=index,
                                                                     use_lorentz_factor = self.use_lorentz_factor[index],     
                                                                     lorentz_formula = self.lorentz_formula[index],        
                                                                     use_polarization_factor = self.use_polarization_factor[index],
                                                                     degree_of_polarization = self.degree_of_polarization[index], 
                                                                     beampath = self.beampath[index],               
                                                                     use_twotheta_mono = self.use_twotheta_mono[index],      
                                                                     twotheta_mono = self.twotheta_mono[index])
            else:
                lorentz_polarization_box = PolarizationParametersBox(widget=self, parent=lorentz_polarization_tab, index=index)

            self.lorentz_polarization_box_array.append(lorentz_polarization_box)

            if not on_init: self.dumpSettings()

    def send_lorentz_polarization(self):
        try:
            if not self.fit_global_parameters is None:
                self.dumpSettings()

                self.fit_global_parameters.set_instrumental_parameters([self.lorentz_polarization_box_array[index].get_lorentz_polarization() for index in range(len(self.use_lorentz_factor))])
                self.fit_global_parameters.regenerate_parameters()

                self.send("Fit Global Parameters", self.fit_global_parameters)

        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 str(e),
                                 QMessageBox.Ok)

            if self.IS_DEVELOP: raise e

    def __check_data_congruence(self, lorenz_polarization_parameters):
        if (len(lorenz_polarization_parameters) == 1 and self.use_single_parameter_set == 0) or (len(lorenz_polarization_parameters) > 1 and self.use_single_parameter_set == 1):
            raise ValueError("Previous L-P parameters are incongruent with the current choice of using a single set")

    def set_data(self, data):
        if not data is None:
            try:
                self.fit_global_parameters = data.duplicate()

                phases = self.fit_global_parameters.measured_dataset.phases
                if phases is None: raise ValueError("Add Phase(s) before this widget")

                diffraction_patterns = self.fit_global_parameters.measured_dataset.diffraction_patterns
                if diffraction_patterns is None: raise ValueError("Add Diffraction Pattern(s) before this widget!")

                if not self.fit_global_parameters.measured_dataset.get_phase(0).use_structure:
                    raise ValueError("Lorentz-Polarization parameters can be used only with a structural model")

                lorenz_polarization_parameters = self.fit_global_parameters.get_instrumental_parameters(PolarizationParameters.__name__)

                if self.use_single_parameter_set == 0:  # NO
                    if lorenz_polarization_parameters is None:
                        if len(diffraction_patterns) != len(self.lorentz_polarization_box_array):
                            self.set_use_single_parameter_set(recycle=ConfirmDialog.confirmed(message="Number of Diffraction Patterns changed:\ndo you want to use the existing data where possible?\n\nIf yes, check for possible incongruences", title="Warning"))
                        else:
                            self.set_use_single_parameter_set(True)
                    else:
                        tabs_to_remove = len(self.displacement) - len(lorenz_polarization_parameters)

                        if tabs_to_remove > 0:
                            for index in range(tabs_to_remove):
                                self.lorentz_polarization_tabs.removeTab(-1)
                                self.lorentz_polarization_box_array.pop()

                        for diffraction_pattern_index in range(len(lorenz_polarization_parameters)):
                            lorenz_polarization_parameters_item = self.fit_global_parameters.get_instrumental_parameters_item(PolarizationParameters.__name__, diffraction_pattern_index)

                            if diffraction_pattern_index < len(self.displacement):
                                self.lorentz_polarization_tabs.setTabText(diffraction_pattern_index,
                                                                          OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, diffraction_pattern_index, False))

                                lorentz_polarization_box = self.lorentz_polarization_box_array[diffraction_pattern_index]
                            else:
                                lorentz_polarization_box = PolarizationParametersBox(widget=self,
                                                                                     parent=gui.createTabPage(self.lorentz_polarization_tabs, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, diffraction_pattern_index, False)),
                                                                                     index=diffraction_pattern_index)
                                self.lorentz_polarization_box_array.append(lorentz_polarization_box)

                            if not lorenz_polarization_parameters_item is None: lorentz_polarization_box.set_data(lorenz_polarization_parameters_item)
                else:
                    if lorenz_polarization_parameters is None:
                        self.set_use_single_parameter_set(True)
                    else:
                        self.__check_data_congruence(lorenz_polarization_parameters)

                        lorenz_polarization_parameters_item = self.fit_global_parameters.get_instrumental_parameters_item(PolarizationParameters.__name__, 0)

                        self.lorentz_polarization_tabs.setTabText(0, OWGenericWidget.diffraction_pattern_name(self.fit_global_parameters, 0, True))
                        if not lorenz_polarization_parameters_item is None: self.lorentz_polarization_box_array[0].set_data(lorenz_polarization_parameters_item)

                self.dumpSettings()

                if self.is_automatic_run:
                    self.send_lorentz_polarization()

            except Exception as e:
                QMessageBox.critical(self, "Error",
                                     str(e),
                                     QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def dumpSettings(self):
        self.dump_use_lorentz_factor()
        self.dump_lorentz_formula()
        self.dump_use_polarization_factor()
        self.dump_degree_of_polarization()
        self.dump_beampath()
        self.dump_use_twotheta_mono()
        self.dump_twotheta_mono()


    def dump_use_lorentz_factor(self):
        bkp_use_lorentz_factor = copy.deepcopy(self.use_lorentz_factor)

        try:
            self.use_lorentz_factor = []

            for index in range(len(self.lorentz_polarization_box_array)):
                self.use_lorentz_factor.append(self.lorentz_polarization_box_array[index].use_lorentz_factor)
        except Exception as e:
            self.use_lorentz_factor = copy.deepcopy(bkp_use_lorentz_factor)

            if self.IS_DEVELOP: raise  e

    def dump_lorentz_formula(self):
        bkp_lorentz_formula = copy.deepcopy(self.lorentz_formula)

        try:
            self.lorentz_formula = []

            for index in range(len(self.lorentz_polarization_box_array)):
                self.lorentz_formula.append(self.lorentz_polarization_box_array[index].lorentz_formula)
        except Exception as e:
            self.lorentz_formula = copy.deepcopy(bkp_lorentz_formula)

            if self.IS_DEVELOP: raise  e

    def dump_use_polarization_factor(self):
        bkp_use_polarization_factor = copy.deepcopy(self.use_polarization_factor)

        try:
            self.use_polarization_factor = []

            for index in range(len(self.lorentz_polarization_box_array)):
                self.use_polarization_factor.append(self.lorentz_polarization_box_array[index].use_polarization_factor)
        except Exception as e:
            self.use_polarization_factor = copy.deepcopy(bkp_use_polarization_factor)

            if self.IS_DEVELOP: raise  e

    def dump_degree_of_polarization(self):
        bkp_degree_of_polarization = copy.deepcopy(self.degree_of_polarization)

        try:
            self.degree_of_polarization = []

            for index in range(len(self.lorentz_polarization_box_array)):
                self.degree_of_polarization.append(self.lorentz_polarization_box_array[index].degree_of_polarization)
        except Exception as e:
            self.degree_of_polarization = copy.deepcopy(bkp_degree_of_polarization)

            if self.IS_DEVELOP: raise  e

    def dump_beampath(self):
        bkp_beampath = copy.deepcopy(self.beampath)

        try:
            self.beampath = []

            for index in range(len(self.lorentz_polarization_box_array)):
                self.beampath.append(self.lorentz_polarization_box_array[index].beampath)
        except Exception as e:
            self.beampath = copy.deepcopy(bkp_beampath)

            if self.IS_DEVELOP: raise  e

    def dump_use_twotheta_mono(self):
        bkp_use_twotheta_mono = copy.deepcopy(self.use_twotheta_mono)

        try:
            self.use_twotheta_mono = []

            for index in range(len(self.lorentz_polarization_box_array)):
                self.use_twotheta_mono.append(self.lorentz_polarization_box_array[index].use_twotheta_mono)
        except Exception as e:
            self.use_twotheta_mono = copy.deepcopy(bkp_use_twotheta_mono)

            if self.IS_DEVELOP: raise  e

    def dump_twotheta_mono(self):
        bkp_twotheta_mono = copy.deepcopy(self.twotheta_mono)

        try:
            self.twotheta_mono = []

            for index in range(len(self.lorentz_polarization_box_array)):
                self.twotheta_mono.append(self.lorentz_polarization_box_array[index].twotheta_mono)
        except Exception as e:
            self.twotheta_mono = copy.deepcopy(bkp_twotheta_mono)

            if self.IS_DEVELOP: raise  e


from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QVBoxLayout
from orangecontrib.wonder.util.gui_utility import InnerBox


class PolarizationParametersBox(InnerBox):
    widget = None
    is_on_init = True

    parameter_functions = {}

    index = 0

    def __init__(self,
                 widget=None,
                 parent=None,
                 index=0,
                 use_lorentz_factor=1,
                 lorentz_formula=LorentzFormula.Shkl_Shkl,
                 use_polarization_factor=0,
                 degree_of_polarization=0.0,
                 beampath=Beampath.PRIMARY,
                 use_twotheta_mono=1,
                 twotheta_mono=28.443):
        super(PolarizationParametersBox, self).__init__()

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.setFixedWidth(widget.CONTROL_AREA_WIDTH - 35)
        self.setFixedHeight(500)

        self.widget = widget
        self.index = index

        self.use_lorentz_factor      = use_lorentz_factor
        self.lorentz_formula         = lorentz_formula
        self.use_polarization_factor = use_polarization_factor
        self.degree_of_polarization  = degree_of_polarization
        self.beampath                = beampath
        self.use_twotheta_mono       = use_twotheta_mono
        self.twotheta_mono           = twotheta_mono

        self.CONTROL_AREA_WIDTH = widget.CONTROL_AREA_WIDTH

        parent.layout().addWidget(self)
        container = self

        orangegui.comboBox(container, self, "use_lorentz_factor", label="Add Lorentz Factor", items=["No", "Yes"], labelWidth=300, orientation="horizontal", callback=self.set_LorentzFactor)

        self.lorentz_box = gui.widgetBox(container, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 20, height=30)
        self.lorentz_box_empty = gui.widgetBox(container, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 20, height=30)

        orangegui.comboBox(self.lorentz_box, self, "lorentz_formula", label="Formula", items=LorentzFormula.tuple(), labelWidth=300, orientation="horizontal", callback=widget.dump_lorentz_formula)

        self.set_LorentzFactor()

        orangegui.separator(container)

        orangegui.comboBox(container, self, "use_polarization_factor", label="Add Polarization Factor", items=["No", "Yes"], labelWidth=300,
                           orientation="horizontal", callback=self.set_Polarization)

        self.polarization_box = gui.widgetBox(container, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 20, height=200)
        self.polarization_box_empty = gui.widgetBox(container, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 20, height=200)

        gui.lineEdit(self.polarization_box, self, "degree_of_polarization", "Deg. Pol. (0\u2264Q\u22641)", labelWidth=300, valueType=float, callback=widget.dump_degree_of_polarization)

        orangegui.comboBox(self.polarization_box, self, "use_twotheta_mono", label="Use Monochromator", items=["No", "Yes"], labelWidth=300,
                           orientation="horizontal", callback=self.set_Monochromator)

        self.monochromator_box = gui.widgetBox(self.polarization_box, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 20, height=95)
        self.monochromator_box_empty = gui.widgetBox(self.polarization_box, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 20, height=95)

        orangegui.comboBox(self.monochromator_box, self, "beampath", label="Beampath", items=Beampath.tuple(), labelWidth=300,
                           orientation="horizontal", callback=widget.dump_beampath)

        gui.lineEdit(self.monochromator_box, self, "twotheta_mono", "2\u03B8 Monochromator [deg]", labelWidth=300, valueType=float, callback=widget.dump_twotheta_mono)

        self.set_Polarization()

        self.is_on_init = False

    def set_LorentzFactor(self):
        self.lorentz_box.setVisible(self.use_lorentz_factor==1)
        self.lorentz_box_empty.setVisible(self.use_lorentz_factor==0)
        
        if not self.is_on_init: self.widget.dump_use_lorentz_factor()

    def set_Monochromator(self):
        self.monochromator_box.setVisible(self.use_twotheta_mono==1)
        self.monochromator_box_empty.setVisible(self.use_twotheta_mono==0)
        
        if not self.is_on_init: self.widget.dump_use_twotheta_mono()

    def set_Polarization(self):
        self.polarization_box.setVisible(self.use_polarization_factor==1)
        self.polarization_box_empty.setVisible(self.use_polarization_factor==0)
        if self.use_polarization_factor==1: self.set_Monochromator()
        
        if not self.is_on_init: self.widget.dump_use_polarization_factor()
        
    def get_lorentz_polarization(self):
        if self.use_polarization_factor == 1:
            congruence.checkPositiveNumber(self.degree_of_polarization, "Deg. Pol.")
            congruence.checkLessOrEqualThan(self.degree_of_polarization, 1.0, "Deg. Pol.", "1.0")

        if self.use_polarization_factor == 1 and self.use_twotheta_mono==1:
            congruence.checkStrictlyPositiveAngle(self.twotheta_mono, "2\u03B8 Monochromator")

        return PolarizationParameters(use_lorentz_factor=self.use_lorentz_factor == 1,
                                      lorentz_formula=self.lorentz_formula,
                                      use_polarization_factor=self.use_polarization_factor,
                                      twotheta_mono=None if (self.use_polarization_factor == 0 or self.use_twotheta_mono == 0) else self.twotheta_mono,
                                      beampath=self.beampath,
                                      degree_of_polarization=self.degree_of_polarization)
    
    def set_data(self, polarization_parameters):
        self.use_lorentz_factor = 1 if polarization_parameters.use_lorentz_factor else self.use_lorentz_factor
        self.lorentz_formula = polarization_parameters.lorentz_formula
        self.use_polarization_factor = 1 if polarization_parameters.use_polarization_factor else self.use_polarization_factor
        if self.use_polarization_factor == 1:
            self.degree_of_polarization = polarization_parameters.degree_of_polarization
            twotheta_mono = polarization_parameters.twotheta_mono
            if not twotheta_mono is None:
                self.use_twotheta_mono = 1
                self.twotheta_mono = twotheta_mono
                self.beampath = polarization_parameters.beampath
            else:
                self.use_twotheta_mono = 0

        self.set_LorentzFactor()
        self.set_Polarization()

if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = OWLorentzPolarization()
    ow.show()
    a.exec_()
    ow.saveSettings()
