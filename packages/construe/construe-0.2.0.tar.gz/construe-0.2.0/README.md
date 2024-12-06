# Construe: An LLM Benchmark Utility

**An LLM inferencing benchmark tool focusing on device-specific latency and memory usage.**

## Quick Start

This package is intended to be installed with `pip` and it will create a command line program `construe` on your `$PATH` to execute benchmarking comamnds:

```
$ pip install construe
$ which construe
$ construe --help
```

There are several top-level configurations that you can specify either as an environment variable or a command line option before the command. The environment variables are as follows:

- `$CONSTRUE_ENV` or `$ENV`: specify the name of the experimental environment for comparison purposes.
- `$CONSTRUE_DEVICE` or `$TORCH_DEVICE`: specify the name of the default device to use with PyTorch e.g. cpu, mps, or cuda.

The command line utility help is as follows:

```
Usage: construe [OPTIONS] COMMAND [ARGS]...

Options:
  --version          Show the version and exit.
  -d, --device TEXT  specify the pytorch device to run on e.g. cpu, mps or
                     cuda
  -e, --env TEXT     name of the experimental environment for comparison
                     (default is hostname)
  -h, --help         Show this message and exit.

Commands:
  basic
  moondream
```

## Basic Benchmarks

The basic benchmarks implement dot product benchmarks from the [PyTorch documentation](https://pytorch.org/tutorials/recipes/recipes/benchmark.html). These benchmarks can be run using `construe basic`; for example by running:

```
$ construe -e "MacBook Pro 2022 M1" basic -o results-macbook.pickle
```

The `-e` flag specifies the environment for comparison purposes and the `-o` flag saves the measurements out to disk as a Pickle file that can be loaded for comparison to other environments later.

Command usage is as follows:

```
Usage: construe basic [OPTIONS]

Options:
  -e, --env TEXT             name of the experimental environment for
                             comparison (default is hostname)
  -o, --saveto TEXT          path to write the measurements pickle data to
  -t, --num-threads INTEGER  specify number of threads for benchmark (default
                             to maximum)
  -F, --fuzz / --no-fuzz     fuzz the tensor sizes of the inputs to the
                             benchmark
  -S, --seed INTEGER         set the random seed for random generation
  -h, --help                 Show this message and exit.
```

## Moondream Benchmarks

The [moondream](https://huggingface.co/vikhyatk/moondream2) package contains small image-to-text computer vision models that can be used in the first step of a [content moderation](https://www.cloudraft.io/blog/content-moderation-using-llamaindex-and-llm) workflow (e.g. image to text, moderate text). This benchmark executes the model for _encoding_ and _inferencing_ on a small number of images and reports the average time for both operations and the line-by-line memory usage of the model.

It can be run as follows:

```
$ construe moondream
```

Command usage is as follows:

```
Usage: construe moondream [OPTIONS]

Options:
  -h, --help  Show this message and exit.
```

## Releases

To release the construe library and deploy to PyPI run the following commands:

```
$ python -m build
$ twine upload dist/*
```