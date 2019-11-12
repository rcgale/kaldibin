import kaldibin


def ivector_extract_online2(
        spk2utt,
        feats,
        *_,
        config='',
        wxtype='ark',
        wxfilename='-'
):
    '''
    WARNING: INCOMPLETE WRAPPER IMPLEMENTATION
    :param spk2utt:
    :param feats:
    :param _:
    :param config:
    :param wxtype:
    :param wxfilename:
    :return:
    '''

    return kaldibin._context.run(
        'src/online2bin/ivector-extract-online2',
        '--config={}'.format(config),
        spk2utt,
        feats,
        wxtype=wxtype,
        wxfilename=wxfilename
    )


def online2_wav_nnet3_latgen_faster(
        nnet3,
        fst,
        spk2utt,
        wav,
        *_,
        max_active=2147483647,
        beam=16.0,
        do_endpointing=False,
        frame_subsampling_factor=1,
        lattice_beam=10.0,
        acoustic_scale=0.1,
        word_symbol_table='',
        config='',
        wxtype='ark',
        wxfilename='-'
):
    '''
    WARNING: INCOMPLETE WRAPPER IMPLEMENTATION
    :param nnet3:
    :param fst:
    :param spk2utt:
    :param wav:
    :param _:
    :param max_active:
    :param beam:
    :param do_endpointing:
    :param frame_subsampling_factor:
    :param lattice_beam:
    :param acoustic_scale:
    :param word_symbol_table:
    :param config:
    :param wxtype:
    :param wxfilename:
    :return:
    '''

    return kaldibin._context.run(
        "src/online2bin/online2-wav-nnet3-latgen-faster",
        "--online=false",
        "--do-endpointing={}".format('true' if do_endpointing else 'false'),
        "--config={}".format(config),
        "--frame-subsampling-factor={}".format(frame_subsampling_factor),
        "--max-active={}".format(max_active),
        "--beam={}".format(beam),
        "--lattice-beam={}".format(lattice_beam),
        "--acoustic-scale={}".format(acoustic_scale),
        "--word-symbol-table={}".format(word_symbol_table),
        nnet3,
        fst,
        spk2utt,
        wav,
        wxtype=wxtype,
        wxfilename=wxfilename
    )