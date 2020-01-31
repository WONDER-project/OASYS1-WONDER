import sys, copy

from PyQt5.QtWidgets import QMessageBox, QApplication

from orangewidget.settings import Setting
from orangewidget import gui as orangegui
from orangewidget.widget import OWAction

from orangecontrib.wonder.widgets.gui.ow_generic_widget import OWGenericWidget
from orangecontrib.wonder.util.gui_utility import gui
from orangecontrib.wonder.util import congruence
from orangecontrib.wonder.fit.parameters.fit_global_parameters import FitGlobalParameters
from orangecontrib.wonder.fit.parameters.measured_data.phase import Phase
from orangecontrib.wonder.fit.parameters.microstructure.size import SizeParameters
from orangecontrib.wonder.fit.wppm_functions import Distribution, Normalization, Shape, WulffCubeFace

class OWSize(OWGenericWidget):

    name = "Size"
    description = "Define Size"
    icon = "icons/size.png"
    priority = 16

    want_main_area =  False

    active = Setting([1])

    shape = Setting([1])
    distribution = Setting([1])

    mu = Setting([4.0])
    mu_fixed = Setting([0])
    mu_has_min = Setting([1])
    mu_min = Setting([0.01])
    mu_has_max = Setting([0])
    mu_max = Setting([0.0])
    mu_function = Setting([0])
    mu_function_value = Setting([""])

    sigma = Setting([0.5])
    sigma_fixed = Setting([0])
    sigma_has_min = Setting([1])
    sigma_min = Setting([0.01])
    sigma_has_max = Setting([1])
    sigma_max = Setting([1.0])
    sigma_function = Setting([0])
    sigma_function_value = Setting([""])

    truncation = Setting([0.5])
    truncation_fixed = Setting([0])
    truncation_has_min = Setting([1])
    truncation_min = Setting([0.01])
    truncation_has_max = Setting([1])
    truncation_max = Setting([1.0])
    truncation_function = Setting([0])
    truncation_function_value = Setting([""])

    cube_face = Setting([1])

    add_saxs = Setting([False])
    normalize_to = Setting([0])

    inputs = [("Fit Global Parameters", FitGlobalParameters, 'set_data')]
    outputs = [("Fit Global Parameters", FitGlobalParameters)]

    def __init__(self):
        super().__init__(show_automatic_box=True)

        main_box = gui.widgetBox(self.controlArea,
                                 "Size", orientation="vertical",
                                 width=self.CONTROL_AREA_WIDTH - 10, height=380)

        button_box = gui.widgetBox(main_box,
                                   "", orientation="horizontal",
                                   width=self.CONTROL_AREA_WIDTH-25)

        gui.button(button_box,  self, "Send Size", height=40, callback=self.send_sizes)

        self.sizes_tabs = gui.tabWidget(main_box)
        self.sizes_box_array = []

        for index in range(len(self.shape)):
            size_box = SizeBox(widget=self,
                               parent=gui.createTabPage(self.sizes_tabs, Phase.get_default_name(index)),
                               index = index,
                               active = self.active[index],
                               shape=self.shape[index],
                               distribution = self.distribution[index],
                               mu = self.mu[index],
                               mu_fixed = self.mu_fixed[index],
                               mu_has_min = self.mu_has_min[index],
                               mu_min = self.mu_min[index],
                               mu_has_max = self.mu_has_max[index],
                               mu_max = self.mu_max[index],
                               mu_function = self.mu_function[index],
                               mu_function_value = self.mu_function_value[index],
                               sigma = self.sigma[index],
                               sigma_fixed = self.sigma_fixed[index],
                               sigma_has_min = self.sigma_has_min[index],
                               sigma_min = self.sigma_min[index],
                               sigma_has_max = self.sigma_has_max[index],
                               sigma_max = self.sigma_max[index],
                               sigma_function = self.sigma_function[index],
                               sigma_function_value = self.sigma_function_value[index],
                               truncation = self.truncation[index],
                               truncation_fixed = self.truncation_fixed[index],
                               truncation_has_min = self.truncation_has_min[index],
                               truncation_min = self.truncation_min[index],
                               truncation_has_max = self.truncation_has_max[index],
                               truncation_max = self.truncation_max[index],
                               truncation_function = self.truncation_function[index],
                               truncation_function_value = self.truncation_function_value[index],
                               cube_face = self.cube_face[index],
                               add_saxs = self.add_saxs[index],
                               normalize_to = self.normalize_to[index])

            self.sizes_box_array.append(size_box)

        runaction = OWAction("Send Size", self)
        runaction.triggered.connect(self.send_sizes)
        self.addAction(runaction)

        orangegui.rubber(self.controlArea)

    def get_max_height(self):
        return 480

    def set_data(self, data):
        if not data is None:
            try:
                self.fit_global_parameters = data.duplicate()

                phases = self.fit_global_parameters.measured_dataset.phases

                if phases is None: raise ValueError("No Phases in input data!")

                tabs_to_remove = len(self.shape)-len(phases)

                if tabs_to_remove > 0:
                    for index in range(tabs_to_remove):
                        self.sizes_tabs.removeTab(-1)
                        self.sizes_box_array.pop()

                for phase_index in range(len(phases)):
                    if not self.fit_global_parameters.size_parameters is None:
                        size_parameters = self.fit_global_parameters.get_size_parameters(phase_index)
                    else:
                        size_parameters = None

                    if phase_index < len(self.shape):
                        self.sizes_tabs.setTabText(phase_index, phases[phase_index].get_name(phase_index))
                        size_box = self.sizes_box_array[phase_index]

                        if not size_parameters is None:
                            size_box.set_data(size_parameters)
                    else:
                        size_box = SizeBox(widget=self,
                                           parent=gui.createTabPage(self.sizes_tabs, phases[phase_index].get_name(phase_index)),
                                           index=phase_index,
                                           active=0)

                        if not size_parameters is None:
                            size_box.set_data(size_parameters)

                        self.sizes_box_array.append(size_box)

                self.dumpSettings()

                if self.is_automatic_run:
                    self.send_sizes()

            except Exception as e:
                QMessageBox.critical(self, "Error",
                                     str(e),
                                     QMessageBox.Ok)

                if self.IS_DEVELOP: raise e

    def send_sizes(self):
        try:
            if not self.fit_global_parameters is None:
                self.dumpSettings()

                self.fit_global_parameters.set_size_parameters([self.sizes_box_array[index].get_size_parameters() for index in range(len(self.sizes_box_array))])
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
        self.dump_shape()
        self.dump_distribution()
        self.dump_mu()
        self.dump_sigma()
        self.dump_truncation()
        self.dump_cube_face()
        self.dump_add_saxs()
        self.dump_normalize_to()

    def dump_active(self):
        bkp_active = copy.deepcopy(self.active)

        try:
            self.active = []

            for index in range(len(self.sizes_box_array)):
                self.active.append(self.sizes_box_array[index].active)
        except Exception as e:
            self.active = copy.deepcopy(bkp_active)

            if self.IS_DEVELOP: raise  e

    def dump_shape(self):
        bkp_shape = copy.deepcopy(self.shape)

        try:
            self.shape = []

            for index in range(len(self.sizes_box_array)):
                self.shape.append(self.sizes_box_array[index].shape)
        except Exception as e:
            self.shape = copy.deepcopy(bkp_shape)

            if self.IS_DEVELOP: raise  e

    def dump_distribution(self):
        bkp_distribution = copy.deepcopy(self.distribution)

        try:
            self.distribution = []

            for index in range(len(self.sizes_box_array)):
                self.distribution.append(self.sizes_box_array[index].distribution)
        except Exception as e:
            self.distribution = copy.deepcopy(bkp_distribution)

            if self.IS_DEVELOP: raise e


    def dump_mu(self):
        bkp_mu = copy.deepcopy(self.mu)
        bkp_mu_fixed = copy.deepcopy(self.mu_fixed)
        bkp_mu_has_min = copy.deepcopy(self.mu_has_min)
        bkp_mu_min = copy.deepcopy(self.mu_min)
        bkp_mu_has_max = copy.deepcopy(self.mu_has_max)
        bkp_mu_max = copy.deepcopy(self.mu_max)
        bkp_mu_function = copy.deepcopy(self.mu_function)
        bkp_mu_function_value = copy.deepcopy(self.mu_function_value)

        try:
            self.mu = []
            self.mu_fixed = []
            self.mu_has_min = []
            self.mu_min = []
            self.mu_has_max = []
            self.mu_max = []
            self.mu_function = []
            self.mu_function_value = []

            for index in range(len(self.sizes_box_array)):
                self.mu.append(self.sizes_box_array[index].mu)
                self.mu_fixed.append(self.sizes_box_array[index].mu_fixed)
                self.mu_has_min.append(self.sizes_box_array[index].mu_has_min)
                self.mu_min.append(self.sizes_box_array[index].mu_min)
                self.mu_has_max.append(self.sizes_box_array[index].mu_has_max)
                self.mu_max.append(self.sizes_box_array[index].mu_max)
                self.mu_function.append(self.sizes_box_array[index].mu_function)
                self.mu_function_value.append(self.sizes_box_array[index].mu_function_value)
        except Exception as e:
            self.mu = copy.deepcopy(bkp_mu)
            self.mu_fixed = copy.deepcopy(bkp_mu_fixed)
            self.mu_has_min = copy.deepcopy(bkp_mu_has_min)
            self.mu_min = copy.deepcopy(bkp_mu_min)
            self.mu_has_max = copy.deepcopy(bkp_mu_has_max)
            self.mu_max = copy.deepcopy(bkp_mu_max)
            self.mu_function = copy.deepcopy(bkp_mu_function)
            self.mu_function_value = copy.deepcopy(bkp_mu_function_value)

            if self.IS_DEVELOP: raise  e

    def dump_sigma(self):
        bkp_sigma = copy.deepcopy(self.sigma)
        bkp_sigma_fixed = copy.deepcopy(self.sigma_fixed)
        bkp_sigma_has_min = copy.deepcopy(self.sigma_has_min)
        bkp_sigma_min = copy.deepcopy(self.sigma_min)
        bkp_sigma_has_max = copy.deepcopy(self.sigma_has_max)
        bkp_sigma_max = copy.deepcopy(self.sigma_max)
        bkp_sigma_function = copy.deepcopy(self.sigma_function)
        bkp_sigma_function_value = copy.deepcopy(self.sigma_function_value)

        try:
            self.sigma = []
            self.sigma_fixed = []
            self.sigma_has_min = []
            self.sigma_min = []
            self.sigma_has_max = []
            self.sigma_max = []
            self.sigma_function = []
            self.sigma_function_value = []

            for index in range(len(self.sizes_box_array)):
                self.sigma.append(self.sizes_box_array[index].sigma)
                self.sigma_fixed.append(self.sizes_box_array[index].sigma_fixed)
                self.sigma_has_min.append(self.sizes_box_array[index].sigma_has_min)
                self.sigma_min.append(self.sizes_box_array[index].sigma_min)
                self.sigma_has_max.append(self.sizes_box_array[index].sigma_has_max)
                self.sigma_max.append(self.sizes_box_array[index].sigma_max)
                self.sigma_function.append(self.sizes_box_array[index].sigma_function)
                self.sigma_function_value.append(self.sizes_box_array[index].sigma_function_value)
        except Exception as e:
            self.sigma = copy.deepcopy(bkp_sigma)
            self.sigma_fixed = copy.deepcopy(bkp_sigma_fixed)
            self.sigma_has_min = copy.deepcopy(bkp_sigma_has_min)
            self.sigma_min = copy.deepcopy(bkp_sigma_min)
            self.sigma_has_max = copy.deepcopy(bkp_sigma_has_max)
            self.sigma_max = copy.deepcopy(bkp_sigma_max)
            self.sigma_function = copy.deepcopy(bkp_sigma_function)
            self.sigma_function_value = copy.deepcopy(bkp_sigma_function_value)

            if self.IS_DEVELOP: raise  e

    def dump_truncation(self):
        bkp_truncation = copy.deepcopy(self.truncation)
        bkp_truncation_fixed = copy.deepcopy(self.truncation_fixed)
        bkp_truncation_has_min = copy.deepcopy(self.truncation_has_min)
        bkp_truncation_min = copy.deepcopy(self.truncation_min)
        bkp_truncation_has_max = copy.deepcopy(self.truncation_has_max)
        bkp_truncation_max = copy.deepcopy(self.truncation_max)
        bkp_truncation_function = copy.deepcopy(self.truncation_function)
        bkp_truncation_function_value = copy.deepcopy(self.truncation_function_value)

        try:
            self.truncation = []
            self.truncation_fixed = []
            self.truncation_has_min = []
            self.truncation_min = []
            self.truncation_has_max = []
            self.truncation_max = []
            self.truncation_function = []
            self.truncation_function_value = []

            for index in range(len(self.sizes_box_array)):
                self.truncation.append(self.sizes_box_array[index].truncation)
                self.truncation_fixed.append(self.sizes_box_array[index].truncation_fixed)
                self.truncation_has_min.append(self.sizes_box_array[index].truncation_has_min)
                self.truncation_min.append(self.sizes_box_array[index].truncation_min)
                self.truncation_has_max.append(self.sizes_box_array[index].truncation_has_max)
                self.truncation_max.append(self.sizes_box_array[index].truncation_max)
                self.truncation_function.append(self.sizes_box_array[index].truncation_function)
                self.truncation_function_value.append(self.sizes_box_array[index].truncation_function_value)
        except Exception as e:
            self.truncation = copy.deepcopy(bkp_truncation)
            self.truncation_fixed = copy.deepcopy(bkp_truncation_fixed)
            self.truncation_has_min = copy.deepcopy(bkp_truncation_has_min)
            self.truncation_min = copy.deepcopy(bkp_truncation_min)
            self.truncation_has_max = copy.deepcopy(bkp_truncation_has_max)
            self.truncation_max = copy.deepcopy(bkp_truncation_max)
            self.truncation_function = copy.deepcopy(bkp_truncation_function)
            self.truncation_function_value = copy.deepcopy(bkp_truncation_function_value)

            if self.IS_DEVELOP: raise  e

    def dump_cube_face(self):
        bkp_cube_face = copy.deepcopy(self.cube_face)

        try:
            self.cube_face = []

            for index in range(len(self.sizes_box_array)):
                self.cube_face.append(self.sizes_box_array[index].cube_face)
        except Exception as e:
            self.cube_face = copy.deepcopy(bkp_cube_face)

            if self.IS_DEVELOP: raise  e

    def dump_add_saxs(self):
        bkp_add_saxs = copy.deepcopy(self.add_saxs)

        try:
            self.add_saxs = []

            for index in range(len(self.sizes_box_array)):
                self.add_saxs.append(self.sizes_box_array[index].add_saxs)
        except Exception as e:
            self.add_saxs = copy.deepcopy(bkp_add_saxs)

            if self.IS_DEVELOP: raise  e

    def dump_normalize_to(self):
        bkp_normalize_to = copy.deepcopy(self.normalize_to)

        try:
            self.normalize_to = []

            for index in range(len(self.sizes_box_array)):
                self.normalize_to.append(self.sizes_box_array[index].normalize_to)
        except Exception as e:
            self.normalize_to = copy.deepcopy(bkp_normalize_to)

            if self.IS_DEVELOP: raise  e

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
from orangecontrib.wonder.util.gui_utility import InnerBox

class SizeBox(InnerBox):
    widget = None
    is_on_init = True

    parameter_functions = {}

    index = 0

    def __init__(self,
                 widget=None,
                 parent=None,
                 index = 0,
                 active = 1,
                 shape = 1,
                 distribution = 1,
                 mu = 4.0,
                 mu_fixed = 0,
                 mu_has_min = 1,
                 mu_min = 0.01,
                 mu_has_max = 0,
                 mu_max = 0.0,
                 mu_function = 0,
                 mu_function_value = "",
                 sigma = 0.5,
                 sigma_fixed = 0,
                 sigma_has_min = 1,
                 sigma_min = 0.01,
                 sigma_has_max = 1,
                 sigma_max = 1.0,
                 sigma_function = 0,
                 sigma_function_value = "",
                 truncation = 0.5,
                 truncation_fixed = 0,
                 truncation_has_min = 1,
                 truncation_min = 0.01,
                 truncation_has_max = 1,
                 truncation_max = 1.0,
                 truncation_function = 0,
                 truncation_function_value = "",
                 cube_face = 1,
                 add_saxs = False,
                 normalize_to = 0):
        super(SizeBox, self).__init__()

        self.widget = widget

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.setFixedWidth(widget.CONTROL_AREA_WIDTH - 35)
        self.setFixedHeight(300)

        self.index = index

        self.active                    = active
        self.shape                     = shape                    
        self.distribution              = distribution             
        self.mu                        = mu                       
        self.mu_fixed                  = mu_fixed                 
        self.mu_has_min                = mu_has_min               
        self.mu_min                    = mu_min                   
        self.mu_has_max                = mu_has_max               
        self.mu_max                    = mu_max                   
        self.mu_function               = mu_function              
        self.mu_function_value         = mu_function_value        
        self.sigma                     = sigma                    
        self.sigma_fixed               = sigma_fixed              
        self.sigma_has_min             = sigma_has_min            
        self.sigma_min                 = sigma_min                
        self.sigma_has_max             = sigma_has_max            
        self.sigma_max                 = sigma_max                
        self.sigma_function            = sigma_function           
        self.sigma_function_value      = sigma_function_value     
        self.truncation                = truncation               
        self.truncation_fixed          = truncation_fixed         
        self.truncation_has_min        = truncation_has_min       
        self.truncation_min            = truncation_min           
        self.truncation_has_max        = truncation_has_max       
        self.truncation_max            = truncation_max           
        self.truncation_function       = truncation_function      
        self.truncation_function_value = truncation_function_value
        self.cube_face                 = cube_face                
        self.add_saxs                  = add_saxs                 
        self.normalize_to              = normalize_to             

        self.CONTROL_AREA_WIDTH = widget.CONTROL_AREA_WIDTH-45

        parent.layout().addWidget(self)
        container = self

        self.cb_active = orangegui.comboBox(container, self, "active", label="Active", items=["No", "Yes"], callback=self.set_active, orientation="horizontal")

        self.main_box = gui.widgetBox(container, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH-10)

        self.cb_shape = orangegui.comboBox(self.main_box, self, "shape", label="Shape", items=Shape.tuple(), callback=self.set_shape, orientation="horizontal")
        self.cb_distribution = orangegui.comboBox(self.main_box, self, "distribution", label="Distribution", items=Distribution.tuple(), callback=self.set_distribution, orientation="horizontal")

        size_box = gui.widgetBox(self.main_box, "Size Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-10)

        self.sigma_box = gui.widgetBox(size_box, "", orientation="vertical")

        OWGenericWidget.create_box_in_widget(self, self.sigma_box, "mu", label="\u03bc or D", add_callback=True, min_value=0.0, min_accepted=False, trim=25)
        OWGenericWidget.create_box_in_widget(self, self.sigma_box,  "sigma", label="\u03c3", add_callback=True, min_value=0.0, min_accepted=False, trim=25)

        self.truncation_box = gui.widgetBox(size_box, "", orientation="vertical")

        OWGenericWidget.create_box_in_widget(self, self.truncation_box, "truncation", label="trunc.", add_callback=True, min_value=0.0, max_value=1.0, min_accepted=True, trim=25)

        self.cb_cube_face = orangegui.comboBox(self.truncation_box, self, "cube_face", label="Cube Face", items=WulffCubeFace.tuple(), 
                                               callback=self.callback_cube_face, labelWidth=300, orientation="horizontal")

        self.saxs_box = gui.widgetBox(size_box, "", orientation="vertical")

        orangegui.comboBox(self.saxs_box, self, "add_saxs", label="Add SAXS", items=["No", "Yes"], labelWidth=300, orientation="horizontal",
                           callback=self.set_add_saxs)

        self.normalize_box = gui.widgetBox(self.saxs_box, "", orientation="vertical")

        orangegui.comboBox(self.normalize_box, self, "normalize_to", label="Normalize to", items=Normalization.tuple(), 
                           callback=self.callback_normalize_to, labelWidth=300, orientation="horizontal")

        self.set_shape()
        self.set_active()
        
        self.is_on_init = False

    def after_change_workspace_units(self):
        pass

    def set_index(self, index):
        self.index = index
        
    def set_active(self):
        self.main_box.setEnabled(self.active==1)

        if not self.is_on_init: self.widget.dump_active()

    def set_shape(self):
        if self.cb_distribution.currentText() == Distribution.LOGNORMAL:
            if not (self.cb_shape.currentText() == Shape.SPHERE or self.cb_shape.currentText() == Shape.WULFF):
                if not self.is_on_init:
                    QMessageBox.critical(self, "Error",
                                         "Only Sphere/Wulff Solid shape is supported",
                                         QMessageBox.Ok)
    
                    self.shape = 1
        elif not self.cb_shape.currentText() == Shape.SPHERE:
            if not self.is_on_init:
                QMessageBox.critical(self, "Error",
                                     "Only Sphere shape is supported",
                                     QMessageBox.Ok)

                self.shape = 1
            
        if not self.is_on_init: self.widget.dump_shape()
        
        self.set_distribution()

    def set_add_saxs(self):
        self.normalize_box.setVisible(self.add_saxs==1)
        
        if not self.is_on_init: self.widget.dump_add_saxs()

    def set_distribution(self, is_init=False):
        if not (self.cb_distribution.currentText() == Distribution.LOGNORMAL or \
                #self.cb_distribution.currentText() == Distribution.GAMMA or \
                self.cb_distribution.currentText() == Distribution.DELTA):
            if not is_init:
                QMessageBox.critical(self, "Error",
                                     #"Only Lognormal, Gamma and Delta distributions are supported",
                                     "Only Lognormal and Delta distributions are supported",
                                     QMessageBox.Ok)

                self.distribution = 1
        else:
            self.sigma_box.setVisible(self.cb_distribution.currentText() != Distribution.DELTA)
            self.saxs_box.setVisible(self.cb_distribution.currentText() == Distribution.DELTA)
            if self.cb_distribution.currentText() == Distribution.DELTA: self.set_add_saxs()
            self.truncation_box.setVisible(self.cb_distribution.currentText() == Distribution.LOGNORMAL and self.cb_shape.currentText() == Shape.WULFF)

        if not self.is_on_init: self.widget.dump_distribution()

    def callback_mu(self):
        if not self.is_on_init: self.widget.dump_mu()

    def callback_sigma(self):
        if not self.is_on_init: self.widget.dump_sigma()
        
    def callback_truncation(self):
        if not self.is_on_init: self.widget.dump_truncation()

    def callback_cube_face(self):
        if not self.is_on_init: self.widget.dump_cube_face()

    def callback_normalize_to(self):
        if not self.is_on_init: self.widget.dump_normalize_to()

    def get_parameters_prefix(self):
        return SizeParameters.get_parameters_prefix() + self.get_parameter_progressive()

    def get_parameter_progressive(self):
        return str(self.index + 1) + "_"
    
    def set_data(self, size_parameters):
        OWGenericWidget.populate_fields_in_widget(self, "mu",    size_parameters.mu)
        OWGenericWidget.populate_fields_in_widget(self, "sigma", size_parameters.sigma)

        if size_parameters.shape == Shape.WULFF:
            OWGenericWidget.populate_fields_in_widget(self, "truncation", size_parameters.truncation)
            self.cb_cube_face.setCurrentText(size_parameters.cube_face)

        self.add_saxs = size_parameters.add_saxs

        if size_parameters.add_saxs:
            self.normalize_to = size_parameters.normalize_to

        self.set_shape()
        self.set_distribution()

    def get_size_parameters(self):
        if self.active == 0: return None
        else:
            if not self.mu_function == 1: congruence.checkStrictlyPositiveNumber(self.mu, "\u03bc or D")
            if self.cb_distribution.currentText() != Distribution.DELTA and not self.sigma_function == 1: congruence.checkStrictlyPositiveNumber(self.sigma, "\u03c3")
            if self.cb_distribution.currentText() == Distribution.DELTA and not self.fit_global_parameters.measured_dataset.phases[self.index].use_structure:
                raise Exception("Delta Distribution cannot be used when the structural model is not activated")

            return SizeParameters(shape=self.cb_shape.currentText(),
                                  distribution=self.cb_distribution.currentText(),
                                  mu=OWGenericWidget.populate_parameter_in_widget(self, "mu", self.get_parameters_prefix()),
                                  sigma=None if self.cb_distribution.currentText() == Distribution.DELTA else OWGenericWidget.populate_parameter_in_widget(self, "sigma", self.get_parameters_prefix()),
                                  truncation=OWGenericWidget.populate_parameter_in_widget(self, "truncation",self.get_parameters_prefix()) if (self.cb_distribution.currentText() == Distribution.LOGNORMAL and self.cb_shape.currentText() == Shape.WULFF) else None,
                                  cube_face=self.cb_cube_face.currentText() if (self.cb_distribution.currentText() == Distribution.LOGNORMAL and self.cb_shape.currentText() == Shape.WULFF) else None,
                                  add_saxs=self.add_saxs if self.cb_distribution.currentText() == Distribution.DELTA else False,
                                  normalize_to=self.normalize_to if self.cb_distribution.currentText() == Distribution.DELTA else None)


if __name__ == "__main__":
    a =  QApplication(sys.argv)
    ow = OWSizeNew()
    ow.show()
    a.exec_()
    ow.saveSettings()
