# Why `kaldibin`?

* The idea is for this to be a core interface for accessing Kaldi executables from Python. Then a second package (todo) can be created that does things like the `kaldi/egs/wsj/s5/steps/` scripts do, but in an installable python package.
* The current structure, tied to the Kaldi codebase and `egs/wsj` structure, is a poor separation of concerns that makes creating and sharing recipes harder than it ought to be. And a huge advantage of packaging this material on pypi is the opportunity for independent [versioning](https://semver.org/) of these tools, which will improve backward compatibility of our Kaldi recipes.
* Working in Python is nicer than bash in a number of ways, with a healthy ecosystem of tools and IDEs and um math operators
* Much of the piping and rxspecifier/wxspecifier kind of logic can be handled internally, reducing the toolkit-specific learning curve for would-be recipe writers.
* I'm generally hoping to bring some powerful Kaldi executables' functionality into Python without having to write `subprocess.run` boilerplates each time

## How far along is the effort?

So far I've only implemented a handful of executables that I'm using in my current work, in other words, the ones I've been able to at least minimally test.

Adding a new executable is very easy though, and the existing files should serve as easy copypasta. Pull requests are very much welcome!

## Installation
```bash
pip install kaldibin
```

Currently the approach to hooking into Kaldi tools is an environment variable:

```bash
export KALDI_ROOT=/path/to/kaldi
```

Would be cool to get the compiled executables packaged in a wheel or however it's done, but I haven't figured that out yet.

## Example

### Getting alignments and confidence scores from a lattice file

```python
import kaldibin

# Store our experiment directory to resolve the filenames used below.
DIR = '/path/to/recipe/exp/chain_train_1/'

# Build a labelid -> word mapping from words.txt
with open(DIR + 'graph/words.txt') as words_file:
    word_lookup = { id: word for word, id in [l.split() for l in words_file] }

# The lattice in our example is a Kaldi archive `*.ark` file, gzipped. We'll
# initialize it as the `KaldiGzFile` type in the package. The lexicon and model
# don't use the rspecifier format, so we can call them a `KaldiFile` with no
# type, or simply provide a string.

lattice = kaldibin.KaldiGzFile(DIR + 'decode_test/lat.1.gz', rxtype='ark')
lexicon = kaldibin.KaldiFile(DIR + 'graph/phones/align_lexicon.int', rxtype=None)
model = DIR + 'final.mdl'  # Filename with no rxspecifier; wrapping in KaldiFile() is optional.

# Obtain alignments from the lattice with `lattice-align-words-lexicon`.
word_alignments = kaldibin.lattice_align_words_lexicon(lexicon, model, lattice)

# Note that `word_alignments` is a `KaldiPipe` which can be fed to another
# `kaldibin` function, and executes (once) only when read. For example:

# Convert the alignments to CTM format for human readability.
ctms = kaldibin.lattice_to_ctm_conf(word_alignments)

# This also returns a `KaldiPipe`, but we can use the `.bytes()` method to
# bring it into a Python variable.

ctm_lines = ctms.bytes().decode('utf-8')

for ctm_line in ctm_lines.split('\n'):
    if ' ' in ctm_line:
        utterance_id, speaker_id, start, duration, label_id, confidence = ctm_line.split()
        print(f'{utterance_id}: {word_lookup[label_id]} ({confidence})')
```

The output will look something like this.

```
AVALA-999-1_01_02: <sil> (1.00)
AVALA-999-1_01_02: didn't (0.66)
AVALA-999-1_01_02: the (1.00)
AVALA-999-1_01_02: kid (1.00)
AVALA-999-1_01_02: ride (1.00)
AVALA-999-1_01_02: the (1.00)
AVALA-999-1_01_02: bike (1.00)
AVALA-999-1_01_02: <sil> (1.00)
```
