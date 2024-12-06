from setuptools import setup, find_packages


setup(
    name='FlexLogger',
    version='1.0.0',
    packages=find_packages(),
    description='Wrapper for remote logging to a Database with the help of an API REST.'
                ''
                'For now the required server is a custom-made database being served by an API Rest.'
                'If someone other than me shows interest in this, I can happily share my Schema (Database and API Rest)',
    author='Anderson',
    author_email='anderbytes@gmail.com',

    long_description_content_type="text/markdown",

    install_requires=[
        "requests~=2.32.3",
        "fastapi~=0.115.5"
    ]
)
