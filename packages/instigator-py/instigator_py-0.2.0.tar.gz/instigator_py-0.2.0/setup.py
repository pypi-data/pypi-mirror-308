from setuptools import setup, find_packages

setup(
    name="instigator_py",
    version="0.2.0",  # Manually specify the version
    description="CLI tool for creating boilerplate projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sachin",
    author_email="schnaror@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "instigator_py=instigator_py.cli:main",
        ],
    },
)
