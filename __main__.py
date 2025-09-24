import argparse


def main():
    parser = argparse.ArgumentParser(prog='mktrain', description='Command line interface for the Mario Kart trainer')
    subparsers = parser.add_subparsers()

    from videoeventdetection.dataset_builder import setup_cli
    setup_cli(subparsers)

    from videoeventdetection.training import setup_cli
    setup_cli(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


main()
