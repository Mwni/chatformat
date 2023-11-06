# Chat Format

This is a lightweight Python library for formatting chat prompts for various open source LLMs.

```py
from chatformat import format_chat_prompt

prompt, stop = format_chat_prompt(
	template='vicuna',
	messages=[
		{'role': 'system', 'content': 'You are a very clever LLM.'},
		{'role': 'user', 'content': 'Hello?'}
	]
)
```
will yield the following `prompt`:
```
You are a very clever LLM.

USER: Hello?
ASSISTANT: 
```
The `stop` variable should be used as stopping criteria in your LLM's implementation.


## Install

```bash
pip install chatformat
```


## Supported Formats

Run the `test.py` script to see all formats in action.

### Llama-2

```
<s>[INST] <<SYS>>
{system_message}
<</SYS>>

{user_message} [/INST] {model_reply}</s><s>[INST] {user_message} [/INST] {model_reply}</s>
```

### Alpaca

```
{system_message}

### Instruction:
{user_message}

### Response:
{model_reply}
```

### Vicuna

```
A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.

USER: Hello!
ASSISTANT: Hello!</s>
USER: How are you?
ASSISTANT: I am good.</s>
```

### ChatLM

```
<|im_start|>system
You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.
Knowledge cutoff: 2021-09-01
Current date: 2023-03-01<|im_end|>
<|im_start|>user
How are you?<|im_end|>
<|im_start|>assistant
I am doing well!<|im_end|>
```

## Custom Formats

You can pass a dictionary as template to `format_chat_prompt`, which describes your custom format.

```py
from chatformat import format_chat_prompt

prompt, stop = format_chat_prompt(
	template={
		'with_system': (
			'>system: {system}\n'
			'>user: {user}\n'
			'>assistant: {assistant}'
			'</s>'
		),
		'without_system': (
			'>user: {user}\n'
			'>assistant: {assistant}'
			'</s>'
		),
		'round_seperator': '\n'
	},
	messages=[
		{'role': 'system', 'content': 'You are a very clever LLM.'},
		{'role': 'user', 'content': 'Hello?'}
	]
)
```
The custom template dictionary shall be structured as follows
|Key|Purpose|
|--|--|
|`with_system`|Defines the first round if a system prompt is set.|
|`without_system`|Defines consecutive rounds, and/or first if no system prompt is set.|
|`round_seperator`|Defines how to join multiple rounds.|
|`stop`|Defines the stopword(s) to prevent self-talk. Can be an array. If not set, will be derived from any text following `{assistant}`.|

Take a look at [templates.yml](https://github.com/Mwni/chatformat/blob/main/chatformat/templates.yml) for examples.