from setuptools import setup, find_packages

setup(
    name="funnyapi",
    version="0.5.2",  # Увеличь версию
    description="A fun API for generating jokes and funny facts",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Ksusha",
    author_email="YlC9L@example.com",
    url="https://github.com/kseniaris/funnyapi",
    packages=find_packages(include=["funnyapi", "funnyapi.*"]),
    include_package_data=True,
    package_data={"": ["*.py"]}, 
    python_requires=">=3.6",
)
