from setuptools import find_packages, setup

print("PACKAGES!!!",find_packages())

setup(name='thorpy',
      version='1.5.6a1',
      description='pygame GUI library',
      author='Yann Thorimbert',
      author_email='yann.thorimbert@gmail.com',
      url='http://www.thorpy.org/',
      keywords=['pygame','gui','menus','buttons', 'widgets'],
      packages=find_packages(),
      include_package_data=True,
      license='MIT')
