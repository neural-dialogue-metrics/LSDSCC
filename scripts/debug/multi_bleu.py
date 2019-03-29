"""
When I tried to reproduce the example in the paper, the multi_bleu yields some
surprising results.

In the paper ref_0 should have a higher score than ref_1, but it is not the case with:
- our bleu.
- the nltk bleu.

with or without smoothing.
In our bleu case, the reason is the BP for ref_0 is much lower than that of ref_1, which means ref_0  is punished
harsher than ref_1.
And in the nltk bleu case, the reason is the same. (I stepped into nltk code to inspect the BP and they match our bleu.)

This make me wonder, did I use the wrong bleu?
From the paper:

    we propose a MaxBLEU metric customized
    for response generation based on the Multi-BLEU
    metric (Madnani et al., 2008).

So the bleu supposed to be used is the *Madnani et al., 2008* version.
"""

import bleu as our_bleu
import nltk.translate.bleu_score as nltk_bleu

ref_0 = [
    ['rogen', 'and', 'goldberg', 'are', 'producing', 'a', 'movie', 'that', 'is', 'being', 'written', 'and', 'acted',
     'by', 'the', 'workaholics', 'guys'],
    ['i', 'think', 'rogen', 'is', 'producing', 'a', 'movie', 'from', 'workaholics', 'guys', ',', 'should', 'be', 'fun',
     '!']]

ref_1 = [['he', 's', 'also', 'in', 'top', 'five', 'by', 'chris', 'rock'],
         ['he', 'has', 'an', 'important', 'role', 'in', 'the', 'top', 'five', 'and', 'it', 's', 'hilarious'],
         ['he', 'was', 'quite', 'in', 'in', 'top', 'five', ',', 'another', 'comedy', 'that', 'came', 'out', 'recently'],
         ['looks', 'he', 'have', 'pretty', 'big', 'role', 'in', 'top', 'five', ',', 'the', 'new', 'chris', 'rock',
          'movie']]

hypo = ['the', 'workaholics', 'should', 'be', 'fun', '.']


def bleu_without_bp(translation_sentence, reference_corpus):
    score = our_bleu.bleu_sentence_level(translation_sentence, reference_corpus, smooth=True)
    return score.bleu / score.brevity_penalty


if __name__ == '__main__':
    print('Without smoothing')
    print('our_bleu,ref_0:', our_bleu.bleu_sentence_level(hypo, ref_0))
    print('our_bleu,ref_1:', our_bleu.bleu_sentence_level(hypo, ref_1))

    print('With smoothing')
    print('our_bleu,ref_0:', our_bleu.bleu_sentence_level(hypo, ref_0, smooth=True))
    print('our_bleu,ref_1:', our_bleu.bleu_sentence_level(hypo, ref_1, smooth=True))

    smooth_fn = nltk_bleu.SmoothingFunction()
    print('nltk_bleu,ref_0:', nltk_bleu.sentence_bleu(ref_0, hypo, smoothing_function=smooth_fn.method4))
    print('nltk_bleu,ref_1:', nltk_bleu.sentence_bleu(ref_1, hypo, smoothing_function=smooth_fn.method4))

    print('Smooth-NIST')
    print('nltk_bleu,ref_0:', nltk_bleu.sentence_bleu(ref_0, hypo, smoothing_function=smooth_fn.method3))
    print('nltk_bleu,ref_1:', nltk_bleu.sentence_bleu(ref_1, hypo, smoothing_function=smooth_fn.method3))

    # This gets back to normal
    print('Without BP,With smoothing')
    print('ref_0', bleu_without_bp(hypo, ref_0))
    print('ref_1', bleu_without_bp(hypo, ref_1))

# Without smoothing
# our_bleu,ref_0: BleuScore(bleu=0.0, geo_mean=0, precisions=[0.8333333333333334, 0.6, 0.25, 0.0], brevity_penalty=0.22313016014842982)
# our_bleu,ref_1: BleuScore(bleu=0.0, geo_mean=0, precisions=[0.16666666666666666, 0.0, 0.0, 0.0], brevity_penalty=0.6065306597126334)
# With smoothing
# our_bleu,ref_0: BleuScore(bleu=0.1090934722961538, geo_mean=0.488923022434901, precisions=[0.8571428571428571, 0.6666666666666666, 0.4, 0.25], brevity_penalty=0.22313016014842982)
# our_bleu,ref_1: BleuScore(bleu=0.1339801428338312, geo_mean=0.22089591134157885, precisions=[0.2857142857142857, 0.16666666666666666, 0.2, 0.25], brevity_penalty=0.6065306597126334)
# nltk_bleu,ref_0: 0.08552749803666322
# nltk_bleu,ref_1: 0.12102159467251643
# Without BP,With smoothing
# ref_0 0.488923022434901
# ref_1 0.22089591134157885
