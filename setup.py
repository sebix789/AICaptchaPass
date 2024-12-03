from setuptools import setup, find_packages

# CONFIG SRC AS DEPENDENCY
setup(
    name="AICaptchaPass",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
