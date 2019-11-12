import os
import subprocess
import tempfile
import threading
import uuid

import kaldibin
from kaldibin.adapters.io import KaldiPipe, KaldiFile, KaldiBytes

_KALDI_ROOT = os.environ['KALDI_ROOT'] if 'KALDI_ROOT' in os.environ else None


class KaldiContext(object):
    def __init__(self, kaldi_root=_KALDI_ROOT):
        if not kaldi_root or not os.path.isdir(kaldi_root):
            raise Exception('Kaldi root not found. Set the environment variable KALDI_ROOT.')
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
            os.unlink(to_delete)
        kaldibin._context = self._previous_context

    def run(self, executable, *args, input=None, wxtype, wxfilename):
        exe = os.path.join(self._kaldi_root, executable)
        prepared_args, pipe_handles = _prepare_args(self, args)
        wxspecifier = '{}:{}'.format(wxtype, wxfilename) if wxtype else wxfilename
        process = subprocess.Popen(
            [exe, *prepared_args, wxspecifier],
            stdin=subprocess.PIPE if input is not None else None,
            stdout=subprocess.PIPE,
            stderr=None,
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
    if type(arg) is KaldiBytes or issubclass(type(arg), KaldiBytes):
        os.write(write_handle, arg.bytes)
    else:
        subprocess.run(['cat'], stdin=arg.out_stream, stdout=write_handle, shell=False, close_fds=True)
    os.close(write_handle)


def _is_fifo(arg):
    if type(arg) is KaldiBytes or issubclass(type(arg), KaldiBytes):
        return True
    return hasattr(arg, 'rxtype') and \
           hasattr(arg, 'out_stream') and \
           arg.out_stream is not None


def _is_rwspecifier(arg):
    return hasattr(arg, 'rxtype') and hasattr(arg, 'filename')
