import inspect
import os
import subprocess
import sys
import tempfile
import threading
import uuid
from typing import Dict, Type, Callable

import re

import kaldibin
from kaldibin import magic
from kaldibin.adapters.io import KaldiPipe, KaldiFile, KaldiBytes

_KALDI_ROOT = os.environ['KALDI_ROOT'] if 'KALDI_ROOT' in os.environ else None


class KaldiContext(object):
    def __init__(self, kaldi_root=_KALDI_ROOT):
        if not kaldi_root:
            config = get_config() or {}
            kaldi_root = config.get("kaldi_root")
        self._to_close = []
        self._to_delete = []
        self._kaldi_root = kaldi_root

    def open(self):
        self._previous_context = kaldibin._context
        kaldibin._context = self
        return self

    def close(self):
        for to_close in self._to_close:
            to_close.close()
        for to_delete in self._to_delete:
            if os.path.exists(to_delete):
                os.unlink(to_delete)
        kaldibin._context = self._previous_context

    def run(self, executable, *args, input=None, wxtype, wxfilename):
        if not os.path.isdir(self._kaldi_root):
            raise Exception('Kaldi root not found. Try running: \n\t'
                            'kaldibin-config --kaldi-root /path/to/kaldi\n\n')

        exe = os.path.join(self._kaldi_root, executable)
        prepared_args, pipe_handles = _prepare_args(self, args)
        wxspecifier = '{}:{}'.format(wxtype, wxfilename) if wxtype else wxfilename
        process = subprocess.Popen(
            [exe, *prepared_args, wxspecifier],
            stdin=subprocess.PIPE if input is not None else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
        )
        if input is not None:
            process.communicate(input=input)

        # Run FIFO inputs as separate thread to avoid deadlock
        fifo_args = [arg for arg in args if _is_fifo(arg)]
        for arg, fifo in zip(fifo_args, pipe_handles):
            threading.Thread(target=_write_fifo, args=(arg, fifo)).start()

        if wxfilename == '-':
            pipe_out = KaldiPipe(process, rxtype=wxtype)
            self._to_close.append(pipe_out)
            return pipe_out
        else:
            process.wait()
            return KaldiFile(wxfilename, rxtype=wxtype)


def _prepare_args(kaldi_context, args):
    prepared = []
    fifos = []
    for arg in args:
        if _is_fifo(arg):
            fifo_filename = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
            os.mkfifo(fifo_filename)
            kaldi_context._to_delete.append(fifo_filename)
            fifos.append(fifo_filename)
            prepared.append('{}:{}'.format(arg.rxtype, fifo_filename) if arg.rxtype else fifo_filename)
        elif _is_rwspecifier(arg):
            if hasattr(arg, "is_gz") and arg.is_gz:
                prepared.append('{}:gunzip -c {}|'.format(arg.rxtype, arg.filename))
            elif arg.rxtype:
                prepared.append('{}:{}'.format(arg.rxtype, arg.filename) if arg.rxtype else arg.filename)
            else:
                prepared.append(arg.filename)
        else:
            prepared.append(str(arg))
    return prepared, fifos


def _write_fifo(arg, fifo):
    write_handle = os.open(fifo, os.O_WRONLY | os.O_NOCTTY)
    if isinstance(arg, KaldiBytes):
        os.write(write_handle, arg.bytes)
    elif isinstance(arg, KaldiPipe):
        subprocess.run(['cat'], stdin=arg.out_stream, stdout=write_handle, shell=False, close_fds=True)
    else:
        raise NotImplementedError("Unexpected type in KaldiPipe: {}".format(type(arg)))
    os.close(write_handle)
    os.unlink(fifo)
    if isinstance(arg, KaldiPipe):
        arg.close()


def _is_fifo(arg):
    if type(arg) is KaldiBytes or issubclass(type(arg), KaldiBytes):
        return True
    return hasattr(arg, 'rxtype') and \
           hasattr(arg, 'out_stream') and \
           arg.out_stream is not None


def _is_rwspecifier(arg):
    return hasattr(arg, 'rxtype') and hasattr(arg, 'filename')


def _prepare_value(parameter, value):
    preparers: Dict[Type, Callable] = {
        bool: lambda v: 'true' if v else 'false',
    }

    t = parameter.annotation
    if parameter.annotation is inspect._empty:
        t = type(value)

    preparer = preparers.get(t, lambda v: v)
    prepared = preparer(value)
    return prepared


def _magic_parse_args(func, **kwargs):
    parameters = inspect.signature(func).parameters
    positional = []
    keyword = []
    skip = ("wxtype", "wxfilename", "_")
    for key, parameter in parameters.items():
        if key in skip:
            continue

        value = kwargs.get(key)

        if parameter.kind == inspect.Parameter.KEYWORD_ONLY:
            if kwargs.get(key) == parameter.default:
                continue
            value = _prepare_value(parameter, value)
            arg = '--{}={}'.format(key.replace("_", "-"), value)
            keyword.append(arg)
        else:
            if kwargs.get(key) is None:
                continue
            arg = _prepare_value(parameter, value)
            positional.append(arg)
    return keyword + positional


@magic.application
def configure(*, kaldi_root):
    """
    Writes local configuration for the kaldibin package
    :param _:
    :param kaldi_root: The path to Kaldi, e.g. /Users/babbage/dev/kaldi
    :return:
    """
    if not kaldi_root:
        print("Must provide a value for --kaldi-root !", file=sys.stderr)
        exit(1)

    config = get_config() or {}
    config["kaldi_root"] = kaldi_root
    write_config(config)
    print("Wrote config to {}".format(config_filename()))


def get_config():
    config_file = config_filename()
    if not os.path.isfile(config_file):
        return None
    config = {}
    with open(config_file) as f:
        for line in f:
            for key, value in re.findall("^\s*([^\s].*)\s*:\s*([^\s].*)\s*$", line):
                config[key] = value
    return config


def write_config(config):
    config_file = config_filename()
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    with open(config_file, "w") as f:
        for key, value in config.items():
            print("{}: {}".format(key, value), file=f)


def config_filename():
    return os.path.expanduser("~/.config/kaldibin/config.json")
