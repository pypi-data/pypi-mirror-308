from setuptools import setup, find_packages

setup(
    name="funnyapi",
    version="0.3.1",
    description="A fun API for generating jokes and funny facts",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Ksusha",
    author_email="YlC9L@example.com",
    url="https://github.com/kseniaris/funnyapi",
    packages=find_packages(include=["funnyapi", "funnyapi.*"]),
    include_package_data=True,
    python_requires=">=3.6",
)
