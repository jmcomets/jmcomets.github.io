---
layout: post
title: "Making noise"
---

Some people will recognize the title of this post as mirrored from [Ken
Perlin's talk][], which set up the foundations for a new form of
procedural generation, bringing it to the mainstream. His research is based off
his work on the movie [Tron][], where CGI was scaled to a feature-length film.

Nowadays, procedural generation through generation of noise has become an
important tool in the creation of games. From the roughness of a rock to the
ripples of waves, the flames of a fire to the snow falling from the sky, noise
is what makes these possible! You didn't *really* think that all those
animations were hand-made? The complexity and randomness of such animations
make it extremely difficult for a game designer to produce these at a standard
speed.

In my opinion, Ken Perlin was the first to produce results significant enough
to be noticed and put into application later on. But enough history, let's see
what all the fuss is about!

# "Standard" Perlin noise

The original noise generation algorithm proposed by Ken Perlin combines
interpolation and summation of nearby influences in a discrete grid to induce a
continuous, *homogeneous* noise. Now that's a mouthful, but the concept is
fairly understandable. Given a point in continuous space (to put it simply, floating
point coordinates), find the bounding box in discretized space defined by its
four corners. Each of these corners has an associated *pseudo-random unit
vector*, which is basically chosen from a hash table filled with random vectors
before the computation took place. The resulting noise for the point is given
by interpolating these vectors by the distance of the corner to the point. I'll
get back to this process in detail later on, since it seems hard to grasp
without an example.
