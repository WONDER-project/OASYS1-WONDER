import sys, copy

from PyQt5.QtWidgets import QMessageBox, QApplication

from orangewidget.settings import Setting
from orangewidget import gui as orangegui
from orangewidget.widget import OWAction

from orangecontrib.wonder.widgets.gui.ow_generic_widget import OWGenericWidget
from orangecontrib.wonder.util.gui_utility import gui
from orangecontrib.wonder.fit.parameters.fit_global_parameters import FitGlobalParameters
from orangecontrib.wonder.fit.parameters.microstructure.strain import InvariantPAH, InvariantPAHLaueGroup14, InvariantPAHLaueGroup13, LaueGroup
from orangecontrib.wonder.fit.parameters.measured_data.phase import Phase

class OWStrainInvariant(OWGenericWidget):
    name = "Invariant PAH Strain"
    description = "Define Invariant PAH Strain"
    icon = "icons/strain.png"
    priority = 17

    want_main_area =  False

    active = Setting([1])
    laue_id = Setting([13])

    aa = Setting([0.0])
    aa_fixed = Setting([0])
    aa_has_min = Setting([0])
    aa_min = Setting([0.0])
    aa_has_max = Setting([0])
    aa_max = Setting([0.0])
    aa_function = Setting([0])
    aa_function_value = Setting([""])

    bb = Setting([0.0])
    bb_fixed = Setting([0])
    bb_has_min = Setting([0])
    bb_min = Setting([0.0])
    bb_has_max = Setting([0])
    bb_max = Setting([0.0])
    bb_function = Setting([0])
    bb_function_value = Setting([""])

    e1 = Setting([0.0])
    e1_fixed = Setting([0])
    e1_has_min = Setting([0])
    e1_min = Setting([0.0])
    e1_has_max = Setting([0])
    e1_max = Setting([0.0])
    e1_function = Setting([0])
    e1_function_value = Setting([""])

    e4 = Setting([0.0])
    e4_fixed = Setting([0])
    e4_has_min = Setting([0])
    e4_min = Setting([0.0])
    e4_has_max = Setting([0])
    e4_max = Setting([0.0])
    e4_function = Setting([0])
    e4_function_value = Setting([""])

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

        for index in range(len(self.aa)):
            strain_box = StrainBox(widget=self,
                                   parent=gui.createTabPage(self.strains_tabs, Phase.get_default_name(index)),
                                   index = index,
                                   active = self.active[index],
                                   laue_id=self.laue_id[index],
                                   aa=self.aa[index],
                                   aa_fixed=self.aa_fixed[index],
                                   aa_has_min=self.aa_has_min[index],
                                   aa_min=self.aa_min[index],
                                   aa_has_max=self.aa_has_max[index],
                                   aa_max=self.aa_max[index],
                                   aa_function=self.aa_function[index],
                                   aa_function_value=self.aa_function_value[index],
                                   bb=self.bb[index],
                                   bb_fixed=self.bb_fixed[index],
                                   bb_has_min=self.bb_has_min[index],
                                   bb_min=self.bb_min[index],
                                   bb_has_max=self.bb_has_max[index],
                                   bb_max=self.bb_max[index],
                                   bb_function=self.bb_function[index],
                                   bb_function_value=self.bb_function_value[index],
                                   e1=self.e1[index],
                                   e1_fixed=self.e1_fixed[index],
                                   e1_has_min=self.e1_has_min[index],
                                   e1_min=self.e1_min[index],
                                   e1_has_max=self.e1_has_max[index],
                                   e1_max=self.e1_max[index],
                                   e1_function=self.e1_function[index],
                                   e1_function_value=self.e1_function_value[index],
                                   e4=self.e4[index],
                                   e4_fixed=self.e4_fixed[index],
                                   e4_has_min=self.e4_has_min[index],
                                   e4_min=self.e4_min[index],
                                   e4_has_max=self.e4_has_max[index],
                                   e4_max=self.e4_max[index],
                                   e4_function=self.e4_function[index],
                                   e4_function_value=self.e4_function_value[index])

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

                tabs_to_remove = len(self.aa)-len(phases)

                if tabs_to_remove > 0:
                    for index in range(tabs_to_remove):
                        self.strains_tabs.removeTab(-1)
                        self.strains_box_array.pop()

                for phase_index in range(len(phases)):
                    if not self.fit_global_parameters.strain_parameters is None:
                        strain_parameters = self.fit_global_parameters.get_strain_parameters(phase_index)
                    else:
                        strain_parameters = None

                    if phase_index < len(self.aa):
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
        self.dump_laue_id()
        self.dump_aa()
        self.dump_bb()
        self.dump_e1()
        self.dump_e4()

    def dump_active(self):
        bkp_active = copy.deepcopy(self.active)

        try:
            self.active = []

            for index in range(len(self.strains_box_array)):
                self.active.append(self.strains_box_array[index].active)
        except Exception as e:
            self.active = copy.deepcopy(bkp_active)

            if self.IS_DEVELOP: raise  e
            
    def dump_laue_id(self):
        bkp_laue_id = copy.deepcopy(self.laue_id)

        try:
            self.laue_id = []

            for index in range(len(self.strains_box_array)):
                self.laue_id.append(self.strains_box_array[index].laue_id)
        except Exception as e:
            self.laue_id = copy.deepcopy(bkp_laue_id)

            if self.IS_DEVELOP: raise  e
            
    def dump_aa(self):
        bkp_aa = copy.deepcopy(self.aa)
        bkp_aa_fixed = copy.deepcopy(self.aa_fixed)
        bkp_aa_has_min = copy.deepcopy(self.aa_has_min)
        bkp_aa_min = copy.deepcopy(self.aa_min)
        bkp_aa_has_max = copy.deepcopy(self.aa_has_max)
        bkp_aa_max = copy.deepcopy(self.aa_max)
        bkp_aa_function = copy.deepcopy(self.aa_function)
        bkp_aa_function_value = copy.deepcopy(self.aa_function_value)

        try:
            self.aa = []
            self.aa_fixed = []
            self.aa_has_min = []
            self.aa_min = []
            self.aa_has_max = []
            self.aa_max = []
            self.aa_function = []
            self.aa_function_value = []

            for index in range(len(self.strains_box_array)):
                self.aa.append(self.strains_box_array[index].aa)
                self.aa_fixed.append(self.strains_box_array[index].aa_fixed)
                self.aa_has_min.append(self.strains_box_array[index].aa_has_min)
                self.aa_min.append(self.strains_box_array[index].aa_min)
                self.aa_has_max.append(self.strains_box_array[index].aa_has_max)
                self.aa_max.append(self.strains_box_array[index].aa_max)
                self.aa_function.append(self.strains_box_array[index].aa_function)
                self.aa_function_value.append(self.strains_box_array[index].aa_function_value)
        except Exception as e:
            self.aa = copy.deepcopy(bkp_aa)
            self.aa_fixed = copy.deepcopy(bkp_aa_fixed)
            self.aa_has_min = copy.deepcopy(bkp_aa_has_min)
            self.aa_min = copy.deepcopy(bkp_aa_min)
            self.aa_has_max = copy.deepcopy(bkp_aa_has_max)
            self.aa_max = copy.deepcopy(bkp_aa_max)
            self.aa_function = copy.deepcopy(bkp_aa_function)
            self.aa_function_value = copy.deepcopy(bkp_aa_function_value)

            if self.IS_DEVELOP: raise  e

    def dump_bb(self):
        bkp_bb = copy.deepcopy(self.bb)
        bkp_bb_fixed = copy.deepcopy(self.bb_fixed)
        bkp_bb_has_min = copy.deepcopy(self.bb_has_min)
        bkp_bb_min = copy.deepcopy(self.bb_min)
        bkp_bb_has_max = copy.deepcopy(self.bb_has_max)
        bkp_bb_max = copy.deepcopy(self.bb_max)
        bkp_bb_function = copy.deepcopy(self.bb_function)
        bkp_bb_function_value = copy.deepcopy(self.bb_function_value)

        try:
            self.bb = []
            self.bb_fixed = []
            self.bb_has_min = []
            self.bb_min = []
            self.bb_has_max = []
            self.bb_max = []
            self.bb_function = []
            self.bb_function_value = []

            for index in range(len(self.strains_box_array)):
                self.bb.append(self.strains_box_array[index].bb)
                self.bb_fixed.append(self.strains_box_array[index].bb_fixed)
                self.bb_has_min.append(self.strains_box_array[index].bb_has_min)
                self.bb_min.append(self.strains_box_array[index].bb_min)
                self.bb_has_max.append(self.strains_box_array[index].bb_has_max)
                self.bb_max.append(self.strains_box_array[index].bb_max)
                self.bb_function.append(self.strains_box_array[index].bb_function)
                self.bb_function_value.append(self.strains_box_array[index].bb_function_value)
        except Exception as e:
            self.bb = copy.deepcopy(bkp_bb)
            self.bb_fixed = copy.deepcopy(bkp_bb_fixed)
            self.bb_has_min = copy.deepcopy(bkp_bb_has_min)
            self.bb_min = copy.deepcopy(bkp_bb_min)
            self.bb_has_max = copy.deepcopy(bkp_bb_has_max)
            self.bb_max = copy.deepcopy(bkp_bb_max)
            self.bb_function = copy.deepcopy(bkp_bb_function)
            self.bb_function_value = copy.deepcopy(bkp_bb_function_value)

            if self.IS_DEVELOP: raise  e

    def dump_e1(self):
        bkp_e1 = copy.deepcopy(self.e1)
        bkp_e1_fixed = copy.deepcopy(self.e1_fixed)
        bkp_e1_has_min = copy.deepcopy(self.e1_has_min)
        bkp_e1_min = copy.deepcopy(self.e1_min)
        bkp_e1_has_max = copy.deepcopy(self.e1_has_max)
        bkp_e1_max = copy.deepcopy(self.e1_max)
        bkp_e1_function = copy.deepcopy(self.e1_function)
        bkp_e1_function_value = copy.deepcopy(self.e1_function_value)

        try:
            self.e1 = []
            self.e1_fixed = []
            self.e1_has_min = []
            self.e1_min = []
            self.e1_has_max = []
            self.e1_max = []
            self.e1_function = []
            self.e1_function_value = []

            for index in range(len(self.strains_box_array)):
                self.e1.append(self.strains_box_array[index].e1)
                self.e1_fixed.append(self.strains_box_array[index].e1_fixed)
                self.e1_has_min.append(self.strains_box_array[index].e1_has_min)
                self.e1_min.append(self.strains_box_array[index].e1_min)
                self.e1_has_max.append(self.strains_box_array[index].e1_has_max)
                self.e1_max.append(self.strains_box_array[index].e1_max)
                self.e1_function.append(self.strains_box_array[index].e1_function)
                self.e1_function_value.append(self.strains_box_array[index].e1_function_value)
        except Exception as e:
            self.e1 = copy.deepcopy(bkp_e1)
            self.e1_fixed = copy.deepcopy(bkp_e1_fixed)
            self.e1_has_min = copy.deepcopy(bkp_e1_has_min)
            self.e1_min = copy.deepcopy(bkp_e1_min)
            self.e1_has_max = copy.deepcopy(bkp_e1_has_max)
            self.e1_max = copy.deepcopy(bkp_e1_max)
            self.e1_function = copy.deepcopy(bkp_e1_function)
            self.e1_function_value = copy.deepcopy(bkp_e1_function_value)

            if self.IS_DEVELOP: raise  e

    def dump_e4(self):
        bkp_e4 = copy.deepcopy(self.e4)
        bkp_e4_fixed = copy.deepcopy(self.e4_fixed)
        bkp_e4_has_min = copy.deepcopy(self.e4_has_min)
        bkp_e4_min = copy.deepcopy(self.e4_min)
        bkp_e4_has_max = copy.deepcopy(self.e4_has_max)
        bkp_e4_max = copy.deepcopy(self.e4_max)
        bkp_e4_function = copy.deepcopy(self.e4_function)
        bkp_e4_function_value = copy.deepcopy(self.e4_function_value)

        try:
            self.e4 = []
            self.e4_fixed = []
            self.e4_has_min = []
            self.e4_min = []
            self.e4_has_max = []
            self.e4_max = []
            self.e4_function = []
            self.e4_function_value = []

            for index in range(len(self.strains_box_array)):
                self.e4.append(self.strains_box_array[index].e4)
                self.e4_fixed.append(self.strains_box_array[index].e4_fixed)
                self.e4_has_min.append(self.strains_box_array[index].e4_has_min)
                self.e4_min.append(self.strains_box_array[index].e4_min)
                self.e4_has_max.append(self.strains_box_array[index].e4_has_max)
                self.e4_max.append(self.strains_box_array[index].e4_max)
                self.e4_function.append(self.strains_box_array[index].e4_function)
                self.e4_function_value.append(self.strains_box_array[index].e4_function_value)
        except Exception as e:
            self.e4 = copy.deepcopy(bkp_e4)
            self.e4_fixed = copy.deepcopy(bkp_e4_fixed)
            self.e4_has_min = copy.deepcopy(bkp_e4_has_min)
            self.e4_min = copy.deepcopy(bkp_e4_min)
            self.e4_has_max = copy.deepcopy(bkp_e4_has_max)
            self.e4_max = copy.deepcopy(bkp_e4_max)
            self.e4_function = copy.deepcopy(bkp_e4_function)
            self.e4_function_value = copy.deepcopy(bkp_e4_function_value)

            if self.IS_DEVELOP: raise  e



from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
from orangecontrib.wonder.util.gui_utility import InnerBox

class StrainBox(InnerBox):
    active = 1
    laue_id = 13
    aa = 0.0
    aa_fixed = 0
    aa_has_min = 0
    aa_min = 0.0
    aa_has_max = 0
    aa_max = 0.0
    aa_function = 0
    aa_function_value = ""
    bb = 0.0
    bb_fixed = 0
    bb_has_min = 0
    bb_min = 0.0
    bb_has_max = 0
    bb_max = 0.0
    bb_function = 0
    bb_function_value = ""
    e1 = 0.0
    e1_fixed = 0
    e1_has_min = 0
    e1_min = 0.0
    e1_has_max = 0
    e1_max = 0.0
    e1_function = 0
    e1_function_value = ""
    e4 = 0.0
    e4_fixed = 0
    e4_has_min = 0
    e4_min = 0.0
    e4_has_max = 0
    e4_max = 0.0
    e4_function = 0
    e4_function_value = ""

    widget = None
    is_on_init = True

    parameter_functions = {}

    index = 0

    def __init__(self,
                 widget=None,
                 parent=None,
                 index=0,
                 active=1,
                 laue_id=13,
                 aa = 0.0,
                 aa_fixed = 0,
                 aa_has_min = 0,
                 aa_min = 0.0,
                 aa_has_max = 0,
                 aa_max = 0.0,
                 aa_function = 0,
                 aa_function_value = "",
                 bb = 0.0,
                 bb_fixed = 0,
                 bb_has_min = 0,
                 bb_min = 0.0,
                 bb_has_max = 0,
                 bb_max = 0.0,
                 bb_function = 0,
                 bb_function_value = "",
                 e1 = 0.0,
                 e1_fixed = 0,
                 e1_has_min = 0,
                 e1_min = 0.0,
                 e1_has_max = 0,
                 e1_max = 0.0,
                 e1_function = 0,
                 e1_function_value = "",
                 e4 = 0.0,
                 e4_fixed = 0,
                 e4_has_min = 0,
                 e4_min = 0.0,
                 e4_has_max = 0,
                 e4_max = 0.0,
                 e4_function = 0,
                 e4_function_value = ""):
        super(StrainBox, self).__init__()

        self.widget = widget

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.setFixedWidth(widget.CONTROL_AREA_WIDTH - 35)
        self.setFixedHeight(300)

        self.index = index

        self.active            = active
        self.laue_id           = laue_id 
        self.aa                = aa 
        self.aa_fixed          = aa_fixed
        self.aa_has_min        = aa_has_min
        self.aa_min            = aa_min 
        self.aa_has_max        = aa_has_max
        self.aa_max            = aa_max 
        self.aa_function       = aa_function
        self.aa_function_value = aa_function_value
        self.bb                = bb 
        self.bb_fixed          = bb_fixed
        self.bb_has_min        = bb_has_min
        self.bb_min            = bb_min 
        self.bb_has_max        = bb_has_max
        self.bb_max            = bb_max 
        self.bb_function       = bb_function
        self.bb_function_value = bb_function_value
        self.e1                = e1 
        self.e1_fixed          = e1_fixed
        self.e1_has_min        = e1_has_min
        self.e1_min            = e1_min 
        self.e1_has_max        = e1_has_max
        self.e1_max            = e1_max 
        self.e1_function       = e1_function
        self.e1_function_value = e1_function_value
        self.e4                = e4 
        self.e4_fixed          = e4_fixed
        self.e4_has_min        = e4_has_min
        self.e4_min            = e4_min 
        self.e4_has_max        = e4_has_max
        self.e4_max            = e4_max 
        self.e4_function       = e4_function
        self.e4_function_value = e4_function_value
        
        self.CONTROL_AREA_WIDTH = widget.CONTROL_AREA_WIDTH-45

        parent.layout().addWidget(self)
        container = self

        self.cb_active = orangegui.comboBox(container, self, "active", label="Active", items=["No", "Yes"], callback=self.set_active, orientation="horizontal")

        self.main_box = gui.widgetBox(container, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH-10)

        OWGenericWidget.create_box_in_widget(self, self.main_box, "aa", add_callback=True, min_value=0.0, min_accepted=True, trim=25)
        OWGenericWidget.create_box_in_widget(self, self.main_box, "bb", add_callback=True, min_value=0.0, min_accepted=True, trim=25)

        invariant_box = gui.widgetBox(self.main_box, "Invariant Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH - 10)

        self.cb_laue_id = orangegui.comboBox(invariant_box, self, "laue_id", label="Laue Group", items=LaueGroup.tuple(), callback=self.set_laue_id, orientation="horizontal")

        OWGenericWidget.create_box_in_widget(self, invariant_box, "e1", add_callback=True, trim=25)
        OWGenericWidget.create_box_in_widget(self, invariant_box, "e4", add_callback=True, trim=25)
        
        self.set_active()

        self.is_on_init = False

    def after_change_workspace_units(self):
        pass

    def set_index(self, index):
        self.index = index

    def set_active(self):
        self.main_box.setEnabled(self.active == 1)

        if not self.is_on_init: self.widget.dump_active()

    def set_laue_id(self):
        if not (self.laue_id == 12 or self.laue_id == 13):
            QMessageBox.critical(self, "Error",
                                 "Only " + LaueGroup.get_laue_group(14) + " and " + LaueGroup.get_laue_group(13) + " are supported",
                                 QMessageBox.Ok)

            self.laue_id = 13
            
            self.widget.dump_laue_id()

    def callback_aa(self):
        if not self.is_on_init: self.widget.dump_aa()

    def callback_bb(self):
        if not self.is_on_init: self.widget.dump_bb()

    def callback_e1(self):
        if not self.is_on_init: self.widget.dump_e1()

    def callback_e4(self):
        if not self.is_on_init: self.widget.dump_e4()

    def get_parameters_prefix(self):
        return InvariantPAH.get_parameters_prefix() + self.get_parameter_progressive()

    def get_parameter_progressive(self):
        return str(self.index + 1) + "_"

    def set_data(self, strain_parameters):
        OWGenericWidget.populate_fields_in_widget(self, "aa", strain_parameters.aa)
        OWGenericWidget.populate_fields_in_widget(self, "bb", strain_parameters.bb)
        OWGenericWidget.populate_fields_in_widget(self, "e1", strain_parameters.e1)
        OWGenericWidget.populate_fields_in_widget(self, "e4", strain_parameters.e4)

    def get_strain_parameters(self):
        if self.active == 0: return None
        else:
            if self.laue_id == 12:
                return InvariantPAHLaueGroup13(aa=OWGenericWidget.populate_parameter_in_widget(self, "aa", self.get_parameters_prefix()),
                                               bb=OWGenericWidget.populate_parameter_in_widget(self, "bb", self.get_parameters_prefix()),
                                               e1=OWGenericWidget.populate_parameter_in_widget(self, "e1", self.get_parameters_prefix()),
                                               e4=OWGenericWidget.populate_parameter_in_widget(self, "e4", self.get_parameters_prefix()))
            elif self.laue_id == 13:
                return InvariantPAHLaueGroup14(aa=OWGenericWidget.populate_parameter_in_widget(self, "aa", self.get_parameters_prefix()),
                                               bb=OWGenericWidget.populate_parameter_in_widget(self, "bb", self.get_parameters_prefix()),
                                               e1=OWGenericWidget.populate_parameter_in_widget(self, "e1", self.get_parameters_prefix()),
                                               e4=OWGenericWidget.populate_parameter_in_widget(self, "e4", self.get_parameters_prefix()))
            else:
                return None



if __name__ == "__main__":
    a =  QApplication(sys.argv)
    ow = OWStrainInvariant()
    ow.show()
    a.exec_()
    ow.saveSettings()
