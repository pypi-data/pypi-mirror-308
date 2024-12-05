from setuptools import setup, find_packages

setup(
    name="ekyc_sensor_fts",
    version="0.1",
    packages=find_packages(),
    install_requires=[

    ],
    author="Hoan Dao",
    author_email="hoandq@vnpt.vn",
    description="Decrypt and extract data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/data-science-general-1/ekyc_sensor_fake_detector_featurestore",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)