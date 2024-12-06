from setuptools import setup, find_packages

setup(
    name='brainbase-voice-sdk',
    version='0.1.0',
    description='SDK for interacting with the Brainbase Voice API',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'pydantic>=1.8.2'
    ],
    python_requires='>=3.6',
)
