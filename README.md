# Why `kaldibin`?

* The idea is for this to be a core interface for accessing Kaldi executables from Python. Then a second package (todo) can be created that does things like the `kaldi/egs/wsj/s5/steps/` scripts do, but in an installable python package.
* A huge advantage of packaging this material is a versioning system, which will improve backward compatibility of our Kaldi recipes. And the current structure, tied to the Kaldi codebase and `egs/wsj` structure, is a poor separation of concerns that makes creating and sharing recipes harder than it ought to be.
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
