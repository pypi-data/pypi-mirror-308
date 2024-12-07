[![PyPI - Version](https://badge.fury.io/py/CTADIRAC.svg)](https://pypi.org/project/CTADIRAC/)

# CTADIRAC project

* CTADIRAC is a customized version of the DIRAC interware. As of today, it allows an easy and optimized access to Grid resources (mainly EGI) available to the CTA Virtual Organization (vo.cta.in2p3.fr). When CTAO DPPS will be setup, CTADIRAC will serve as the Computing Ressource and Worflow Management System.
* Follow the [CTADIRAC specific documentation](https://redmine.cta-observatory.org/projects/cta_dirac/wiki/CTA-DIRAC_Users_Guide)
* [Wiki](https://gitlab.cta-observatory.org/cta-computing/dpps/CTADIRAC/-/wikis/)


# Install CTADIRAC Client

See the dedicated [client installation documentation](docs/install_client.md).

# Install CTADIRAC Server

See the dedicated [server installation documentation](docs/install_CTADIRAC.md).

## Deploying on Kubernetes
[CTADIRAC Helm charts](https://gitlab.cta-observatory.org/cta-computing/dpps/workload/CTADIRAC-charts) (in development).

[CTADIRAC fleet deployment](https://gitlab.cta-observatory.org/cta-computing/dpps/workload/ctadirac-deployment) on a Kubernetes cluster.

# Registry

* Get `CTADIRAC` on `PyPi`:

```
pip install CTADIRAC
```

* Get `CTADIRAC` client `docker` image:

```
docker pull gitlab.cta-observatory.org:5555/cta-computing/dpps/ctadirac/dirac-client:latest
```

# Contribute to CTADIRAC

To contribute to CTADIRAC, please check out the full [DIRAC developers guide](http://dirac.readthedocs.io/en/integration/DeveloperGuide/index.html).

## Create the dev environment:

```bash
# Clone the CTADIRAC repository:
git clone git@gitlab.cta-observatory.org:cta-computing/dpps/workload/CTADIRAC.git
cd CTADIRAC

# Create the mamba environment:
mamba env create --file environment.yml
mamba activate ctadirac-dev

# Make an editable installation of CTADIRAC:
pip install -e .

# Enable pre-commit:
mamba install pre-commit
pre-commit install
```

## Running tests

```bash
# Create the testing environment:
mamba env create -y --file utils/ci/env/coverage.yml
mamba activate coverage

# Make an editable installation of CTADIRAC:
python -m pip install -e .

# Run the tests:
python -m pytest tests/unit
# with pytest coverage:
python -m pytest tests/unit --cov=src/CTADIRAC/ --cov-report=term
```

# Contact Information
* Luisa Arrabito <arrabito@in2p3.fr>
