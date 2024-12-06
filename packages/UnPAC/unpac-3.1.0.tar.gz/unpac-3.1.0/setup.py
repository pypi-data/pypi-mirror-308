from setuptools import setup, find_packages

setup(
	name = "UnPAC",
	version="3.1.0",
	packages=find_packages(),
	install_requires=["setuptools>=61.0", "Pandas>=2.2.2", "zipp>=3.17.0", "dicom2nifti>=2.4.11", "pydicom>=3.0.0", "regex>=2023.10.3"
	],
)