<div align="center">
  <img src="https://autrainer.github.io/aucurriculum/_images/logo_banner.png" alt="aucurriculum — A Curriculum Learning Toolkit for Deep Learning Tasks built on top of autrainer">
</div>

# aucurriculum

[![aucurriculum PyPI Version](https://img.shields.io/pypi/v/aucurriculum?logo=pypi&logoColor=b4befe&color=b4befe)](https://pypi.org/project/aucurriculum/)
[![aucurriculum Python Versions](https://img.shields.io/pypi/pyversions/aucurriculum?logo=python&logoColor=b4befe&color=b4befe)](https://pypi.org/project/aucurriculum/)
[![aucurriculum GitHub License](https://img.shields.io/badge/license-MIT-b4befe?logo=c)](https://github.com/autrainer/aucurriculum/blob/main/LICENSE)

A Curriculum Learning Toolkit for Deep Learning Tasks built on top of [autrainer](https://github.com/autrainer/autrainer).

## Installation

To install _aucurriculum_, first ensure that PyTorch (along with torchvision and torchaudio) version 2.0 or higher is installed.
For installation instructions, refer to the [PyTorch website](https://pytorch.org/get-started/locally/).

It is recommended to install _aucurriculum_ within a virtual environment.
To create a new virtual environment, refer to the [Python venv documentation](https://docs.python.org/3/library/venv.html).

Next, install _aucurriculum_ using _pip_.

```bash
pip install aucurriculum
```

To install _aucurriculum_ from source, refer to the [contribution guide](https://autrainer.github.io/aucurriculum/development/contributing.html).

## Next Steps

To get started using _aucurriculum_, the [quickstart guide](https://autrainer.github.io/aucurriculum/usage/quickstart.html) outlines the creation of a simple training configuration
and [tutorials](https://autrainer.github.io/aucurriculum/usage/tutorials.html) provide examples for implementing custom scoring and pacing functions including their configurations.

For a complete list of available CLI commands, refer to the [CLI reference](https://autrainer.github.io/aucurriculum/usage/cli_reference.html) or the [CLI wrapper](https://autrainer.github.io/aucurriculum/usage/cli_wrapper.html).

## Citation

If you use _aucurriculum_ in your research, please consider citing the following [paper](https://doi.org/10.48550/arXiv.2411.00973):

```bibtex
@misc{rampp2024sampledifficulty,
  doi = {10.48550/ARXIV.2411.00973},
  url = {https://arxiv.org/abs/2411.00973},
  author = {Rampp,  Simon and Milling,  Manuel and Triantafyllopoulos,  Andreas and Schuller,  Bj\"{o}rn W.},
  keywords = {Machine Learning (cs.LG),  FOS: Computer and information sciences,  FOS: Computer and information sciences},
  title = {Does the Definition of Difficulty Matter? Scoring Functions and their Role for Curriculum Learning},
  publisher = {arXiv},
  year = {2024},
  copyright = {Creative Commons Attribution Non Commercial Share Alike 4.0 International}
}
```
