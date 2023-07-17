imagebanner
===========

Description
-----------

Since Xiaomi launched `Xiaomi 12s
ultra <https://www.mi.com/global/product/xiaomi-12s-ultra/>`__, it has
been popular to add watermark to the photo, showing camera model, logo,
iso and other parameters. Many third party apps, such as
`Liit <https://apps.apple.com/us/app/liit-photo-editor/id1547215938>`__
also provide this functionaliy.

This repo is aimed at fuji cameras, with film simulation info on the watermark.

Requirements
------------

-  Pillow >= 10.0 (built with libraqm)
-  `exifread <https://pypi.org/project/ExifRead/>`__ >= 3.0.0


Examples and Usage
--------

.. image:: https://github.com/dofine/image-banner/blob/39f4caa9c95d3a9347c8dffc3158f396d327dfc5/tests/test_result.jpg?raw=true
  :alt: Test result.

To use the

.. code-block:: bash

    imagebanner  -i tests/test.jpg -o test_result.jpg --logo-dir assets/cameralogos


Todo
----

-  ☐ Add support for iPhone, as I don’t have any other camera models.
-  ☒ Add support for fuji film simulation exif.
-  ☐ https://github.com/dofine/py-jpg-banner/issues/1 Portrait view.
-  ☐ Add option to copy original photo’s exif to the new edited output
   photo.



.. image:: https://img.shields.io/pypi/v/imagebanner.svg
    :target: https://pypi.python.org/pypi/imagebanner

.. image:: https://img.shields.io/travis/dofine/imagebanner.svg
    :target: https://travis-ci.com/dofine/imagebanner

.. image:: https://readthedocs.org/projects/imagebanner/badge/?version=latest
    :target: https://imagebanner.readthedocs.io/en/latest/?version=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/dofine/imagebanner/shield.svg
    :target: https://pyup.io/repos/github/dofine/imagebanner/
    :alt: Updates
