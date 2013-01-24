import gettext
import itertools
import locale
import os
import re
import sys


class ConfigurationError(Exception):
    pass

def run():
    # python knock 22 2000-2020 ssh remram@example.org /opt/stuff/knock

    # Parse the command line
    port_spec = re.compile(r'^([0-9]+)(?:-([0-9]+))?$')
    ports = []
    ssh_cmd = None
    for i in xrange(1, len(sys.argv)):
        arg = sys.argv[i]

        # Options
        if arg == '--':
            ssh_cmd = sys.argv[i+1:]
            break
        elif arg == '-h':
            usage(sys.stdout)
            sys.exit(0)

        # Try to match a port spec
        m = port_spec.match(arg)
        if m is None:
            # Not ports: assume beginning of ssh command
            ssh_cmd = sys.argv[i:]
            break
        else:
            first, last = m.groups()
            if last is None:
                last = first
            elif last < first:
                raise ConfigurationError(_(u"Port sequence goes backwards: "
                                           "{0}-{1}").format(first, last))
            try:
                first, last = int(first), int(last)
            except ValueError:
                raise ConfigurationError(_(u"Port spec couldn't be parsed"))
            ports.append(xrange(first, last + 1))

    # Turn the list of specs into a single iterable
    ports = itertools.chain.from_iterable(ports)

    if ssh_cmd is None:
        raise ConfigurationError(_(u"ssh command was not specified"))

    # TODO : run
    for p in ports:
        print p


def usage(out):
    out.write(_(u"knock [port] [port-port] [port] [...] ssh [...]\n"
                "Tests that the given ports on the remote side are accessible "
                "from our side.\n"))


def main():
    app_dir = os.path.dirname(os.path.realpath(__file__))

    # Setup gettext
    locale.setlocale(locale.LC_ALL, '')
    if sys.platform.startswith('win'):
        if os.getenv('LANG') is None:
            lang, enc = locale.getlocale()
            os.environ['LANG'] = lang
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

    try:
        run()
        sys.exit(0)
    except ConfigurationError, e:
        sys.stderr.write(_(u"Error: ") + e.message + "\n")
        usage(sys.stderr)
        sys.exit(1)
