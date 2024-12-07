from setuptools import setup, find_packages

setup(
    name="gitgen",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "gitgen = gitgen.cli:main",
        ],
    },
    description="A simple tool to generate git commits to boost GitHub activity",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mubashar Hussain",
    author_email="hello@mubashar.dev",
    url="https://github.com/mubashardev/gitgen",  # Replace with your GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)