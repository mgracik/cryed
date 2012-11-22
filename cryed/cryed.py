# Copyright (c) 2009-2012 Martin Gracik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Author(s):    Martin Gracik <martin@gracik.me>
#

from __future__ import print_function

import contextlib
import getpass
import os
import shutil
import stat
import subprocess
import tempfile


@contextlib.contextmanager
def passfile(passphrase, filename):
    dir_path = os.path.dirname(filename) or os.getcwd()
    tpass_handle, tpass_path = tempfile.mkstemp(prefix='.pass-', dir=dir_path)
    os.close(tpass_handle)
    os.chmod(tpass_path, stat.S_IRUSR | stat.S_IWUSR)
    with open(tpass_path, 'w') as fileobj:
        fileobj.write(passphrase)
    try:
        yield tpass_path
    finally:
        os.unlink(tpass_path)


@contextlib.contextmanager
def cryptfile(filename):
    dir_path = os.path.dirname(filename) or os.getcwd()
    file_handle, file_path = tempfile.mkstemp(prefix='.%s-' % os.path.basename(filename), dir=dir_path)
    os.close(file_handle)
    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
    try:
        yield file_path
    finally:
        os.unlink(file_path)


class CryEd(object):

    PASSPHRASE_RETRIES = 3

    def __init__(self, cipher='aes-256-cbc'):
        self.cipher = '-%s' % cipher
        self.passphrase = None

    def set_passphrase(self):
        self.passphrase = getpass.getpass(prompt='Enter your passphrase: ')

    def verify_passphrase(self):
        assert self.passphrase
        passphrase = getpass.getpass(prompt='Enter your passphrase again: ')
        if passphrase != self.passphrase:
            self.passphrase = None

    def encrypt(self, source, target):
        assert self.passphrase
        with passfile(self.passphrase, target) as tpass_path:
            cmd = ['openssl', 'enc', '-e', self.cipher, '-a', '-in', source, '-out', target,
                   '-pass', 'file:%s' % tpass_path]
            try:
                subprocess.check_call(cmd)
            except subprocess.CalledProcessError as exc:
                msg = "Command '%s' returned non-zero exit status %d" % (' '.join(exc.cmd), exc.returncode)
                raise SystemExit(msg)

    def decrypt(self, source, target):
        assert self.passphrase
        with passfile(self.passphrase, source) as tpass_path:
            cmd = ['openssl', 'enc', '-d', self.cipher, '-a', '-in', source, '-out', target,
                   '-pass', 'file:%s' % tpass_path]
            try:
                subprocess.check_call(cmd)
            except subprocess.CalledProcessError as exc:
                msg = "Command '%s' returned non-zero exit status %d" % (' '.join(exc.cmd), exc.returncode)
                raise SystemExit(msg)

    def cat(self, filename):
        print("Decrypting '%s'" % filename)
        self.set_passphrase()
        with cryptfile(filename) as file_path:
            self.decrypt(source=filename, target=file_path)
            with open(file_path) as fileobj:
                print(''.join(fileobj), end='')

    def edit(self, filename, editor):
        with cryptfile(filename) as file_path:
            if os.path.isfile(filename):
                print("Decrypting '%s'" % filename)
                self.set_passphrase()
                self.decrypt(source=filename, target=file_path)

            # Run the editor.
            try:
                subprocess.check_call([editor, file_path])
            except subprocess.CalledProcessError as exc:
                msg = "Command '%s' returned non-zero exit status %d" % (' '.join(exc.cmd), exc.returncode)
                raise SystemExit(msg)

            print("Encrypting '%s'" % filename)
            if not self.passphrase:
                for _try in range(self.PASSPHRASE_RETRIES):
                    self.set_passphrase()
                    self.verify_passphrase()
                    if self.passphrase:
                        break
                else:
                    # Save the unencrypted file.
                    print('Passphrase not set')
                    save = raw_input('Save the unencrypted file? (yes/no) ')
                    if save.lower() in ('y', 'yes'):
                        shutil.copyfile(file_path, filename)
                    return

            self.encrypt(source=file_path, target=filename)
