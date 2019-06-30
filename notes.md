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

Converting the Voronoi map to the style of the Height Map was done using
a sparse interpolation of the corners of the Voronoi polygons to feed
the height map. This has been successful, but the conversion looses the
map loop. A solution for this is to use the same method for looping the
voronoi map to "loop" the points used to interpolate the data.

I've made a crude terrain map with only ocean, water, coast and land
types. After defining the height of the faces, I first set them to
either LAND or WATER. Then using a basic flood fill, I set the Ocean
type and last the coast. The implementation has slowed down the
execution and tackling this problems should be next on my list.

These are the current main goals:
- Improve the performance
- Use Lloyd's relaxation algorithm when generating the voronoi map. This
  will improve the final result
- Fix the corner's height issue with twin faces
