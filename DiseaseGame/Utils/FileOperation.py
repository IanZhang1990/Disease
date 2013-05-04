#=====================================================================================
# Filename: FileOperation.py
# Author: Ian Zhang
# Description: This file defines file operations needed in the game.
#
#=====================================================================================

class ParameterLoader:
    """Summary: 
                Parameter Loader will load game parameters from a file in the disk
    """
    


    def __init__( self, filename ):
        """Summary:
            Constructor.
        Pamerater:
            filename: the name of the file that defined the parameters of the game
        """
        # Parameter File's name
        self.Filename = str(filename)

        #Parameter Dictionary.
        self.Parameters = dict()


    def LoadFile( self ):
        """Summary:
            Load values from a file.
            The file should look lik:
            MaxValue = 100;
             MinValue = 10;
             Number = 50;
            ...
        """
        try:
            f = file( self.Filename, 'r' );
            while True:
                line = f.readline();
                if len( line ) == 0: # Zero length means EOF
                    break
                if( line[0] != '#' ):
                    #print line;
                    value = line.strip()
                    pair = str( value ).split('=')
                    if len(pair) >= 2 :
                        self.Parameters[pair[0].strip()] = pair[1].strip()
            f.close();
        except StandardError:
            print "Some Error Occured during parsing file "+ self.Filename
            




