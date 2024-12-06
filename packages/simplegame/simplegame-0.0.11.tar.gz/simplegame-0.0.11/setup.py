from setuptools import setup

setup(
    name='simplegame',
    version='0.0.11',
    description='Package for creating simple games',
    url='https://github.com/szotms/simplegame',
    author='Michal Szot',
    author_email='szot.net@gmail.com',
    license='MIT',
    packages=['simplegame'],
    zip_safe=False,
    install_requires=[
       'Pillow>=11.0.0',
       'pygame>=2.6.1'
    ]
)