from common.logger import get_common_logger
from imagegetter.image_getter import ImageGetter
import click

log = get_common_logger()
image_getter = ImageGetter(logger=log)
freshpaperSources = image_getter.get_freshpaper_sources()


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--source",
    default="bing",
    type=click.Choice(freshpaperSources.keys()),
    help="Source for setting the wallpaper.",
)
def main(ctx, source) -> None:
    if ctx.invoked_subcommand is None:
        dir_name = image_getter.get_wallpaper_directory()  # Wallpaper directory name
        try:
            download_image = freshpaperSources.get(source)["download"]
            image_path = download_image(dir_name)
            image_getter.set_wallpaper(image_path)
        except ConnectionError:
            image_path = image_getter.get_saved_wallpaper(dir_name)
            image_getter.set_wallpaper(image_path)
        except Exception as e:
            log.error(e)


if __name__ == "__main__":
    main()
