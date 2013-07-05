import pygame
import Math
from Math.Vector import Vector2D
from Math import Math2D


localPos = Math.Math2D.Transformations.PointToLocalSpace(  Vector2D( 600, 400 ), Vector2D( 0.999081979127, 0.0428392225025 ), Vector2D( -0.0428392225025, 0.999081979127 ), Vector2D(577.660656751, 387.090422179) )

print localPos