from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='lsalib',
      version='0.10.3',
      description='Basic Latent Semantic Analysis library',
      url='https://github.com/CrakeNotSnowman/LatentSemanticAnalysis/tree/master/lsalib',
      author='Keith Murray',
      author_email='kmurrayis@gmail.com',
      license='MIT',
      packages=['lsalib'],
      install_requires=[
          'numpy',
	  'scipy',
          'sklearn',
      ],
      zip_safe=False)
