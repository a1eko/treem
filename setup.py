import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

dependencies = [
    "numpy",
    "matplotlib"
]

setuptools.setup(
    name="treem",
    version="1.0.5.dev8",
    author="Alexander Kozlov",
    author_email="akozlov@kth.se",
    description="Tree-like morphology data processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a1eko/treem",
    packages=setuptools.find_packages(),
    install_requires=dependencies,
    entry_points={
        "console_scripts": [
            "swc = treem.cli:cli",
        ],
    },
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    keywords=[
        "neuron",
        "morphology",
        "reconstruction",
        "processing",
        "morphometry",
        "modification",
        "repair",
    ],
)
