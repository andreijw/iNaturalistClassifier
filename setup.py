from setuptools import find_packages, setup

setup(
    name="i_naturalist_classifier",
    version="1.0.0",
    author="Andrei Jaume",
    license="copyright Andrei Jaume Willenska",
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Developers",
        "License :: " + "copyright Andrei Jaume all rights reserved.",
        "Natural Language :: " + "English",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(),
    install_requires=[],
    package_data={
        "i_naturalist_classifier": ["py.typed"],
    },
    python_requires=">=3.12.0",
    long_description="iNaturalist Classifier",
    long_description_content_type="text/markdown",
)
