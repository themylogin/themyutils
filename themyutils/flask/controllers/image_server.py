# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from flask import request
import hashlib
from mimetypes import guess_type
import os
from PIL import Image
from PIL.ExifTags import TAGS
try:
    from redlock import RedLockFactory
except ImportError:
    pass
import requests
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.routing import Rule, Submount
from werkzeug.wrappers import BaseResponse
from werkzeug.wsgi import wrap_file

__all__ = [b"ImageServer"]

INTERNET_IMAGE_HEADER = "X-themyutils-internet-image-request"


def image_handler(handler):
    def request_handler(self, **kwargs):
        if INTERNET_IMAGE_HEADER in request.headers:
            raise BadRequest()

        filename = kwargs["filename"].encode("utf-8")
        filename_append = (b"?" + request.query_string if request.query_string else b"")
        if len(filename + filename_append) > 255:
            filename_append = b"$%s" % hashlib.sha256(filename_append).hexdigest()
        path = os.path.join(self.path, filename + filename_append)

        if self.allow_internet:
            if not os.path.exists(path) and b"/" in filename:
                with self.lock(path):
                    if not os.path.exists(path):
                        path_incomplete = path + b".download"
                        [proto, etc] = filename.split(b"/", 1)
                        url = proto + b"://" + etc + b"?" + request.query_string

                        try:
                            r = requests.get(url, headers={INTERNET_IMAGE_HEADER: "true"}, stream=True)
                            try:
                                os.makedirs(os.path.dirname(path))
                            except OSError:
                                pass
                            with open(path_incomplete, "w") as f:
                                for chunk in r.iter_content(1024):
                                    f.write(chunk)
                        except:
                            if os.path.exists(path_incomplete):
                                os.unlink(path)
                            raise NotFound()
                        else:
                            os.rename(path_incomplete, path)

        if not os.path.exists(path):
            raise NotFound()

        processed_path = os.path.join(self.path, request.path[len(self.url_path) + 1:].encode("utf-8") + filename_append)
        if not os.path.exists(processed_path):
            with self.lock(processed_path):
                if not os.path.exists(processed_path):
                    im = Image.open(path)
                    if hasattr(im, "_getexif"):
                        try:
                            exif = im._getexif()
                        except:
                            exif = None

                        if exif:
                            metadata = {TAGS.get(k): v for k, v in exif.iteritems()}
                            if "Orientation" in metadata:
                                orientation = metadata["Orientation"]
                                if orientation == 1:
                                    # Nothing
                                    im = im.copy()
                                elif orientation == 2:
                                    # Vertical Mirror
                                    im = im.transpose(Image.FLIP_LEFT_RIGHT)
                                elif orientation == 3:
                                    # Rotation 180°
                                    im = im.transpose(Image.ROTATE_180)
                                elif orientation == 4:
                                    # Horizontal Mirror
                                    im = im.transpose(Image.FLIP_TOP_BOTTOM)
                                elif orientation == 5:
                                    # Horizontal Mirror + Rotation 90° CCW
                                    im = im.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_90)
                                elif orientation == 6:
                                    # Rotation 270°
                                    im = im.transpose(Image.ROTATE_270)
                                elif orientation == 7:
                                    # Horizontal Mirror + Rotation 270°
                                    im = im.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
                                elif orientation == 8:
                                    # Rotation 90°
                                    im = im.transpose(Image.ROTATE_90)

                    im_processed = handler(self, im, **kwargs)

                    try:
                        os.makedirs(os.path.dirname(processed_path))
                    except OSError:
                        pass
                    im_processed.save(processed_path, format=im.format, quality=85)

        if not os.path.isfile(processed_path):
            raise NotFound()

        return BaseResponse(wrap_file(request.environ, open(processed_path, "r")),
                            mimetype=guess_type(processed_path)[0])

    return request_handler


class ImageServer(object):
    def __init__(self, app, path, url_path=None, allow_internet=False, redis_lock=None):
        self.app = app
        self.path = path.encode("utf-8")
        self.lock_factory = RedLockFactory(redis_lock) if redis_lock else None

        if url_path is None:
            if self.path.startswith(app.static_folder):
                self.url_path = self.path[len(os.path.normpath(os.path.join(app.static_folder, os.path.pardir))):]
            else:
                raise ValueError("url_path can't be None when path is not within app.static_folder")
        else:
            self.url_path = url_path

        self.allow_internet = allow_internet

        app.url_map.add(Submount(self.url_path, [
            Rule("/<int(max=1920):width>/<path:filename>",                                      endpoint="fit_image_%s" % path),
            Rule("/<int(max=1920):width>/_/<path:filename>",                                    endpoint="fit_image_%s" % path),
            Rule("/_/<int(max=1920):height>/<path:filename>",                                   endpoint="fit_image_%s" % path),
            Rule("/<int(max=1920):width>/<int(max=1920):height>/<path:filename>",               endpoint="fit_image_%s" % path),
            Rule("/fit/<int(max=1920):width>/<int(max=1920):height>/<path:filename>",           endpoint="fit_image_%s" % path),

            Rule("/min-size/<int(max=1920):size>/<path:filename>",                              endpoint="min_size_image_%s" % path),

            Rule("/crop/<int(max=1920):width>/<int(max=1920):height>/<path:filename>",          endpoint="crop_image_%s" % path),
            Rule("/crop/<any(   'top-left',  'top',      'top-right', "
                            "       'left', 'center',        'right', "
                            "'bottom-left', 'bottom', 'bottom-right'):gravity>"
                 "/<int(max=1920):width>/<int(max=1920):height>/<path:filename>",               endpoint="crop_image_%s" % path),

            Rule("/pad/<int(max=1920):width>/<int(max=1920):height>/<path:filename>",           endpoint="pad_image_%s" % path),
            Rule("/pad/<color>/<int(max=1920):width>/<int(max=1920):height>/<path:filename>",   endpoint="pad_image_%s" % path),

            Rule("/stretch/<int(max=1920):width>/<path:filename>",                              endpoint="stretch_image_%s" % path),
            Rule("/stretch/<int(max=1920):width>/_/<path:filename>",                            endpoint="stretch_image_%s" % path),
            Rule("/stretch/_/<int(max=1920):height>/<path:filename>",                           endpoint="stretch_image_%s" % path),
            Rule("/stretch/<int(max=1920):width>/<int(max=1920):height>/<path:filename>",       endpoint="stretch_image_%s" % path),

            # will just download from internet if allow_internet is enabled
            Rule("/<path:filename>",                                                            endpoint="pass_image_%s" % path),
        ]))
        for endpoint in ["fit_image", "min_size_image", "crop_image", "pad_image", "stretch_image", "pass_image"]:
            app.view_functions["%s_%s" % (endpoint, path)] = getattr(self, "execute_%s" % endpoint)

    @image_handler
    def execute_fit_image(self, im, **kwargs):
        image_width = float(im.size[0])
        image_height = float(im.size[1])

        if "width" in kwargs and "height" in kwargs:
            requested_width = float(kwargs["width"])
            requested_height = float(kwargs["height"])

            if image_width / image_height > requested_width / requested_height:
                new_width = requested_width
                new_height = new_width / image_width * image_height
            else:
                new_height = requested_height
                new_width = new_height / image_height * image_width
        elif "width" in kwargs:
            requested_width = float(kwargs["width"])

            new_width = requested_width
            new_height = new_width / image_width * image_height
        elif "height" in kwargs:
            requested_height = float(kwargs["height"])

            new_height = requested_height
            new_width = new_height / image_height * image_width
        else:
            raise BadRequest()

        if new_width > image_width or new_height > image_height:
            new_width = image_width
            new_height = image_height

        return im.resize((int(new_width), int(new_height)), Image.ANTIALIAS)

    @image_handler
    def execute_min_size_image(self, im, **kwargs):
        image_width = float(im.size[0])
        image_height = float(im.size[1])

        requested_size = float(kwargs["size"])

        if image_width < image_height:
            new_width = requested_size
            new_height = new_width / image_width * image_height
        else:
            new_height = requested_size
            new_width = new_height / image_height * image_width

        if new_width > image_width or new_height > image_height:
            new_width = image_width
            new_height = image_height

        return im.resize((int(new_width), int(new_height)), Image.ANTIALIAS)

    @image_handler
    def execute_crop_image(self, im, **kwargs):
        image_width = float(im.size[0])
        image_height = float(im.size[1])

        requested_width = float(kwargs["width"])
        requested_height = float(kwargs["height"])

        if image_width / image_height > requested_width / requested_height:
            new_uncropped_height = requested_height
            new_uncropped_width = new_uncropped_height / image_height * image_width
        else:
            new_uncropped_width = requested_width
            new_uncropped_height = new_uncropped_width / image_width * image_height
        im_uncropped = im.resize((int(new_uncropped_width), int(new_uncropped_height)), Image.ANTIALIAS)

        if "gravity" in kwargs:
            requested_gravity = kwargs["gravity"]
        else:
            requested_gravity = "center"

        if new_uncropped_width > requested_width:
            if "left" in requested_gravity:
                crop = (0, 0, requested_width, requested_height)
            elif "right" in requested_gravity:
                crop = (new_uncropped_width - requested_width, 0, new_uncropped_width, requested_height)
            else:
                crop = ((new_uncropped_width - requested_width) / 2.0, 0, (new_uncropped_width - requested_width) / 2.0 + requested_width, requested_height)
        elif new_uncropped_height > requested_height:
            if "top" in requested_gravity:
                crop = (0, 0, requested_width, requested_height)
            elif "bottom" in requested_gravity:
                crop = (0, new_uncropped_height - requested_height, requested_width, new_uncropped_height)
            else:
                crop = (0, (new_uncropped_height - requested_height) / 2.0, requested_width, (new_uncropped_height - requested_height) / 2.0 + requested_height)
        else:
            crop = (0, 0, requested_width, requested_height)

        return im_uncropped.crop((int(crop[0]), int(crop[1]), int(crop[2]), int(crop[3])))

    @image_handler
    def execute_pad_image(self, im, **kwargs):
        image_width = float(im.size[0])
        image_height = float(im.size[1])

        requested_width = float(kwargs["width"])
        requested_height = float(kwargs["height"])

        if image_width / image_height > requested_width / requested_height:
            new_width = requested_width
            new_height = new_width / image_width * image_height
        else:
            new_height = requested_height
            new_width = new_height / image_height * image_width

        if new_width > image_width or new_height > image_height:
            new_width = image_width
            new_height = image_height

        if "color" in kwargs:
            requested_color = kwargs["color"]
        else:
            requested_color = "black"

        try:
            im_with_fields = Image.new("RGBA", (int(requested_width), int(requested_height)), requested_color)
        except ValueError:
            raise BadRequest()
        im_with_fields.paste(im.resize((int(new_width), int(new_height)), Image.ANTIALIAS),
                             (int((requested_width - new_width) / 2.0), int((requested_height - new_height) / 2.0)))

        return im_with_fields

    @image_handler
    def execute_stretch_image(self, im, **kwargs):
        image_width = float(im.size[0])
        image_height = float(im.size[1])

        if "width" in kwargs and "height" in kwargs:
            new_width = float(kwargs["width"])
            new_height = float(kwargs["height"])
        elif "width" in kwargs:
            requested_width = float(kwargs["width"])

            new_width = requested_width
            new_height = new_width / image_width * image_height
        elif "height" in kwargs:
            requested_height = float(kwargs["height"])

            new_height = requested_height
            new_width = new_height / image_height * image_width
        else:
            raise BadRequest()

        return im.resize((int(new_width), int(new_height)), Image.ANTIALIAS)

    @image_handler
    def execute_pass_image(self, im, **kwargs):
        return im

    def lock(self, resource):
        return _ImageServerLock(self.lock_factory, resource)


class _ImageServerLock(object):
    def __init__(self, factory, resource):
        self.factory = factory
        self.resource = resource

        self.lock = None

    def __enter__(self):
        if self.factory:
            self.lock = self.factory.create_lock(self.resource, retry_times=50, retry_delay=200, ttl=10000)
            return self.lock.acquire()
        else:
            return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.lock:
            self.lock.release()
