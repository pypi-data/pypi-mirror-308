from setuptools import setup, find_packages

with open("README.md", "r") as f:
	description = f.read()

setup(
	name = "UnPAC",
	version="3.2.0",
	packages=find_packages(),
	install_requires=["setuptools", "Pandas", "zipp", "dicom2nifti", "pydicom", "regex"
	],
	long_description=description,
	long_description_content_type="text/markdown"
)