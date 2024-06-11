import argparse
import os

import data.utils
import model.utils as model_utils
from WUN_Sep.model.waveunet import Waveunet
from model.predict import predict_song

def main(args):
    # MODEL
    num_features = [args.features*i for i in range(1, args.levels+1)] if args.feature_growth == "add" else \
                   [args.features*2**i for i in range(0, args.levels)]
    target_outputs = int(args.output_size * args.sr)

    model = Waveunet(args.channels, num_features, args.channels, args.instruments, kernel_size=args.kernel_size,
                     target_output_size=target_outputs, depth=args.depth, strides=args.strides,
                     conv_type=args.conv_type, res=args.res, separate=args.separate)

    if args.cuda:
        model = model_utils.DataParallel(model)
        print("move model to gpu")
        model.cuda()

    print("Loading model from checkpoint " + str(args.load_model))
    state = model_utils.load_model(model, None, args.load_model, args.cuda)
    print('Step', state['step'])

    preds = predict_song(args, args.input, model)

    output_folder = os.path.dirname(args.input) if args.output is None else args.output
    for inst in preds.keys():
        data.utils.write_wav(os.path.join(output_folder, os.path.basename(args.input) + "_" + inst + ".wav"), preds[inst], args.sr)
if __name__ == '__main__':
    default_args = {
        'instruments': ["bass", "drums", "other", "vocals"],
        'cuda': False,
        'features': 32,
        'load_model': 'checkpoints/waveunet/model',
        'batch_size': 4,
        'levels': 6,
        'depth': 1,
        'sr': 44100,
        'channels': 2,
        'kernel_size': 5,
        'output_size': 2.0,
        'strides': 4,
        'conv_type': "gn",
        'res': "fixed",
        'separate': 1,
        'feature_growth': "double",
        'input': os.path.join("audio_examples", "Cristina Vane - So Easy", "mix.mp3"),
        'output': None
    }

    main(**default_args)