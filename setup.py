from setuptools import setup, find_packages

setup(
    name="lasm",
    version="1.0",
    description="LLM Attack Surface Measurement Framework",
    packages=find_packages(),
    install_requires=[
        "networkx",
        "numpy",
        "scipy",
        "pandas",
        "torch",
        "transformers",
        "accelerate",
        "scikit-learn",
        "typing-extensions"
    ],
)
