"""Console script for imagebanner."""
import sys
import click
from .main import add_border_to_image
import os


@click.command()
@click.option(
    "-i",
    "--input",
    "infile",
    type=click.Path(exists=True),
    help="Input filename or dirname",
)
@click.option(
    "-o", "--output", "outfile", type=click.Path(), help="Output filename or dirname"
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
    "--logo-dir",
    "logodir",
    type=click.Path(exists=True),
    help="Camera logo dir path.",
)
def main(infile, outfile, add_camera_logo, add_lens, logodir):
    """Console script for imagebanner."""
    if os.path.isfile(infile) and os.path.isfile(outfile):
        add_border_to_image(
            image_path=infile,
            output_path=outfile,
            camera_logo_dir=logodir,
            add_camera_logo=add_camera_logo,
            add_lens=add_lens,
        )
    if os.path.isdir(infile) and os.path.isdir(outfile):
        for f in os.listdir(infile):
            add_border_to_image(
                image_path=os.path.join(infile, f),
                output_path=os.path.join(outfile, f),
                camera_logo_dir=logodir,
                add_camera_logo=add_camera_logo,
                add_lens=add_lens,
            )
    if os.path.isfile(infile) and os.path.isdir(outfile):
        add_border_to_image(
            image_path=infile,
            output_path=os.path.join(outfile, infile),
            camera_logo_dir=logodir,
            add_camera_logo=add_camera_logo,
            add_lens=add_lens,
        )
    else:
        raise click.BadArgumentUsage("infile is a dir, but outfile is a file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
