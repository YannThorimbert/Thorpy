from setuptools import find_packages, setup

"""Upload on PyPi :
1. python setup.py bdist_wheel --universal

2. twine upload dist/*
"""

setup(name='thorpy',
      version='1.8',
      description='GUI library for pygame',
      long_description='GUI library for pygame',
      author='Yann Thorimbert',
      author_email='yann.thorimbert@gmail.com',
      url='http://www.thorpy.org/',
      keywords=['pygame', 'gui', 'menus', 'buttons', 'widgets'],
      packages=find_packages(),
      include_package_data=True,
      license='MIT')
