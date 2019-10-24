.. -*-restructuredtext-*-

freshpaper
==========

.. image:: https://img.shields.io/pypi/v/freshpaper.svg
    :target: https://pypi.python.org/pypi/freshpaper
    :alt: PyPi version

.. image:: https://app.fossa.io/api/projects/git%2Bgithub.com%2Fguptarohit%2Ffreshpaper.svg?type=shield
    :target: https://app.fossa.io/projects/git%2Bgithub.com%2Fguptarohit%2Ffreshpaper?ref=badge_shield
    :alt: FOSSA Status

.. image:: https://img.shields.io/pypi/l/freshpaper.svg
    :target: https://github.com/guptarohit/freshpaper/blob/master/LICENSE
    :alt: License

.. image:: https://pepy.tech/badge/freshpaper
    :target: https://pepy.tech/project/freshpaper
    :alt: Downloads

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Code style: black

freshpaper automatically sets `Bing <https://www.bing.com/>`_ photo of the day or `NASA-APOD <https://apod.nasa.gov/apod/astropix.html/>`_ or `Random Unsplash photo <https://source.unsplash.com>`_ as your desktop's wallpaper. Available for Windows, macOS & Linux.


Installation
------------

::

    $ pip install freshpaper

Update to latest release:

::

    $ pip install -U freshpaper


Usage
------

To update the wallpaper simply run:

::

    $ freshpaper

The default source of wallpaper is ``bing``. Available sources: ``bing``, ``nasa``, ``unsplash_random``.

To change the source of the wallpaper, run:

::

    $ freshpaper --source <source_name>
    
Help command of cli utility:

::

    $ freshpaper --help
    Usage: freshpaper [OPTIONS] COMMAND [ARGS]...

    Options:
      --source [bing|nasa|unsplash_random]  Source for setting the wallpaper.
      --help           Show this message and exit.

Contributing
------------

Feel free to make a pull request! :octocat:

If you found this useful, I'd appreciate your consideration in the below. ✨🍰

.. image:: https://user-images.githubusercontent.com/7895001/52529389-e2da5280-2d16-11e9-924c-4fe3f309c780.png
    :target: https://www.buymeacoffee.com/rohitgupta
    :alt: Buy Me A Coffee

.. image:: https://user-images.githubusercontent.com/7895001/52529390-e8379d00-2d16-11e9-913b-4d09db90403f.png
    :target: https://www.patreon.com/bePatron?u=14009502
    :alt: Become a Patron!


License
-------

.. image:: https://app.fossa.io/api/projects/git%2Bgithub.com%2Fguptarohit%2Ffreshpaper.svg?type=large
    :target: https://app.fossa.io/projects/git%2Bgithub.com%2Fguptarohit%2Ffreshpaper?ref=badge_large
    :alt: FOSSA Status
