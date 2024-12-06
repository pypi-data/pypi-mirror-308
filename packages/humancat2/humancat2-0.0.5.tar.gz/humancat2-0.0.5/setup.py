from setuptools import setup, find_packages

setup(
    name='humancat2',
    version='0.0.5',
    description='GitHub Action Build Test Sample',
    author='jaeyun',
    author_email='imjyp2727@gmail.com',
    url='https://github.com/ParkJaeyun94/github-action-course',
    install_requires=[],
    packages=find_packages(exclude=[]),
    keywords=['sample', 'cat', 'human', 'humancat'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False
)
