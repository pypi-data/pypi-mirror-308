from setuptools import setup, find_packages
import  os 


# def read_requirements(file):
#     with open(os.path.join(os.path.dirname("Synthetic Data Generator"), file), encoding="utf-8") as f:
#         return f.read().splitlines()

def read_file(file):
    """
    Reads the content of a given file and returns it as a string.
    
    Args:
        file (str): The path to the file to read.
    
    Returns:
        str: The content of the file as a single string.
    """
    with open(file, encoding="utf-8") as f:
        return f.read()

# Read in long description, version, and requirements from files
long_description = read_file("README.md")
# version = read_file("VERSION")
# requirements = read_requirements("requirements.txt")

# Set up the package
setup(
    name='SDG_LLM',
    version='0.0.2',
    author='Darshan Kumar',
    author_email='Darshankumarr03@gmail.com',
    # url='https://best-practice-and-impact.github.io/example-package-python/',
    description='Synthetic data generator for LLM evaluation',
    # long_description_content_type="text/x-rst",
    # long_description=long_description,
    license="MIT license",
    packages=find_packages(where="SDG_LLM/src"),
    package_dir={'': 'SDG_LLM/src'},  # Exclude test directory from distribution
    install_requires=[
        "langchain",
        "langchain_groq",
        "langchain_community",
        "langchain_core",
        "transformers",
        "pymupdf",
        "youtube-transcript-api",
        "pytube",
        "langchain-unstructured"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
