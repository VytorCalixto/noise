# Notes
My notes while developing this project

## Height maps

My first approach was based on sampling a Perlin noise function, with
many octaves. While this method provided beautiful outputs it had three
main problems:
1. It was slow, since the size of the height map was the same of the
   output image
2. It's nearly impossible to make maps "loop" so they can be used on a
   globe
3. Manipulating the structure means looking at every point (1 point = 1
   pixel). So any function after this step (like temperature and biomes)
   would require passing through the whole map
   
## Voronoi

The Voronoi method provided to be faster and mitigated problems 1 and 2.
I still haven't tried to generate rivers, but should be easy according
to literature.

Right now I'm tackling converting the Voronoi map to the style of the
Height Map and my first approach was using a sparse interpolation of the
corners of the Voronoi polygons to feed the height map. This has been
successful, but the conversion looses the map loop. A solution for this
is to not use the polygon corners, but the polygons mean height, stored
on the "faces" and the faces center point as the sparse points.

My idea for a next approach is not to interpolate the data, but use the
value of the polygon "face" height as the data for the height map. Then,
it's possible to try to add some minor noise and turbulence so the
polygons don't look like polygons.
