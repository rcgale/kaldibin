import os
import shutil
import sys
from typing import Optional

import kaldibin
from kaldibin import KaldiFile, magic


@magic.application
def make_mfcc(
        data,
        log_dir: Optional[str], # = "{data}/log",
        mfcc_dir,
        *,
        nj=4,
        mfcc_config="conf/mfcc.conf",
        compress=True,
        write_utt2num_frames=False,
        feats_scp="{data}/feats.scp",
        wav_scp="{data}/wav.scp",
        backup_dir="{data}/.backup",
        spk2warp="{data}/spk2warp",
        utt2warp="{data}/utt2warp",
        utt2spk="{data}/utt2spk",
        segments="{data}/segments",
):
    """
    Make MFCCs

    :param data:
    :param log_dir: Directory for logging
    :param mfcc_dir:
    :param nj:
    :param mfcc_config:
    :param compress:
    :param write_utt2num_frames:
    :param feats_scp: Location of feats.scp file
    :param wav_scp: Location of wav.scp file
    :param backup_dir: Location of backup directory
    :param spk2warp: Location of spk2warp file
    :param utt2warp: Location of utt2warp file
    :param utt2spk: Location of utt2spk file
    :param segments: Location of segments file
    :return:
    """

    # Being explicit and configurable with filenames conventions
    if "{data}" in log_dir: log_dir = log_dir.format(data=data)
    if "{data}" in feats_scp: feats_scp = feats_scp.format(data=data)
    if "{data}" in wav_scp: wav_scp = wav_scp.format(data=data)
    if "{data}" in backup_dir: backup_dir = backup_dir.format(data=data)
    if "{data}" in spk2warp: spk2warp = spk2warp.format(data=data)
    if "{data}" in utt2warp: utt2warp = utt2warp.format(data=data)
    if "{data}" in utt2spk: utt2spk = utt2spk.format(data=data)
    if "{data}" in segments: segments = segments.format(data=data)

    script_name = os.path.basename(sys.argv[0])
    name = os.path.basename(data)

    os.makedirs(mfcc_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    if os.path.exists(feats_scp):
        print("{}: moving {} to {}".format(script_name, feats_scp, backup_dir))
        os.makedirs(backup_dir, exist_ok=True)
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        shutil.move(feats_scp, backup_dir)

    for required in [wav_scp, mfcc_config]:
        if not os.path.exists(required):
            raise FileNotFoundError("{}: no such file {}".format(script_name, required))

    #TODO utils/validate_data_dir.sh --no-text --no-feats $data || exit 1from

    vtln_options = {}
    if os.path.exists(spk2warp):
        vtln_options["vtln_map"] = spk2warp
        vtln_options["utt2spk"] = utt2spk
    elif os.path.exists(utt2warp):
        vtln_options["vtln_map"] = utt2warp

    write_num_frames_options = {}
    if write_utt2num_frames:
        # TODO: Touch this up
        write_num_frames_options["write_num_frames"] = "ark,t:$logdir/utt2num_frames.JOB"



    #TODO
    '''
    for n in $(seq $nj); do
      # the next command does nothing unless $mfccdir/storage/ exists, see
      # utils/create_data_link.pl for more info.
      utils/create_data_link.pl $mfccdir/raw_mfcc_$name.$n.ark
    done
    '''

    if os.path.isfile(segments):
        print("{} [info]: segments file exists: using that.".format(script_name))
        split_segments = ["{}/segments.{}".format(log_dir, name, n) for n in range(nj)]
        #TODO
        '''
        
          utils/split_scp.pl $data/segments $split_segments || exit 1;
          rm $logdir/.error 2>/dev/null
        
          $cmd JOB=1:$nj $logdir/make_mfcc_${name}.JOB.log \
            extract-segments scp,p:$scp $logdir/segments.JOB ark:- \| \
            compute-mfcc-feats $vtln_opts --verbose=2 --config=$mfcc_config ark:- ark:- \| \
            copy-feats --compress=$compress $write_num_frames_opt ark:- \
              ark,scp:$mfccdir/raw_mfcc_$name.JOB.ark,$mfccdir/raw_mfcc_$name.JOB.scp \
             || exit 1;
        '''
    else:
        print("{}: [info]: no segments file exists: assuming wav.scp indexed by utterance.".format(script_name))
        split_scps = ["{}/wav_{}.{}.scp".format(log_dir, name, n) for n in range(nj)]

        wav_scp = KaldiFile(wav_scp, rxtype='scp')
        out_ark = "{}/raw_mfcc_{}.JOB.ark".format(mfcc_dir, name)
        out_scp = "{}/raw_mfcc_{}.JOB.scp".format(mfcc_dir, name)

        mfccs = kaldibin.compute_mfcc_feats(
            wav_scp,
            **vtln_options,
            verbose=2,
            config=mfcc_config,
            wxtype="ark,scp",
            wxfilename="{},{}".format(out_ark, out_scp)
        )

        '''utils/split_scp.pl $scp $split_scps || exit 1;'''


if __name__ == "__main__":
    make_mfcc()