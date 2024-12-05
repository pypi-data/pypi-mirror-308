import requests
from setuptools import setup


def last_version(package_name: str) -> str:
    response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
    if response.status_code == 200:
        return response.json()['info']['version']
    else:
        return "0.0"


def increment_version(version: str) -> str:
    new_version = int(float(version) * 10) + 1
    return "{0:.1f}".format(new_version / 10)


if __name__ == "__main__":
    package_name = "params-grid"
    with open("README.md", "r") as f:
        long_description = f.read()

    setup(
        name=package_name,
        version=increment_version(last_version(package_name)),
        description="Tool for defining and working with hyperparams of machine learning models.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/darkhan-ai/params-grid",
        packages=["params_grid"],
        install_requires=[
            "optuna",
            "pandas",
        ],
        zip_safe=False,
    )
