from setuptools import setup, find_packages

setup(name='wrapper_typeform',
      version='0.2',
      packages=find_packages(),
      description=' Convert Data from Typeform API to two lists (questions and answers) written in Python',
      url='https://github.com/Hippo26/wrapper_typeform-python',
      author='Hippolyte Hazard, Artémis Llamosi',
      author_email='hippolyte.hazard@gmail.com',
      license='GPL',
      install_requires=[
          'requests', 'pandas','uuid'
      ],
      zip_safe=False)
