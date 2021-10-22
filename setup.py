from setuptools import setup, find_packages

setup(
    name="mclumix",
    version="0.0.0.1",
    # name="tfg666",
    # version="0.0.0.0.44",
    keywords=("pip", "mclumi"),
    description="UMI de-duplication",
    long_description="UMI de-duplication based on MCL",
    license="MIT",

    url="https://github.com/cribbslab; https://github.com/2003100127",
    author="Jianfeng Sun",
    author_email="jianfeng.sun@ndorms.ox.ac.uk",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    python_requires='>3.6',
    install_requires=[
        'pandas==1.3.3',
        'numpy==1.21.2',
        'pysam==0.17.0',
        'markov_clustering==0.0.6.dev0',
        'networkx==2.6.3',
        'pyfiglet==0.8.post1',
    ],
    entry_points={
        'console_scripts': [
            'mclumi=mclumi.Main:main',
        ],
    }
)