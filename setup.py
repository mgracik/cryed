from distutils.core import setup

setup(name='cryed',
      version='1.0',
      description='CryptoEditor',
      author='Martin Gracik',
      author_email='martin@gracik.me',
      url='http://',
      download_url='http://',
      license='MIT',
      package_dir = {'': 'src'},
      packages = ['cryed'],
      scripts = ['src/bin/ccat',
                 'src/bin/cedit',
                 'src/bin/ppgen']
      )
