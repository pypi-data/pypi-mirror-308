from setuptools import find_packages, setup

setup(
    name="shib-config-green",
    version="0.0.31",
    description="Used to update and manage the Shibboleth Service Provider Directory in Green Production for" 
                "Terra Dotta",
    packages=find_packages(),
    author="JonathanM",
    author_email="jonathan.mckay@terradotta.com",
    install_requires=["pyodbc>=5.2.0", "requests>=2.32.3"],
    extras_require={
        "dev": ["setuptools>=75.5.0", "pytest>=8.3.3"],
    },
    entry_points={
        'console_scripts': [
            'run-shib = mgmt_scripts.run:main',
        ]
    },
    python_requires=">=3.12",
)
