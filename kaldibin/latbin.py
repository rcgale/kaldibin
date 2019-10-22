import kaldibin


def lattice_1best(
        lattice,
        *_,
        acoustic_scale=1.0,
        lm_scale=1.0,
        word_ins_penalty=0.0
):
    return kaldibin._context.run(
        "src/latbin/lattice-1best",
        "--acoustic-scale={}".format(acoustic_scale),
        "--lm-scale={}".format(lm_scale),
        "--word-ins-penalty={}".format(word_ins_penalty),
        lattice,
        wxtype="ark",
        wxfilename="-"
    )


def lattice_align_phones(
        model,
        lattice,
        output_error_lats=True,
        remove_epsilon=True,
        reorder=True,
        replace_output_symbols=False
):
    return kaldibin._context.run(
        "src/latbin/lattice-align-phones",
        "--output-error-lats={}".format("true" if output_error_lats else "false"),
        "--remove-epsilon={}".format("true" if remove_epsilon else "false"),
        "--reorder={}".format("true" if reorder else "false"),
        "--replace-output-symbols={}".format("true" if replace_output_symbols else "false"),
        model,
        lattice,
        wxtype="ark",
        wxfilename = "-"
    )


def lattice_align_words_lexicon(
        lexicon,
        model,
        lattice,
        *_,
        allow_duplicate_paths=False,
        max_expand=-1,
        output_error_lats=True,
        output_if_empty=False,
        partial_word_label=0,
        reorder=True,
        test=False
):
    return kaldibin._context.run(
        "src/latbin/lattice-align-words-lexicon",
        "--allow-duplicate-paths={}".format("true" if allow_duplicate_paths else "false"),
        "--max-expand={}".format(max_expand),
        "--output-error-lats={}".format("true" if output_error_lats else "false"),
        "--output-if-empty={}".format("true" if output_if_empty else "false"),
        "--partial-word-label={}".format(partial_word_label),
        "--reorder={}".format("true" if reorder else "false"),
        lexicon,
        model,
        lattice,
        wxtype = "ark",
        wxfilename = "-"
    )


def lattice_determinize(
        lattice,
        *_,
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
    return kaldibin._context.run(
        "src/latbin/lattice-determinize",
        "--acoustic-scale={}".format(acoustic_sale),
        "--beam={}".format(beam),
        "--beam-ratio={}".format(beam_ratio),
        "--delta={}".format(delta),
        "--max-loop={}".format(max_loop),
        "--max-mem={}".format(max_mem),
        "--minimize={}".format("true" if minimize else "false"),
        "--num-loops={}".format(num_loops),
        "--prune={}".format("true" if prune else "false"),
        lattice,
        wxtype="ark",
        wxfilename="-"
    )


def lattice_to_ctm_conf(
        lattice,
        *_,
        acoustic_scale=1.0,
        confidence_digits=2,
        decode_mbr=True,
        frame_shift=0.01,
        inv_acoustic_scale=1.0,
        lm_scale=1.0,
        print_silence=False
):
    return kaldibin._context.run(
        "src/latbin/lattice-to-ctm-conf",
        "--acoustic-scale={}".format(float(acoustic_scale)),
        "--confidence-digits={}".format(int(confidence_digits)),
        "--decode-mbr={}".format("true" if decode_mbr else "false"),
        "--frame-shift={}".format(frame_shift),
        "--inv-acoustic-scale={}".format(inv_acoustic_scale),
        "--lm-scale={}".format(lm_scale),
        "--print-silence={}".format("true" if print_silence else "false"),
        lattice,
        wxtype = None,
        wxfilename = "-"
    )


def nbest_to_ctm(
        nbest,
        *_,
        frame_shift=0.01,
        precision=2,
        print_silence=False
):
    return kaldibin._context.run(
        "src/latbin/nbest-to-ctm",
        "--frame-shift={}".format(float(frame_shift)),
        "--precision={}".format(int(precision)),
        "--print-silence={}".format("true" if print_silence else "false"),
        nbest,
        wxtype = None,
        wxfilename = "-"
    )
