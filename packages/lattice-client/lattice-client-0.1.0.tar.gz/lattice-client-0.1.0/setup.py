import setuptools

setuptools.setup(
    name="lattice-client",
    version="0.1.0",
    packages=["lattice"],
    install_requires=[
        "cloudpickle==2.2.1",
        "httpx==0.24.0",
        "networkx==3.1",
        "requests==2.26.0",
        "rich==13.3.5",
    ],
)
