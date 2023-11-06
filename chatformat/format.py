import os
import yaml
from .exceptions import ChatFormatException


with open(os.path.join(os.path.dirname(__file__), 'templates.yml')) as f:
	templates = yaml.load(f, Loader=yaml.Loader)


def format_chat_prompt(template, messages):
	if type(template) == dict:
		if 'with_system' not in template or 'without_system' not in template:
			raise ChatFormatException('Custom templates must define "with_system" and "without_system"')
	else:
		if template not in templates:
			raise ChatFormatException('No chat template for "%s" defined' % template)
		else:
			template = templates[template]
		
	if len(messages) == 0:
		raise ChatFormatException('No messages passed (message list is empty)')
	
	system, rounds = split_messages(messages)
	blocks = []

	if not system and 'system_default' in template:
		system = template['system_default']

	for i in range(len(rounds)):
		is_first = i == 0
		is_last = i >= len(rounds) - 1
		user, assistant = rounds[i]

		blocks.append(
			format_round(
				template, 
				system=system if is_first else None,
				user=user,
				assistant=assistant,
				closed=not is_last
			)
		)

	final_prompt = (
		template['round_seperator']
		if 'round_seperator' in template 
		else ''
	).join(blocks)

	if 'stop' in template:
		stop = template['stop']
	else:
		stop = template['without_system'].split('{assistant}')[1]

		if len(stop) == 0:
			stop = None
	

	return final_prompt, stop


def split_messages(messages):
	rounds = []

	if messages[0]['role'] == 'system':
		system = messages[0]['content']
		offset = 1
	else:
		system = None
		offset = 0

	for i in range(offset, len(messages), 2):
		m1 = messages[i]
		m2 = messages[i+1] if len(messages) >= i+2 else None


		if m1['role'] != 'user':
			raise ChatFormatException('Message #%i must be of role "user"' % (i+1))
		
		if m2 and m2['role'] != 'assistant':
			raise ChatFormatException('Message #%i must be of role "assistant"' % (i+2))
		
		rounds.append((m1['content'], m2['content'] if m2 else None))

	return system, rounds

	
def format_round(template, system, user, assistant, closed=True):
	if system:
		prompt = template['with_system']
		prompt = prompt.replace('{system}', system)
	else:
		prompt = template['without_system']

	prompt = prompt.replace('{user}', user)

	if closed:
		prompt = prompt.format(assistant=assistant)
	else:
		prompt = prompt[0:prompt.index('{assistant}')]

		if assistant:
			prompt += assistant


	return prompt