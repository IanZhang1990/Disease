#=====================================================================================
# Filename: CellSpace.py
# Author: Ian Zhang
# Description: Class to divide a 2D space into a grid of cells each of which
#                   may contain a number of entities. This class can help improve 
#                   performance by creating multiple threads to update man states
#
#                   If an entity is capable of moving, and therefore capable of moving
#                   between cells, the Update method should be called each update-cycle
#                   to sychronize the entity and the cell space it occupies
#=====================================================================================


class CellSpace(object):
    """defines a cell containing a list of pointers to entities"""
    def __init__(self):
        self.Memebr = list()                                # all the entities inhabiting this cell



