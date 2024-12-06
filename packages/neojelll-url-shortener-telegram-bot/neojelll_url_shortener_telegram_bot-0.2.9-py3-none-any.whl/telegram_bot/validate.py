async def is_valid_message(message: str) -> dict | str:
	lst: list[str] = message.split()

	if len(lst) > 3:
		return 'Вы ввели слишком много параметров или поставили лишний пробел в сообщении попробуйте еще раз'
	
	if len(lst) == 1:
		return {'url': lst[0]}
	
	elif len(lst) == 2:
		if not lst[1].isalnum():
			return "Похоже что то не так с префиксом попробуйте еще раз"
		return {'url': lst[0], 'prefix': lst[1]}
	
	else:
		if not lst[1].isalnum():
			return "Похоже что то не так с префиксом попробуйте еще раз"
	
		elif not lst[2].isdigit():
			return 'Похоже что то не так с последним параметром (это должно быть число) попробуте еще раз'
		
		else:
			return {'url': lst[0], 'prefix': lst[1], 'expiration': lst[2]}
