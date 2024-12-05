"""Setup for the neurocollage package."""

from pathlib import Path

from setuptools import find_namespace_packages
from setuptools import setup

reqs = [
    "bluepysnap>=3.0.1",
    "brainbuilder>=0.20.1",
    "click>=8",
    "geomdl>=5.2.8",
    "joblib>=1.1",
    "mapbox-earcut>=1",
    "matplotlib>=3.6",
    "morph_tool>=2.9",
    "networkx>=2.5",
    "neurom>=3.2",
    "numpy>=1.26",
    "pandas>=2.1",
    "pyglet>=1.5.20,<2",
    "pyquaternion>=0.9.5",
    "pyquaternion>=0.9.5",
    "region_grower>=1.5.1",
    "scikit-learn>=1.1",
    "scipy>=1.13",
    "tqdm>=4.60",
    "trimesh>=3.23",
    "voxcell>=3.1.5",
    "vtk>=9.0.2",
]

doc_reqs = [
    "docutils<0.21",  # Temporary fix for m2r2
    "m2r2",
    "sphinx",
    "sphinx-bluebrain-theme",
    "sphinx-click",
]

test_reqs = [
    "mock>=3",
    "coverage>=6.5,<7",
    "pytest>=6.1",
    "pytest-click>=1.1",
    "pytest-console-scripts>=1.4",
    "pytest-cov>=4.1",
    "pytest-html>=3.2",
]

setup(
    name="neurocollage",
    author="Blue Brain Project, EPFL",
    description="A tool to create 2D morphology collage plots based on matplotlib.",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://neurocollage.readthedocs.io",
    project_urls={
        "Tracker": "https://github.com/BlueBrain/neurocollage/issues",
        "Source": "https://github.com/BlueBrain/neurocollage",
    },
    license="Apache License 2.0",
    packages=find_namespace_packages(include=["neurocollage*"]),
    python_requires=">=3.9",
    use_scm_version=True,
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=reqs,
    extras_require={
        "docs": doc_reqs,
        "test": test_reqs,
    },
    entry_points={
        "console_scripts": [
            "neurocollage=neurocollage.cli:main",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
