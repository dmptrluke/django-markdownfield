import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = {}
with open("./markdownfield/version.py") as fp:
    exec(fp.read(), version)

install_requires = [
    'django>=2.2',
    'markdown',
    'bleach',
    'bleach_whitelist'
]

setuptools.setup(
    name="django-markdownfield",
    version=version['__version__'],
    author="Luke Rogers",
    author_email="lukeroge@gmail.com",
    description="A markdown field.",
    install_requires=install_requires,
    extras_require={
        ':python_version == "3.6"': [
            'dataclasses',
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dmptrluke/django-markdownfield",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
