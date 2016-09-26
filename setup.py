from distutils.core import setup

setup(
    name='pyReframe',
    version='0.1',
    packages=['', ''],
    package_dir={'': 'pyReframe'},
    download_url = 'https://github.com/alchayward/pyReframe/tarball/0.1'
    url='https://github.com/alchayward/pyReframe.git',
    license='MIT',
    author='Andrew L. C. Hayward',
    author_email='alc.hayward@gmail.com',
    description='a port of clojures reframe to python', requires=['pyrsistent', 'rx'])
