import argparse
import os
import shutil
import sys

import kaldibin
from kaldibin import KaldiFile


def main():
    parser = argparse.ArgumentParser(description='Make MFCCs')
    parser.add_argument('data')
    parser.add_argument('log_dir', nargs="?", help="Directory for logging, defaults to [data]/log.")
    parser.add_argument('mfcc_dir')
    parser.add_argument('--nj', type=int, default=4)
    parser.add_argument('--mfcc-config', default="conf/mfcc.conf")
    parser.add_argument('--compress', type=bool, default=True)
    parser.add_argument('--write-utt2num-frames', type=bool, default=False)
    parser.add_argument('--feats-scp', help="Defaults to [data]/feats.scp")
    parser.add_argument('--wav-scp', help="Defaults to [data]/wav.scp")
    parser.add_argument('--backup-dir', help="Defaults to [data]/.backup")
    parser.add_argument('--spk2warp', help="Defaults to [data]/spk2warp")
    parser.add_argument('--utt2warp', help="Defaults to [data]/utt2warp")
    parser.add_argument('--utt2spk', help="Defaults to [data]/utt2spk")
    parser.add_argument('--segments', help="Defaults to [data]/segments")
    args = parser.parse_args()

    # Being explicit and configurable with filenames conventions
    if args.log_dir is None: args.log_dir = os.path.join(args.data, "log")
    if args.feats_scp is None: args.feats_scp = os.path.join(args.data, "feats.scp")
    if args.wav_scp is None: args.wav_scp = os.path.join(args.data, "wav.scp")
    if args.backup_dir is None: args.backup_dir = os.path.join(args.data, ".backup")
    if args.spk2warp is None: args.spk2warp = os.path.join(args.data, "spk2warp")
    if args.utt2warp is None: args.utt2warp = os.path.join(args.data, "utt2warp")
    if args.utt2spk is None: args.utt2spk = os.path.join(args.data, "utt2spk")
    if args.segments is None: args.segments = os.path.join(args.data, "segments")

    script_name = os.path.basename(sys.argv[0])
    name = os.path.basename(args.data)

    os.makedirs(args.mfcc_dir, exist_ok=True)
    os.makedirs(args.log_dir, exist_ok=True)

    if os.path.exists(args.feats_scp):
        print("{}: moving {} to {}".format(script_name, args.feats_scp, args.backup_dir))
        os.makedirs(args.backup_dir, exist_ok=True)
        shutil.move(args.feats_scp, args.backup_dir)

    for required in [args.wav_scp, args.mfcc_config]:
        if not os.path.exists(required):
            raise FileNotFoundError("{}: no such file {}".format(script_name, required))

    #TODO utils/validate_data_dir.sh --no-text --no-feats $data || exit 1from

    vtln_options = {}
    if os.path.exists(args.spk2warp):
        vtln_options["vtln_map"] = args.spk2warp
        vtln_options["utt2spk"] = args.utt2spk
    elif os.path.exists(args.utt2warp):
        vtln_options["vtln_map"] = args.utt2warp

    write_num_frames_options = {}
    if args.write_utt2num_frames:
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

    if os.path.isfile(args.segments):
        print("{} [info]: segments file exists: using that.".format(script_name))
        split_segments = ["{}/segments.{}".format(args.log_dir, name, n) for n in range(args.nj)]
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
        split_scps = ["{}/wav_{}.{}.scp".format(args.log_dir, name, n) for n in range(args.nj)]

        wav_scp = KaldiFile(args.wav_scp)
        out_ark = "{}/raw_mfcc_{}.JOB.ark".format(args.mfcc_dir, name)
        out_scp = "{}/raw_mfcc_{}.JOB.scp".format(args.mfcc_dir, name)
        mfccs = kaldibin.compute_mfcc_feats(
            wav_scp,
            **vtln_options,
            verbose=2,
            config=args.mfcc_config,
            wxtype="ark,scp",
            wxfilename="{},{}".format(out_ark, out_scp)
        )


        '''utils/split_scp.pl $scp $split_scps || exit 1;'''
if __name__ == "__main__":
    main()