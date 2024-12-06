import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testomaton", 
    version="0.2.2",
    author="Patryk Chamuczyński, Testify AS",
    author_email="p.chamuczynski@testify.no",
    description="Model based combinatorial test data generator",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://bitbucket.org/testify-no/tomato",
    license="GNU Affero General Public License v3 or later (AGPLv3+)",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
    keywords = 'testing pairwise test_generation',
    package_dir = {"": "src",},
    packages=setuptools.find_packages(where="src"),
    py_modules=['tomato', 'generator', 'model', 'constraint', 'solver', 'beaver'],
    install_requires=['python-sat', 
                      'pyparsing',
                      'pyaml',
                      'regex'],
    entry_points={
        'console_scripts':[
            'tomato=testomaton.tomato:main',
            'beaver=testomaton.beaver:main',
            'jigsaw=testomaton.jigsaw:main',
        ]
    },
)
