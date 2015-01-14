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
### Mutation
### Cross-over

# Benchmarks

## Dataset "uk12"
## Dataset "wg22"
## Dataset "wg59"
