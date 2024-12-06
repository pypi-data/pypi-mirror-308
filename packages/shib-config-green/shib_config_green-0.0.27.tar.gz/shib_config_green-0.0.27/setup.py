from setuptools import find_packages, setup

setup(
    name="shib-config-green",
    version="0.0.27",
    description="Used to update and manage the Shibboleth Service Provider Directory in Green Production for"
                "Terra Dotta",
    package_dir={"": "mgmt_scripts"},
    packages=find_packages(where="mgmt_scripts"),
    author="JonathanM",
    author_email="jonathan.mckay@terradotta.com",
    install_requires=["pyodbc>=5.2.0", "Requests>=2.32.3"],
    extra_require={
        "dev": ["setuptools>=75.5.0", "pytest>=8.3.3"],
    },
    entry_points={
        'console_scripts': [
            'run-shib = __main__:main',
        ]
    },
    python_requires=">=3.12",
)
