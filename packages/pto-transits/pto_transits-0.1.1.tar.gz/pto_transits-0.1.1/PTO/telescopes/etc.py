


def _find_stellar_type_ESPRESSO(T_eff: float) -> str:
        """
        Find stellar type based on effective temperature.

        Parameters
        ----------
        T_eff : float
            Effective temperature of the star in K.

        Returns
        -------
        spectral_type : str
            Spectral type closest to the true one that is available in ESPRESSO ETC.

        """
        if T_eff > 54000:
            return 'O5'
        elif T_eff > 43300:
            return 'O9'
        elif T_eff > 29200:
            return 'B1'
        elif T_eff > 23000:
            return 'B3'
        elif T_eff > 15000:
            return 'B8'
        elif T_eff > 11800:
            return 'B9'
        elif T_eff > 10000:
            return 'A0'
        elif T_eff > 9450:
            return 'A1'
        elif T_eff > 8480:
            return 'F0'
        elif T_eff > 5900:
            return 'G0'
        elif T_eff > 5560:
            return 'G2'
        elif T_eff > 4730:
            return 'K2'
        elif T_eff > 3865:
            return 'K7'
        else:
            return 'M2'



class ETC():
    
    def _provide_SNR(self):
        
        
        ...
    
    
    

    pass


class ETC_ESPRESSO_1UT(ETC):
    def _get_stellar_type(self,
                        stellar_temperature:float):
        return _find_stellar_type_ESPRESSO(stellar_temperature)
    
    def _load_file(self,
                   stellar_temperature:float,
                   seeing:float):
        import numpy as np
        from scipy.interpolate import interp1d

        # File path
        file_path = f'./ETC/ETC_ESPRESSO/{self._get_stellar_type(stellar_temperature)}/{seeing}arcsec_900s.etc'

        # Initialize lists to store the data
        wavelength = []
        SNR = []

        # Read the file
        with open(file_path, 'r') as file:
            for line in file:
                # Ignore commented lines
                if line.startswith('#'):
                    continue
                # Split the line into wavelength and SNR
                parts = line.split()
                if len(parts) == 2:
                    wavelength.append(float(parts[0]))
                    SNR.append(float(parts[1]))

        # Convert lists to numpy arrays
        wavelength = np.array(wavelength)
        SNR = np.array(SNR)

        # Create an interpolation function
        interpolation_function = interp1d(wavelength, SNR, kind='linear', fill_value="extrapolate")

        return interpolation_function
    
    def _open_all_scenarios(self, stellar_temperature: float):
        
        best_scenario = self._load_file(stellar_temperature, 0.5)
        mean_scenario = self._load_file(stellar_temperature, 0.8)
        worst_scenario = self._load_file(stellar_temperature, 1.3)



class ETC_ESPRESSO_4UT(ETC):
    def _get_stellar_type(self,
                        stellar_temperature:float):
        return _find_stellar_type_ESPRESSO(stellar_temperature)

    def _load_file(self,
                   stellar_temperature:float,
                   seeing:float):
        import numpy as np
        from scipy.interpolate import interp1d

        # File path
        file_path = f'./ETC/ETC_ESPRESSO_4UT/{self._get_stellar_type(stellar_temperature)}/{seeing}arcsec_900s.etc'

        # Initialize lists to store the data
        wavelength = []
        SNR = []

        # Read the file
        with open(file_path, 'r') as file:
            for line in file:
                # Ignore commented lines
                if line.startswith('#'):
                    continue
                # Split the line into wavelength and SNR
                parts = line.split()
                if len(parts) == 2:
                    wavelength.append(float(parts[0]))
                    SNR.append(float(parts[1]))

        # Convert lists to numpy arrays
        wavelength = np.array(wavelength)
        SNR = np.array(SNR)

        # Create an interpolation function
        interpolation_function = interp1d(wavelength, SNR, kind='linear', fill_value="extrapolate")

        return interpolation_function
    
    def _open_all_scenarios(self, stellar_temperature: float):
        
        best_scenario = self._load_file(stellar_temperature, 0.5)
        mean_scenario = self._load_file(stellar_temperature, 0.8)
        worst_scenario = self._load_file(stellar_temperature, 1.3)