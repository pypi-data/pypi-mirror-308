from setuptools import setup, find_packages

setup(
    name="fnet_import_parser",
    version="0.1.4",
    packages=find_packages(),
    
    package_dir={"": "."},
    entry_points={
        "console_scripts": [
            "fnet_import_parser=fnet_import_parser.cli.index:main",
        ],
    },
    python_requires=">=3.9",
    install_requires=[
      
      "stdlib-list" ,
      
      "pyyaml" 
      
    ],
    # Optional metadata, to be added later:
    # author="justai.pro",  # Your name (optional)
    # author_email="devops@justai.pro",  # Your email address (optional)
    # description="A Python dependency analyzer for import parsing and metadata extraction.",
    # long_description=open("README.md").read(),
    # long_description_content_type="text/markdown",
    # url="https://gitlab.com/fnetai/py-import-parser",
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     # "Operating System :: OS Independent",
    # ],
    # include_package_data=True,  # Include non-Python files (e.g., YAML files) (optional)
)