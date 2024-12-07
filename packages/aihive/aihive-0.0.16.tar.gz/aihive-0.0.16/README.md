# Welcome to the Hive 🐝

A general-purpose multi-agent orchestration framework for building agentic software.

## Install

Requires Python 3.10+

```shell
pip install aihive
```

or

```shell
pip install aihive
```

## Usage

```python
from aihive import Nest, Worker

nest = Nest()

worker_agent = Worker(
    name="Sophisticated writer",
    instructions="You write about honey bees.",
)

response = nest.run(
    agent=worker_agent,
    messages=[{"role": "user", "content": "Create a motivational haiku to inspire beekeepers."}],
)

print(response.messages[-1]["content"])
```

```
Fields of golden light,  
Bees dance through blossoms with grace—  
Sweet rewards await.
```

## Acknowledgments

This project includes code from [OpenAI Swarm](https://github.com/openai/swarm).

- Ilan Bigio - [ibigio](https://github.com/ibigio)
- James Hills - [jhills20](https://github.com/jhills20)
- Shyamal Anadkat - [shyamal-anadkat](https://github.com/shyamal-anadkat)
- Charu Jaiswal - [charuj](https://github.com/charuj)
- Colin Jarvis - [colin-openai](https://github.com/colin-openai)
- Katia Gil Guzman - [katia-openai](https://github.com/katia-openai)
