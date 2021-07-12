import telebot, random
from telebot import types
from sqlighter import SQLighter

tgtoken = '1378870721:AAG3i0VM0aESGcfiniLo7FPpbQwQ4ScZvR0'
bot = telebot.TeleBot(tgtoken)
db = SQLighter('sql.db')

#user_role choice buttons
chooseyourpath = types.InlineKeyboardMarkup(row_width = 2)
path1 = types.InlineKeyboardButton('High school student', callback_data = 'setrolehsc')
path2 = types.InlineKeyboardButton('College student', callback_data = 'setrolecol')
chooseyourpath.add(path1, path2)

def start_menu(role):
	keyboard = types.ReplyKeyboardMarkup(row_width = 3, resize_keyboard = False)
	print(role)
	if role == 'hsc':
		button1 = types.KeyboardButton(text = 'I want a match!')
		buttonshow = types.KeyboardButton(text = 'My requests')
		buttonstg1 = types.KeyboardButton(text = 'Change univs & majors')
		buttonstg2 = types.KeyboardButton(text = 'Change UTC')
		buttonstg3 = types.KeyboardButton(text = 'Change info about myself')
		keyboard.add(button1, buttonshow, buttonstg1, buttonstg2, buttonstg3)
	if role == 'col':
		buttonshow = types.KeyboardButton(text = 'All requests')
		buttonstg1 = types.KeyboardButton(text = 'Change my univs & majors')
		buttonstg2 = types.KeyboardButton(text = 'Change UTC')
		buttonstg3 = types.KeyboardButton(text = 'Change info about myself')
		keyboard.add(buttonshow, buttonstg1, buttonstg2, buttonstg3)
	return keyboard

@bot.message_handler(commands = ['start'])
def greeting(message):
	if not db.check_user(message.from_user.id):
		db.add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
		greeting = 'Hello! I am <b>{1.first_name} Bot</b>! Here as a high school student you can ask college students some questions about their university and have a friendly chat \nOR maybe you are a college student who is eager to speak with younger ones and help them choose their dream university!'
		greeting2 = 'Which one of them are you?'
		bot.send_message(message.chat.id, greeting.format(message.from_user, bot.get_me()), parse_mode = 'html')
		#Which one of them are you? (Inline keyboard)
		bot.send_message(message.chat.id, greeting2.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = chooseyourpath)
	if db.get_status == 'register':
		greeting = 'Hello! I am <b>{1.first_name} Bot</b>! Here as a high school student you can ask college students some questions about their university and have a friendly chat \nOR maybe you are a college student who is eager to speak with younger ones and help them choose their dream university!'
		greeting2 = 'Which one of them are you?'
		bot.send_message(message.chat.id, greeting.format(message.from_user, bot.get_me()), parse_mode = 'html')
		#Which one of them are you? (Inline keyboard)
		bot.send_message(message.chat.id, greeting2.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = chooseyourpath)

@bot.message_handler(commands = ['leave'])
def leaving (message):
	status = db.get_status(message.from_user.id)[0][0]
	if status == 'chatting':
		role = db.get_role(message.from_user.id)[0][0]
		print(role)
		print(db.get_hsc_comrade(message.from_user.id))
		if role == 'hsc':
			text = "You've ended the conversation"
			bot.send_message(message.chat.id, text, reply_markup = start_menu('hsc'))
			text = "The other guy has ended the conversation with you"
			db.change_status(message.from_user.id, 'inmenu')
			userid = db.get_hsc_comrade(message.from_user.id)[0][0]
			bot.send_message(userid, text, reply_markup = start_menu('col'))
			db.change_status(userid, 'inmenu')
			db.del_comrade(message.from_user.id, userid)
		elif role == 'col':
			text = "You've ended the conversation"
			bot.send_message(message.chat.id, text, reply_markup = start_menu('col'))
			db.change_status(message.from_user.id, 'inmenu')
			text = "The other guy has ended the conversation with you"
			userid = db.get_col_comrade(message.from_user.id)[0][0]
			bot.send_message(userid, text, reply_markup = start_menu('hsc'))
			db.change_status(userid, 'inmenu')
			db.del_comrade(userid, message.from_user.id)

@bot.message_handler(content_types = ['text'])
def receiving_messages(message):
	status = db.get_status(message.from_user.id)[0][0]
	if status == 'chatting':
		role = db.get_role(message.from_user.id)[0][0]
		if role == 'hsc':
			print(db.get_hsc_comrade(message.from_user.id))
			bot.send_message(db.get_hsc_comrade(message.from_user.id)[0][0], message.text)
		elif role == 'col':
			bot.send_message(db.get_col_comrade(message.from_user.id)[0][0], message.text)
	print('gotthemessage')
	print(status)
	if status == 'inmenu':
		print('gotthemessage')
		response = message.text
		user_role = db.get_role(message.from_user.id)
		hsc_searchlist = db.get_hsc_acad(message.from_user.id)
		if response == 'I want a match!':
			userids = db.get_test(message.from_user.id)
			print(userids)
			print(len(userids))
			arrlen = len(userids)
			duplicate_userids = db.get_hsc_requests(message.from_user.id)
			text = ''
			if arrlen > 5:
				n = 6
				for i in range(1, n):
					print(i)
					r = random.randint(0, arrlen - i)
					userid = userids[r][0]
					userinfo = db.get_userinfo(userid)[0]
					col_searchlist = db.get_col_acad(userid)
					print(userid)
					print(userinfo)
					print(col_searchlist)
					if userids[r] in duplicate_userids:
						n += 1
					else:
						text = userinfo[0] + ' ' + userinfo[1] + '\n'
						prev = ''
						text1 = ''
						for pair in col_searchlist:
							if pair[0] == prev:
								text1 += ', ' + pair[1]
							else:
								text1 += '), ' + pair[0] + '(' + pair[1]
							prev = pair[0]
						text1 += ')\nAbout: ' + userinfo[2]
						text += text1[3:]
						invlink = types.InlineKeyboardMarkup()
						button = types.InlineKeyboardButton('Send an invitation', callback_data = 'linkme' + str(userid))
						invlink.add(button)
						bot.send_message(message.chat.id, text, reply_markup = invlink)
						if not r == arrlen - i:
							userids[r][0] = userids[arrlen - i][0]
							userids[arrlen - 1][0] = userid
			else:
				for userid in userids:
					userinfo = db.get_userinfo(userid[0])[0]
					col_searchlist = db.get_col_acad(userid[0])
					print(userid[0])
					print(userinfo)
					print(col_searchlist)
					if not userid in duplicate_userids:
						text = userinfo[0] + ' ' + userinfo[1] + '\n'
						print(userinfo)
						prev = ''
						text1 = ''
						for pair in col_searchlist:
							if pair[0] == prev:
								text1 += ', ' + pair[1]
							else:
								text1 += '), ' + pair[0] + '(' + pair[1]
						text1 += ')\nAbout: ' + userinfo[2]
						text += text1[3:]
						invlink = types.InlineKeyboardMarkup()
						button = types.InlineKeyboardButton('Send an invitation', callback_data = 'linkme' + str(userid[0]))
						invlink.add(button)
						print(userid[0])
						bot.send_message(message.chat.id, text, reply_markup = invlink)
			if not text:
				text = 'Ohh, looks like there are no fitting students for you. You should edit university & majors list or try again later.\nAlso you may have already requested all fitting candidates for a conversation'
				bot.send_message(message.from_user.id, text)
			text = 'to send someone a message send me money)'
			bot.send_message(message.chat.id, text)
		print('gotthemessage')
		print(response, user_role)
		if user_role[0][0] == 'col' and 'All requests' in response:
			print('requests?')
			role = db.get_role(message.from_user.id)[0][0]
			print(role)
			if response == 'All requests':
				print("!")
				print(db.get_col_requests(message.from_user.id))
				text = ''
				requests = db.get_col_requests(message.from_user.id)
				for userid in requests:
					print('works great'+str(userid[0]))
					userinfo = db.get_userinfo(userid[0])[0]
					hsc_searchlist = db.get_hsc_acad(userid[0])
					print(userid[0])
					print(userinfo)
					print(hsc_searchlist)
					text = userinfo[0] + ' ' + userinfo[1] + '\n'
					last = False
					prev = ''
					text1 = ''
					empty = False
					print(hsc_searchlist)
					for pair in hsc_searchlist:
						print(pair)
						last = False
						if pair[0] == prev:
							text1 += ', ' + pair[1]
							last = True
						else:
							if empty:
								text1 = ', ' + pair[0]
							else:
								text1 += '), ' + pair[0]
							if pair[1]:
								empty = False
								text1 += '(' + pair[1]
								last = True						
							else:
								empty = True
						prev = pair[0]
					if last:
						text1 += ')'
					text += text1[3:] + '\nAbout: ' + userinfo[2]
					canapp = types.InlineKeyboardMarkup()
					button = types.InlineKeyboardButton('Approve', callback_data = 'approve' + str(userid[0]))
					button1 = types.InlineKeyboardButton('Cancel', callback_data = 'canlink' + str(userid[0]))
					canapp.add(button, button1)
					print(userid[0])
					bot.send_message(message.chat.id, text, reply_markup = canapp)
				if not text:
					text = "hmm... You don't have any active requests."
					bot.send_message(message.from_user.id, text)

			elif role == 'hsc' and response == 'My requests':
				print("!")
				print(db.get_hsc_requests(message.from_user.id))
				text = ''
				requests = db.get_hsc_requests(message.from_user.id)
				print
				for userid in requests:
					print('works great'+str(userid[0]))
					userinfo = db.get_userinfo(userid[0])[0]
					col_searchlist = db.get_col_acad(userid[0])
					print(userid[0])
					print(userinfo)
					print(col_searchlist)
					text = userinfo[0] + ' ' + userinfo[1] + '\n'
					prev = ''
					text1 = ''
					for pair in col_searchlist:
						if pair[0] == prev:
							text1 += ', ' + pair[1]
						else:
							text1 += '), ' + pair[0] + '(' + pair[1]
						prev = pair[0]
					text1 += ')\nAbout: ' + userinfo[2]
					text += text1[3:]
					cancel = types.InlineKeyboardMarkup()
					button = types.InlineKeyboardButton('Cancel', callback_data = 'canlink' + str(userid[0]))
					cancel.add(button)
					print(userid[0])
					bot.send_message(message.chat.id, text, reply_markup = cancel)
				if not text:
					text = "hmm... You don't have an active request. Get yourself a match and have one!"
					bot.send_message(message.from_user.id, text)
				
				'''
				for userid in db.get_hsc_requests(message.from_user.id):
					print(userid)
					userinfo = db.get_userinfo(userid[0])
					print(userinfo)
					col_searchlist = db.get_col_acad(userid[0])
					text = userinfo[0][0] + ' ' + userinfo[0][1] + '\n' + 'From ' + col_searchlist[0][0] + ', took ' + col_searchlist[0][1] + ' major\n' + 'About: ' + userinfo[0][2]
					cancel = types.InlineKeyboardMarkup()
					button = types.InlineKeyboardButton('Cancel', callback_data = 'canlink' + str(userid[0]))
					cancel.add(button)
					bot.send_message(message.from_user.id, text, reply_markup = cancel)
				if not text:
					text = "hmm... You don't have an active request. Get yourself a match and have one!"
					bot.send_message(message.from_user.id, text)
					'''
		print('gotthemessage')
		if response == 'Change my univs & majors':
			if db.get_role(message.from_user.id)[0][0] == 'col': 
				db.change_status(message.from_user.id, 'ch1col_wruniversities')
				db.clear_userlist(message.from_user.id)
				text = 'One-by-one, write up all the universities you would like to hear about. After you have listed all, write "Done"'
				bot.send_message(message.from_user.id, text, reply_markup = types.ReplyKeyboardRemove())
		elif response == 'Change univs & majors':
			if db.get_role(message.from_user.id)[0][0] == 'hsc': 
				db.change_status(message.from_user.id, 'ch1hsc_wruniversities')
				db.clear_userlist(message.from_user.id)
				text = 'One-by-one, write up all the universities you would like to hear about. After you have listed all, write "Done"'
				bot.send_message(message.from_user.id, text, reply_markup = types.ReplyKeyboardRemove())
		elif response == 'Change UTC':
			print('changeutc')
			db.change_status(message.from_user.id, 'ch1wrutc')
			text = 'For meetings I must ensure you are comfortable with time. What is your timezone (UTC)?'
			bot.send_message(message.chat.id, text, reply_markup = types.ReplyKeyboardRemove())
		elif response == 'Change info about myself':
			db.change_status(message.from_user.id, 'ch1wrabout')
			text = 'Tell me a little bit about yourself you want others to know about (in one message)'
			bot.send_message(message.chat.id, text, reply_markup = types.ReplyKeyboardRemove())
		elif response == 'Delete my data':
			db.change_status(message.from_user.id, 'register')
			db.clear_userlist(message.from_user.id)
			db.clear_userinfo(message.from_user.id)
			text = 'Goodbye! I hope you liked using me!'
			bot.send_message(message.chat.id, text, reply_markup = types.ReplyKeyboardRemove())

	elif status == 'wrlanguages':
		if message.text == 'Done' or message.text == "done":
			status = 'wrabout'
			text = 'Last thing - tell me a little bit about yourself you want others to know about'
			bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')
			'''
			status = 'wrtime'
			timetext = 'Great. Now, what are the most comfortable hours for you to chat? Pick them from this list'
			pickhours = types.InlineKeyboardMarkup(row_width = 13)
			bot.send_message(message.chat.id, timetext.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = pickhours)
			'''
		else:
			#need to export data to database
			pass
	elif 'wrabout' in status:
		db.add_about(message.from_user.id, message.text)
		db.change_status(message.from_user.id, 'inmenu')
		if 'ch1' in status:
			text = "I've changed info about you"
			bot.send_message(message.from_user.id, text, reply_markup = start_menu(db.get_role(message.from_user.id)[0][0]))
		else:
			text = 'All done! Now you can use my full power!'
			bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = start_menu(db.get_role(message.from_user.id)[0][0]))
	if 'wrutc' in status:
		try:
			utc = message.text
			if -12 <= int(utc) <= 12:
				db.add_utc(message.from_user.id, int(utc))
				if 'ch1' in status:
					if int(utc) > 0:
						utc = '+' + utc
					db.change_status(message.from_user.id, 'inmenu')
					text = 'Your UTC is changed to ' + utc
					bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = start_menu(db.get_role(message.from_user.id)[0][0]))
				else:
					text = "I've added your timezone(UTC" + utc + ")" 
					bot.send_message(message.from_user.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')
					db.change_status(message.from_user.id, 'wrabout') 
					text = 'Last thing - tell me a little bit about yourself you want others to know about (in one message)'
					bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')	
			else:
				text = 'Timezone offset varies from -12 to 12'
				bot.send_message(message.from_user.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')
			print("no problem")
		except ValueError:
			try:
				utc = int(message.text[3:])
				if message.text[:3] == 'UTC' or message.text[:3] == 'utc':
					if -12 <= utc <= 12:
						db.add_utc(message.from_user.id, utc)
						if 'ch1' in status:
							db.change_status(message.from_user.id, 'inmenu')
							text = 'Your UTC is changed to ' + utc
							bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = start_menu(db.get_role(message.from_user.id)[0][0]))
						else:
							text = "I've added your timezone(UTC" + utc + ")"
							utcconfirm = types.InlineKeyboardMarkup(row_width = 1)
							utcbutton1 = types.InlineKeyboardButton('Confirm', callback_data = 'utcconfirm')
							utcbutton2 = types.InlineKeyboardButton('Cancel', callback_data = 'utccancel')
							utcconfirm.add(utcbutton1, utcbutton2)
							bot.send_message(message.from_user.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = utcconfirm) 
							text = 'Last thing - tell me a little bit about yourself you want others to know about (in one message)'
							bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')	
							db.change_status(message.from_user.id, 'wrabout')
					else:
						text = 'Timezone offset varies from -12 to 12'
						bot.send_message(message.from_user.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')
				else: 
					text = 'Are you talking about UTC time?'
					bot.send_message(message.from_user.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')
				print("mere human")
			except ValueError:
				text = "Please write your timezone in the following formats: 'UTC*timezone*' or simply 'timezone'"
				bot.send_message(message.from_user.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')
#-------------------------------------------------------------------------------------------------------------------------------------------------------
	if 'col_wruniversities' in status:
		if message.text == 'Done' or message.text == 'done':
			if 'ch1' in status:
				db.change_status(message.from_user.id, 'inmenu')
				text = 'All done! You list of universities is changed'
				bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = start_menu('col'))
			else:
				db.change_status(message.from_user.id, 'wrutc')
				text = 'For meetings I must ensure you are comfortable with time. What is your timezone (UTC)?'
				bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')

		else:
			#looking for univs and answers
			queryres = db.output_checked_univ(message.text)
			if len(queryres) == 0:
				text = 'Sorry, I do not know such university, try again'
				bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')

			elif len(queryres) == 1:		
				univ = queryres[0][0]
				if db.check_col_univ(message.from_user.id, univ):
					text = "I've already added that university"
					bot.send_message(message.from_user.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')
				else:
					db.add_col_univ(message.from_user.id, univ)
					text = "I've added " + univ + " to your list. What majors did you take there? When you're done, write 'Next'"		

					#colcancel button
					callback_data = 'colunivcancel' + queryres[0][0]
					colcancel = types.InlineKeyboardMarkup(row_width = 1)
					colcanbut = types.InlineKeyboardButton('Cancel', callback_data = callback_data[:64])
					colcancel.add(colcanbut)

					db.change_status(message.from_user.id, 'col_wrmajors')
					bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = colcancel)

			elif len(queryres) <= 5: 
				text = "Ok, I've found these universities:\n"
				univlist = types.InlineKeyboardMarkup(row_width = len(queryres) + 1)
				for univ_name in queryres:
					callback_data = 'coluniv' + univ_name[0]
					univlist.add(types.InlineKeyboardButton(univ_name[0], callback_data = callback_data[:64]))
				univlist.add(types.InlineKeyboardButton('It is not here...', callback_data = 'cancel'))
				text = text + 'Choose one of them by clicking one of the buttons below'
				bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = univlist)

			else:
				text = 'Sorry, but I know many universities that have similar names. Could you specify?'
				bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')

	elif 'col_wrmajors' in status:
		if message.text == 'Next' or message.text == 'next':
			univ = db.get_col_last_univ(message.from_user.id)[0][0]
			messageids = db.get_col_messageids(message.from_user.id, univ)
			if messageids:
				db.change_status(message.from_user.id, 'col_wruniversities')			
				for messageid in messageids:

					bot.edit_message_reply_markup(chat_id = message.from_user.id, message_id = messageid[0], reply_markup = None)
			else:
				text = 'You must write at least one major'
				bot.send_message(message.from_user.id, text)

		else:
			univ = db.get_col_univ_for_major(message.from_user.id)[0][0]
			major = message.text.upper()
			if db.check_col_major(message.from_user.id, univ, major):
				text = 'You have already told me about this major'
				bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')
			else:
				print(message.message_id)
				print(message.from_user.id)
				print(univ)
				print(major)
				messageid = message.message_id + 1
				db.add_col_searchlist(message.from_user.id, messageid, univ, major)
				callback_data = 'colmajorcancel' + str(db.get_col_id(message.from_user.id, univ, major)[0][0])
				colmajorcancel = types.InlineKeyboardMarkup(row_width = 1)
				colcanbut = types.InlineKeyboardButton('Cancel', callback_data = callback_data[:64])
				colmajorcancel.add(colcanbut)
				text = "I've added " + major + " major for " + univ
				bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = colmajorcancel)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
	if 'hsc_wruniversities' in status:
		if message.text == 'Done' or message.text == 'done':
			if 'ch1' in status:
				db.change_status(message.from_user.id, 'inmenu')
				text = 'All done! Your list of universities is changed!'
				bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = start_menu('hsc'))
			else:
				db.change_status(message.from_user.id, 'wrutc')
				text = 'For meetings I must ensure you are comfortable with time. What is your timezone (UTC)?'
				bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')
		else:
			#looking for univs and answers
			queryres = db.output_checked_univ(message.text)
			if len(queryres) == 0:
				text = 'Sorry, I do not know such university, try again'
				bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')

			elif len(queryres) == 1:		
				univ = queryres[0][0]
				if db.check_hsc_univ(message.from_user.id, univ):
					text = "I've already added that university"
					bot.send_message(message.from_user.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')
				else:
					db.add_hsc_univ(message.from_user.id, univ)
					text = "I've added " + univ + " to your list. What majors are you interested in? You can leave it blank if you want. When you're done, write 'Next'"		

					#hsccancel button
					callback_data = 'hscunivcancel' + queryres[0][0]
					hsccancel = types.InlineKeyboardMarkup(row_width = 1)
					hsccanbut = types.InlineKeyboardButton('Cancel', callback_data = callback_data[:64])
					hsccancel.add(hsccanbut)

					db.change_status(message.from_user.id, 'hsc_wrmajors')
					bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = hsccancel)

			elif len(queryres) <= 5: 
				text = "Ok, I've found these universities:\n"
				univlist = types.InlineKeyboardMarkup(row_width = len(queryres) + 1)
				for univ_name in queryres:
					callback_data = 'hscuniv' + univ_name[0]
					univlist.add(types.InlineKeyboardButton(univ_name[0], callback_data = callback_data[:64]))
				univlist.add(types.InlineKeyboardButton('It is not here...', callback_data = 'cancel'))
				text = text + 'Choose one of them by clicking one of the buttons below'
				bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = univlist)

			else:
				text = 'Sorry, but I know many universities that have similar names. Could you specify?'
				bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')

	elif 'hsc_wrmajors' in status:
		if message.text == 'Next' or message.text == 'next':
			db.change_status(message.from_user.id, 'hsc_wruniversities')
			univ = db.get_hsc_last_univ(message.from_user.id)[0][0]
			messageids = db.get_hsc_messageids(message.from_user.id, univ)
			for messageid in messageids:

				bot.edit_message_reply_markup(chat_id = message.from_user.id, message_id = messageid[0], reply_markup = None)

		else:
			univ = db.get_hsc_univ_for_major(message.from_user.id)[0][0]
			major = message.text.upper()
			if db.check_hsc_major(message.from_user.id, univ, major):
				text = 'You have already told me about this major'
				bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html')
			else:
				print(message.message_id)
				print(message.from_user.id)
				print(univ)
				print(major)
				messageid = message.message_id + 1
				db.add_hsc_searchlist(message.from_user.id, messageid, univ, major)
				callback_data = 'hscmajorcancel' + str(db.get_hsc_id(message.from_user.id, univ, major)[0][0])
				hscmajorcancel = types.InlineKeyboardMarkup(row_width = 1)
				hsccanbut = types.InlineKeyboardButton('Cancel', callback_data = callback_data[:64])
				hscmajorcancel.add(hsccanbut)
				text = "I've added " + major + " major for " + univ
				bot.send_message(message.chat.id, text.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = hscmajorcancel)


@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
	try:
		trigger = call.data
		status = db.get_status(call.from_user.id)[0][0]
		print(trigger)
		if 'setrole' in trigger:
			print('works')
			role = db.get_role(call.from_user.id)[0][0]
			if not role or 'confirm' in trigger:
				if 'col' in trigger:
					db.change_role(call.from_user.id, 'col')
					db.change_status(call.from_user.id, 'col_wruniversities')
					univtext = 'Cool! Can you tell us about colleges you were in? After you have listed all, write "Done"'
					bot.send_message(call.from_user.id, univtext, parse_mode = 'html')
				elif 'hsc' in trigger:
					db.change_role(call.from_user.id, 'hsc')
					db.change_status(call.from_user.id, 'hsc_wruniversities')
					univtext = 'Good. Now, one-by-one, write up all the universities you would like to hear about. After you have listed all, write "Done"' 
					bot.send_message(call.from_user.id, univtext, parse_mode = 'html')			
			else:
				if 'col' in trigger and role == 'hsc':
					confirm = types.InlineKeyboardMarkup()
					button = types.InlineKeyboardButton('Confirm', callback_data = 'confirmsetrolecol')
					confirm.add(button)
					text = "Are you sure? If you change your role I'll have to erase all the data about you and start the registration again"
					bot.send_message(call.from_user.id, text, reply_markup = confirm)
				if 'hsc' in trigger and role == 'col':
					confirm = types.InlineKeyboardMarkup()
					button = types.InlineKeyboardButton('Confirm', callback_data = 'confirmsetrolehsc')
					confirm.add(button)
					text = "Are you sure? If you change your role I'll have to erase all the data about you and start the registration again"
					bot.send_message(call.from_user.id, text, reply_markup = confirm)
		elif "linkme" in trigger:
			if status == 'inmenu':
				if len(db.get_hsc_requests(call.from_user.id)) > 5:
					text = "Sorry, but you should not ask for that much conversations)"
					bot.send_message(call.from_user.id, text)
					#elif requests[call.from_user.id].count(int(trigger[6:])):
				else:
					bot.delete_message(call.message.chat.id, call.message.message_id)
					print(db.get_hsc_requests(call.from_user.id))
					print((trigger[6:],))
					if not (int(trigger[6:]),) in db.get_hsc_requests(call.from_user.id):
						db.add_request(call.from_user.id, trigger[6:])
						userinfo = db.get_userinfo(trigger[6:])[0]
						fullname = ''

						text = "You've asked for a conversation with a " + userinfo[0] + ' ' + userinfo[1]
						bot.send_message(call.message.chat.id, text)
						userinfo = db.get_userinfo(call.from_user.id)[0]
						text = userinfo[0] + ' ' + userinfo[1] + ' has asked for a conversation with you. View all requests to accept the invitation'
						bot.send_message(trigger[6:], text)
		if "approve" in trigger:
			if status == 'inmenu':
				db.del_request(trigger[7:], call.from_user.id)
				db.change_status(call.message.chat.id , 'chatting')
				db.change_status(trigger[7:], 'chatting')
				db.add_comrade(trigger[7:], call.from_user.id) 
				userinfo = db.get_userinfo(trigger[7:])[0]
				text = "I've started the conversation with " + userinfo[0] + userinfo[1] 
				bot.send_message(call.from_user.id, text)
				userinfo = db.get_userinfo(call.from_user.id)[0]
				text = "I've started the conversation with " + userinfo[0] + userinfo[1] 
				bot.send_message(trigger[7:], text)				
				bot.delete_message(call.message.chat.id, call.message.message_id)
		if "reject" in trigger:
			if status == 'inmenu':
				db.del_request(trigger[7:], call.from_user.id)
				userinfo = db.get_userinfo(trigger[7:])[0]
				text = "You've rejected an invitation from " + userinfo[0] + ' ' + userinfo[1] 
				bot.send_message(call.from_user.id, text)
				userinfo = db.get_userinfo(call.from_user.id)[0]
				text = userinfo[0] + ' ' + userinfo[1] + 'has rejected an inviation from you'
				bot.send_message(trigger[7:], text)
				bot.delete_message(call.message.chat.id, call.message.message_id)
		if "canlink" in trigger:
			if status == 'inmenu':
				userinfo = db.get_userinfo(trigger[7:])[0]
				db.del_request(call.from_user.id, trigger[7:])
				bot.send_message(call.message.chat.id, userinfo[0] + ' ' + userinfo[1]  + ' is removed from your requests' )
				bot.delete_message(call.message.chat.id, call.message.message_id)

		elif trigger == 'utcconfirm':
			bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup = None)
			text = 'Now, I need to know the most comfortable hours for you to meet. Choose them from the keyboard down below.'
			hours = types.InlineKeyboardMarkup(row_width = 6)
			for i in range(24):
				hour = types.InlineKeyboardButton(str(i) + ':00', callback_data = 'hour' + str(i))
				hours.add(hour)
			ok = types.InlineKeyboardButton('OK', callback_data = 'hourok')
			hours.add(ok)
			bot.send_message(call.from_user.id, text, parse_mode = 'html', reply_markup = hours)
		elif trigger == 'utccancel':
			bot.delete_message(call.from_user.id, call.message.message_id)
			db.delete_utc(call.from_user.id)
			db.change_status(call.from_user.id, 'wrutc')
		elif 'hour' in trigger:
			if 'hourok' in trigger:
				pass
			elif 'hour*' in trigger:
				pass
			else:
				""""
				for i in range(int(trigger[4:])):
					hour = types.InlineKeyboardButton(str(i) + ':00', callback_data = 'hour' + str(i))
					hours.add(hour)
				hour = types.InlineKeyboardButton(trigger[4:] + ':00', callback_data = '')
				ok = types.InlineKeyboardButton('OK', callback_data = 'hourok')
				hours.add(ok)
				bot.send_message(call.from_user.id, text, parse_mode = 'html', reply_markup = hours)
				"""
				print(call['message']['messageid'])

		elif trigger == 'cancel':
			bot.delete_message(call.from_user.id, call.message.message_id)
		elif 'colmajorcancel' in trigger:
			db.del_col_major_searchlist(trigger[14:])
			bot.delete_message(call.from_user.id, call.message.message_id)
		elif 'colunivcancel' in trigger:
			univ = trigger[13:]
			messageids = db.get_col_messageids(call.from_user.id, univ)
			if status == 'col_wrmajor' and univ in db.get_col_last_univ(call.from_user.id)[0][0]:
				db.change_status(call.from_user.id, 'col_wruniversities')
			db.del_col_univ(call.from_user.id, trigger[13:])
			db.del_col_searchlist(call.from_user.id, trigger[13:])
			bot.delete_message(call.from_user.id, call.message.message_id)
			for messageid in messageids:
				bot.delete_message(call.from_user.id, messageid[0])

		elif 'coluniv' in trigger:
			if 'col_wruniversities' in status:
				if len(call.data) == 64:
					univ = db.output_checked_univ(call.data[7:])[0][0]
				else:
					univ = call.data[7:]
				if db.check_col_univ(call.from_user.id, univ):
					text = "I've already added that university"
					bot.send_message(call.from_user.id, text.format(call.from_user, bot.get_me()), parse_mode = 'html')
				else:
					db.add_col_univ(call.from_user.id, univ)
					text = "I've added " + univ + " to your list. What majors did you take there? When you're done, write 'Next'"

					#colcancel button
					callback_data = 'colunivcancel' + univ
					colcancel = types.InlineKeyboardMarkup(row_width = 1)
					colcanbut = types.InlineKeyboardButton('Cancel', callback_data = callback_data[:64])
					colcancel.add(colcanbut)	

					db.change_status(call.from_user.id, 'col_wrmajors')
					bot.send_message(call.from_user.id, text.format(call.from_user, bot.get_me()), parse_mode = 'html', reply_markup = colcancel)

		elif 'hscmajorcancel' in trigger:
			db.del_hsc_major_searchlist(trigger[14:])
			bot.delete_message(call.from_user.id, call.message.message_id)
		elif 'hscunivcancel' in trigger:
			univ = trigger[13:]
			messageids = db.get_hsc_messageids(call.from_user.id, univ)
			if status == 'hsc_wrmajors' and univ in db.get_hsc_last_univ(call.from_user.id)[0][0]:
				db.change_status(call.from_user.id, 'hsc_wruniversities')
			db.del_hsc_univ(call.from_user.id, trigger[13:])
			db.del_hsc_searchlist(call.from_user.id, trigger[13:])
			bot.delete_message(call.from_user.id, call.message.message_id)
			for messageid in messageids:
				bot.delete_message(call.from_user.id, messageid[0])

		elif 'hscuniv' in trigger:
			if 'hsc_wruniversities' in status:
				if len(call.data) == 64:
					univ = db.output_checked_univ(call.data[7:])[0][0]
				else:
					univ = call.data[7:]
				if db.check_hsc_univ(call.from_user.id, univ):
					text = "I've already added that university"
					bot.send_message(call.from_user.id, text.format(call.from_user, bot.get_me()), parse_mode = 'html')
				else:
					db.add_hsc_univ(call.from_user.id, univ)
					text = "I've added " + univ + " to your list. What majors are you interested in? You can leave it blank if you want. When you're done, write 'Next'"

					#hsccancel button
					callback_data = 'hscunivcancel' + univ
					hsccancel = types.InlineKeyboardMarkup(row_width = 1)
					hsccanbut = types.InlineKeyboardButton('Cancel', callback_data = callback_data[:64])
					hsccancel.add(hsccanbut)	

					db.change_status(call.from_user.id, 'hsc_wrmajors')
					bot.send_message(call.from_user.id, text.format(call.from_user, bot.get_me()), parse_mode = 'html', reply_markup = hsccancel)

	except Exception as e:
		print(repr(e))

#RUN 
bot.polling(none_stop = True)

"""
REPLY BUTTONS
markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
ch1 = types.KeyboardButton('Стеклый')
ch2 = types.KeyboardButton('Как трезвышко')
markup.add(ch1, ch2)
bot.send_message(message.chat.id, 'Какдиллак?', parse_mode = 'html', reply_markup = markup) 

INLINE BUTTONS
menu = types.InlineKeyboardMarkup(row_width = 2)
ch1 = types.InlineKeyboardButton('Da ti che', callback_data = 'oi')
ch2 = types.InlineKeyboardButton('Blyaaa', callback_data = 'mama prishla')
markup.add(ch1, ch2)

WHY NOT
#remove inline buttons
bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'same text', reply_markup = None)
# show alert
bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = 'what are you watching at')


inline call output

{'game_short_name': None, 
'chat_instance': '2529530939244595459', 
'id': '1886761320562710446', 
'from_user': {'id': 439295852, 'is_bot': False, 'first_name': 'Denis', 'username': None, 'last_name': 'Son', 'language_code': 'ru', 'can_join_groups': None, 'can_read_all_group_messages': None, 'supports_inline_queries': None}, 
'message': {'content_type': 'text', 'message_id': 153, 'from_user': <telebot.types.User object at 0x00000000033AC0C8>, 'date': 1596391615, 'chat': <telebot.types.Chat object at 0x00000000033AC708>, 'forward_from': None, 'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None, 'forward_date': None, 'reply_to_message': None, 'edit_date': None, 'media_group_id': None, 'author_signature': None, 'text': 'Which one of them are you?', 'entities': None, 'caption_entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'animation': None, 'dice': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None,
			'json': {'message_id': 153, 
					 'from': {'id': 1378870721, 'is_bot': True, 'first_name': 'CollegeTalk', 'username': 'collegetalkbot'}, 
					 'chat': {'id': 439295852, 'first_name': 'Denis', 'last_name': 'Son', 'type': 'private'}, 
					 'date': 1596391615, 
					 'text': 'Which one of them are you?',
					 'reply_markup': {'inline_keyboard': [[{'text': 'High school student', 'callback_data': 'hsc'}, {'text': 'College student', 'callback_data': 'col'}]]}}}, 
'data': 'hsc', 'inline_message_id': None}
"""

"""
{'content_type': 'text', 'message_id': 1294, 'from_user': {'id': 439295852, 'is_bot': False, 'first_name': 'Denis', 'username': None, 'last_name': 'Son', 'language_code': 'ru', 'can_join_groups': None, 'can_read_all_group_messages': None, 'supports_inline_queries': None}, 'date': 1597917524, 'chat': {'id': 439295852, 'type': 'private', 'title': None, 'username': None, 'first_name': 'Denis', 'last_name': 'Son', 'all_members_are_administrators': None, 'photo': None, 'description': None, 'invite_link': None, 'pinned_message': None, 'permissions': None, 'slow_mode_delay': None, 'sticker_set_name': None, 'can_set_sticker_set': None}, 'forward_from': None, 'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None, 'forward_date': None, 
'reply_to_message': None, 
'edit_date': None, 'media_group_id': None, 'author_signature': None, 'text': '654', 'entities': None, 'caption_entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'animation': None, 'dice': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None, 'json': {'message_id': 1294, 'from': {'id': 439295852, 'is_bot': False, 'first_name': 'Denis', 'last_name': 'Son', 'language_code': 'ru'}, 'chat': {'id': 439295852, 'first_name': 'Denis', 'last_name': 'Son', 'type': 'private'}, 'date': 1597917524, 'text': '654'}}

{'content_type': 'text', 'message_id': 1296, 'from_user': {'id': 439295852, 'is_bot': False, 'first_name': 'Denis', 'username': None, 'last_name': 'Son', 'language_code': 'ru', 'can_join_groups': None, 'can_read_all_group_messages': None, 'supports_inline_queries': None}, 'date': 1597917534, 'chat': {'id': 439295852, 'type': 'private', 'title': None, 'username': None, 'first_name': 'Denis', 'last_name': 'Son', 'all_members_are_administrators': None, 'photo': None, 'description': None, 'invite_link': None, 'pinned_message': None, 'permissions': None, 'slow_mode_delay': None, 'sticker_set_name': None, 'can_set_sticker_set': None}, 'forward_from': None, 'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None, 'forward_date': None, 
'reply_to_message': {'content_type': 'text', 'message_id': 1293, 'from_user': <telebot.types.User object at 0x00000000033BED08>, 'date': 1597917481, 'chat': <telebot.types.Chat object at 0x00000000033BEF88>, 'forward_from': None, 'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None, 'forward_date': None, 'reply_to_message': None, 'edit_date': None, 'media_group_id': None, 'author_signature': None, 'text': 'All done! Now you can use my full power!', 'entities': None, 'caption_entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'animation': None, 'dice': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None, 'json': {'message_id': 1293, 'from': {'id': 1378870721, 'is_bot': True, 'first_name': 'CollegeTalk', 'username': 'collegetalkbot'}, 'chat': {'id': 439295852, 'first_name': 'Denis', 'last_name': 'Son', 'type': 'private'}, 'date': 1597917481, 'text': 'All done! Now you can use my full power!'}}, 
'edit_date': None, 'media_group_id': None, 'author_signature': None, 'text': '654', 'entities': None, 'caption_entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'animation': None, 'dice': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None, 'json': {'message_id': 1296, 'from': {'id': 439295852, 'is_bot': False, 'first_name': 'Denis', 'last_name': 'Son', 'language_code': 'ru'}, 'chat': {'id': 439295852, 'first_name': 'Denis', 'last_name': 'Son', 'type': 'private'}, 'date': 1597917534, 'reply_to_message': {'message_id': 1293, 'from': {'id': 1378870721, 'is_bot': True, 'first_name': 'CollegeTalk', 'username': 'collegetalkbot'}, 'chat': {'id': 439295852, 'first_name': 'Denis', 'last_name': 'Son', 'type': 'private'}, 'date': 1597917481, 'text': 'All done! Now you can use my full power!'}, 'text': '654'}}
"""
