import atexit
import os

from kaldibin.adapters.io import KaldiBytes, KaldiFile, KaldiGzFile, KaldiPipe, KaldiBytesArk
from kaldibin.adapters.context import KaldiContext
from kaldibin.featbin import compute_cmvn_stats, compute_mfcc_feats, wav_copy
from kaldibin.latbin import lattice_1best, lattice_align_phones, lattice_align_words_lexicon, lattice_determinize,\
    lattice_to_ctm_conf, nbest_to_ctm
from kaldibin.online2bin import ivector_extract_online2, online2_wav_nnet3_latgen_faster

_KALDI_ROOT = os.environ['KALDI_ROOT'] if 'KALDI_ROOT' in os.environ else None
_context = KaldiContext(_KALDI_ROOT)
_context.open()
atexit.register(_context.close)
