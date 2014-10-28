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

## Pure python
