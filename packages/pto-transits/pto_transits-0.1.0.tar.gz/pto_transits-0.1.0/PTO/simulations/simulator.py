from dataclasses import dataclass
import specutils as sp
import pandas as pd
# import rats.spectra_manipulation as sm


try:
    import petitRADTRANS as prt
except:
    raise ImportError('petitRADTRANS instalation not found. Please install petitRADTRANS to use this module.')




@dataclass
class Simulator():
    
    def define_target(self,
                      information: pd.Series,
                      ):
        
        self.information = information

    
    def _simulate_stellar_spectrum(self):
        ...
        
        
    def _simulate_planet_spectrum():
        ...
    
    def _simulate_RM_CLV_effect():
        ...
    
    def _get_dataset_spectra():
        ...
    
    def _get_dataset_ccf():
        ...
    
    def analyze_transmission_spectrum():
        ...
    
    def analyze_RM():
        ...
    
    
    
    
    
    
    
    
    
