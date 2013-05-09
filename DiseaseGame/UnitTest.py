
from Math.Vector import Vector2D

vector = Vector2D( -10003.0, 3000.0 )
print id( vector )
vector.Truncate( 100.0 )
print id( vector )

print vector