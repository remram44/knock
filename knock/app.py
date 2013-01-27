import os
import re
import sys

from knock.remote import Remote
from knock.knocker import PortKnocker
from knock.ports import PortList
import subprocess


class ConfigurationError(Exception):
    pass


_CMD_SWITCH_SERVER = '--_internal_-server-mode'


def run():
    argc = len(sys.argv)

    if argc > 1 and sys.argv[1] == _CMD_SWITCH_SERVER:
        if argc > 2 and sys.argv[2] == '-l':
            assert argc > 3
            rev_host = sys.argv[3]
            i = 4
        else:
            try:
                rev_host = os.environ['SSH_CLIENT']
                rev_host = rev_host.split(' ')[0]
            except KeyError:
                raise ConfigurationError(_(
                        u"Coudldn't guess local hostname from SSH environment "
                        "-- please use -l"))
            i = 2
        rports = PortList()
        while i < argc:
            rports.add(sys.argv[i])
            i += 1
        remote = Remote(sys.stdin, sys.stdout)
        runner = PortKnocker(remote, rev_host)
        runner.run(False, rports)
        remote.close()
        sys.exit(0)

    # Parse the command line
    lports = PortList()
    rports = PortList()
    ssh_args = None
    ssh_prog = None
    host = None
    rev_host = None
    i = 1
    while i < argc:
        arg = sys.argv[i]

        # Options
        if arg == '--':
            ssh_args = sys.argv[i+1:]
            break
        elif arg == '-h':
            usage(sys.stdout)
            sys.exit(0)
        elif arg == '-s':
            if i + 1 >= argc:
                raise ConfigurationError(_(u"Option -s requires an argument"))
            elif ssh_prog is not None:
                raise ConfigurationError(_(u"Option -s was specified more "
                                           "than once"))
            ssh_prog = sys.argv[i + 1]
            i += 1
        elif arg == '-r':
            if i + 1 >= argc:
                raise ConfigurationError(_(u"Option -r requires an argument"))
            elif host is not None:
                raise ConfigurationError(_(u"Option -r was specified more "
                                           "than once"))
            host = sys.argv[i + 1]
            i += 1
        elif arg == '-l':
            if i + 1 >= argc:
                raise ConfigurationError(_(u"Option -l requires an argument"))
            elif host is not None:
                raise ConfigurationError(_(u"Option -l was specified more "
                                           "than once"))
            rev_host = sys.argv[i + 1]
            i += 1
        else:
            if arg and arg[0] == '-':
                arg = arg[1:]
                port_list = lports
            else:
                port_list = rports

            if not port_list.add(arg):
                # Not ports: assume beginning of remaining parameters
                ssh_args = sys.argv[i:]
                break
        i += 1

    if not ssh_args:
        raise ConfigurationError(_(u"ssh arguments were not specified"))

    if not ssh_prog:
        ssh_prog = 'ssh'

    if not host:
        m = re.match(r'^(?:[^@: ]+@)?([^@: ]+)$', ssh_args[0])
        if m is None:
            raise ConfigurationError(_(u"Couldn't guess remote hostname from "
                                       "SSH command -- please use -r"))
        host = m.group(1)

    # Run the command on the other side
    try:
        ssh_cmd = [ssh_prog] + ssh_args + [_CMD_SWITCH_SERVER]
        if rev_host:
            ssh_cmd += ['-l', rev_host]
        ssh_cmd += rports.to_arglist()
        proc = subprocess.Popen(ssh_cmd,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
    except OSError:
        raise ConfigurationError(_(u"Couldn't start the ssh process"))

    # Create a communication wrapper
    remote = Remote(proc.stdout, proc.stdin)

    # Run
    runner = PortKnocker(remote, host)
    runner.run(True, lports)
    remote.close()
    sys.exit(0)


def usage(out):
    out.write(_(u"knock [options] [ports] [...] [user@host] [path/to/knock]\n"
                "\n"
                "  Tests for port accessibility between here and the remote "
                "machine.\n"
                "\n"
                "  Ports can have the format '42' or '41-47'; a '-' prefix "
                "means to test the\nlocal port from the remote side.\n"
                "\n"
                "Recognized options:\n"
                "  -h\n    Prints this help and exits\n"
                "  -s <ssh_cmd>\n    Sets the SSH binary (default: 'ssh')\n"
                "  -r <hostname>\n    Sets the hostname or address of the "
                "remote machine that we'll use to test\n    remote ports\n"
                "  -l <hostname>\n    Sets the hostname or address of this "
                "machine that will be used by the\n    remote to test local "
                "ports\n"))


def main():
    try:
        run()
    except ConfigurationError, e:
        sys.stderr.write(_(u"Error: ") + e.message + u"\n")
        usage(sys.stderr)
        sys.exit(1)
