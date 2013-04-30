#=====================================================================================
# Filename: Virus.py
# Author: Ian Zhang
# Description: This file defines Virus related classes, 
#               which defines properties and methods of Viruses.
#=====================================================================================

from Utils.FileOperation import ParameterLoader

#===========================================================
#           VirusParamLoader Class
#===========================================================
class VirusParamLoader(ParameterLoader):
    """Summary:
        This parameter loader is designed for loading virus parameters only.
    """

    def __init__( self, virusFilename ):
        """Summary:
            Constructor of VirusParamLoader Class
            Parameters:
            virusFilename:  The name of the file that defines parameters of a virus. It has to be ended with ".virus"
        """
        if( str(virusFilename).endswith('.virus') ):
            ParameterLoader.__init__(self, virusFilename);
            ParameterLoader.LoadFile(self);

#===========================================================
#           Virus Class
#===========================================================
class Virus(object):
    """Describes the basic properties of a virus"""

    def __init__(self, virusparamLoader):
        """Summary:
            Constructor of Virus Class
            Parameters:
            paramLoader:  The virus parameter loader
        """
        try:
            self.Name = str(virusparamLoader.Parameters.get('Name', 'Unknown'))                                 # The name of the virus.
            self.InfectRate = float(virusparamLoader.Parameters.get('InfectRate',1.0))                          # The possibility of infecting this virus. By default, it is 100%.
            self.Incubation = float(virusparamLoader.Parameters.get('Incubation', 20))                          # The virus can incubate 20 days, by default
            self.MortalityRate = float(virusparamLoader.Parameters.get('MortalityRate', 1.0))               # The mortality rate after getting the virus. By default, it is 100%.
            self.MortalityTime = int(virusparamLoader.Parameters.get('MortalityTime', 10))                  # After this days, the infected man will begin to die. It can alse be saved, though.
            self.SelfCureRate = float(virusparamLoader.Parameters.get('SelfCureRate', 0.0))                 # 0 percent of people can cure themselves without medicine care, by default.
            self.MedicalCureRate = float(virusparamLoader.Parameters.get('MedicalCureRate', 1.0))       # 100% infected people with medicine care will be cured, by default.
        except StandardError:
            pass

