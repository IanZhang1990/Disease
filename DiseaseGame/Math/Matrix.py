#=====================================================================================
# Filename: Matrix.py
# Author: Ian Zhang
# Description: This file defines matrix related class and functions.
#=====================================================================================

from Math.Vector import Vector2D
import math
import copy

class Matrix3x3(object):
    """A simple 3x3 matrix which is frequently used in 2D games"""

    def __init__( self, valueArray = None ):
        if valueArray is None:
            self.__values = [[0,0,0],[0,0,0],[0,0,0]]
        elif isinstance( valueArray, list ) and len( valueArray ) >= 9:
            self.__values[0][0] = value[0]
            self.__values[0][1] = value[1]
            self.__values[0][2] = value[2]
            self.__values[1][0] = value[3]
            self.__values[1][1] = value[4]
            self.__values[1][2] = value[5]
            self.__values[2][0] = value[6]
            self.__values[2][1] = value[7]
            self.__values[2][2] = value[8]
        else:
            return                    

        self.Identity()
        pass

    def Identity( self ):
        """Make the matrix identity"""
        self._00 = 1.0; self._01 = 0.0; self._02 = 0.0;
        self._10 = 0.0; self._11 = 1.0; self._12 = 0.0;
        self._20 = 0.0; self._21 = 0.0; self._22 = 1.0;
        pass

    def __mul__( self, other ):
        """Multiply self and another matrix, return the result as a new matrix.
        Parameters:
        @other: another 3x3 matrix or a list with 3 elements"""
        if( isinstance( other, Matrix3x3 ) ):    # Multiply a matrix
            temp = Matrix3x3()

            # first row
            temp._00 = ( self._00 * other._00 ) + ( self._01 * other._10 ) + ( self._02 * other._20 )
            temp._01 = ( self._00 * other._01 ) + ( self._01 * other._11 ) + ( self._02 * other._21 )
            temp._02 = ( self._00 * other._02 ) + ( self._01 * other._12 ) + ( self._02 * other._22 )
            # second row
            temp._10 = ( self._10 * other._00 ) + ( self._11 * other._10 ) + ( self._12 * other._20 )
            temp._11 = ( self._10 * other._01 ) + ( self._11 * other._11 ) + ( self._12 * other._21 )
            temp._12 = ( self._10 * other._02 ) + ( self._11 * other._12 ) + ( self._12 * other._22 )
            # third row
            temp._20 = ( self._20 * other._00 ) + ( self._21 * other._10 ) + ( self._22 * other._20 )
            temp._21 = ( self._20 * other._01 ) + ( self._21 * other._11 ) + ( self._22 * other._21 )
            temp._22 = ( self._20 * other._02 ) + ( self._21 * other._12 ) + ( self._22 * other._22 )

            return temp
        elif hasattr(other, "__getitem__"): # Multiply a 3-row vector( type: list ) 
            temp2 = [0,0,0]
            temp2[0] = (self._00 * other[0]) + (self._01 * other[1]) + (self._02 *other[2])
            temp2[1] = (self._10 * other[0]) + (self._11 * other[1]) + (self._12 *other[2])
            temp2[2] = (self._20 * other[0]) + (self._21 * other[1]) + (self._22 *other[2])
        else:
            raise TypeError()
    __rmul__ = __mul__

    def __imul__( self, other ):
        """Matrix = Matrix * other"""
        if isinstance( other, Matrix3x3 ):
            temp = self * other
            #self.__copy( temp )
            self.__values = copy(temp.__values)
        else:
            raise TypeError()
        pass

    def __add__( self, other ):
        """Add another matrix"""
        if isinstance( other, Matrix3x3 ):
            temp = Matrix3x3()
            temp._00 = self._00 + other._00;     temp._01 = self._01 + other._01;     temp._01 = self._01 + other._01;
            temp._10 = self._10 + other._10;     temp._11 = self._11 + other._11;     temp._11 = self._11 + other._11;
            temp._20 = self._20 + other._20;     temp._21 = self._21 + other._21;     temp._21 = self._21 + other._21;
            return temp
        else:
            raise TypeError()
    __radd__ = __add__

    def __iadd__(self, other):
        """+="""
        if ( isinstance( other, Matrix3x3 ) ):
            temp = self + other
            #self.__copy( temp )
            self.__values = copy(temp.__values)
        else:
            raise TypeError()

    def __sub__( self, other ):
        """Minus"""
        if isinstance( other, Matrix3x3 ):
            temp = Matrix3x3()
            temp._00 = self._00 - other._00;     temp._01 = self._01 - other._01;     temp._01 = self._01 - other._01;
            temp._10 = self._10 - other._10;     temp._11 = self._11 - other._11;     temp._11 = self._11 - other._11;
            temp._20 = self._20 - other._20;     temp._21 = self._21 - other._21;     temp._21 = self._21 - other._21;
            return temp
        else:
            raise TypeError()
    __rsub__ = __sub__

    def __isub__(self, other):
        """+="""
        if ( isinstance( other, Matrix3x3 ) ):
            temp = self - other
            self.__values = copy(temp.__values)
            #self.__copy( temp )
        else:
            raise TypeError()

    
    def Scale( self, xScale, yScale ):
        """Scale a matrix"""
        temp = Matrix3x3()
        temp._00 = xScale; temp._01 = 0; temp._02 = 0;
        temp._10 = 0.0; temp._11 = yScale; temp._12 = 0;
        temp._20 = 0.0; temp._21 = 0; temp._22 = 1.0;
        
        temp2 = self * temp
        #self.__copy( temp2 )
        self.__values = copy(temp2.__values)
        pass

    def Translate( self, offsetX, offsetY ):
        """Translate current matrix"""
        mat = Matrix3x3()
        mat._00 = 1; mat._01 = 0; mat._02 = 0;
        mat._10 = 0; mat._11 = 1;  mat._12 = 0;
        mat._20 = offsetX; mat._21 = offsetY; mat._22 = 1;
        temp = self * mat
        #self.__copy( temp )
        self.__values = (temp.__values)
        pass

    def Rotate( self, rot ):
        """Rotate the matrix with an angle"""
        mat = Matrix3x3()

        Sin = math.sin( rot )
        Cos = math.cos( rot )
        
        mat._00 = Cos;           mat._01 = Sin;           mat._02 = 0;
        mat._10 = -Sin;          mat._11 = Cos;        mat._12 = 0;
        mat._20 = 0;              mat._21 = 0;              mat._22 = 1;
        temp = self * mat
        #self.__copy( temp )
        self.__values = (temp.__values)

    def Rotate( self, forward, side ):
        """Rotate the matrix with two vectors"""
        if isinstance( forward, Vector2D ) and isinstance( side, Vector2D ):
            mat = Matrix3x3()
            mat._00 = forward.x; mat._01 = forward.y; mat._02 = 0;
            mat._10 = side.x;        mat._11 = side.y;        mat._12 = 0;
            mat._20 = 0;              mat._21 = 0;              mat._22 = 1;
            temp = self * mat
            #self.__copy( temp )
            self.__values = (temp.__values)
        else:
            raise TypeError()
        pass

    def TransformVector2Ds( self, vectorList ):
        """applies a 2D transformation matrix to a list of Vector2Ds"""
        if isinstance( vectorList, list ):
            for vector in vectorList:
                tempX = ( self._00 * vector.x ) + ( self._10 * vector.y ) + self._20
                tempY = ( self._01 * vector.x ) + ( self._11 * vector.y ) + self._21
                vector.x = tempX
                vector.y = tempY

    def TransformVector2D( self, vector2d ):
        """applies a 2D transformation matrix to a Vector2D instance"""
        if isinstance( vector2d, Vector2D ):
            tempX = ( self._00 * vector2d.x ) + ( self._10 * vector2d.y ) + self._20
            tempY = ( self._01 * vector2d.x ) + ( self._11 * vector2d.y ) + self._21
            vector2d.x = tempX
            vector2d.y = tempY

    def __copy( self, other ):
        if isinstance( other, Matrix3x3 ):
            self._00 = other._00; self._01 = other._01; self._02 = other._02;
            self._10 = other._10; self._11 = other._11; self._12 = other._12;
            self._20 = other._20; self._21 = other._21; self._22 = other._22;

            
    ##############
    ### Define Properties
    @property
    def _00( self ):
        return self.__values[0][0]
    @_00.setter
    def _00( self, value ):
        self.__values[0][0] = value
    @_00.deleter
    def _00( self ):
        pass

    @property
    def _01( self ):
        return self.__values[0][1]
    @_01.setter
    def _01( self, value ):
        self.__values[0][1] = value
    @_01.deleter
    def _01( self ):
        pass

    @property
    def _02( self ):
        return self.__values[0][2]
    @_02.setter
    def _02( self, value ):
        self.__values[0][2] = value
    @_02.deleter
    def _02( self ):
        pass

    @property
    def _10( self ):
        return self.__values[1][0]
    @_10.setter
    def _10( self, value ):
        self.__values[1][0] = value
    @_10.deleter
    def _10( self ):
        pass

    @property
    def _11( self ):
        return self.__values[1][1]
    @_11.setter
    def _11( self, value ):
        self.__values[1][1] = value
    @_11.deleter
    def _11( self ):
        pass

    @property
    def _12( self ):
        return self.__values[1][2]
    @_12.setter
    def _12( self, value ):
        self.__values[1][2] = value
    @_12.deleter
    def _12( self ):
        pass

    @property
    def _20( self ):
        return self.__values[2][0]
    @_20.setter
    def _20( self, value ):
        self.__values[2][0] = value
    @_20.deleter
    def _20( self ):
        pass

    @property
    def _21( self ):
        return self.__values[2][1]
    @_21.setter
    def _21( self, value ):
        self.__values[2][1] = value
    @_21.deleter
    def _21( self ):
        pass

    @property
    def _22( self ):
        return self.__values[2][2]
    @_22.setter
    def _22( self, value ):
        self.__values[2][2] = value
    @_22.deleter
    def _22( self ):
        pass
    