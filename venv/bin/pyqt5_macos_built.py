#!/Users/janghanbin/PycharmProjects/ImageDownloader/venv/bin/python
'''
This script installs a prebuilt version of PyQt5 for Mac OS.
Remember that Qt5 has to be installed already in your system.

Extra info: https://bitbucket.org/pposca/pyqt5-macos-built
Issues:     https://bitbucket.org/pposca/pyqt5-macos-built/issues

Usage:
    pyqt5_macos_built.py install
    pyqt5_macos_built.py clean
    pyqt5_macos_built.py [-h | --help]

Options:
    -h --help           Shows this screen
    install             Installs PyQt5
    clean               Uninstalls PyQt5

'''
import os
import site
import re
import sys
from docopt import docopt

BIN_DIR = os.environ.get('VIRTUAL_ENV', '/usr/local')
SITE_DIR = site.getsitepackages()[0]
BIN_FILES = ['pylupdate5', 'pyrcc5', 'pyuic5', 'sip']
LIBS = ['sip.so']


def shorten(path):
    return re.sub('^' + os.getcwd() + '/', '', path)


def help_and_exit_if_no_args():
    if not sys.argv[1:]:
        print(__doc__.strip())
        exit()


def install(verbose=True):
    if verbose:
        print('Installing...')

    for bin_file in BIN_FILES:
        src = SITE_DIR + '/PyQt5/bin/' + bin_file
        dest = BIN_DIR + '/bin/' + bin_file
        os.symlink(src, dest)
        if verbose:
            print('{}: {} -> {}'.format(bin_file, shorten(dest), shorten(src)))

    for lib in LIBS:
        src = SITE_DIR + '/PyQt5/lib/' + lib
        dest = SITE_DIR + '/' + lib
        os.symlink(src, dest)
        if verbose:
            print('{}: {} -> {}'.format(lib, shorten(dest), shorten(src)))


def ensure_platform():
    pass


def check_install():
    print('\nChecking installation...')
    from PyQt5.QtCore import QT_VERSION_STR
    print('PyQt {} installed successfully!!!'.format(QT_VERSION_STR))


def remove_link(path, verbose=True):
    if os.path.islink(path):
        os.remove(path)
        if verbose:
            print('Removing {}'.format(path))


def clean(verbose=True):
    if verbose:
        print('Cleaning installation...')

    for bin_file in BIN_FILES:
        remove_link(BIN_DIR + '/bin/' + bin_file)

    for lib in LIBS:
        remove_link(SITE_DIR + '/' + lib)

    if verbose:
        print('Installation cleaned succesfully!!!')


if __name__ == '__main__':
    ensure_platform()
    help_and_exit_if_no_args()

    args = docopt(__doc__)
    if args['install']:
        install()
        check_install()

    if args['clean']:
        clean()
