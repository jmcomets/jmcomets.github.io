---
layout: post
title: "Evolving the TSP"
---

So recently I've been taking a course on *Bio-inspired computer science*,
produced by a great teacher/researcher: (Guillaume
Beslon)[http://liris.cnrs.fr/guillaume.beslon/). Needless to say that is was
way too interesting for me not to get my hands dirty and try out the theory.

# The Traveling Salesman Problem

You probably already know this problem: a traveling salesman needs to visit a
series of cities as fast as he can. It is a NP-hard problem with many possible
approaches in order to solve it.

I used the open dataset available
[here](http://people.sc.fsu.edu/~jburkardt/datasets/cities/cities.html) to test
the algorithm.

To be honest, in this case a genetic algorithm isn't adapted: in a 2D world,
where all distances are euclidean and no boundaries/obstacles are involved, it
would probably be faster and even more robust to use a basic heuristic
approach. Still though, it was an **interesting exercise**.

# Genetic algorithm

There are many things to say concerning genetic algorithms, so I'll try to keep
it short and to the point.

Genetic algorithms (GAs) make use of an *evolutive process* for a *population
of solutions* (or genomes, or individuals -- there's a bit of biological
terminology). GAs also produce somewhat "suboptimal" solution to the problem.

You can use a GA in multiple cases, the two big use cases in my opinion being:

1. the solution set is too big for brute-force
2. you have no idea how to find a good solution

There are a few things you need to be able to do:

- generate a random set of solutions
- estimate how good a solution is, or at least compare two solutions
- slightly and randomly modify a solution, changing how good it is
- combine two solutions somehow, making a "child" solution

Here's a bit of pseudocode/python describing what a genetic algorithm usually
looks like:

{% highlight python %}
population = random_population(population_size)
for _ in range(nb_iterations):
    population = selection(population, nb_selected)
    population = reproduction(population, population_size)
{% endhighlight %}

And that's it! You mainly need to implement selection/reproduction, which are
the two methods you'll need to think about (random_population is fairly
straightforward in most cases). You'll notice the variety of parameters, which
is probably the weirdest thing about GAs: **they need a bunch of parameters**.

<!-- TODO: explain the process (combining gradient descent and random search) -->

In the case of the TSP, any permutation of cities is in fact a solution to the
problem. Therefore we'll define the genome of a solution as an ordered list of
cities. Note that we will never try to optimize the path itself, but the idea
here-and behind any genetic algorithm-is actually to evolve a population of
solutions, somehow selecting the "fitter" solutions and producing other
solutions which resemble these.

## Initial population

A genome being defined as a permutation of cities, we can initialize a random
population as follows :

{% highlight python %}
def initialize_population(cities, popsize):
    population = [list(cities) for _ in range(popsize)]
    for genome in population:
        random.shuffle(genome)
    return population
{% endhighlight %}

Personally, I like to write one-liners, here I'm a bit disappointed since I
can't actually `random.shuffle` modifies the given list in place and doesn't
return anything.

## Selection

*Ah, the interesting part!* There are a lot of ways to do selection in genetic
algorithms, such as elitism, roulette-based, tournament and a few others I
haven't worked with...

Each method has its benefits and drawbacks, but I personally prefer the
roulette-based method, which seems more "just" than others (who said nature was
just?).

{% highlight python %}
def selection(population, fitness_f, popsize):
    new_population = []
    for _ in range(popsize):
        # compute initial fitnesses
        genome_fitnesses = [(g, fitness_f(g)) for g in population
                            if g not in new_population]

        # normalize fitnesses
        total_fs = sum(f for _, f in genome_fitnesses)
        genome_fitnesses = ((g, f/total_fs) for g, f in genome_fitnesses)

        # accumulate fitnesses
        genome_fitnesses = sorted(genome_fitnesses, key=lambda gf: gf[1], reverse=True)
        genome_fitnesses = [(gf[0], gf[1]/sum(f for _, f in genome_fitnesses[:i+1]))
                            for i, gf in enumerate(genome_fitnesses)]

        # select first genome with fitness gt a random number from [0, 1)
        rn = random.random()
        for genome, fitness in genome_fitnesses:
            if fitness > rn:
                selected_genome = genome
                break
        new_population.append(selected_genome)
    return new_population
{% endhighlight %}

## Reproduction : genetic operators giving a new population

The reproduction phase of a genetic algorithm is what I believe to be the most
important phase. Now some people say the beauty of the evolutionary process is
the balance between selection and mutation: **that is very true**. I simply
think that the selection process is further from the problem that the
reproduction phase.

This phase can be describe as follows: given a certain population of parents,
combine them together following a certain strategy to produce the new
population for the next iteration of the algorithm.

Again, there are many ways to do this, a few notable ones are:

1. monogamous and mortal: parents are "married" and have a number of children
   (random distribution), and have a certain probability of dying. This
   situation follows our current western model and the probability distribution
   is usually mirrored from actual statistics.
2. selective, immortal and polygamous: parents have children with others until
   the population limit is reached.

In the case of this problem, I chose to go with the second version, based on
the simplicity of the problem.

### Mutation

The mutation operator consists in a *slight* modification of a new child's
genome upon creation. This is similar to a random walk and is one of the core
concepts of an evolutionary algorithm. Imagine if we only had a combination of
our ancestor's genome, would that conceptually make us any different from
someone else than, say, our common ancestor?

Like all genetic operators, the mutation has a (generally small) probability of
happening.

It must affect the genome of the child *slightly* (this is important), if the
modification is too great, the GA can be assimilated to a random search. In my
case, I chose to swap the order of two cities to keep the solution somewhat
similar, yet changing it.

{% highlight python %}
def mutation(child):
    i, j = (random.randint(0, len(child) - 1) for _ in range(2))
    child[i], child[j] = child[j], child[i]
{% endhighlight %}

### Cross-over

The cross-over operator is what defines the combination of two parent solutions
to generate a new child. Think of it as taking genomes and merging them
together by taking parts of each genome. Once again, there are many ways of
doing this, I decided to swap a fragment of the genes of both parents and
choosing one of the two resulting genomes (one being the "opposite" of the
other).

Like all genetic operators, the cross-over has a probability of happening.

{% highlight python %}
def crossover(first, second):
    a, b = 0, 0
    while not a < b:
        a, b = (random.randint(0, len(first)-1) for _ in range(2))
    for i in range(a, b+1):
        j = second.index(first[i])
        first[i], second[j] = second[j], first[i]
    return random.choice((first, second))
{% endhighlight %}

# Benchmarks

I've included here below the results of running the GA for the TSP with the
following parameters:

- number of iterations = 200
- population size = 80
- selected proportion = 20%
- cross-over probability = 30%
- mutation probability = 5%

## Dataset "uk12"

![Benchmark for uk12, starting at Edinburgh]({{ site.url }}/assets/img/evolving-the-tsp/uk12-Edinburgh.png)
![Benchmark for uk12, starting at Newcastle]({{ site.url }}/assets/img/evolving-the-tsp/uk12-Newcastle.png)
![Benchmark for uk12, starting at Oxford]({{ site.url }}/assets/img/evolving-the-tsp/uk12-Oxford.png)

## Dataset "wg22"

![Benchmark for wg22, starting at Aachen]({{ site.url }}/assets/img/evolving-the-tsp/wg22-Aachen.png)
![Benchmark for wg22, starting at Kassel]({{ site.url }}/assets/img/evolving-the-tsp/wg22-Kassel.png)
![Benchmark for wg22, starting at Muenster]({{ site.url }}/assets/img/evolving-the-tsp/wg22-Muenster.png)

## Dataset "wg59"

![Benchmark for wg59, starting at Bayreuth]({{ site.url }}/assets/img/evolving-the-tsp/wg59-Bayreuth.png)
![Benchmark for wg59, starting at Bielefeld]({{ site.url }}/assets/img/evolving-the-tsp/wg59-Bielefeld.png)
![Benchmark for wg59, starting at Bochum]({{ site.url }}/assets/img/evolving-the-tsp/wg59-Bochum.png)
