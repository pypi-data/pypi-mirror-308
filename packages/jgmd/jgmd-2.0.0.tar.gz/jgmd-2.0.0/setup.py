from distutils.core import setup

setup(
    name="jgmd",  # How you named your package folder (MyLib)
    packages=["jgmd"],  # Chose the same as "name"
    version="2.0.0",  # Start with a small number and increase it with every change you make
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="A general-purpose python package for logging, event-emission, and other common code.",
    author="Jonathan Gardner",
    author_email="jonathangardnermd@outlook.com",
    url="https://github.com/jonathangardnermd/jgmd",
    download_url="https://github.com/jonathangardnermd/jgmd/archive/refs/tags/v2.0.0.tar.gz",
    keywords=[
        "PYTHON",
        "LOGGING",
        "EVENTS",
        "UTILITY",
    ],
    install_requires=["tabulate"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.13",
    ],
)
