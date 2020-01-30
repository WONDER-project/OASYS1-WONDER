import sys, copy

from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtCore import Qt

from orangewidget.settings import Setting
from orangewidget import gui as orangegui
from orangewidget.widget import OWAction

from orangecontrib.wonder.widgets.gui.ow_generic_widget import OWGenericWidget
from orangecontrib.wonder.util.gui_utility import gui, ConfirmDialog
from orangecontrib.wonder.util import congruence
from orangecontrib.wonder.util.fit_utilities import Symmetry

from orangecontrib.wonder.fit.parameters.fit_global_parameters import FitGlobalParameters
from orangecontrib.wonder.fit.parameters.measured_data.phase import Phase

class OWPhases(OWGenericWidget):
    name = "Phases"
    description = "Phases description"
    icon = "icons/phases.png"
    priority = 1.2

    want_main_area = False

    a                                     = Setting([0.0])
    a_fixed                               = Setting([0])
    a_has_min                             = Setting([0])
    a_min                                 = Setting([0.0])
    a_has_max                             = Setting([0])
    a_max                                 = Setting([0.0])
    a_function                            = Setting([0])
    a_function_value                      = Setting([""])
    symmetry                              = Setting([2])
    use_structure                         = Setting([0])
    formula                               = Setting([""])
    intensity_scale_factor                = Setting([1.0])
    intensity_scale_factor_fixed          = Setting([0])
    intensity_scale_factor_has_min        = Setting([0])
    intensity_scale_factor_min            = Setting([0.0])
    intensity_scale_factor_has_max        = Setting([0])
    intensity_scale_factor_max            = Setting([0.0])
    intensity_scale_factor_function       = Setting([0])
    intensity_scale_factor_function_value = Setting([""])
    phase_name                                  = Setting([""])

    inputs = [("Fit Global Parameters", FitGlobalParameters, 'set_data')]
    outputs = [("Fit Global Parameters", FitGlobalParameters)]

    fit_global_parameters = None

    def __init__(self):
        super().__init__(show_automatic_box=True)

        main_box = gui.widgetBox(self.controlArea,
                                 "Phases", orientation="vertical",
                                 width=self.CONTROL_AREA_WIDTH - 5, height=380)

        button_box = gui.widgetBox(main_box,
                                   "", orientation="horizontal",
                                   width=self.CONTROL_AREA_WIDTH - 25)

        gui.button(button_box, self, "Send Phases", height=50, callback=self.send_phases)

        tabs_button_box = gui.widgetBox(main_box, "", addSpace=False, orientation="horizontal")

        btns = [gui.button(tabs_button_box, self, "Insert Phase Before", callback=self.insert_before),
                gui.button(tabs_button_box, self, "Insert Phase After", callback=self.insert_after),
                gui.button(tabs_button_box, self, "Remove Phase", callback=self.remove)]

        for btn in btns:
            btn.setFixedHeight(35)

        self.phases_tabs = gui.tabWidget(main_box)
        self.phases_box_array = []

        for index in range(len(self.a)):
            phase_tab = gui.createTabPage(self.phases_tabs, "Phase " + str(index + 1))
            
            phase_box = PhaseBox(widget=self,
                                 parent=phase_tab,
                                 index = index,
                                 a                                    = self.a[index],
                                 a_fixed                              = self.a_fixed[index],
                                 a_has_min                            = self.a_has_min[index],
                                 a_min                                = self.a_min[index],
                                 a_has_max                            = self.a_has_max[index],
                                 a_max                                = self.a_max[index],
                                 a_function                           = self.a_function[index],
                                 a_function_value                     = self.a_function_value[index],
                                 symmetry                             = self.symmetry[index],
                                 use_structure                        = self.use_structure[index],
                                 formula                              = self.formula[index],
                                 intensity_scale_factor               = self.intensity_scale_factor[index],
                                 intensity_scale_factor_fixed         = self.intensity_scale_factor_fixed[index],
                                 intensity_scale_factor_has_min       = self.intensity_scale_factor_has_min[index],
                                 intensity_scale_factor_min           = self.intensity_scale_factor_min[index],
                                 intensity_scale_factor_has_max       = self.intensity_scale_factor_has_max[index],
                                 intensity_scale_factor_max           = self.intensity_scale_factor_max[index],
                                 intensity_scale_factor_function      = self.intensity_scale_factor_function[index],
                                 intensity_scale_factor_function_value= self.intensity_scale_factor_function_value[index],
                                 phase_name                                 = self.phase_name[index])


            self.phases_box_array.append(phase_box)

        runaction = OWAction("Send Phases", self)
        runaction.triggered.connect(self.send_phases)
        self.addAction(runaction)

        orangegui.rubber(self.controlArea)

    def get_max_height(self):
        return 480

    def insert_before(self):
        current_index = self.phases_tabs.currentIndex()

        if ConfirmDialog.confirmed(parent=self,
                                   message="Confirm Insertion of a new element before " + self.phases_tabs.tabText(
                                           current_index) + "?"):
            phase_tab = gui.widgetBox(self.phases_tabs, addToLayout=0, margin=4)
            phase_box = PhaseBox(widget=self, parent=phase_tab, index=current_index)
            phase_box.after_change_workspace_units()

            self.phases_tabs.insertTab(current_index, phase_tab, "TEMP")
            self.phases_box_array.insert(current_index, phase_box)

            for index in range(current_index, self.phases_tabs.count()):
                self.phases_tabs.setTabText(index, "Phase" + str(index + 1))
                self.phases_box_array[index].index = index

            self.dumpSettings()
            self.phases_tabs.setCurrentIndex(current_index)

    def insert_after(self):
        current_index = self.phases_tabs.currentIndex()

        if ConfirmDialog.confirmed(parent=self,
                                   message="Confirm Insertion of a new element after " + self.phases_tabs.tabText(
                                           current_index) + "?"):
            phase_tab = gui.widgetBox(self.phases_tabs, addToLayout=0, margin=4)
            phase_box = PhaseBox(widget=self, parent=phase_tab, index=current_index + 1)
            phase_box.after_change_workspace_units()

            if current_index == self.phases_tabs.count() - 1:  # LAST
                self.phases_tabs.addTab(phase_tab, "TEMP")
                self.phases_box_array.append(phase_box)
            else:
                self.phases_tabs.insertTab(current_index + 1, phase_tab, "TEMP")
                self.phases_box_array.insert(current_index + 1, phase_box)

            for index in range(current_index, self.phases_tabs.count()):
                self.phases_tabs.setTabText(index, "Phase" + str(index + 1))
                self.phases_box_array[index].index = index

            self.dumpSettings()
            self.phases_tabs.setCurrentIndex(current_index + 1)

    def remove(self):
        if self.phases_tabs.count() <= 1:
            QMessageBox.critical(self, "Error",
                                 "Remove not possible, Fit process needs at least 1 element",
                                 QMessageBox.Ok)
        else:
            current_index = self.phases_tabs.currentIndex()

            if ConfirmDialog.confirmed(parent=self,
                                       message="Confirm Removal of " + self.phases_tabs.tabText(
                                               current_index) + "?"):
                self.phases_tabs.removeTab(current_index)
                self.phases_box_array.pop(current_index)

                for index in range(current_index, self.phases_tabs.count()):
                    self.phases_tabs.setTabText(index, "Phase" + str(index + 1))
                    self.phases_box_array[index].index = index

                self.dumpSettings()
                self.phases_tabs.setCurrentIndex(current_index)

    def send_phases(self):
        try:
            if not self.fit_global_parameters is None:
                self.dumpSettings()

                self.check_congruence()

                phases = [self.phases_box_array[index].get_phase() for index in range(len(self.phases_box_array))]

                self.fit_global_parameters.measured_dataset.set_phases(phases)
                self.fit_global_parameters.evaluate_functions()  # in case that a is a function of other parameters

                self.fit_global_parameters.regenerate_parameters()

                self.send("Fit Global Parameters", self.fit_global_parameters)

        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 str(e),
                                 QMessageBox.Ok)

            if self.IS_DEVELOP: raise e

    def check_congruence(self):
        use_structure_first = self.phases_box_array[0].use_structure

        for index in range(1, len(self.phases_box_array)):
            if use_structure_first != self.phases_box_array[index].use_structure:
                raise Exception("Incongruity: all the Phases must have the same setup of the structural model")

    def set_data(self, data):
        if not data is None:
            try:
                self.fit_global_parameters = data.duplicate()

                diffraction_patterns = self.fit_global_parameters.measured_dataset.diffraction_patterns
                phases               = self.fit_global_parameters.measured_dataset.phases

                if diffraction_patterns is None: raise ValueError("No Diffraction Pattern in input data!")

                if not phases is None:
                    if (len(phases) != len(self.phases_box_array)):
                        recycle = ConfirmDialog.confirmed(message="Number of phases changed:\ndo you want to use the existing phases where possible?\n\nIf yes, check for possible incongruences",
                                                          title="Warning")

                        self.phases_tabs.clear()
                        self.phases_box_array = []

                        for index in range(len(phases)):
                            phase_tab = gui.createTabPage(self.phases_tabs, "Phase " + str(index + 1))

                            if recycle and index < len(self.a): #keep the existing
                                phase_box = PhaseBox(widget=self,
                                                     parent=phase_tab,
                                                     index = index,
                                                     a                                    = self.a[index],
                                                     a_fixed                              = self.a_fixed[index],
                                                     a_has_min                            = self.a_has_min[index],
                                                     a_min                                = self.a_min[index],
                                                     a_has_max                            = self.a_has_max[index],
                                                     a_max                                = self.a_max[index],
                                                     a_function                           = self.a_function[index],
                                                     a_function_value                     = self.a_function_value[index],
                                                     symmetry                             = self.symmetry[index],
                                                     use_structure                        = self.use_structure[index],
                                                     formula                              = self.formula[index],
                                                     intensity_scale_factor               = self.intensity_scale_factor[index],
                                                     intensity_scale_factor_fixed         = self.intensity_scale_factor_fixed[index],
                                                     intensity_scale_factor_has_min       = self.intensity_scale_factor_has_min[index],
                                                     intensity_scale_factor_min           = self.intensity_scale_factor_min[index],
                                                     intensity_scale_factor_has_max       = self.intensity_scale_factor_has_max[index],
                                                     intensity_scale_factor_max           = self.intensity_scale_factor_max[index],
                                                     intensity_scale_factor_function      = self.intensity_scale_factor_function[index],
                                                     intensity_scale_factor_function_value= self.intensity_scale_factor_function_value[index],
                                                     phase_name                                 = self.phase_name[index])
                            else:
                                phase_box = PhaseBox(widget=self, parent=phase_tab, index = index)

                            self.phases_box_array.append(phase_box)
                    else:
                        for index in range(len(phases)):
                            self.phases_box_array[index].set_data(phases[index])

                self.dumpSettings()

                if self.is_automatic_run:
                    self.send_phases()

            except Exception as e:
                QMessageBox.critical(self, "Error",
                                     str(e),
                                     QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    ##############################
    # SINGLE FIELDS SIGNALS
    ##############################

    def dumpSettings(self):
        self.dump_a()
        self.dump_symmetry()
        self.dump_use_structure()
        self.dump_formula()
        self.dump_intensity_scale_factor()
        self.dump_phase_name()
        
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

            for index in range(len(self.phases_box_array)):
                self.a.append(self.phases_box_array[index].a)
                self.a_fixed.append(self.phases_box_array[index].a_fixed)
                self.a_has_min.append(self.phases_box_array[index].a_has_min)
                self.a_min.append(self.phases_box_array[index].a_min)
                self.a_has_max.append(self.phases_box_array[index].a_has_max)
                self.a_max.append(self.phases_box_array[index].a_max)
                self.a_function.append(self.phases_box_array[index].a_function)
                self.a_function_value.append(self.phases_box_array[index].a_function_value)
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

    def dump_symmetry(self):
        bkp_symmetry = copy.deepcopy(self.symmetry)

        try:
            self.symmetry = []

            for index in range(len(self.phases_box_array)):
                self.symmetry.append(self.phases_box_array[index].symmetry)
        except:
            self.symmetry = copy.deepcopy(bkp_symmetry)

    def dump_use_structure(self):
        bkp_use_structure = copy.deepcopy(self.use_structure)

        try:
            self.use_structure = []

            for index in range(len(self.phases_box_array)):
                self.use_structure.append(self.phases_box_array[index].use_structure)
        except:
            self.use_structure = copy.deepcopy(bkp_use_structure)

    def dump_formula(self):
        bkp_formula = copy.deepcopy(self.formula)

        try:
            self.formula = []

            for index in range(len(self.phases_box_array)):
                self.formula.append(self.phases_box_array[index].formula)
        except:
            self.formula = copy.deepcopy(bkp_formula)

    def dump_intensity_scale_factor(self):
        bkp_intensity_scale_factor = copy.deepcopy(self.intensity_scale_factor)
        bkp_intensity_scale_factor_fixed = copy.deepcopy(self.intensity_scale_factor_fixed)
        bkp_intensity_scale_factor_has_min = copy.deepcopy(self.intensity_scale_factor_has_min)
        bkp_intensity_scale_factor_min = copy.deepcopy(self.intensity_scale_factor_min)
        bkp_intensity_scale_factor_has_max = copy.deepcopy(self.intensity_scale_factor_has_max)
        bkp_intensity_scale_factor_max = copy.deepcopy(self.intensity_scale_factor_max)
        bkp_intensity_scale_factor_function = copy.deepcopy(self.intensity_scale_factor_function)
        bkp_intensity_scale_factor_function_value = copy.deepcopy(self.intensity_scale_factor_function_value)

        try:
            self.intensity_scale_factor = []
            self.intensity_scale_factor_fixed = []
            self.intensity_scale_factor_has_min = []
            self.intensity_scale_factor_min = []
            self.intensity_scale_factor_has_max = []
            self.intensity_scale_factor_max = []
            self.intensity_scale_factor_function = []
            self.intensity_scale_factor_function_value = []

            for index in range(len(self.phases_box_array)):
                self.intensity_scale_factor.append(self.phases_box_array[index].intensity_scale_factor)
                self.intensity_scale_factor_fixed.append(self.phases_box_array[index].intensity_scale_factor_fixed)
                self.intensity_scale_factor_has_min.append(self.phases_box_array[index].intensity_scale_factor_has_min)
                self.intensity_scale_factor_min.append(self.phases_box_array[index].intensity_scale_factor_min)
                self.intensity_scale_factor_has_max.append(self.phases_box_array[index].intensity_scale_factor_has_max)
                self.intensity_scale_factor_max.append(self.phases_box_array[index].intensity_scale_factor_max)
                self.intensity_scale_factor_function.append(self.phases_box_array[index].intensity_scale_factor_function)
                self.intensity_scale_factor_function_value.append(self.phases_box_array[index].intensity_scale_factor_function_value)
        except:
            self.intensity_scale_factor = copy.deepcopy(bkp_intensity_scale_factor)
            self.intensity_scale_factor_fixed = copy.deepcopy(bkp_intensity_scale_factor_fixed)
            self.intensity_scale_factor_has_min = copy.deepcopy(bkp_intensity_scale_factor_has_min)
            self.intensity_scale_factor_min = copy.deepcopy(bkp_intensity_scale_factor_min)
            self.intensity_scale_factor_has_max = copy.deepcopy(bkp_intensity_scale_factor_has_max)
            self.intensity_scale_factor_max = copy.deepcopy(bkp_intensity_scale_factor_max)
            self.intensity_scale_factor_function = copy.deepcopy(bkp_intensity_scale_factor_function)
            self.intensity_scale_factor_function_value = copy.deepcopy(bkp_intensity_scale_factor_function_value)

    def dump_phase_name(self):
        bkp_phase_name = copy.deepcopy(self.phase_name)

        try:
            self.phase_name = []

            for index in range(len(self.phases_box_array)):
                self.phase_name.append(self.phases_box_array[index].phase_name)
        except:
            self.phase_name = copy.deepcopy(bkp_phase_name)

from PyQt5.QtWidgets import QVBoxLayout
from orangecontrib.wonder.util.gui_utility import InnerBox

class PhaseBox(InnerBox):
    a = 0.0
    a_fixed = 0
    a_has_min = 0
    a_min = 0.0
    a_has_max = 0
    a_max = 0.0
    a_function = 0
    a_function_value = ""
    symmetry = 2
    use_structure = 0
    formula = ""
    intensity_scale_factor = 1.0
    intensity_scale_factor_fixed = 0
    intensity_scale_factor_has_min = 0
    intensity_scale_factor_min = 0.0
    intensity_scale_factor_has_max = 0
    intensity_scale_factor_max = 0.0
    intensity_scale_factor_function = 0
    intensity_scale_factor_function_value = ""
    phase_name = ""

    widget = None
    is_on_init = True

    parameter_functions = {}

    phase = None

    index = 0

    def __init__(self,
                 widget=None,
                 parent=None,
                 index=0,
                 a=0.0,
                 a_fixed=0,
                 a_has_min=0,
                 a_min=0.0,
                 a_has_max=0,
                 a_max=0.0,
                 a_function=0,
                 a_function_value="",
                 symmetry=2,
                 use_structure=0,
                 formula="",
                 intensity_scale_factor=1.0,
                 intensity_scale_factor_fixed=0,
                 intensity_scale_factor_has_min=0,
                 intensity_scale_factor_min=0.0,
                 intensity_scale_factor_has_max=0,
                 intensity_scale_factor_max=0.0,
                 intensity_scale_factor_function=0,
                 intensity_scale_factor_function_value="",
                 phase_name=""):
        super(PhaseBox, self).__init__()

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.setFixedWidth(widget.CONTROL_AREA_WIDTH - 35)
        self.setFixedHeight(300)

        self.widget = widget
        self.index = index

        self.a = a
        self.a_fixed = a_fixed
        self.a_has_min = a_has_min
        self.a_min = a_min
        self.a_has_max = a_has_max
        self.a_max = a_max
        self.a_function = a_function
        self.a_function_value = a_function_value
        self.symmetry = symmetry
        self.use_structure = use_structure
        self.formula = formula
        self.intensity_scale_factor = intensity_scale_factor
        self.intensity_scale_factor_fixed = intensity_scale_factor_fixed
        self.intensity_scale_factor_has_min = intensity_scale_factor_has_min
        self.intensity_scale_factor_min = intensity_scale_factor_min
        self.intensity_scale_factor_has_max = intensity_scale_factor_has_max
        self.intensity_scale_factor_max = intensity_scale_factor_max
        self.intensity_scale_factor_function = intensity_scale_factor_function
        self.intensity_scale_factor_function_value = intensity_scale_factor_function_value
        self.phase_name=phase_name

        self.CONTROL_AREA_WIDTH = widget.CONTROL_AREA_WIDTH - 45

        parent.layout().addWidget(self)
        container = self

        gui.lineEdit(container, self, "phase_name", "Phase id", labelWidth=110, valueType=str, callback=widget.dump_phase_name)

        self.cb_symmetry = orangegui.comboBox(container, self, "symmetry", label="Symmetry", items=Symmetry.tuple(),
                                              callback=self.set_symmetry, orientation="horizontal")

        OWGenericWidget.create_box_in_widget(self, container, "a", "a [nm]", add_callback=True, min_value=0.0,
                                             min_accepted=False, trim=5)

        orangegui.separator(container)

        structure_box = gui.widgetBox(container,
                                      "", orientation="vertical",
                                      width=self.CONTROL_AREA_WIDTH)

        orangegui.comboBox(structure_box, self, "use_structure", label="Use Structural Model", items=["No", "Yes"],
                           callback=self.set_structure, labelWidth=350, orientation="horizontal")

        self.structure_box_1 = gui.widgetBox(structure_box,
                                             "", orientation="vertical",
                                             width=self.CONTROL_AREA_WIDTH - 5, height=60)

        gui.lineEdit(self.structure_box_1, self, "formula", "Chemical Formula", labelWidth=110, valueType=str,
                     callback=widget.dump_formula)

        OWGenericWidget.create_box_in_widget(self, self.structure_box_1, "intensity_scale_factor", "I0",
                                             add_callback=True, min_value=0.0, min_accepted=False, trim=5)

        self.structure_box_2 = gui.widgetBox(structure_box,
                                             "", orientation="vertical",
                                             width=self.CONTROL_AREA_WIDTH - 5, height=60)


        self.set_structure()

        self.is_on_init = False

    def after_change_workspace_units(self):
        pass

    def set_index(self, index):
        self.index = index

    def set_structure(self):
        self.structure_box_1.setVisible(self.use_structure == 1)
        self.structure_box_2.setVisible(self.use_structure == 0)

        if not self.is_on_init: self.widget.dump_use_structure()

    def set_symmetry(self):
        if not Phase.is_cube(self.cb_symmetry.currentText()):
            QMessageBox.critical(self, "Error",
                                 "Only Cubic Systems are supported",
                                 QMessageBox.Ok)

            self.symmetry = 2

        if not self.is_on_init: self.widget.dump_symmetry()

    def callback_a(self):
        if not self.is_on_init: self.widget.dump_a()

    def callback_intensity_scale_factor(self):
        if not self.is_on_init: self.widget.dump_intensity_scale_factor()

    def get_parameters_prefix(self):
        return Phase.get_parameters_prefix() + self.get_parameter_progressive()

    def get_parameter_progressive(self):
        return str(self.index + 1) + "_"

    def set_data(self, phase):
        OWGenericWidget.populate_fields_in_widget(self, "a", phase.a)
        self.use_structure = 1 if phase.use_structure else 0

        if self.use_structure == 1:
            OWGenericWidget.populate_fields_in_widget(self, "intensity_scale_factor", phase.intensity_scale_factor)
            self.formula = phase.formula

        simmetries = Symmetry.tuple()
        for index in range(0, len(simmetries)):
            if simmetries[index] == phase.symmetry:
                self.symmetry = index

        self.set_structure()
        self.set_symmetry()

    def get_phase(self):
        if self.use_structure == 0:
            phase = Phase.init_cube(a0=OWGenericWidget.populate_parameter_in_widget(self, "a", self.get_parameters_prefix()),
                                    symmetry=self.cb_symmetry.currentText(),
                                    name=self.phase_name,
                                    progressive=self.get_parameter_progressive())
        elif self.use_structure == 1:
            phase = Phase.init_cube(a0=OWGenericWidget.populate_parameter_in_widget(self, "a", self.get_parameters_prefix()),
                                    symmetry=self.cb_symmetry.currentText(),
                                    use_structure=True,
                                    formula=congruence.checkEmptyString(self.formula, "Chemical Formula"),
                                    intensity_scale_factor=OWGenericWidget.populate_parameter_in_widget(self, "intensity_scale_factor", self.get_parameters_prefix()),
                                    name=self.phase_name,
                                    progressive=self.get_parameter_progressive())

        return phase


if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = OWPhases()
    ow.show()
    a.exec_()
    ow.saveSettings()
