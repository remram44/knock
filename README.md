Knock: Network Openness ChecKer

# Description

Knock is a simple tool that tests if ports are available between two machines.
Simply put Knock on each side and run it on the local machine -- it will spawn
its server process on the other side via SSH.

Knock is capable of testing remote ports from the local side but also local
ports from the remote side; simply prefix the port or port range with a '-'.

# Example

For example, to test that ports 10042-10044 and port 6667 on the remote host
are accessible from the local machine, and that ports 4500-4502 on the local
host are available from the remote machine, run:

    python knock 10042-10044 6667 -4500-4502 user@example.org python /opt/knock

It will print out the results on the console:

<pre>
Results for ports scanned on the remote machine:
Port        Status
10042       open
10043       close
10044       open
6667        remote skipped
--------------------
Total: 2 open, 1 closed

Results for ports scanned on the local machine:
Port        Status
4500        open
4501        open
4502        open
--------------------
Total: 3 open, 0 closed
</pre>

The messages "remote skipped" or "local error" indicate that a port wasn't
tested because it couldn't be grapped with bind(). This can happen if the port
is already in use or if the program wasn't allowed to grab it (on most unixes,
port numbers below 1024 are only available to root).
