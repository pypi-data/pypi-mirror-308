import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alpha_hybird_model",
    version="0.1.1",  # Ensure this is updated if uploading new versions
    author="Ihtesham Jahangir",
    author_email="ihteshamjahangir21@gmail.com",
    description="Alpha Hybrid CNN model for classification tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ihtesham-jahangir/alpha_hybird_model",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy>=1.24.0",  # Latest version compatible with TensorFlow 2.12.0
        "matplotlib>=3.7.1",  # Latest stable release
        "tensorflow>=2.12.0",  # Latest stable version of TensorFlow
        "setuptools>=65.5.0",  # Latest stable version
        "wheel>=0.40.0",  # Latest stable version
    ],
    entry_points={
        'console_scripts': [
            'alpha_hybird_train=scripts.train_model:main',  # Entry point for the training script
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
