from setuptools import find_packages, setup

# Read the requirements from the file
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="selected_words_counter",
    version="0.1",
    packages=find_packages(where="src"),
    install_requires=required,
    author="Michael de Winter",
    description="A Python tool that counts specific selected words in a directory of files of different file formats. Outputs the results in a .excel file",
    package_dir={"": "src"},
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Provincie-Zuid-Holland/selected_words_counter",
    python_requires=">=3.10",
)
