import atexit
import os

from kaldibin.adapters.io import KaldiBytes, KaldiFile, KaldiGzFile, KaldiPipe
from kaldibin.adapters.context import KaldiContext
from kaldibin.featbin import compute_mfcc_feats
from kaldibin.latbin import lattice_1best, lattice_align_phones, lattice_align_words_lexicon, nbest_to_ctm

_KALDI_ROOT = os.environ['KALDI_ROOT'] if 'KALDI_ROOT' in os.environ else None
_context = KaldiContext(_KALDI_ROOT)
_context.open()
atexit.register(_context.close)
