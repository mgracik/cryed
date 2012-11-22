from distutils.core import setup

setup(name='cryed',
      version='1.0',
      description='CryptoEditor',
      author='Martin Gracik',
      author_email='martin@gracik.me',
      url='http://',
      download_url='http://',
      license='MIT',
      packages = ['cryed'],
      scripts = ['cryed/bin/ccat',
                 'cryed/bin/cedit',
                 'cryed/bin/ppgen']
      )
