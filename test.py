from chatformat import format_chat_prompt

example_chat = [
	{'role': 'system', 'content': 'You are a very clever LLM.'},
	{'role': 'user', 'content': 'Hello?'},
	{'role': 'assistant', 'content': 'Hello.'},
	{'role': 'user', 'content': 'What are you thinking?'},
	{'role': 'assistant', 'content': 'I think that'},
]

example_custom_template = {
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
} 

for template in ('llama-2', 'vicuna', 'alpaca', 'chatml', 'human-response', example_custom_template):
	prompt, _ = format_chat_prompt(
		template=template,
		messages=example_chat
	)

	print((template if type(template) == str else 'custom').ljust(20, '-'))
	print(prompt)
	print('--------------------')
	print()
	print()