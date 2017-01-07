from setuptools import find_packages, setup

setup(name='thorpy',
      packages = ['thorpy'],
      version='1.5.3',
      description='pygame GUI library',
      author='Yann Thorimbert',
      author_email='yann.thorimbert@gmail.com',
      url='http://www.thorpy.org/',
      download_url='https://github.com/YannThorimbert/Thorpy/tarball/1.5.3',
      keywords=['pygame','gui','menus','buttons'],
      packages=find_packages(),
      include_package_data=True,
      license='MIT')
