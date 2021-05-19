import kaldibin


def nnet3_latgen_faster(
        nnet,
        fst,
        features,
        *,
        acoustic_scale=0.1,
        allow_partial=False,
        beam=16,
        beam_delta=0.5,
        computation_debug=False,
        debug_computation=False,
        delta=0.000976562,
        determinize_lattice=True,
        extra_left_context=0,
        extra_left_context_initial=-1,
        extra_right_context=0,
        extra_right_context_final=-1,
        frame_subsampling_factor=1,
        frames_per_chunk=50,
        hash_ratio=2.0,
        ivectors='',
        lattice_beam=10.0,
        max_active=2147483647,
        max_mem=50000000,
        min_active=200,
        minimize=False,
        online_ivector_period=0,
        online_ivectors='',
        phone_determinize=True,
        prune_interval=25,
        utt2spk='',
        word_determinize=True,
        word_symbol_table='',
        **args
    ):
    '''
    WARNING: INCOMPLETE WRAPPER IMPLEMENTATION

    :param nnet:
    :param fst:
    :param features:
    :param _:
    :param acoustic_scale:
    :param allow_partial:
    :param beam:
    :param beam_delta:
    :param computation_debug:
    :param debug_computation:
    :param delta:
    :param determinize_lattice:
    :param extra_left_context:
    :param extra_left_context_initial:
    :param extra_right_context:
    :param extra_right_context_final:
    :param frame_subsampling_factor:
    :param frames_per_chunk:
    :param hash_ratio:
    :param ivectors:
    :param lattice_beam:
    :param max_active:
    :param max_mem:
    :param min_active:
    :param minimize:
    :param online_ivector_period:
    :param online_ivectors:
    :param phone_determinize:
    :param prune_interval:
    :param utt2spk:
    :param word_determinize:
    :param word_symbol_table:
    :param args:
    :return:
    '''

    args = kaldibin._magic_parse_args(nnet3_latgen_faster, **locals())
    return kaldibin._context.run(
        'src/nnet3bin/nnet3-latgen-faster',
        *args,
        wxtype="ark",
        wxfilename="-"
    )
