from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements.txt
def parse_requirements(filename):
    """Parse requirements from requirements.txt file."""
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    requirements = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("-"):
            # Extract package name without version pinning for flexibility
            pkg = line.split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0]
            requirements.append(pkg)
    return requirements

setup(
    name='smc360',
    version='1.0.0',
    packages=find_packages(exclude=["test", "test.*", "example", "example.*"]),
    install_requires=[
        "boto3>=1.26.0",
        "click>=8.0.0",
        "dash>=2.10.0",
        "dash-ace>=0.2.0",
        "dash-bootstrap-components>=1.4.0",
        "Flask>=2.2.0",
        "halo>=0.0.31",
        "psycopg2-binary>=2.9.0",
        "python-dotenv>=1.0.0",
        "PyYAML>=6.0",
        "requests>=2.28.0",
        "snowflake-connector-python>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "moto>=4.0.0",
        ],
    },
    include_package_data=True,
    author='Mohammed Adil Farooq',
    author_email='adil.farooq@blend360.com',
    description='Social media data connector for extracting, parsing, and managing social media data at scale.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fishOmlette/SMC360',
    project_urls={
        "Bug Tracker": "https://github.com/fishOmlette/SMC360/issues",
        "Source Code": "https://github.com/fishOmlette/SMC360",
    },
    license='MIT',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="social-media youtube instagram data-extraction api-client",
    entry_points={
        'console_scripts': [
            'smc360 = smc360.cli:main'
        ]
    },
    python_requires='>=3.9'
)
