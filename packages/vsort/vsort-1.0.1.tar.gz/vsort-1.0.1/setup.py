from setuptools import setup, find_packages

setup(
    name="vsort",
    version="1.0.1",
    author="khiat Mohammed Abderrezzak",
    author_email="khiat.dev@gmail.com",
    license="MIT",
    description="Sophisticate Sorting Algorithms",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/vsort/",
    packages=find_packages(),
    install_requires=[
        "heep>=1.0.2",
        "pynput>=1.7.7",
        "pyfiglet>=1.0.2",
        "hashtbl>=1.0.5",
    ],
    keywords=[
        "sorting algorithms",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
