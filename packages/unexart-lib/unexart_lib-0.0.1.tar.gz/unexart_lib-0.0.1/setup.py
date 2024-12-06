from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r', encoding='utf-8') as f:
    return f.read()

setup(
  name='unexart_lib',
  version='0.0.1',
  author='unexart',
  author_email='unexart4132@gmail.com',
  description='This is the simplest module created for educational purposes.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/UnexarT/unexart_lib',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='Fibonacci bubblesort calculator',
  project_urls={
    'GitHub': 'https://github.com/UnexarT/unexart_lib'
  },
  python_requires='>=3.6'
)