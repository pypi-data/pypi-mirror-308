import argparse
from .api import dump


def main():
    parser = argparse.ArgumentParser(
        description="Dump Hugging Face datasets to audio or image folders"
    )

    parser.add_argument(
        "dataset",
        help="Dataset name or path",
    )

    parser.add_argument(
        "dist",
        help="Destination folder path",
    )

    parser.add_argument(
        "--audio-column",
        help="Column name containing audio data",
    )

    parser.add_argument(
        "--image-column",
        help="Column name containing image data",
    )

    parser.add_argument(
        "--metadata-format",
        choices=["jsonl", "csv"],
        default="jsonl",
        help="Format for metadata file",
    )

    args = parser.parse_args()

    dump(
        dataset=args.dataset,
        dist=args.dist,
        audio_column=args.audio_column,
        image_column=args.image_column,
        metadata_format=args.metadata_format,
    )


if __name__ == "__main__":
    main()
