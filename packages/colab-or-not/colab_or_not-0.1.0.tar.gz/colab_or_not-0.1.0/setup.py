#  Copyright (c) 2024 Higher Bar AI, PBC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from setuptools import setup, find_packages

with open('README.rst') as file:
    readme = file.read()


setup(
    name='colab-or-not',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.10',
    install_requires=[
        'requests~=2.32.3',
        'python-dotenv~=1.0.1',
        'ipython',
        'ipywidgets'
    ],
    package_data={
    },
    url='https://github.com/higherbar-ai/colab-or-not',
    project_urls={'Documentation': 'https://colab-or-not.readthedocs.io/'},
    license='Apache 2.0',
    author='Christopher Robert',
    author_email='crobert@higherbar.ai',
    description='A Python package to help make Jupyter notebooks runnable in Colab or local environments.',
    long_description=readme
)
