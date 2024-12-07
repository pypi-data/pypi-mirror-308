# AI Hive

A general-purpose multi-agent orchestration framework.

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
from aihive import Swarm, AI

swarm = Swarm()

def ask_queen_agent():
    return queen_agent

worker_agent = AI(
    name="Worker AI",
    instructions="You are a helpful worker agent.",
    functions=[transfer_to_queen_agent],
)

queen_agent = AI(
    name="Queen AI",
    instructions="Guide your worker agents to be helpful.",
)

response = swarm.run(
    agent=worker_agent,
    messages=[{"role": "user", "content": "Create a motivational haiku to inspire the worker agents."}],
)

print(response.messages[-1]["content"])
```

```
Hope glimmers brightly,
New paths converge gracefully,
What can I assist?
```

## Acknowledgments

This project includes code from [OpenAI Swarm](https://github.com/openai/swarm).

- Ilan Bigio - [ibigio](https://github.com/ibigio)
- James Hills - [jhills20](https://github.com/jhills20)
- Shyamal Anadkat - [shyamal-anadkat](https://github.com/shyamal-anadkat)
- Charu Jaiswal - [charuj](https://github.com/charuj)
- Colin Jarvis - [colin-openai](https://github.com/colin-openai)
- Katia Gil Guzman - [katia-openai](https://github.com/katia-openai)
