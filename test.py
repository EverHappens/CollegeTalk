

test1 = (123,)
test2 = [(123,), (234,)]

if test1 in test2:
	print("good")


@bot.message_handler(content_types = ['text'])
	def receiving_messages(message):
		pricelist = db.get_pricelist(message.from_user.id)
		empty = False
		for product in pricelist:
			if product[1]:
				empty = False
			else:
				empty = True
			text = product[0]
			if empty:
				text += "'s price is TBD"
			else:
				text += ' costs ' + str(product[1]) + '$'
			bot.send_message(message.from_user.id, text)