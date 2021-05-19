import kaldibin


def lattice_1best(
        lattice,
        *,
        acoustic_scale=1.0,
        lm_scale=1.0,
        word_ins_penalty=0.0
):
    args = kaldibin._magic_parse_args(lattice_1best, **locals())
    return kaldibin._context.run(
        "src/latbin/lattice-1best",
        *args,
        wxtype="ark",
        wxfilename="-"
    )


def lattice_align_phones(
        model,
        lattice,
        *,
        output_error_lats=True,
        remove_epsilon=True,
        reorder=True,
        replace_output_symbols=False
):
    args = kaldibin._magic_parse_args(lattice_align_phones, **locals())
    return kaldibin._context.run(
        "src/latbin/lattice-align-phones",
        *args,
        wxtype="ark",
        wxfilename = "-"
    )


def lattice_align_words_lexicon(
        lexicon,
        model,
        lattice,
        *,
        allow_duplicate_paths=False,
        max_expand=-1,
        output_error_lats=True,
        output_if_empty=False,
        partial_word_label=0,
        reorder=True,
        test=False
):
    args = kaldibin._magic_parse_args(lattice_align_words_lexicon, **locals())
    return kaldibin._context.run(
        "src/latbin/lattice-align-words-lexicon",
        *args,
        wxtype = "ark",
        wxfilename = "-"
    )


def lattice_determinize(
        lattice,
        *,
        acoustic_sale=1.0,
        beam=10.0,
        beam_ratio=0.9,
        delta=0.000976562,
        max_loop=500000,
        max_mem=50000000,
        minimize=False,
        num_loops=20,
        prune=False
):
    args = kaldibin._magic_parse_args(lattice_determinize, **locals())
    return kaldibin._context.run(
        "src/latbin/lattice-determinize",
        *args,
        wxtype="ark",
        wxfilename="-"
    )


def lattice_to_ctm_conf(
        lattice,
        *,
        acoustic_scale=1.0,
        confidence_digits=2,
        decode_mbr=True,
        frame_shift=0.01,
        inv_acoustic_scale=1.0,
        lm_scale=1.0,
        print_silence=False
):
    args = kaldibin._magic_parse_args(lattice_to_ctm_conf, **locals())
    return kaldibin._context.run(
        "src/latbin/lattice-to-ctm-conf",
        *args,
        wxtype = None,
        wxfilename = "-"
    )


def nbest_to_ctm(
        nbest,
        *,
        frame_shift=0.01,
        precision=2,
        print_silence=False
):
    args = kaldibin._magic_parse_args(nbest_to_ctm, **locals())
    return kaldibin._context.run(
        "src/latbin/nbest-to-ctm",
        *args,
        wxtype = None,
        wxfilename = "-"
    )
