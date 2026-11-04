---
title: "The Shape of a World You Cannot Leave"
subtitle: "A plain-language guide to the Poincaré conjecture, Perelman's proof, and what a computer check can and cannot tell us"
author: "@jhonsu777 (with AI assistance: Claude, Anthropic)"
date: "Version 1.0, 4 November 2026 (UTC). Not independently reviewed. Exposition only: no new mathematical result is claimed."
---

# Abstract

In 1904 Henri Poincaré asked how you could recognize the three-dimensional sphere from the inside. Grigori Perelman settled the question in 2002–2003, building on Richard Hamilton's Ricci flow. This essay explains the question and the idea of the proof to readers who know no advanced mathematics, then gives the precise statements for those who want them. It also explains what the recent Lean formalization by Qin, Liao, Khaitan and Chow adds, and it says plainly what we did not check.

# How to read this essay

| Tag | Meaning |
|:--|:----------|
| **[E]** | Established mathematics, from the published literature cited below. |
| **[L]** | Reported by the authors of the Lean formalization. We did not rerun it. |
| **[M]** | Shown on MathDB or in the prize catalogue when we looked. |
| **[C]** | Our own computation, reproducible with `poincare_checks.py`. |

Analogies are teaching aids, not mathematics. All the mathematics here is due to the cited authors. We did not read the classical papers line by line, and this essay has not been independently reviewed.

# 1. The question, with a rope

Imagine you are an ant on an apple. You walk anywhere you like, unrolling a rope behind you, and you return to your starting point. Now you pull the rope. It slides over the surface and comes back to you.

On a doughnut this can fail. If your walk went through the hole, the rope gets stuck: no amount of pulling will bring it back without leaving the surface.

So an ant that has never left its world can tell an apple from a doughnut. For closed surfaces, the rope test is enough: if every loop can be pulled in, the surface is a sphere, up to stretching. **[E]**

Poincaré asked whether the same test works one dimension up. Our space looks three-dimensional. Suppose a universe is finite, has no edge, and every rope loop can be pulled in. Must it be the three-dimensional sphere?

The three-sphere is hard to picture because it does not fit inside our space. It is the set of points at distance one from the origin in four dimensions:

$$S^3=\{x\in\mathbb{R}^4:\ \|x\|=1\}.$$

**The conjecture.** Every closed, simply connected three-dimensional manifold is homeomorphic to $S^3$. **[E]** Here "closed" means finite with no edge, and "simply connected" is the rope test.

# 2. Why it took a century

Poincaré first tried a weaker test, based on homology, and then found a counterexample himself: the Poincaré homology sphere. So he proposed the rope test instead. **[E]**

Oddly, higher dimensions fell first. Smale settled dimensions five and above in 1961, and Freedman settled dimension four in 1982. **[E]** Dimension three is hard for a reason that is easy to feel: there is little room to move things around, but plenty of room for shapes to be complicated. A smooth version in dimension four is still open. **[E]**

# 3. The big idea: let the shape smooth itself

Think of a metal plate with hot and cold spots. Heat flows, the differences fade, and the plate approaches a uniform temperature. Nobody has to design this: the equation does it.

In 1982 Hamilton proposed doing this to the shape of space. **[E]** Ricci flow changes the way distances are measured:

$$\frac{\partial g}{\partial t}=-2\,\mathrm{Ric}(g).$$

Where a shape curves strongly like a sphere, it contracts. Bumps tend to even out, in a way that resembles heat spreading. Hamilton proved that a closed three-manifold with positive Ricci curvature evolves toward a round sphere after rescaling. **[E]**

The simplest example shows the flow's behaviour exactly. For a round three-sphere of radius one, the flow gives

$$r^2(t)=1-4t.$$

The sphere stays perfectly round and shrinks to nothing at $t=1/4$, while its curvature grows without limit. **[C]**

# 4. The problem: necks

Now take a dumbbell shape, with two balls joined by a thin neck. The neck has strong curvature around it, so it shrinks quickly and pinches before the balls disappear. The flow breaks. For years, the fear was that singularities could be far wilder than that.

Hamilton's plan was surgery: just before a neck pinches, cut it and cap both ends. **[E]** Then let the flow continue. The method needed answers to hard questions. Can we recognize every singularity? Can we control them? Could infinitely many cuts pile up in finite time?

# 5. What Perelman did

In three preprints from 2002–2003, Perelman answered those questions. **[E]** His contribution included:

- **Monotone quantities.** He introduced quantities such as entropy and reduced volume that change in only one direction along the flow, giving firm control.
- **No collapse.** At small scales, the geometry cannot become too thin. This rules out bad limits.
- **A map of singularities.** Near any place of very high curvature, the shape looks like one of a small list of models, such as a thin neck or a cap.
- **Controlled surgery.** Each cut removes a definite amount of volume. Since the total volume is limited, only finitely many cuts can occur in any finite time.

# 6. The finish: everything disappears

Here is the step that makes the rope test matter. For a simply connected starting shape, Ricci flow with surgery **goes extinct in finite time**: every piece vanishes. **[E]** Perelman proved this, and Colding and Minicozzi gave another proof with a beautiful estimate. They use a width $W(t)$, which roughly measures how large a surface you must drag across the manifold to sweep it out. Their bound is

$$\frac{d}{dt}W\le -4\pi+\frac{3}{4(t+C)}\,W.$$

We checked the arithmetic of the resulting argument: the upper bound reaches zero at a finite time. **[C]** Since a width cannot be negative, the flow must stop before then.

Now run the movie backward. Each piece that vanishes is a recognizable simple shape. Each surgery can be undone by gluing. For a simply connected manifold, the pieces and the gluing can only ever rebuild a sphere. **[E]** So the original world was a sphere after all.

This is also a special case of a larger result. Perelman's work proved Thurston's geometrization conjecture: every closed three-manifold can be cut into pieces carrying one of eight model geometries. **[E]**

# 7. How mathematicians came to trust it

Perelman posted his papers online and did not submit them to a journal. Several teams then spent years checking and filling in details: Kleiner and Lott, Morgan and Tian, and Cao and Zhu. **[E]** In 2006 he declined the Fields Medal. In 2010 the Clay Mathematics Institute awarded him the Millennium Prize of one million dollars, and he declined that too. **[M]**

# 8. What the computer check adds, and what it does not

Lean is a program that checks a proof down to basic logical steps. In 2026 Qin, Liao, Khaitan and Chow reported a Lean formalization of the Hamilton–Perelman route, including Moise's smoothing theorem. **[L]**

- **Reported result.** They state the smooth and topological theorems, and they report that the theorems depend only on `propext`, `Classical.choice` and `Quot.sound`. **[L]**
- **Size.** The MathDB submission contains 14,234 helper modules. **[L]**
- **Tools.** The authors state that automated assistance was used for proofs and prose. **[L]**
- **MathDB.** The problem page shows the status as solved and marks one submission as "Lean verified". **[M]** MathDB's own terms warn that its check is automated, and that a verification is not a certification.
- **Prize catalogue.** When we looked, the catalogue still recorded "Lean proof: No", so its acceptance was not established. **[M]**

**What we did not do.** We did not compile this formalization or audit how faithful its statement is. Its size makes that a large job. So this essay reports the verification and does not vouch for it.

**What a formal proof means.** It shows that the stated theorem follows from the axioms, if the checker is sound. It does not explain the idea, and it does not show that the Lean statement is the question Poincaré asked. People have to check that. The theorem's standing does not depend on Lean either: it rests on two decades of expert scrutiny. **[E]**

# 9. The idea in one paragraph

An ant can test its world with a rope, and Poincaré asked if that test identifies the three-sphere. Hamilton's idea was to let the geometry smooth itself, like heat. Sometimes a thin neck pinches, so you cut it and cap the ends. Perelman proved this can be controlled, and that for a world passing the rope test, everything eventually vanishes into simple pieces. Run backward, those pieces can only build a sphere. A question about shape was answered by watching shape change over time.

# References

1. H. Poincaré. *Cinquième complément à l'Analysis situs*, Rend. Circ. Mat. Palermo 18 (1904).
2. S. Smale. *Generalized Poincaré's conjecture in dimensions greater than four*, Ann. of Math. 74 (1961).
3. M. Freedman. *The topology of four-dimensional manifolds*, J. Differential Geom. 17 (1982).
4. R. Hamilton. *Three-manifolds with positive Ricci curvature*, J. Differential Geom. 17 (1982).
5. G. Perelman. arXiv:math/0211159, arXiv:math/0303109, arXiv:math/0307245.
6. T. Colding, W. Minicozzi. *Estimates for the extinction time for the Ricci flow on certain 3-manifolds and a question of Perelman*, arXiv:math/0308090.
7. B. Kleiner, J. Lott. *Notes on Perelman's papers*, arXiv:math/0605667.
8. J. Morgan, G. Tian. *Ricci Flow and the Poincaré Conjecture*, arXiv:math/0607607.
9. H.-D. Cao, X.-P. Zhu. *A complete proof of the Poincaré and geometrization conjectures*, Asian J. Math. 10 (2006).
10. Z. Qin, Y. Liao, A. Khaitan, B. Chow. *A Lean Formalization of the Hamilton–Perelman Proof of the Three-Dimensional Poincaré Conjecture*, arXiv:2609.33842.
11. J. Milnor. *The Poincaré Conjecture*, Clay Mathematics Institute problem description.
12. MathDB, problem 316224. <https://mathdb.com/p/316224/poincare-conjecture>
