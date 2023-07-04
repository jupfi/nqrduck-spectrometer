import logging
from PyQt5.QtCore import pyqtSignal
from nqrduck.module.module_model import ModuleModel
from .base_spectrometer import BaseSpectrometer

logger = logging.getLogger(__name__)

class SpectrometerModel(ModuleModel):
    spectrometer_added = pyqtSignal(BaseSpectrometer)
    active_spectrometer_changed = pyqtSignal(BaseSpectrometer)

    def __init__(self, module) -> None:
        super().__init__(module)
        self._active_spectrometer = None
        self._available_spectrometers = dict()

    @property
    def active_spectrometer(self):
        return self._active_spectrometer
    
    @active_spectrometer.setter
    def active_spectrometer(self, value):
        self._active_spectrometer = value
        self.active_spectrometer_changed.emit(value)
    
    @property
    def available_spectrometers(self):
        return self._available_spectrometers
    
    def add_spectrometers(self, spectrometer_module_name, module):
        self._available_spectrometers [spectrometer_module_name] = module
        logger.debug("Added module: %s", spectrometer_module_name)
        self.spectrometer_added.emit(module)


