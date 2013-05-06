from Utils import FileOperation
from Game import Virus

pramLoader = FileOperation.ParameterLoader( "test.txt")
pramLoader.LoadFile();

virusParmLoder = Virus.VirusParamLoader( "BirdFlu.virus" );
virus = Virus.Virus( virusParmLoder )

print virus.Name

for i in range( 0, 10 ):
    print i

members = [ 1, 2, 3, 4, 5, 6, 7 ]

one = members[3]
mid = 3.5
members.remove( one )
print members
members.insert( 3, mid )
print members
one = members[4]

print "End"