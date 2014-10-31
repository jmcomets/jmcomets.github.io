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

Although the [wiki article](http://en.wikipedia.org/wiki/Monte_Carlo_method)
goes in detail on the subject, I thought it was a good idea to try applying the
optimization on this very inefficient method of computation.

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

We'll be focusing on optimizing `throw_darts_in_unit_square`, holding most of
the problem's complexity: throwing a large number of darts.

## Pure python

A pure python version of the dart throw would look like this:

{% highlight python %}
def throw_darts_pure_python(amount):
    hits = 0
    for _ in range(int(amount)):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        hits += x**2 + y**2 <= 1
    return hits
{% endhighlight %}

As usual in Python, code is pretty self-explanatory: select a random point in
the unit square, then test if it is in the unit circle (eg. `x² + y² <= 1`).
Again, I'm using Python 3, so the use of `range()` isn't a problem. In previous
versions you'd probably use `xrange()` to make sure you don't build a humongous
list.

As you can also imagine, this is a naive version, since it doesn't have
any optimization whatsoever. Variables are all PyObjects and there no
vectorized computations (no need to remind you [why Python is
slow](https://jakevdp.github.io/blog/2014/05/09/why-python-is-slow/)).

Below is the benchmark results of this version. Note the log scales for both
the number of iterations and the time complexity of the method. You'll also be
glad to notice (well, at least I was) that we get a nice linear complexity,
that corresponds is the nature of the problem.

![Benchmark for pure python version]({{ site.url }}/assets/img/estimating-pi-with-python/1-7-pure-python.png)

To understand better what's happening under the hood, I profiled the code with
[Robert Kern's line_profiler](https://github.com/rkern/line_profiler). The
following results are set for 1 000 000 iterations.


       Hits         Time  Per Hit   % Time  Line Contents
    =====================================================
                                            def throw_darts_pure_python(amount):
          1            2      2.0      0.0      hits = 0
    1000001       693509      0.7     11.7      for _ in range(int(amount)):
    1000000      1905288      1.9     32.1          x = random.uniform(0, 1)
    1000000      1699462      1.7     28.6          y = random.uniform(0, 1)
    1000000      1638124      1.6     27.6          hits += x**2 + y**2 <= 1
          1            1      1.0      0.0      return hits

You can see that obviously, most of the time is spent inside that 1 million
long loop (no kidding huh?). I'm a bit surprised by the results, mainly that
`random.uniform()` isn't as slow as I expected it to be. It's actually *really
fast*. That's because the implementation uses a low-level C module. Although
the difference between the two calls puzzles me... The first person that
figures out why the first call to `random.uniform()` is faster than the second
**gets a pint**.

## Enter Numpy

Now, you've probably already heard of [Numpy](http://www.numpy.org/), famous
for n-dimension array manipulation (eg. arrays and matrices) in Python. There's
  a lot of things Numpy can do, but in my case I'm just going to be using it
  for optimizing random uniform arrays. Since Numpy is written in C, most of
    the calls are indeed faster than python code. Though we shouldn't forget
    that **there is an overhead to calling C code from Python**.

Below is a new version, making use of Numpy's own implementation of random
module:

{% highlight python %}
def throw_darts_numpy_random_sample(amount):
    hits = 0
    xs = numpy.random.random(amount)
    ys = numpy.random.random(amount)
    for i in range(int(amount)):
        hits += xs[i]**2 + ys[i]**2 <= 1
    return hits
{% endhighlight %}

And now for the benchmark results:

![Benchmark for intermediate numpy version]({{ site.url }}/assets/img/estimating-pi-with-python/1-7-numpy-random-sample.png)

Yes, this version is in fact *slower* than the pure python version, even though
we're generating the 2 million random numbers as a batch. A line coverage is
needed to explain why this happened:

       Hits         Time  Per Hit   % Time  Line Contents
    =====================================================
                                            def throw_darts_numpy_random_sample(amount):
          1            2      2.0      0.0      hits = 0
          1        19874  19874.0      0.3      xs = numpy.random.random(amount)
          1        19697  19697.0      0.2      ys = numpy.random.random(amount)
    1000001       914805      0.9     11.6      for i in range(int(amount)):
    1000000      6956696      7.0     87.9          hits += xs[i]**2 + ys[i]**2 <= 1
          1            1      1.0      0.0      return hits

Ok, you should notice quickly that most of the time is spent in that huge loop
(99.5% actually). That's because of all that simple yet sub-optimal python
looping code. That simple `for i in range(int(amount))` has to increment a
PyObject 1 million times, and that **adds up to a lot**. Oh and don't even get
me started on that single line inside the loop: two Numpy array indexing, with
conversion to PyObject in order to apply the exponent operator, that's far from
optimal.

Besides the slugginess of the loop, things have sped up. Numpy allocates two
million random elements a lot faster than the cumulated time of two million
Python `random.uniform()`. About a hundred times faster actually (1905288 +
1699462 = 3604750 vs 19874 + 19697 = 39571).

In order to make this piece of code faster than the pure python version, and as
you may have guessed it: we're going to have to move that final line in the
loop down to Numpy via **vectorization**.

## Three cheers for vectorization

I think the results speak for themselves from now on, so I'll let you interpret
the results yourself (hint: they're good).

{% highlight python %}
def throw_darts_numpy_random_sample_vectorized(amount):
    xs = numpy.random.random(amount)
    ys = numpy.random.random(amount)
    throw = numpy.vectorize(lambda s: s <= 1, otypes=[numpy.uint8])
    hits = throw(xs * xs + ys * ys)
    return numpy.sum(hits)
{% endhighlight %}

Benchmark results:

![Benchmark for vectorized version]({{ site.url }}/assets/img/estimating-pi-with-python/1-7-numpy-random-sample-vectorized.png)

Wait, what's that non-linear curve at the beginning? Oh sorry, not commenting.

Profiling:

    Hits         Time  Per Hit   % Time  Line Contents
    ==================================================
                                         def throw_darts_numpy_random_sample_vectorized(amount):
       1        19780  19780.0      3.0      xs = numpy.random.random(amount)
       1        19662  19662.0      2.9      ys = numpy.random.random(amount)
       1           64     64.0      0.0      throw = numpy.vectorize(lambda s: s <= 1, otypes=[numpy.uint8])
       1       628962 628962.0     93.9      hits = throw(xs * xs + ys * ys)
       1         1172   1172.0      0.2      return numpy.sum(hits)

At this point I believe we're near the best trade-off optimization/time spent
optimizing. The next step for this kind of problem is parallel computing, which
is fairly easy in this case.

## multiprocessing.Pool

*AKA how to make old, single-core code multi-core in less than 10 minutes.*

    def throw_darts_parallel(amount):
        pool = multiprocessing.Pool()

        # Compute argument for each worker based on the number of workers. Each
        # worker should have nearly the same amount of work to do, extra work being
        # given to the first worker. The number of processes computation is taken
        # from multiprocessing.pool's __init__ method.
        nb_processes = os.cpu_count() or 1
        proc_args = [amount / nb_processes] * nb_processes
        proc_args[0] += amount % nb_processes # assuming you have at least one core

        # replace throw_darts_func with the desired method of computation
        return sum(pool.map(throw_darts_func, proc_args))

That's it. I'm not too fast of a typer, but the coding took me about 5 minutes.

## Conclusion

I'm not going to repeat for the n-th time that Python is awesome, cause that's
what `import antigravity` is for. What I will say is that you can achieve a lot
with it, and if speed is a major factor, you can easily move the
allocation/vectorization problems down to the C level with a little more work.
Moreover, if your problem is easily splittable, you can parallelize the
computation in a very short amount of time, with little downsides.

All the code used for this article is open-source and available on
[Github](https://github.com/jmcomets/pi-estimation), should you want to re-use
it.
