import kaldibin


def compute_cmvn_stats(
        feats,
        *_,
        binary=True,
        spk2utt='',
        weights='',
        wxtype='ark',
        wxfilename='-'
):
    return kaldibin._context.run(
        'src/featbin/compute-cmvn-stats',
        '--binary={}'.format('true' if binary else 'false'),
        '--spk2utt={}'.format(spk2utt),
        '--weights={}'.format(weights),
        feats,
        wxtype=wxtype,
        wxfilename=wxfilename
    )


def compute_mfcc_feats(
        wavs,
        *_,
        allow_downsample=False,
        blackman_coeff=0.42,
        cepstral_lifter=22,
        channel=-1,
        debug_mel=False,
        dither=1.0,
        energy_floor=0.0,
        frame_length=25,
        frame_shift=10,
        high_freq=0,
        htk_compat=False,
        low_freq=20,
        min_duration=0,
        num_ceps=13,
        num_mel_bins=23,
        output_format='kaldi',
        preemphasis_coefficient=0.97,
        raw_energy=True,
        remove_dc_offset=True,
        round_to_power_of_two=True,
        sample_frequency=16000,
        snip_edges=True,
        subtract_mean=False,
        use_energy=True,
        utt2spk='',
        vtln_high=-500,
        vtln_low=100,
        vtln_map='',
        vtln_warp=1,
        window_type='povey',
        verbose=0,
        config='',
        wxtype='ark',
        wxfilename='-'
):
    return kaldibin._context.run(
        'src/featbin/compute-mfcc-feats',
        '--allow-downsample={}'.format('true' if allow_downsample else 'false'),
        '--blackman-coeff={}'.format(blackman_coeff),
        '--cepstral-lifter={}'.format(cepstral_lifter),
        '--channel={}'.format(channel),
        '--debug-mel={}'.format('true' if debug_mel else 'false'),
        '--dither={}'.format(dither),
        '--energy-floor={}'.format(energy_floor),
        '--frame-length={}'.format(frame_length),
        '--frame-shift={}'.format(frame_shift),
        '--high-freq={}'.format(high_freq),
        '--htk-compat={}'.format('true' if htk_compat else 'false'),
        '--low-freq={}'.format(low_freq),
        '--min-duration={}'.format(min_duration),
        '--num-ceps={}'.format(num_ceps),
        '--num-mel-bins={}'.format(num_mel_bins),
        '--output-format={}'.format(output_format),
        '--preemphasis_coefficient={}'.format(preemphasis_coefficient),
        '--raw-energy={}'.format('true' if raw_energy else 'false'),
        '--remove-dc-offset={}'.format('true' if remove_dc_offset else 'false'),
        '--round-to-power-of-two={}'.format('true' if round_to_power_of_two else 'false'),
        '--sample-frequency={}'.format(sample_frequency),
        '--snip-edges={}'.format('true' if snip_edges else 'false'),
        '--subtract-mean={}'.format('true' if subtract_mean else 'false'),
        '--use-energy={}'.format('true' if use_energy else 'false'),
        '--utt2spk={}'.format(utt2spk),
        '--vtln-high={}'.format(vtln_high),
        '--vtln-low={}'.format(vtln_low),
        '--vtln-map={}'.format(vtln_map),
        '--vtln-warp={}'.format(vtln_warp),
        '--window-type={}'.format(window_type),
        '--verbose={}'.format(verbose),
        '--config={}'.format(config),
        wavs,
        wxtype=wxtype,
        wxfilename=wxfilename
    )


def wav_copy(wav, *_, wxtype='ark', wxfilename='-'):
    return kaldibin._context.run(
        'src/featbin/wav-copy',
        wav,
        wxtype=wxtype,
        wxfilename=wxfilename
    )