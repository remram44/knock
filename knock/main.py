import gettext
import locale
import sys
import os


def setup():
    app_dir = os.path.dirname(os.path.realpath(__file__))

    # Setup gettext
    locale.setlocale(locale.LC_ALL, '')
    gettext.install('knock', os.path.join(app_dir, 'locales'), True)

    # Setup the Python path
    try:
        import knock.main
    except ImportError:
        sys.path.insert(0, os.path.realpath(os.path.join(app_dir, '..')))
        try:
            import knock.main
        except ImportError:
            sys.stderr.write(_(u"Couldn't setup the Python path\n"))
            sys.exit(2)


def main():
    setup()

    import knock.app
    knock.app.main()
