#=====================================================================================
# Filename: Matrix.py
# Author: Ian Zhang
# Description: This file defines matrix related class and functions.
#=====================================================================================

from Math.Vector import Vector2D
import math

class Matrix3x3(object):
    """A simple 3x3 matrix which is frequently used in 2D games"""

    def __init__( self ):
        self.__00 = 0.0
        self.__01 = 0.0
        self.__02 = 0.0
        self.__10 = 0.0
        self.__11 = 0.0
        self.__12 = 0.0
        self.__20 = 0.0
        self.__21 = 0.0
        self.__22 = 0.0
        pass

    def __init__( self, _00, _01, _02, _10, _11, _12,_20, _21, _22 ):
        self.__00 = _00
        self.__01 = _01
        self.__02 = _02
        self.__10 = _10
        self.__11 = _11
        self.__12 = _12
        self.__20 = _20
        self.__21 = _21
        self.__22 = _22
        pass

    def Identity( self ):
        """Make the matrix identity"""
        self.__00 = 1.0; self.__01 = 0.0; self.__02 = 0.0;
        self.__10 = 0.0; self.__11 = 1.0; self.__12 = 0.0;
        self.__20 = 0.0; self.__21 = 0.0; self.__22 = 1.0;
        pass

    def __mul__( self, other ):
        """Multiply self and another matrix, return the result as a new matrix.
        Parameters:
        @other: another 3x3 matrix or a list with 3 elements"""
        if( isinstance( other, Matrix3x3 ) ):    # Multiply a matrix
            temp = Matrix3x3()

            # first row
            temp.__00 = ( self.__00 * other.__00 ) + ( self.__01 * other.__10 ) + ( self.__02 * other.__20 )
            temp.__01 = ( self.__00 * other.__01 ) + ( self.__01 * other.__11 ) + ( self.__02 * other.__21 )
            temp.__02 = ( self.__00 * other.__02 ) + ( self.__01 * other.__12 ) + ( self.__02 * other.__22 )
            # second row
            temp.__10 = ( self.__10 * other.__00 ) + ( self.__11 * other.__10 ) + ( self.__12 * other.__20 )
            temp.__11 = ( self.__10 * other.__01 ) + ( self.__11 * other.__11 ) + ( self.__12 * other.__21 )
            temp.__12 = ( self.__10 * other.__02 ) + ( self.__11 * other.__12 ) + ( self.__12 * other.__22 )
            # third row
            temp.__20 = ( self.__20 * other.__00 ) + ( self.__21 * other.__10 ) + ( self.__22 * other.__20 )
            temp.__21 = ( self.__20 * other.__01 ) + ( self.__21 * other.__11 ) + ( self.__22 * other.__21 )
            temp.__22 = ( self.__20 * other.__02 ) + ( self.__21 * other.__12 ) + ( self.__22 * other.__22 )

            return temp
        elif hasattr(other, "__getitem__"): # Multiply a 3-row vector( type: list ) 
            temp2 = [0,0,0]
            temp2[0] = (self.__00 * other[0]) + (self.__01 * other[1]) + (self.__02 *other[2])
            temp2[1] = (self.__10 * other[0]) + (self.__11 * other[1]) + (self.__12 *other[2])
            temp2[2] = (self.__20 * other[0]) + (self.__21 * other[1]) + (self.__22 *other[2])
        else:
            raise TypeError()
    __rmul__ = __mul__

    def __imul__( self, other ):
        """Matrix = Matrix * other"""
        if isinstance( other, Matrix3x3 ):
            self = self * other
        else:
            raise TypeError()
        pass

    def __add__( self, other ):
        """Add another matrix"""
        if isinstance( other, Matrix3x3 ):
            temp = Matrix3x3()
            temp.__00 = self.__00 + other.__00;     temp.__01 = self.__01 + other.__01;     temp.__01 = self.__01 + other.__01;
            temp.__10 = self.__10 + other.__10;     temp.__11 = self.__11 + other.__11;     temp.__11 = self.__11 + other.__11;
            temp.__20 = self.__20 + other.__20;     temp.__21 = self.__21 + other.__21;     temp.__21 = self.__21 + other.__21;
            return temp
        else:
            raise TypeError()
    __radd__ = __add__

    def __iadd__(self, other):
        """+="""
        if ( isinstance( other, Matrix3x3 ) ):
            self = self + other
        else:
            raise TypeError()

    def __sub__( self, other ):
        """Minus"""
        if isinstance( other, Matrix3x3 ):
            temp = Matrix3x3()
            temp.__00 = self.__00 - other.__00;     temp.__01 = self.__01 - other.__01;     temp.__01 = self.__01 - other.__01;
            temp.__10 = self.__10 - other.__10;     temp.__11 = self.__11 - other.__11;     temp.__11 = self.__11 - other.__11;
            temp.__20 = self.__20 - other.__20;     temp.__21 = self.__21 - other.__21;     temp.__21 = self.__21 - other.__21;
            return temp
        else:
            raise TypeError()
    __rsub__ = __sub__

    def __isub__(self, other):
        """+="""
        if ( isinstance( other, Matrix3x3 ) ):
            self = self - other
        else:
            raise TypeError()

    
    def Scale( self, xScale, yScale ):
        """Scale a matrix"""
        temp = Matrix3x3()
        temp.__00 = xScale; temp.__01 = 0; temp.__02 = 0;
        temp.__10 = 0.0; temp.__11 = yScale; temp.__12 = 0;
        temp.__20 = 0.0; temp.__21 = 0; temp.__22 = 1.0;
        self *= temp
        pass

    def Translate( self, offsetX, offsetY ):
        """Translate current matrix"""
        mat = Matrix3x3()
        mat.__00 = 1; mat.__01 = 0; mat.__02 = 0;
        mat.__10 = 0; mat.__11 = 1;  mat.__12 = 0;
        mat.__20 = x; mat.__21 = y; mat.__22 = 1;
        self *= mat
        pass

    def Rotate( self, rot ):
        """Rotate the matrix with an angle"""
        mat = Matrix3x3()

        Sin = math.sin( rot )
        Cos = math.cos( rot )
        
        mat.__00 = Cos;           mat.__01 = Sin;           mat.__02 = 0;
        mat.__10 = -Sin;          mat.__11 = Cos;        mat.__12 = 0;
        mat.__20 = 0;              mat.__21 = 0;              mat.__22 = 1;
        self *= mat

    def Rotate( self, forward, side ):
        """Rotate the matrix with two vectors"""
        if isinstance( forward, Vector2D ) and isinstance( side, Vector2D ):
            mat = Matrix3x3()
            mat.__00 = forward.x; mat.__01 = forward.y; mat.__02 = 0;
            mat.__10 = side.x;        mat.__11 = side.y;        mat.__12 = 0;
            mat.__20 = 0;              mat.__21 = 0;              mat.__22 = 1;
            self *= mat
        else:
            raise TypeError()
        pass

    def TransformVector2Ds( self, vectorList ):
        """applies a 2D transformation matrix to a list of Vector2Ds"""
        if isinstance( vectorList, list ):
            for vector in vectorList:
                tempX = ( self.__00 * vector.x ) + ( self.__10 * vector.y ) + self.__20
                tempY = ( self.__01 * vector.x ) + ( self.__11 * vector.y ) + self.__21
                vector.x = tempX
                vector.y = tempY

    def TranscormVector2D( self, vector2d ):
        """applies a 2D transformation matrix to a Vector2D instance"""
        if isinstance( vector2d, Vector2D ):
            tempX = ( self.__00 * vector2d.x ) + ( self.__10 * vector2d.y ) + self.__20
            tempY = ( self.__01 * vector2d.x ) + ( self.__11 * vector2d.y ) + self.__21
            vector2d.x = tempX
            vector2d.y = tempY