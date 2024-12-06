# AI Bee Hive

A general-purpose framework for orchestrating LLM workflows (forked from OpenAI's Swarm).

## Install

Requires Python 3.10+

```shell
pip install aibeehive
```

or

```shell
pip install aibeehive
```

## Usage

```python
from aibeehive import Swarm, Bee

swarm = Swarm()

def ask_queen_bee():
    return queen_bee

worker_bee = Bee(
    name="Worker Bee",
    instructions="You are a helpful worker bee.",
    functions=[transfer_to_queen_bee],
)

queen_bee = Bee(
    name="Queen Bee",
    instructions="Guide your worker bees to be helpful.",
)

response = swarm.run(
    bee=worker_bee,
    messages=[{"role": "user", "content": "Create a motivational haiku to inspire the worker bees."}],
)

print(response.messages[-1]["content"])
```

```
Hope glimmers brightly,
New paths converge gracefully,
What can I assist?
```

## Table of Contents

- [Overview](#overview)
- [Examples](#examples)
- [Documentation](#documentation)
  - [Running Swarm](#running-swarm)
  - [Bees](#bees)
  - [Functions](#functions)
  - [Streaming](#streaming)
- [Evaluations](#evaluations)
- [Utils](#utils)

# Big Thanks to OpenAI Core Contributors

- Ilan Bigio - [ibigio](https://github.com/ibigio)
- James Hills - [jhills20](https://github.com/jhills20)
- Shyamal Anadkat - [shyamal-anadkat](https://github.com/shyamal-anadkat)
- Charu Jaiswal - [charuj](https://github.com/charuj)
- Colin Jarvis - [colin-openai](https://github.com/colin-openai)
- Katia Gil Guzman - [katia-openai](https://github.com/katia-openai)

## Acknowledgments

This project includes code from [OpenAI Swarm](https://github.com/openai/swarm).
