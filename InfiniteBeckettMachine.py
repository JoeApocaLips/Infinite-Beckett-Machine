#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# >>> INFINITE BECKETT MACHINE <<<
#  
# Procedural text generator inspired by Samuel Beckett.
# Generates a 10-chapter book via combinatorial assembly of
# grammatical templates and clustered vocabulary, producing a unique text on each run.
#
# Copyright (c) 2026 Concept & Code by Joe ApocaLips <japocalips@gmail.com>
#
# Source: https://github.com/JoeApocaLips/
#
# VOCABULARY CATEGORIES
# V       — Verbs. Format: !verb|participle
#           ! = exclude from passive (VPV), | = irregular participle
# VPV     — Verbs Passive Valid (subset of V)
# adv_c   — Continuity adverbs
# adv_d   — Doubt adverbs
# N_a     — Abstract nouns
# N_c     — Concrete nouns
# A       — Adjectives
# mod     — Modals
# mod_neg — Negative modals
# neg     — Negations
# pr      — Pronouns
# wh      — Wh-words
# dc      — Discourse markers
#
# Licensed under the MIT License.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# v1.0 — 06 Mar 2026
import sys
from random import seed, random, randint, sample, choices, choice as c
from collections import deque
from inspect import signature
from pathlib import Path
from string import punctuation

# rd.seed('9798670552141'[::-1]) # MY ISBN
'''
if len(sys.argv) > 1: # BY ISBN
    ISBN = sys.argv[1].replace('-','')
    print('ISBN:', ISBN)
    seed(ISBN[::-1])
else: ISBN = ''
'''

# MORPHOLOGICAL FUNCTIONS
def v_s(v):
    if v == 'be': return 'is'
    if v == 'have': return 'has'
    if (c:=v[-1]) not in 'ysxzoh': return v + 's'
    if c == 'y' and v[-2] not in 'aeiou': return v[:-1] + 'ies'
    if c in 'sxzo' or v[-2:] in ('ch', 'sh'): return v + 'es'
    return v + 's'

def v_ed(v): return v if v in modals else V_ed[v]

gerondif_map = {'be':'being', 'have':'having', 'can':'to be able', 'lie':'lying', 'die':'dying',
                'tie':'tying', 'quit':'quitting'}
def v_ing(v): # gerund
    if v in modals: return v
    if v in gerondif_map: return gerondif_map[v]
    if (len(v) >= 3 and v[-1] not in 'wxyaeiou'  and v[-2] in 'aeiou' and v[-3] not in 'aeiou'
        and v[-2:] not in ('ee','oo','ea','ai','ou','au')): return v + v[-1] + 'ing'
    if v[-1] == 'e': return v[:-1] + 'ing'
    return v + 'ing'

def v_cj(pr, v): return v_s(v) if pr not in ('I','you','they','we') else v

def art(w): return f"{'an' if w[0] in 'aeiou' else 'a'} {w}"

# VOCABULARY
# Format: ! = exclude from passive, | = irregular participle
V = [x.split('|') for x in """
!be|been !go|gone say|said see|seen know|known !come|come hear|heard !wait
try|tried !fail stop|stopped !move speak|spoken think|thought feel|felt !have|had make|made
take|taken give|given !stand|stood !lie|lain !rise|risen !fall|fallen !walk
!run|run !sit|sat get|got !put|put keep|kept !let|let !help show|shown call !work
!seem want use find|found tell|told ask !become|become leave|left mean|meant
reach hold|held catch|caught drop|dropped lift push pull draw|drawn
write|written read|read break|broken open close turn face
bear|borne bring|brought buy|bought cost|cost cut|cut dig|dug feed|fed fight|fought
forget|forgotten grow|grown hide|hidden hit|hit hurt|hurt kneel|knelt lay|laid lead|led
learn|learnt light|lit lose|lost pay|paid prove quit|quit ring|rung
seek|sought sell|sold send|sent set|set shake|shaken shine|shone shoot|shot
shut|shut sing|sung sink|sunk sleep|slept slide|slid split|split spread|spread
steal|stolen stick|stung strike|struck swear|sworn sweep|swept swing|swung
teach|taught tear|torn throw|thrown understand|understood wake|woken wear|worn     
""".split()]
# VPV = VERBS_PASSIVE_VALID
VPV, V_ed, V = \
[p[0] for p in V if p[0][0]!='!'], \
  {(v:=p[0].lstrip('!')):p[1] if len(p)>1 else v[:(None,-1)[v[-1]=='e']]+'ed' for p in V},\
    [p[0].lstrip('!') for p in V]

adv_c = """on again still yet ever never now then soon here there away back forth up down in out over under
through around about near far hence thence""".split()
adv_d = """perhaps maybe possibly probably perchance seemingly apparently ostensibly supposedly evidently
presumably somehow conceivably admittedly""".split()
N_a = """nothing something everything anything voice body time place darkness silence void end beginning soul mind
thought memory hope fear dream wish life death truth word name sound pain joy sorrow anger love peace war light
shadow form matter spirit flesh blood breath sleep wake dawn dusk noon night day year age era moment eternity""".split()
N_c = """skull bone ash dust mud ditch finger chest throat skin nail hair eye hand foot stick road path stone
rock wall door window floor room ground earth sky lamp candle fire water rope chain key box bed cloth paper
book line wire coat hat boot rag sack jar tin
pebble twig plank slab pit heap wound needle blade cork lump clod mound dune shore ridge groove post gate latch screw
bolt pin thread straw mat pail""".split()
A = """empty full bright clear hidden certain good bad right wrong true false dark light weary tired old young sad
glad soft hard strong weak brave afraid calm quiet loud fast slow ready finished done gone happy angry cold warm
wet dry clean dirty new ancient fresh stale sharp dull rough smooth heavy thick thin wide narrow deep shallow high
low long short big small great little vast tiny huge massive slender fragile sturdy brittle tough gentle harsh kind
cruel sweet bitter sour hot cool freezing solid liquid dense sparse crowded vacant occupied busy idle active passive
alive dead born created destroyed whole partial complete incomplete perfect imperfect pure impure sacred profane holy
cursed blessed damned lost found revealed""".split()
mod = 'must can could will would should might may dare need ought shall'.split()
mod_neg = "can't couldn't won't wouldn't shan't daren't needn't shouldn't mightn't mustn't".split()
neg = 'no not none nor neither never nothing nowhere'.split()
pr = """I you they we he she it one someone anyone everyone noone nobody everybody somebody myself
yourself himself herself itself oneself ourselves yourselves themselves""".split()
wh = 'where who when what how why which whether whence whither wherefore'.split()
dc = 'yes well so indeed alas ah oh lo behold hark nay aye enough come forward hush'.split()

modals = set(mod + mod_neg)

# CONFIGURATION
WEIGHTS_BASE = {'adv_c': .9, 'V': .8, 'N_a': .7, 'N_c': .2, 'A': .1, 'mod': .7, 'mod_neg': .7,
                'adv_d': .5, 'pr': .4, 'neg': .7, 'wh': .6, 'dc': .3}

CLUSTER_LENGTHS_BASE = {'adv_c': (10, 20), 'V': (5, 15), 'N_a': (4, 10), 'N_c': (1, 2),
                        'A': (1, 1), 'mod': (5, 12), 'mod_neg': (5, 12), 'adv_d': (3, 6),
                        'pr': (6, 12), 'neg': (5, 12), 'wh': (3, 5), 'dc': (2, 4)}

RETURN_PROBABILITY_BASE = 0.3
DEQUE_MAXLEN = 5

# GLOBAL STATE
active_keywords, clust_histo, cur_cat, clust_phr_count, clust_targ_len = [], None, None, 0, 0
VOCAB_FOCUS, WEIGHTS = None, WEIGHTS_BASE.copy()
CLUSTER_LENGTHS, RETURN_PROBABILITY = CLUSTER_LENGTHS_BASE.copy(), RETURN_PROBABILITY_BASE
full_text = []
 
# DIRECT LIST MAPPING
VOCAB = globals()

FORMULA_TEMPLATES = [
    lambda verb='VPV', neg='neg': f"{verb}. {neg}. {verb} on",  # 1
    lambda pr='pr', modal_neg='mod_neg', modal='mod', verb='V':
        f"{pr} {modal_neg} {verb}. {pr} {modal} {verb}",  # 2
    lambda pr='pr', verb='V', adj='A', dc='dc': f"{pr} {v_cj(pr,verb)} {adj}. {dc} {pr} {v_cj(pr,verb)} not",  # 3
    lambda noun1='N_a', noun2='N_a', noun3='N_a': f"{noun1}, {noun2}, {noun3}, and so on",  # 4
    lambda wh='wh', verb='V': f"{wh} to {verb}? no matter",  # 5
    lambda adj='A': f"{adj}. it is {adj}. it must be nearly {adj}",  # 6
    lambda wh1='wh', wh2='wh', wh3='wh': f"{wh1} now? {wh2} now? {wh3} now?",  # 7
    lambda verb='VPV': f"nothing to be {v_ed(verb)}",  # 8
    lambda word='adv_c': f"{word}. {word} {word}",  # 9
    lambda verb='VPV': f"let's {verb}. they do not {verb}",  # 10
    lambda pr='pr': f"{pr} {'does' if pr not in ('I','you','they','we') else 'do'}n't know",  # 11
    lambda pr='pr', verb='V', loc='adv_c', neg='neg': f"{pr} {v_cj(pr,verb)} {loc}. {neg}, not {loc}",  # 12
    lambda pr='pr', verb='V', noun1='N_a', noun2='N_a': f"{pr} {v_cj(pr,verb)} {noun1}. {pr} {v_cj(pr,verb)} {noun2}",  # 13
    lambda word='adv_c': f"{word}",  # 14
    lambda verb='V', neg='neg': f"{neg} {v_s(verb)}",  # 15
    lambda pr='pr', modal='mod': f"{pr} {modal} go on",  # 16
    lambda pr='pr', verb='VPV': f"{pr} {v_cj(pr,verb)}. {v_cj(pr,'forget')}.",  # 17
    lambda adv='adv_d', noun='N_a': f"{adv} {noun}",  # 18
    lambda noun='N_a': f"there is {noun}",  # 19
    lambda adj1='A', adj2='A', dc='dc': f"{adj1}, {dc} {adj2}",  # 20
    lambda word='adv_c':
        c(["{w}... {w}... {w}...", "{w}... {w} not... {w}...", "{w}... still {w}... {w}..."]).format(w=word),  # 21
    lambda wh='wh': f"{wh}?",  # 22
    lambda adv='adv_d', adv2='adv_d': f"{adv}... {adv2}.",  # 23
    lambda word='dc', dc2='dc': f"{word}. {dc2}. {word}.",  # 24
    lambda pr='pr', verb='V', mod='mod': f"{pr} {mod} not {verb}. {pr} {v_cj(pr,verb)}.",  # 25
    lambda pr='pr', verb='V', neg='neg': f"{pr} {v_cj(pr,verb)} {neg}. {pr} {v_cj(pr,verb)} still.",  # 26
    lambda adv='adv_c', adv2='adv_c', verb='V': f"{adv} {adv2}. {verb} after.",  # 27
    lambda adv='adv_c', verb='V': f"while {adv}. {verb} on.",  # 28
    lambda wh='wh', pr='pr', verb='V': f"{wh} {pr}? {pr} {v_cj(pr,verb)}.",  # 29
    lambda verb='VPV', verb2='VPV': f"{verb}. {verb2} {v_ing(verb)}.",  # 30
    lambda verb='V', mod_neg='mod_neg': f"{mod_neg} {verb}. {mod_neg} {verb}.",  # 31
    lambda pr='pr', verb='VPV': f"{pr} was {v_ed(verb)}.",  # 33
    lambda verb='VPV': f"to be {v_ed(verb)}. or not.",  # 32
    lambda adj1='A', adj2='A', neg='neg': f"{neg} {adj1}. {adj2} rather.",  # 34
    lambda noun1='N_a', noun2='N_a': f"like {noun1}. Like {noun2}.",  # 35
    lambda noun='N_a', neg='neg': f"there {neg} {noun}.",  # 36
    lambda pr='pr', verb='V': f"{pr} {v_cj(pr,verb)} {pr}.",  # 37
    lambda noun='N_a', adv='adv_d': f"{noun}. {adv} {noun}.",  # 38
    lambda pr='pr', verb='V', neg='neg': f"{pr} {v_cj(pr,verb)} {neg}. {neg}. {neg}.",  # 39
    lambda verb1='VPV', verb2='VPV', neg='neg': f"{verb1} or {verb2}. {neg} {verb1}. {neg} {verb2}.",  # 40
    lambda pr='pr', verb='V', dc='dc': f"{pr} {v_cj(pr,verb)} or {dc}.",  # 41
    lambda pr='pr', adv='adv_c': f"{pr} {adv}. {pr} {adv} still.",  # 42
    lambda verb='V', adv='adv_c': f"{verb} {adv}. {verb} {adv} again.",  # 43
    lambda pr='pr', verb='V': f"{pr} knows {pr} {v_cj(pr,verb)}.",  # 44
    lambda noun='N_a', neg='neg': f"the {noun} passes. {neg}. it stays.",  # 45
    lambda noun='N_c', verb='V', dc='dc': f"the {noun} {v_cj('it',verb)}. {dc}.",  # 46
    lambda noun1='N_a', noun2='N_a': f"{art(noun1)}. {art(noun2)}.",  # 47
    lambda noun='N_a', adv='adv_c': f"{adv} the {noun}. {adv} the {noun}.",  # 48
    lambda verb='VPV', verb2='VPV': f"before {verb}. after {verb2}.",  # 49
    lambda adv='adv_c', verb='VPV': f"too late to {verb}. {adv}.",    # 50
    lambda verb='VPV': f"no use {v_ing(verb)}.",                       # 51
    lambda pr='pr', verb='VPV': f"{v_cj(pr,'say')} {verb}. {v_cj(pr,'say')} {verb} again.",  # 52
    lambda noun='N_a': f"call it {noun}. call it nothing.",            # 53
    lambda verb='VPV', verb2='VPV': f"if {verb}. then {verb2}. perhaps.",  # 54
    lambda noun='N_a', verb='VPV': f"if there is {noun}. {verb}.",         # 55
    lambda noun='N_c': f"the {noun}. the {noun} still.",               # 56
    lambda noun1='N_c', noun2='N_c': f"{noun1} and {noun2}. nothing more.",  # 57
    lambda verb='VPV': f"never {verb}. not once. not ever.",           # 58
    lambda noun='N_a', wh='wh': f"{wh} the {noun}? the {noun}."      # 59
]

FORMULA_LIBRARY = tuple((func, tuple(p.default for p in signature(func).parameters.values()))
                        for func in FORMULA_TEMPLATES)
               
TEMPLATE_WEIGHTS = [.8, 1.0, 1.0, .8, 1.0, .4, .6, 1.0, .4, 1.0, 0.8, 1.0, 1.0, .3, .8, .6,
                    1.0, .8, .7, .8, .4, .3, .6, .5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, .6, 1.0,
                    1.0, 1.0, .7, .9, .8, .8, .8, 1.0, .8, .7, .8, .9, 1.0, .9, .8, .7,
                    1.0, 1.0, .9, .8, .9, .7, .7, .8, .9, .8, .9]

# (persistence, cluster_mult, vocab_focus, memory_keep)
CHAPTERS = (
    (0.50, 0.8, None,              2),
    (0.60, 1.0, ('V', 'adv_c'),   2),
    (0.70, 1.2, ('V', 'adv_c'),   3),
    (0.75, 1.3, ('adv_d', 'N_a'), 3),
    (0.85, 1.5, ('V', 'adv_c'),   3),
    (0.80, 1.4, ('neg', 'V'),     3),
    (0.65, 1.0, ('N_a', 'A'),     2),
    (0.75, 1.2, ('V', 'adv_c'),   3),
    (0.90, 1.8, ('adv_c', 'neg'), 4),
    (0.95, 2.0, ('adv_c',),       4),
)

PHRASES_PER_CHAPTER = 671 # 818

# ENGINE
def initialize_new_cluster():
    global active_keywords, clust_phr_count, clust_targ_len, cur_cat
    if clust_histo and random() < RETURN_PROBABILITY:
        active_keywords, cur_cat = c(list(clust_histo))
    else:
        cur_cat = c(VOCAB_FOCUS if VOCAB_FOCUS else list(WEIGHTS.keys()))
        vocab = VOCAB[cur_cat]
        active_keywords = sample(vocab, min(randint(1, 3), len(vocab)))
    clust_targ_len = randint(*CLUSTER_LENGTHS[cur_cat])
    clust_phr_count = 0
    clust_histo.append((active_keywords.copy(), cur_cat))

def should_change_cluster():
    if clust_phr_count >= clust_targ_len: return True
    return random() < (clust_phr_count / clust_targ_len) * .5

def select_word(category, memoize):
    isVPV, realcat = (True,'V') if category=='VPV' else (False,category) 
    if active_keywords and cur_cat==realcat and random() < WEIGHTS.get(realcat, 0.5) \
        and (vocab:=[w for w in active_keywords if w not in memoize
                     and (not isVPV or w in VOCAB['VPV'])]):
            pass
    else: vocab = VOCAB.get(category, V)
    if len(vocab)==1: w = vocab[0]
    else:
        while (w:=c(vocab)) in memoize: continue
    memoize.add(w)
    return w
    
def generate_phrase(template=None):
    global clust_phr_count, full_text
    if not active_keywords or should_change_cluster():
        initialize_new_cluster()
        full_text.append('\n')
    if not template: template = c(FORMULA_LIBRARY)
    memo = set()
    phrase = template[0](*[select_word(cat, memo) for cat in template[1]])
    clust_phr_count += 1
    return phrase

def generate_phrases(count):
    return (capitalize(punc(generate_phrase(t))) for t in choices(FORMULA_LIBRARY, weights=TEMPLATE_WEIGHTS, k=count))
    
def capitalize(s): return s if s[0].isupper() else s[0].upper() + s[1:]
def punc(s): return s if s[-1] in punctuation else s + '.'
'''
def generate_text(num_phrases=250):
    global active_keywords, clust_phr_count, clust_histo
    active_keywords, clust_phr_count, clust_histo = [], 0, deque(maxlen=DEQUE_MAXLEN)
    initialize_new_cluster()
    return ' '.join(capitalize(punc(generate_phrase())) for _ in range(num_phrases))
'''
def apply_chapter_config(chapter):
    global WEIGHTS, CLUSTER_LENGTHS, RETURN_PROBABILITY, VOCAB_FOCUS
    persistence, cluster_mult, vocab_focus, _ = chapter
    WEIGHTS = {k: v * persistence for k, v in WEIGHTS_BASE.items()}
    CLUSTER_LENGTHS = {
        k: (int(v[0] * cluster_mult), int(v[1] * cluster_mult))
        for k, v in CLUSTER_LENGTHS_BASE.items()
    }
    RETURN_PROBABILITY = persistence * 0.7
    VOCAB_FOCUS = list(vocab_focus) if vocab_focus else None

def manage_chapter_memory(chapter, clust_histo):
    _, _, _, memory_keep = chapter
    return deque(list(clust_histo)[-memory_keep:], maxlen=DEQUE_MAXLEN), []

def generate_full_text():
    global active_keywords, clust_phr_count, clust_histo, WEIGHTS, CLUSTER_LENGTHS, RETURN_PROBABILITY, VOCAB_FOCUS, full_text
    active_keywords, clust_phr_count = [], 0
    clust_histo = deque(maxlen=DEQUE_MAXLEN)
    full_text = []
    for i, chapter in enumerate(CHAPTERS):
        apply_chapter_config(chapter)
        
        if i > 0: full_text.append("\n\n<!-- PAGEBREAK -->\n\n")
        full_text.append(f"{i+1}.\n")
        
        full_text.extend(generate_phrases(PHRASES_PER_CHAPTER))
        
        if i < len(CHAPTERS) - 1:
            clust_histo, active_keywords = manage_chapter_memory(CHAPTERS[i+1], clust_histo)
    return ''.join(s if s and s[-1]=='\n' else (s+' ') for s in full_text)

if __name__ == "__main__":
    for k in sorted(WEIGHTS_BASE.keys()): print(k, len(VOCAB[k]))
    print('modals', len(modals))
    print('FORMULA_TEMPLATES', len(FORMULA_LIBRARY), len(FORMULA_TEMPLATES))
    assert len(TEMPLATE_WEIGHTS) == len(FORMULA_LIBRARY)
    print('Computing...')
    text = generate_full_text() 
    print(text[:2000]+'(...)')
    outputfile = Path(__file__).with_suffix('.out')
    print('Writing...', outputfile.name, len(text))
    outputfile.write_text(text, encoding='utf8')
    print('Done.')
    