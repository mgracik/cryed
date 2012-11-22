from distutils.core import setup

version = __import__('cryed').__version__

setup(name='cryed',
      version=version,
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
