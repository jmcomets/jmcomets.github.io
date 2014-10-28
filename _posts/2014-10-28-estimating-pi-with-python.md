---
layout: post
title: "Estimating Pi with Python"
---

As you may or not know, I am a huge fan of Python, and love hacking with it. I
was recently at the [PyconFr](http://www.pycon.fr/2014/) were I attended
several talks on Python stuff:

- scientific tools: Sage, IPython Notebook, SymPy
- asyncio overview *(freaking awesome)*
- web frameworks benchmarking: [where does Python stand?](https://speakerdeck.com/ronnix/performance-des-frameworks-web-python-vs-the-world-v1-dot-1)

The conference was [eventified here](http://eventifier.com/event/pyconfr14/) if
you feel like checking it out. Careful though, talks are in **French**!

Anyway, one of the lightning talks on optimization got me thinking: "I should
try to solve some optimization problems with Python!".

# Estimating 3.14: the monte-carlo method

Although the [wiki article](http://en.wikipedia.org/wiki/Monte_Carlo_method) is
pretty detailed on the subject, I thought it was a good idea to try applying
the optimization on this very inefficient method of computation.

Note that I used Python 3 in each of the examples, and had them run on my
machine (dual-core i3 2.4 GHz / 4 Gb RAM).

## Basic Idea

No need for another explanation, the concept is rather simple:

    For example, consider a circle inscribed in a unit square. Given that the
    circle and the square have a ratio of areas that is π/4, the value of π can be
    approximated using a Monte Carlo method:

    1. Draw a square on the ground, then inscribe a circle within it.
    2. Uniformly scatter some objects of uniform size (grains of rice or sand) over the square.
    3. Count the number of objects inside the circle and the total number of objects.
    4. The ratio of the two counts is an estimate of the ratio of the two areas, which is π/4. Multiply the result by 4 to estimate π.

Pulled right off [Wikipedia](http://en.wikipedia.org/wiki/Monte_Carlo_method).
I read the great book "High performance Python" (Practical Performant
Programming for Humans), by Micha Gorelick and Ian Ozsvald
([link](http://shop.oreilly.com/product/0636920028963.do)), in which they also
use this problem to illustrate parallelism benefits.

Keeping it simple as always, here's what we'll do:

{% highlight python %}
def pi(nb_iters):
    hits_in_unit_circle = throw_darts_in_unit_square(nb_iters)
    return hits_in_unit_circle * 4 / float(nb_iters)
{% endhighlight %}

We'll be focusing on optimizing `throw_darts_in_unit_square`, which holds most
of the problem's complexity: throwing a large number of darts.

## Pure python

A pure python version of the dart throw

{% highlight python %}
def throw_darts_pure_python(amount):
    hits = 0
    for _ in range(int(amount)):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        hits += x**2 + y**2 <= 1
    return hits
{% endhighlight %}
