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
from Math.InvertedAABBox2D import InvertedAABBox2D
from Math.Vector import Vector2D
from Utils import ThreadManagement
from Game.Man import Man
import Game



class Cell(object):
    """defines a cell containing a list of pointers to entities"""
    def __init__(self, topLeft, bottomRight):
        self.Members = list()                                # all the entities inhabiting this cell
        self.Buildings = list()                                # all the buildings located in this cell
        self.AABBox = None                                 # The cell's bouding box.

        if isinstance( topLeft, Vector2D ) and isinstance( bottomRight, Vector2D ):
            self.AABBox = InvertedAABBox2D( topLeft, bottomRight )
        pass

    def Empty(self):
        """empty its member list"""
        self.Members = list()

    def Render( self ):
        """Render the cell in the screen"""
        if( self.AABBox != None ):
            self.AABBox.Render()

class SpacePartition:
    """Subdivision class"""
    def __init__( self, width, height, cellsX, cellsY, maxEntities, gameWorld ):
        """Parameters:
            @width: width of the environment
            @height: height of the environment
            @cellsX: number of cells horizontally
            @cellsY: number of cells vertically
            @maxEntities: maximum number of entities to add"""
        self.Cells = list()
        self.CurrentNeighbor = None
        self.SpaceWidth = width
        self.SpaceHeight = height
        self.NumCellsX = cellsX
        self.NumCellsY = cellsY
        self.NumOfEntities = 0
        self.MaxEntities = maxEntities
        self.GameWorld = gameWorld
        self.Neighbors = list()
        for idx in range( 0, self.MaxEntities ):
            self.Neighbors.append( None )

        # Calculate bounds of each cell
        self.CellSizeX = width / cellsX
        self.CellSizeY = height/ cellsY

        # Create cells
        for y in range( 0, self.NumCellsY ):
            for x in range( 0, self.NumCellsX ):
                left  = x * self.CellSizeX
                right = left + self.CellSizeX
                top = y * self.CellSizeY
                bottom = top + self.CellSizeY
                self.Cells.append( Cell( Vector2D(left, top), Vector2D( right, bottom) ) )
        pass

    def AddEntity( self, entity ):
        """Add entity to the class by allocating them to the appropriate cell.
        Parameters:
            @entity: an entity. type: Man"""
        if entity is None:
            return
        elif not isinstance( entity, Man ):
            return

        if self.NumOfEntities < self.MaxEntities:
            idx = self.PartitionToIndex( entity.Pos )
            self.Cells[idx].Members.append( entity )
            self.NumOfEntities = self.NumOfEntities + 1
        pass

    def AddBuilding( self, building ):
        """Add a builidng to the class, and find the cell the building located in.
        Parameters:
            @building: a building
        """
        if not isinstance( building, Game.Urban.Building ):
            return

        #### TODO: The next several lines should be modified
        idx = self.PartitionToIndex( building.Pos )         ############################### A building is not a point, so it can be in at most 4 cells 
        self.Cells[idx].Buildings.append( building )         



    def UpdateEntity_Blocked( self, entity, oldPos ):
        """Update an entity's cell by calling this from the entity's Update() method.
        Parameters:
            @entity: the entity you want to update. ( Man )
            @oldPos: the entity's old position, ( Vector2D )"""
        # TODO:
        # Updating an entity's cell index will be very important for multi-thread

        if( not self.GameWorld.MultiThreadUpdate ):
            self.UpdateEntity_NoBlock( entity, oldPos, False )
        else:
            oldIdx = self.PartitionToIndex( oldPos )
            newIdx = self.PartitionToIndex( entity.Pos ) 
            if oldIdx == newIdx:
                return
            else:
                self.GameWorld.CellThreadManagement.postUpdateQueue.put_nowait( ( entity, oldPos ) )


    def UpdateEntity_NoBlock( self, entity, oldPos, ifFirstTime = False ):
        oldIdx = self.PartitionToIndex( oldPos )
        newIdx = self.PartitionToIndex( entity.Pos ) 
        if oldIdx == newIdx and not ifFirstTime:
            return
        try:
            self.Cells[oldIdx].Members.remove( entity )
        except:
            pass
        try:
            self.Cells[newIdx].Members.append( entity )
        except:
            pass

    def CalculateNeighbors( self, targetPos, queryRadius ):
        """this method calculates all a target's neighbors and stores them in
        the neighbor list. After you have called this method use the begin, 
        next and end methods to iterate through the list.
        Parameters:
            @targetPos: Vector2D
            @queryradius: float"""

        curNbor = self.Neighbors[0]
        curNborIdx = 0
        # create the query box that is the bounding box of the target's query area
        QueryBox = InvertedAABBox2D( targetPos - Vector2D( queryRadius, queryRadius ), 
                                                          targetPos + Vector2D(queryRadius, queryRadius) )
        # Iterate through each cell and test to see if its bounding box overlaops with the query box.
        # if it does and it also contains entities then make further proximity tests
        for curCell in self.Cells:
            # test to see if its bounding box overlaops with the query box
            if curCell.AABBox.IsOverlapWith( QueryBox ) and len(curCell.Members) > 0:
                # add any entities found within query radius to the neighbor list
                for entity in curCell.Members:
                    if entity.Pos.get_dist_sqrd( targetPos ) < queryRadius * queryRadius:
                        #self.Neighbors.remove( curNbor )  ------ This code seems to be wrong
                        self.Neighbors.pop( curNborIdx )
                        self.Neighbors.insert( curNborIdx, entity )
                        curNborIdx = curNborIdx + 1
                        curNbor = curNbor = self.Neighbors[curNborIdx]            

        curNbor = None
        pass

    def PartitionToIndex( self, position ):
        """Given a 2D vector representing a position within the game world, this
        method calculates an index into its appropriate cell"""
        idx = int( self.NumCellsX * position.x / self.SpaceWidth ) + ( int( self.NumCellsY*position.y/self.SpaceHeight ) * self.NumCellsX )
        # check boundary
        cellsLen = len(self.Cells)
        if idx > int( cellsLen - 1 ):
            idx = int(cellsLen - 1)
        return idx

    def FirstNeighbor( self ):
        """Returns a reference ot the first entity of the neighbor list"""
        self.CurrNborIndx = 0
        self.CurrentNeighbor = self.Neighbors[self.CurrNborIndx]
        return self.CurrentNeighbor

    def NextNeighbor( self ):
        """Returns the next entity of the current entity in the neighbor list"""
        self.CurrNborIndx = self.CurrNborIndx + 1
        self.CurrentNeighbor = self.Neighbors[self.CurrNborIndx]
        return self.CurrentNeighbor

    def EndNeighbor(self):
        """Returns true if the current entity is in the end of the neighbor list"""
        return self.CurrentNeighbor == self.Neighbors[-1] or self.CurrentNeighbor == None or len(self.Neighbors) == 0 or self.Neighbors == None

    def EmptyCells( self ):
        """Empty the cells of entities"""
        for cell in self.Cells:
            cell.Empty()
        pass

    def Render( self ):
        """Render every cell in the screen"""
        for cell in self.Cells:
            cell.Render()
        pass
