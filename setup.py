"""Setup configuration for Roast My Strava package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="roast-my-strava",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A friendly Strava activity analytics dashboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/roast-my-activity-data",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=2.0.0",
        "altair>=5.0.0",
        "python-dateutil>=2.8.2",
    ],
    entry_points={
        "console_scripts": [
            "roast-my-strava=app:main",
        ],
    },
)
