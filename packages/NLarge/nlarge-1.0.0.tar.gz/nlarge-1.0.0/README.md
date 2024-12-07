# SC4001 NLarge

## Purpose of Project

NLarge is a project focused on exploring and implementing various data
augmentation techniques for Natural Language Processing (NLP) tasks. The primary
goal is to enhance the diversity and robustness of training datasets, thereby
improving the performance and generalization capabilities of NLP models. This
project includes traditional data augmentation methods such as synonym
replacement and random substitution, as well as advanced techniques using Large
Language Models (LLMs).

## Initializing Virtual Environment

We use Poetry in this project for dependency management. To get started, you
will need to install Poetry.

```shell
pip install poetry
```

Afterwards, you can install the needed packages from Python with the help of
Poetry using the command below:

```shell
poetry install
```

## Repository Contents

- [`report.tex`](report/report.tex): The LaTeX document containing the detailed
  report of the project, including methodology, experiments, results, and
  analysis.
- [`example/`](example): Contains example scripts for data augmentation and
  model training.
  - [`demo.ipynb`](example/demo.ipynb)
  - [`Result of test`](example/test/)
- [`NLarge/`](NLarge): The main package containing the data augmentation and
  model implementation.
  - [`dataset_concat.py`](NLarge/dataset_concat.py)
  - [`llm.py`](NLarge/llm.py)
  - [`pipeline.py`](NLarge/pipeline.py)
  - [`random.py`](NLarge/random.py)
  - [`synonym.py`](NLarge/synonym.py)
  - [`utils/`](NLarge/utils)

## Usage

To run the models and experiments, you can use the python notebooks in the
`example/` directory. The notebooks contain detailed explanations and code
snippets for data augmentation and model training. For the results of the
experiments, you can refer to the `example/test/` directory.

We also refer the user to [`demo_attention.ipynb`](example/demo_attention.ipynb)
for a more detailed example of how to use the `pipeline.py` module. The notebook
contains the code for training a model with attention mechanism using the
NLarge library as a toolkit for data augmentation.

### Compute limitation

Should you face computational limitation, you can use the datasets that we 
have preprocessed and saved in the `example/llm-dataset/` directory. As the inference
time for the Large Language Models (LLMs) can be quite long, we have preprocessed
in advance such that end users can directly use the preprocessed datasets for
training and testing purposes.

## Development

While the library has been developed and tested, the library can be easily 
extended with additional data augmentation techniques or with new models to
support the testing and research of the performance of different augmentation
techniques.

The library can be easily extended with additional data augmentation techniques
through creation of new modules or files in the `NLarge` package.

## Website

You can access the PiPy page of the project from the link here:
[pypi page](https://pypi.org/project/NLarge/)

Our github repository can be found here:
[github page](https://github.com/HiIAmTzeKean/SC4001-NLarge)

## Contributing

Contributions to this project are welcome. If you have any suggestions or
improvements, please create a pull request or open an issue.
