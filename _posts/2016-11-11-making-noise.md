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

## Pseudorandom vector generation

Using Numpy, generating a matrix of random floating-point numbers is pretty
straightforward:

{% highlight python %}
grads = np.random.random_sample((nb_gradients + 1, 2))
{% endhighlight %}

Now we have a matrix whose elements are in the range (-1, 1). We need them to
be in the range (0, 1).

{% highlight python %}
grads = 2 * grads - 1
{% endhighlight %}

Now we need to make sure that every row of the matrix forms a unit vector. To
do this, let's simply divide each component by the norm of the full vector.

{% highlight python %}
for i, row in enumerate(grads):
    x, y = row
    norm = dot_product(x, y, x, y) ** .5
    grads[i] = x / norm, y / norm
{% endhighlight %}

The `dot_product` function simply computes the euclidean dot product of two
2-dimensional vectors.

## Hashing a position in the grid

In order to choose a pseudorandom vector for a position, one must be able to
map a discrete grid position to a row index in the gradients matrix. Ken Perlin
originally used a shuffled set of integers and a simple modulo to achieve this.
Here's the generating of a such permutation set using Numpy.

{% highlight python %}
permutations = np.arange(nb_permutations, dtype=np.uint8)
np.random.shuffle(permutations)
{% endhighlight %}

One trick used by Ken was to double the permutation set, in order to easily
combine the hashed x and y positions to choose a permutation. This is weird at
first, but in the end it's just a clever hack that simply involves adding the
position to a hash, looping over the permutations using a modulo.

{% highlight python %}
permutations = np.append(permutations, permutations)

x_hash = permutations[x % len(permutations)]
xy_hash = permutations[x_hash + (y % len(permutations))]
{% endhighlight %}

## Wrapping up: the noise function

Once you have the hashing for an arbitrary position and the gradient vectors,
the implementation of the noise function is rather straightforward:

1. convert the point from world-coordinates to local-coordinates
2. compute hashes for each corner around the point
3. take the gradient vectors for each hash
4. interpolate between the gradients

This last step is the only one that needs a bit of thought, the rest is as
follows:

{% highlight python %}
xi, yi = floor(x), floor(y)

# position -> hash -> gradient
ps, nb_ps = permutations, len(permutations)
grads, nb_grads = gradients, len(gradients)
x0, y0 =      xi  % nb_ps,      yi  % nb_ps
x1, y1 = (1 + xi) % nb_ps, (1 + yi) % nb_ps
g00 = grads[ps[ps[x0] + y0] % nb_grads]
g01 = grads[ps[ps[x0] + y1] % nb_grads]
g10 = grads[ps[ps[x1] + y0] % nb_grads]
g11 = grads[ps[ps[x1] + y1] % nb_grads]

# corner influences
dx, dy = x - xi, y - yi
return interpolate(dx, dy, g00, g01, g10, g11)
{% endhighlight %}

I'll leave that interpolation bit for exercise, it wouldn't be any fun otherwise!

[Ken Perlin's talk]: http://www.noisemachine.com/talk1
[Tron]: http://www.imdb.com/title/tt0084827
