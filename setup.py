from setuptools import setup

setup(name='deaglequote',
      version='0.1',
      description='Phone Wallpaper Quote Generator',
      url='http://github.com/bryandeagle/quote',
      author='Bryan Deagle',
      author_email='bryan@dea.gl',
      license='MIT',
      packages=['deaglequote'],
      install_requires=[
          'feedparser',
          'Pillow'],
      zip_safe=False)
