"""Main module."""


from PIL import Image, ImageFont, ImageDraw
from PIL.ExifTags import TAGS, GPSTAGS, IFD
from datetime import datetime
from pathlib import Path
import exifread
import os
import logging
from . import logging_config
from .constants import FILMMODE_DICT, FONT_NAME

logger = logging.getLogger(__name__)
logger.propagate = False


script_dir = os.path.dirname(__file__)


def _get_exif_from_img_file(image_path):
    exif = {}
    with open(image_path, "rb") as img:
        exif = exifread.process_file(img)
    return exif


def get_fuji_filmmode(image_path):
    with open(image_path, "rb") as f:
        tags = exifread.process_file(f)
    filmmode = tags.get("MakerNote Tag 0x1401")
    if filmmode is None:
        return None
    else:
        filmmode = int(f"{filmmode}")
        return FILMMODE_DICT.get(filmmode, None)


def _resize_image(img, width=0, height=0):
    """Resize image to the given width or height. If either `width` or `height` is 0,
    the image is resized to `height` or `width` and keeps the original ratio. If both `width`
    and `height` are greater than 0, the image is resized to the given `width`

    Args:
        img (object): Image.open() object.
        width (int, optional): _description_. Defaults to 0.
        height (int, optional): _description_. Defaults to 0.

    Returns:
        object: _description_
    """
    ratio = img.width / img.height
    if width > 0:
        return img.resize((width, int(width / ratio)))
    elif height > 0:
        return img.resize((int(height * ratio), height))
    else:
        raise RuntimeError("At least one of width and height shoult be > 0")


def add_border_to_image(
    image_path, output_path, camera_logo_dir=None, add_camera_logo=True, add_lens=True
):
    """给图像添加边框，并在边框内添加拍摄信息和相机logo（可选）。

    Args:
        image_path (str): 图像文件的路径。
        output_path (str): 保存新图像的路径。
        camera_logo_dir (str): 相机logo文件夹的路径，不传入时使用包内附带
        add_camera_logo (bool, optional): 是否添加相机logo。默认为 True。
        add_lens (bool, optional): 是否添加镜头信息。默认为 True。
    """
    # 读取图片
    image_path = Path(image_path)
    image = Image.open(image_path)

    # 读取 exif 信息
    exif_data = _get_exif_from_img_file(image_path)

    # 获取照片的拍摄机型、iso、快门速度、镜头参数和富士胶片模拟名称
    camera_make = str(exif_data.get("Image Make", ""))
    if camera_make == "":
        image.save(output_path, "JPEG", quality=95)
        return
    camera_model = str(exif_data.get("Image Model", ""))
    iso = str(exif_data.get("EXIF ISOSpeedRatings", ""))
    shutter_speed = exif_data["EXIF ExposureTime"].printable
    # if shutter_speed is not None:
    #     shutter_speed = float(shutter_speed)
    #     shutter_speed = (
    #         str(shutter_speed) if shutter_speed >= 1 else f"1/{int(1/shutter_speed)}"
    #     )

    lens = exif_data.get("EXIF LensModel").printable
    # 获取照片的拍摄日期
    capture_date = datetime.strptime(
        exif_data["EXIF DateTimeOriginal"].printable, "%Y:%m:%d %H:%M:%S"
    ).strftime("%Y-%m-%d %H:%M:%S %a")

    film_mode = get_fuji_filmmode(image_path)
    focal_length = exif_data.get("EXIF FocalLengthIn35mmFilm")
    f_number = exif_data.get("EXIF FNumber")

    # 尺寸
    margin_left = int(0.02 * image.width)  # 左右边距
    margin_top = int(0.01 * image.height)  # 上下边距
    banner_height = int(0.08 * image.height)
    main_sub_gap = int(image.height * 0.005)
    anchor = (margin_left, image.height + margin_top)
    banner_start_y = image.height + margin_top

    # 颜色
    border_color = (255, 255, 255)  # 设置边框颜色为白色
    text_color = {"main": (0, 0, 0), "sub": (100, 100, 100)}  # 主字体是黑色

    # 字体
    text_font = {
        "main": ImageFont.truetype(FONT_NAME, int(image.height * 0.03)),
        "sub": ImageFont.truetype(FONT_NAME, int(image.height * 0.02)),
    }

    new_image = Image.new(
        "RGB", (image.width, image.height + banner_height), border_color
    )
    new_image.paste(image, (0, 0))

    new_image_draw = ImageDraw.Draw(new_image)

    if focal_length is not None:
        iso_aperture_text = f"{focal_length}mm f/{f_number} {shutter_speed}s ISO{iso}"
        # 先把文本框的位置都写好
        _iso_text_bbox = new_image_draw.textbbox(
            xy=(0, 0), text=iso_aperture_text, font=text_font["main"], language="en"
        )
        # iso/fnumber text
        _iso_text_xy = (image.width - margin_left - _iso_text_bbox[2], anchor[1])
        new_image_draw.text(
            _iso_text_xy,
            iso_aperture_text,
            fill=text_color["main"],
            font=text_font["main"],
        )
        # 拍摄时间
        new_image_draw.text(
            (_iso_text_xy[0] + 10, anchor[1] + _iso_text_bbox[3] + 10),
            f"{capture_date}",
            fill=text_color["sub"],
            font=text_font["sub"],
        )
        capture_date_box = new_image_draw.textbbox(
            xy=(0, 0), text=f"{capture_date}", font=text_font["sub"], language="en"
        )
        if film_mode is not None:
            # draw filmmode logo
            logger.debug(banner_height)
            _filmmode_img = Image.open(
                os.path.join(
                    script_dir, f"../../assets/fujifilmsimulations/{film_mode}.jpg"
                )
            )
            _fimmode_img_resized = _resize_image(
                _filmmode_img, height=int(banner_height - 2 * margin_top)
            )
            new_image.paste(
                _fimmode_img_resized,
                (_iso_text_xy[0] - _filmmode_img.width, image.height + margin_top),
            )

    if add_camera_logo:
        if camera_make is None:
            logger.warning("camera make is missing in exif.")
            new_image.save(output_path, "JPEG", quality=95)
            return
        logo_filepath = Path(f"{script_dir}/../../assets/cameralogos/")
        logger.debug(f"logo dir: {logo_filepath}")
        if not Path.exists(logo_filepath):
            if Path.exists(Path(camera_logo_dir)):
                camero_logo_jpg = os.path.join(
                    camera_logo_dir, f"{camera_make.lower()}.jpg"
                )
            else:
                logger.warning(
                    "add_camera_logo is True, but did'nt find valid logo jpg file."
                )
                new_image.save(output_path, "JPEG", quality=95)
                return
        else:
            camero_logo_jpg = os.path.join(
                camera_logo_dir, f"{camera_make.lower()}.jpg"
            )

        logger.info(f"using camera maker logo: {camero_logo_jpg}")
        draw_camera_logo = Image.open(camero_logo_jpg)

        _logo_new_height = capture_date_box[3] + _iso_text_bbox[3]
        _logo_new_width = int(
            _logo_new_height * draw_camera_logo.width / draw_camera_logo.height
        )
        draw_camera_logo_resized = _resize_image(
            draw_camera_logo, height=_logo_new_height
        )

        new_image.paste(draw_camera_logo_resized, (anchor[0], banner_start_y))
        # write model text
        make_model_text = f"{camera_model}"
        new_image_draw.text(
            (anchor[0] + draw_camera_logo_resized.width + 10, banner_start_y),
            make_model_text,
            fill=text_color["main"],
            font=text_font["main"],
            language="en",
        )
        make_model_xy = new_image_draw.textbbox(
            xy=(0, 0), text=make_model_text, font=text_font["main"], language="en"
        )
        if add_lens:
            _lens_text_xy_coor = (
                anchor[0] + draw_camera_logo_resized.width + 10,
                banner_start_y + make_model_xy[3] + 5,
            )
            new_image_draw.text(
                _lens_text_xy_coor,
                f"{lens}",
                fill=text_color["sub"],
                font=text_font["sub"],
                language="en",
            )

    new_image.save(output_path, "JPEG", quality=95)
    return
