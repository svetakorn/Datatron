#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:13:08 2017

@author: larousse
"""

# pylint: disable=missing-docstring

from pymorphy2 import MorphAnalyzer

SYNONYMS = [
    ('субъект', 'территория', 'регион', 'область', 'край', 'республика',
     'место', 'москва', 'санкт-петербург', 'севастополь', 'байконур'),
    ('период', 'год', 'срок', 'время'),
]


def parse_phrase(phrase):
    morph = MorphAnalyzer()
    res = []

    def _check_accs(parsed_word):
        if all(p.tag.case == 'accs' for p in parsed_word):
            return True
        elif not res:
            return False
        return (res[-1].tag.transitivity == 'tran'
                or res[-1].tag.POS == 'PREP'
                or res[-1].tag.case == 'accs')

    for word in phrase.split(' '):
        parsed = morph.parse(word)
        if parsed[0].tag.case == 'accs' and not _check_accs(parsed):
            res.append([p for p in parsed if p.tag.case != 'accs'][0])
        else:
            res.append(parsed[0])
    return res


def agree_words(target, source):
    changelist = set()
    for grammeme in ('gender', 'number', 'case', 'person'):
        sgr = getattr(source.tag, grammeme)
        tgr = getattr(target.tag, grammeme)
        if sgr != tgr and None not in (sgr, tgr):
            changelist.add(sgr)
    return target.inflect(changelist)


def find_main_word(phrase):
    finder = [n for n, w in enumerate(phrase) if {'NOUN', 'nomn'} in w.tag]
    if finder:
        return finder[0]
    return None


def check_agreement(word1, word2):
    match = False
    for grammeme in ('gender', 'number', 'case', 'person'):
        gr_pair = (getattr(word1.tag, grammeme),
                   getattr(word2.tag, grammeme))
        if None in gr_pair:
            continue
        elif gr_pair[0] != gr_pair[1]:
            return False
        match = True
    return match


def find_phrase_in_context(phrase, context):
    mainpos = find_main_word(phrase)
    if mainpos is None:
        return None
    main = phrase[mainpos]
    main_synonyms = set(sum(
        [group for group in SYNONYMS if main.normal_form in group],
        (main.normal_form,)
    ))
    for num, word in enumerate(context):
        if word.normal_form in main_synonyms:
            return num
    return None


def put_phrase_in_context(phrase, context, target_pos):
    source_pos = find_main_word(phrase)
    source_word = phrase[source_pos]
    target_word = context[target_pos]
    new_main = source_word.inflect({target_word.tag.case})

    new_context = []
    for num, word in enumerate(context):
        if num == target_pos \
           or (0 <= num - target_pos + source_pos < len(phrase)
               and phrase[num - target_pos + source_pos].normal_form == word.normal_form):
            new_context.append(None)
        elif check_agreement(word, target_word):
            new_context.append(agree_words(word, new_main))
        else:
            new_context.append(word)

    insert = []
    for pos, word in enumerate(phrase):
        if pos == source_pos:
            insert.append(new_main)
        elif check_agreement(word, source_word):
            insert.append(agree_words(word, new_main))
        else:
            insert.append(word)

    res = new_context[:target_pos] + insert + new_context[target_pos + 1:]
    return [w for w in res if w is not None]


def unparse_phrase(phrase):
    return ' '.join(w.word for w in phrase)
