from setuptools import setup
from pathlib import Path

GEN_version = "0.0.5"
READ_name = "nelean"

here = Path(__file__).parent.resolve()

setup(
    name=READ_name,
    version=GEN_version,
    author="rendaw",
    url="https://gitlab.com/rendaw/nelean",
    download_url="https://gitlab.com/rendaw/nelean/-/archive/v{v}/nelean-v{v}.tar.gz".format(
        v=GEN_version
    ),
    license="MIT",
    description="A deterministic Lisp formatter",
    long_description=(here / "readme.md").read_text(),
    long_description_content_type="text/markdown",
    classifiers=[],
    py_modules=["nelean"],
    entry_points={"console_scripts": ["nelean=nelean:main"]},
)
