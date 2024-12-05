from setuptools import setup, find_packages

setup(
    name="plagiarism_check_app",
    version="0.0.17",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "nltk",
        "pytest",
        "jinja2"
    ],
    include_package_data=True,  # Ensure non-Python files are included
    package_data={  # Specify additional files to include
        'plagiarism_check_app': [
            'templates/*.html',
            'static/*',
        ],
    },
    entry_points={
        "console_scripts": [
            "start-plagiarism-check-app=app.main:main",
        ],
    },
    description="A FastAPI app",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vira Boiko",
    author_email="vira.shendrykk@gmail.com",
    url="https://github.com/viraboik/plagiarismcheck.git",
)
