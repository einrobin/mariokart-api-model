import torch

from .dataset import load_dataset_metadata
from .train import TrainConfig, create_dataset_loaders, create_model, train_model


def setup_cli(subparsers):
    parser = subparsers.add_parser("train")

    parser.add_argument("-i", "--input", help="Path to the annotations.json", required=True)
    parser.add_argument("-s", "--frame-size", help="Number in pixels of the width and height of each frame", type=int,
                        required=False, default=128)
    parser.add_argument("-f", "--frames-per-clip", help="Number of frames in each clip", type=int, required=False,
                        default=32)
    parser.add_argument("-b", "--batch-size", help="Size per batch", type=int, required=False, default=4)
    parser.add_argument("-n", "--epochs", help="Number of epochs the training should run through", type=int,
                        required=False,
                        default=15)
    parser.add_argument("-r", "--learning-rate", help="Learning rate for the training", type=float, required=False,
                        default=1e-4)
    parser.add_argument("--force-cpu",
                        help="Forces the training to run on the CPU, otherwise uses the GPU automatically if available",
                        action="store_true")
    parser.add_argument("-o", "--output", help="Path where the trained model shall be stored", required=False,
                        default="./model.pth")

    parser.set_defaults(func=prepare_data)


def prepare_data(args):
    input_dataset_dir = args.input

    print("Loading dataset metadata...")
    metadata = load_dataset_metadata(input_dataset_dir)

    device = "cpu"
    if not args.force_cpu:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if device == "cpu":
            print("Cannot find any available GPU!")

    if device == "cpu":
        print("Training will run on the CPU!")

    config = TrainConfig(frame_size=args.frame_size, frames_per_clip=args.frames_per_clip, batch_size=args.batch_size,
                         epoch_count=args.epochs, learning_rate=args.learning_rate, device=device)

    print("The following options will be used to train the model:")
    print(f"Frame Size: {config.frame_size}x{config.frame_size} px")
    print(f"Frames per Clip: {config.frames_per_clip}")
    print(f"Batch Size: {config.batch_size}")
    print(f"Training Epochs: {config.epoch_count}")
    print(f"Learning rate: {config.learning_rate}")
    print(f"Device: {config.device}")

    print("Loading dataset videos...")
    loaders = create_dataset_loaders(metadata, config)
    model = create_model(metadata, config)

    print("Beginning with training, this will take a while...")
    train_model(model, loaders, config)

    out_file = args.output
    print(f"Training finished! Writing to file {out_file}...")
    torch.save(model.state_dict(), out_file)
    print(f"Model has been written to {out_file}")
