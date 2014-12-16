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

## Initial population
## Selection
## Reproduction : genetic operators giving a new population
### Mutation
### Cross-over

# Benchmarks

## Dataset "uk12"
## Dataset "wg22"
## Dataset "wg59"
