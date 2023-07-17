"""Console script for imagebanner."""
import sys
import click
from .main import add_border_to_image


@click.command()
@click.option(
    "-i",
    "--input",
    "infile",
    type=click.Path(exists=True),
    help="Input photo filename.",
)
@click.option(
    "-o", "--output", "outfile", type=click.File("w"), help="Output photo filename."
)
@click.option(
    "--add-camera-logo",
    is_flag=True,
    show_default=True,
    default=True,
    help="Add camera logo.",
)
@click.option(
    "--add-lens", is_flag=True, show_default=True, default=True, help="Add lens text."
)
@click.option(
    "-l",
    "--logo-dir",
    "logodir",
    type=click.Path(exists=True),
    help="Camera logo dir path.",
)
def main(infile, outfile, add_camera_logo, add_lens, logodir):
    """Console script for imagebanner."""
    add_border_to_image(
        image_path=infile,
        output_path=outfile,
        camera_logo_dir=logodir,
        add_camera_logo=add_camera_logo,
        add_lens=add_lens,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
