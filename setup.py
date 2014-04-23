try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


description = """
Knock: Network Openness ChecKer

Knock is a small tool that tests if ports are available between two machines.
Simply put Knock on each side and run it on the local machine -- it spawns its
"server" process on the other side via SSH, checks the requested ports, and
displays the results in the console.

Knock is capable of testing remote ports from the local side but also local
ports from the remote side; simply prefix the port or port range with a '-'.
"""
setup(name='knock',
      version='0.1',
      packages=['knock'],
      entry_points={
          'console_scripts': [
              'knock = knock.main:main']},
      description='Knock: Network Openness ChecKer',
      author="Remi Rampin",
      author_email='remirampin@gmail.com',
      url='http://github.com/remram44/knock',
      long_description=description,
      license='Apache License 2.0',
      keywords=['port', 'checker', 'network', 'map', 'mapper', 'openness',
                'test', 'connection'],
      classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        'Programming Language :: Python'])
