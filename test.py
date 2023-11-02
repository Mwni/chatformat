from chatformat import format_chat_prompt

example_chat = [
	{'role': 'system', 'content': 'You are a very clever LLM.'},
	{'role': 'user', 'content': 'Hello?'},
	{'role': 'assistant', 'content': 'Hello.'},
	{'role': 'user', 'content': 'What are you thinking?'},
	{'role': 'assistant', 'content': 'I think that'},
]

for template in ('llama-2', 'vicuna', 'alpaca', 'chatml'):
	prompt = format_chat_prompt(
		template=template,
		messages=example_chat
	)

	print(template.ljust(20, '-'))
	print(prompt)
	print('--------------------')
	print()
	print()