from setuptools import setup, find_packages

setup(name='reactiv',
      version='1.0.3',
      description='Rapid and EAsy Change detection in radar TIme-series by Variation coefficient',
      long_description=open('README.md').read(),
      url='https://github.terradue.com/reactiv.git',
      author='Elise Colin Koeniguer et al',
      license='GNU General Public License v3.0',
      packages=find_packages(),
      include_package_data=True,	
      zip_safe=False)

