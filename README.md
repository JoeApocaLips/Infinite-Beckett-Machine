<p align="center">
  <img src="logo.jpg" width="400" alt="Infinite Beckett Machine" />
</p>

# Infinite Beckett Machine
**I can't go on. I'll go on. Again.**

*A Beckettian Book Generator — 10 Chapters, ~28,000 Words*

A procedural long-form text generator **inspired** by Samuel Beckett's *Texts for Nothing* and *The Unnamable*.

This program produces a complete book — ten chapters of compulsive, fragmented prose — that echoes Beckett's late style:
- a voice that speaks without knowing why
- repetition as the only available logic
- negation that turns back on itself
- clusters of language that drift and return
- the impossibility of ending, and the impossibility of stopping

The output is a single text file (`InfiniteBeckettMachine.out`), structured in **ten generative chapters**, each governed by its own configuration of persistence, vocabulary focus, and cluster density:

- **Chapter 1** — Incipit of emptiness — sparse, unarranged, no focal pressure
- **Chapter 2–3** — Verbal momentum — verbs and continuity adverbs dominate, clusters lengthen
- **Chapter 4** — Doubtful murmur — doubt adverbs and abstract nouns surface
- **Chapter 5** — Maximum drive — verbs at peak persistence, longest clusters
- **Chapter 6** — Negation chapter — `neg` and verbs interlock, refusal structures proliferate
- **Chapter 7** — Nominal plateau — abstract nouns and adjectives, movement slows
- **Chapter 8** — Return of the verb — resurgence after the nominal trough
- **Chapter 9** — Compulsive repetition — adverbs and negation at high density
- **Chapter 10** — Terminal drift — adverbs only, maximum persistence, near-mechanical recurrence

All sentences are generated through **60 constrained syntactic templates** applied to a weighted lexicon of ~600 words across 13 grammatical categories, with full morphological conjugation (3rd person agreement, irregular past participles, gerunds).

> **No text from Beckett's published works is reproduced verbatim.**

## Architecture

The generator operates through three interlocking mechanisms:

**Lexical clustering** — at any moment, the engine focuses on a *cluster* of 1–3 keywords drawn from a single category. Clusters persist for a variable number of phrases, then shift — occasionally returning to a previous cluster via a configurable probability.

**Template selection** — 60 syntactic formulas are drawn with individual weights. Each formula declares its argument types (`V`, `N_a`, `N_c`, `pr`, `mod`, etc.), and the engine resolves them against the active cluster and a per-phrase memoization set to avoid repetition within a single sentence.

**Chapter configuration** — each of the 10 chapters tunes four parameters: *persistence* (how strongly keywords attract selection), *cluster multiplier* (cluster length scaling), *vocabulary focus* (which categories are prioritised), and *memory keep* (how many clusters carry over to the next chapter).

## 📖 Output Sample

```
No mouth, no sense, and yet can

without memory, without trace, and yet I know

no word, and yet it speaks ceaselessly

Neither time, nor memory, nor even the shadow of chair

what remains?

no body, no name, and yet a voice

Without name, without place, without echo, and yet I can

No soul, and yet one goes

why go on?

No echo, no room, and yet continue

No time, and yet it whispers

Without foot, without strength, without word, and yet she feels

is there anything left to say?

I must go on, I cannot go on, I'll go on
```

## ▶️ How to Run

```bash
python InfiniteBeckettMachine.py
```

Output is written to `InfiniteBeckettMachine.out` in the same directory.

To generate a deterministic, reproducible text from an ISBN seed, uncomment the seed block at the top of the script and pass the ISBN as argument:

```bash
python InfiniteBeckettMachine.py 9798670552141
```

Then copy the `.out` file into the `book/` directory and run `makebook.bat` to generate the PDF via Pandoc & MiKTeX.

## Vocabulary Categories

| Symbol   | Description                              | Size |
|----------|------------------------------------------|------|
| `V`      | Verbs (with morphological flags)         | ~120 |
| `VPV`    | Passive-valid verb subset                | ~80  |
| `N_a`    | Abstract nouns                           | ~60  |
| `N_c`    | Concrete nouns                           | ~80  |
| `A`      | Adjectives                               | ~80  |
| `mod`    | Modals                                   | 12   |
| `mod_neg`| Negative modals                          | 10   |
| `adv_c`  | Continuity adverbs                       | ~25  |
| `adv_d`  | Doubt adverbs                            | ~12  |
| `pr`     | Pronouns                                 | ~20  |
| `neg`    | Negations                                | 9    |
| `wh`     | Wh-words                                 | 11   |
| `dc`     | Discourse markers                        | ~15  |

## Afterword

*Infinite Beckett Machine* is a procedural book generator built from a combinatorial system of syntactic templates, weighted lexical categories, and a clustering engine that drifts between focus and dispersion — the way attention drifts in Beckett's late prose.

It is not an imitation. It is a machine that has read *Texts for Nothing* and *The Unnamable* and drawn the wrong conclusions. It speaks in ten chapters because it cannot stop. It repeats because repetition is the only form available to a voice with nothing to say and no option to fall silent.

No sentence is lifted from Beckett's published works. Every line is generated fresh from templates and morphological rules. The source code included in the appendix is not documentation — it is the score for a voice that must continue.

— Joe ApocaLips, 2026.

> "Ever tried. Ever failed. No matter. Try again. Fail again. Fail better."  
> — Samuel Beckett, *Worstward Ho*.

##
<p align="center">
  <img src="logo.gif" width="400" alt="Infinite Beckett Machine" />
</p>
