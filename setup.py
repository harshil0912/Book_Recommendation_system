## Creating proper project setup
## Creating local package



from setuptools import find_packages, setup

setup(
    name="books_recommender",
    version="0.0.1",
    author="Harshil",
    packages=find_packages()
)