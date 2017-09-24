from setuptools import setup, Command

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='Top 10 Hacker News',
      version='0.1',
      description=' Unbabel Fullstack coding challenge',
      author='Hugo Marques',
      author_email='o.endereco.do.hugo@gmail.com',
      url='https://github.com/fofinho666/fullstack-coding-challenge',
      install_requires=requirements
      )
