import pytorch_lightning as pl
import argparse
import sys

from model import PedalNet
from prepare import prepare


def main(args):
    """
    This trains the PedalNet model to match the output data from the input data.

    When you resume training from an existing model, you can override hparams such as
        max_epochs, batch_size, or learning_rate. Note that changing num_channels,
        dilation_depth, num_repeat, or kernel_size will change the shape of the WaveNet
        model and is not advised.

    """

    hparams = vars(args)
    model = PedalNet(
        num_channels=hparams["num_channels"],
        dilation_depth=hparams["dilation_depth"],
        num_repeat=hparams["num_repeat"],
        kernel_size=hparams["kernel_size"],
        learning_rate=hparams["learning_rate"],
        batch_size=hparams["batch_size"],
        model=hparams["model"],
    )
    trainer = pl.Trainer(
        log_every_n_steps=100,
        max_epochs=args.max_epochs,
    )

    trainer.fit(model)
    trainer.save_checkpoint(args.model)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", nargs="?", default="data/in.wav")
    parser.add_argument("out_file", nargs="?", default="data/out.wav")
    parser.add_argument("--sample_time", type=float, default=100e-3)
    parser.add_argument("--normalize", type=bool, default=True)

    parser.add_argument("--num_channels", type=int, default=4)
    parser.add_argument("--dilation_depth", type=int, default=9)
    parser.add_argument("--num_repeat", type=int, default=2)
    parser.add_argument("--kernel_size", type=int, default=3)

    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--learning_rate", type=float, default=3e-3)

    parser.add_argument("--max_epochs", type=int, default=1000)
    parser.add_argument("--gpus", type=int, default=-1)
    parser.add_argument("--tpu_cores", type=int, default=None)
    parser.add_argument("--cpu", action="store_true")

    parser.add_argument("--model", type=str, default="models/pedalnet/pedalnet.ckpt")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    main(args)
