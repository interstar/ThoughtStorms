from setuptools import setup

setup(name='thoughtstorms',
      version='0.0.3',
      description='Components from Project ThoughtStorms (ThoughtStorms wiki and associated software)',
      long_description="""Project ThoughtStorms is the software behind ThoughtStorms Wiki and some associated other programs.
      
We're now breaking these components out into a separate library that is available on PyPI and can be installed with pip.
      
      """,
      long_description_content_type='text/markdown',
      url='https://github.com/interstar/ThoughtStorms',
      author='Phil Jones',
      author_email='interstar@gmail.com',
      license='MIT',
      packages=['thoughtstorms'],
      install_requires=["Markdown","PyYAML>=3.12"],
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers'],
      zip_safe=False)
