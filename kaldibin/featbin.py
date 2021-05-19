import kaldibin
from kaldibin import magic


def compute_cmvn_stats(
        feats,
        *,
        binary=True,
        spk2utt='',
        weights='',
        wxtype='ark',
        wxfilename='-'
):
    args = kaldibin._magic_parse_args(compute_cmvn_stats, **locals())
    return kaldibin._context.run(
        'src/featbin/compute-cmvn-stats',
        *args,
        wxtype=wxtype,
        wxfilename=wxfilename
    )


def compute_mfcc_feats(
        wavs,
        *,
        allow_downsample=False,
        allow_upsample=False,
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
    args = kaldibin._magic_parse_args(compute_mfcc_feats, **locals())
    return kaldibin._context.run(
        'src/featbin/compute-mfcc-feats',
        *args,
        wxtype=wxtype,
        wxfilename=wxfilename
    )


def wav_copy(
        wav,
        *,
        wxtype='ark',
        wxfilename='-'
):
    args = kaldibin._magic_parse_args(compute_mfcc_feats, **locals())
    return kaldibin._context.run(
        'src/featbin/wav-copy',
        *args,
        wxtype=wxtype,
        wxfilename=wxfilename
    )