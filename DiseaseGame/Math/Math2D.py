class Math2D(object):
    """Math for a 2D area"""

    def WrapAround( posVec2d, maxX, maxY ):
        """reats a window as a toroid"""
        if posVect2d.x > maxX: 
            posVect2d.x = 0.0
        if posVect2d.x < 0:
            posVect2d.x = float(maxX)
        if posVect2d.y > maxY:
            posVect2d.y = 0.0
        if posVect2d.y < 0:
            posVect2d.y = float(maxY)


