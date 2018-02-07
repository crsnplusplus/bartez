from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='bartez',
      version='0.1',
      description='',
      long_description=readme(),
      classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='crossword generator',
      url='http://github.com/crsnplusplus/bartez',
      author='crsnplusplus',
      author_email='crsnplusplus@gmail.com',
      license='MIT',
      packages=['bartez'],
      install_requires=[
          'networkx',
          'community_detect',
          'matplotlib',
      ],
      test_suite='tests',
      entry_points={
          'main': ['bartez=bartez.main:main'],
      },
      include_package_data=True,
      zip_safe=False)
