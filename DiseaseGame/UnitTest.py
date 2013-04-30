from Utils import FileOperation
from Game import Virus

pramLoader = FileOperation.ParameterLoader( "test.txt")
pramLoader.LoadFile();

virusParmLoder = Virus.VirusParamLoader( "BirdFlu.virus" );
virus = Virus.Virus( virusParmLoder )

print virus.Name