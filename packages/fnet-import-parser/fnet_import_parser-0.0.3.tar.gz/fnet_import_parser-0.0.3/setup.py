from setuptools import setup

setup(
    name="fnet-import-parser",  # The name of your package (required)
    version="0.0.3",  # Package version (required)
    packages=["cli", "src"],  # The packages to include in the distribution (required)
    package_dir={"src": "src", "cli": "cli"},  # Map package names to directories (required)
    entry_points={
        "console_scripts": [
            "fnet-import-parser=cli.index:main",  # Command-line tool definition (required for CLI functionality)
        ],
    },
    python_requires=">=3.9",  # Minimum required Python version (required)
    install_requires=[
        "stdlib-list",  # Required dependency
        "pyyaml",
    ],
    # Optional metadata, to be added later:
    # author="justai.pro",  # Your name (optional)
    # author_email="devops@justai.pro",  # Your email address (optional)
    description="A Python dependency analyzer for import parsing and metadata extraction.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/fnetai/py-import-parser",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent",
    ],
    # include_package_data=True,  # Include non-Python files (e.g., YAML files) (optional)
)