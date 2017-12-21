from setuptools import setup, find_packages

setup(name='wrapper_typeform',
      version='0.1',
      packages=find_packages(),
      description=' Convert Data from Typeform API to two lists (questions and answers) written in Python',
      url='https://github.com/Hippo26/wrapper_typeform-python',
      author='Hippolyte Hazard',
      author_email='hippolyte.hazard@gmail.com',
      license='GPL',
      packages=['wrapper_typeform'],
      install_requires=[
          'requests', 'pandas','uuid','time'
      ],
      zip_safe=False)
