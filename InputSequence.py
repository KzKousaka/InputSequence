# -*- coding: utf-8 -*-
"""
    SublimeInputSequence.py(InputSequenceCommand)
    http://cosing-plus.com/
    
    This plug-in will output a sequence numbers in
    mulutiple caret position.
    
    ver 2.0.0b - 2014.5.5
"""

import sublime, sublime_plugin
import re,string

class InputSequenceCommand(sublime_plugin.TextCommand):

	# constant numbers
	CH_CODE_LITTLE_A = ord(u'a')
	CH_CODE_LITTLE_Z = ord(u'z')
	CH_CODE_CAP_A = ord(u'A')
	CH_CODE_CAP_Z = ord(u'Z')
	CH_CODE_0 = ord(u'0')
	CH_CODE_9 = ord(u'9')

	OVERFLOW_AUTO   = 0 # 自動ケタ合わせ
	OVERFLOW_ZERO	= 1 # ケタ調整無し（ゼロ埋め)

	OP_MODE_ADD = 0
	OP_MODE_SUM = 1
	OP_MODE_MUL = 2
	OP_MODE_DIV = 3

	WT_NUM     = 10
	WT_ALPHA   = 26
	WT_x       = 16
	WT_o       = 8
	WT_b       = 2

	
	DT_NUM 	           = 0
	DT_NUM_ADD         = 1
	DT_CAP_ALPHA       = 2
	DT_CAP_ALPHA_ADD   = 3
	DT_LITLE_ALPHA     = 4
	DT_LITLE_ALPHA_ADD = 5
	DT_X               = 6
	DT_X_ADD           = 7
	DT_x               = 8
	DT_x_ADD           = 9
	DT_d               = 10
	DT_d_ADD           = 11
	DT_o               = 12
	DT_o_ADD           = 13
	DT_b               = 14
	DT_b_ADD           = 15

	FMT_DEFAULT  = 0
	FMT_X        = 1
	FMT_x        = 2
	FMT_d        = 3
	FMT_o        = 4
	FMT_b        = 5
	FMT_A        = 6
	FMT_a        = 7


	trimRef = {ord(' '):'', ord('\t'):'', ord('\r'):'', ord('\n'):''}

	def make_str(self, params):

		if params['num'] < 0 :
			return ""
		if params['num'] > 0xFFFFFFFFFFFFFFFF :
			return ""
		
		i = 0
		dt_len = len(params['digits_type'])
		insart_str = ""
		c = ""
		num = params['num']
		d = 0
		dt_a = 0
		p = 0

		while i < dt_len:
			dt = params['digits_type'][i]
			c = ""
			if dt == self.DT_NUM or dt == self.DT_NUM_ADD:
				p = 10
				d = int(num % p)
				c = chr(self.CH_CODE_0 + d)
				dt_a = self.DT_NUM_ADD
			
			elif dt == self.DT_CAP_ALPHA or dt == self.DT_CAP_ALPHA_ADD:
				p = 26
				d = int(num % p)
				c = chr(self.CH_CODE_CAP_A + d)
				dt_a = self.DT_CAP_ALPHA_ADD
			
			elif dt == self.DT_LITLE_ALPHA or dt == self.DT_LITLE_ALPHA_ADD:
				p = 26
				d = int(num % p)
				c = chr(self.CH_CODE_LITTLE_A + d)
				dt_a = self.DT_LITLE_ALPHA_ADD
			
			elif dt == self.DT_b or dt == self.DT_b_ADD:
				p = 2
				d = int(num % p)
				c = chr(self.CH_CODE_0 + d)
				dt_a = self.DT_b_ADD
			
			elif dt == self.DT_o or dt == self.DT_o_ADD:
				p = 8
				d = int(num % p)
				c = chr(self.CH_CODE_0 + d)
				dt_a = self.DT_o_ADD

			elif dt == self.DT_X or dt == self.DT_X_ADD:
				p = 16
				d = int(num % p)
				c = chr((self.CH_CODE_0 if d < 10 else self.CH_CODE_CAP_A-10 )+ d)
				dt_a = self.DT_X_ADD

			elif dt == self.DT_x or dt == self.DT_x_ADD:
				p = 16
				d = int(num % p)
				c = chr((self.CH_CODE_0 if d < 10 else self.CH_CODE_LITTLE_A-10 )+ d)
				dt_a = self.DT_x_ADD

			num = (num - d) / p

			if i+1 or dt_len or params['overflow'] or self.OVERFLOW_AUTO and d == 0:
				insart_str = ''.join((c, insart_str))

			i += 1

			if i == dt_len and params['overflow'] == self.OVERFLOW_AUTO and num > 0:
				dt_len += 1
				params['digits_type'].append(dt_a)

		
		return insart_str


	def increment(self, params):
		op   = params['operation']
		coef = params['coefficient']

		if op == self.OP_MODE_ADD:
			params['num'] += coef

		elif op == self.OP_MODE_SUM:
			params['num'] -= coef

		elif op == self.OP_MODE_MUL:
			params['num'] *= coef

		elif op == self.OP_MODE_DIV:
			params['num'] -= params['num'] % 2
			params['num'] /= coef

		return params


	def insert(self, edit, params):

		# get caret position
		for region in self.view.sel():

			if params['period'] is not None :
				if params['num'] > params['period']:
					if not params['repeat'] :
						return
					
					# insert_str = params['begin_num']
					params['num']        	= params['num_init']
					params['digits_type']   = params['digits_init'][:]

			insert_str = self.make_str(params)
					
			if region.empty():	# non select word
				self.view.insert(edit, region.a, insert_str)
			
			else:				# select word
				self.view.replace(edit, region, insert_str)

			if params['step_cnt'] >= params['step_num']-1:
				params['step_cnt'] = 0
				num = params['num']
				params = self.increment(params)
				if num <= 0 and params['num'] <= 0:
					return
			else:
				params['step_cnt'] += 1



	def create_params(self, word):

		params = {
			'overflow'    : self.OVERFLOW_AUTO,
			'operation'   : self.OP_MODE_ADD,
			'coefficient' : 1,
			'num'         : None,
			'num_init'    : 0,
			'digits_num'  : 0,
			'digits_type' : [],
			'digits_init' : [],
			'step_num'    : 1,
			'step_cnt'    : 0,
			'period'      : None,
			'repeat'      : True,
			'repeat_init' : None,
		}

		#print("input  = "+word)
		word = word.translate(self.trimRef)
		if word == "":
			word = "0"
		#print("trimed = " + word);

		# search format signiture
		pattern = re.compile( r'(%[\+#0-9]*?[abdoxAX])|([\+\-\*\/\,][0-9]+)|([\.\~\@][0-9]+)|(\$?[a-zA-Z0-9]+)' )
		#pattern = re.compile( r'(%[abdoxAX])|([\+\-\*\/\,]?[0-9]+)|([\.\~\@\$]?[0-9a-zA-Z]+)|([a-zA-Z][a-zA-Z0-9]*)' )
		iterator = pattern.finditer(word)

		keys = []
		
		num_val		= None
		fmt_type	= None
		digits_type = None
		digits_num	= 0

		#パラメータをチェック
		for match in iterator:
			val=match.group()
			print("#",val)
			keys.append(val)

			cmd = val[0]

			if '0' <= cmd <= '9'\
				or 'a' <= cmd <= 'z'\
				or 'A' <= cmd <= 'Z'\
				or '$' == cmd:

				num_val = val
				
			elif cmd == '%':

				i = 1
				digits_param = ""
				digits_type = self.DT_NUM
				digits_num = 1
				while i < len(val) :
					cmd = val[i]
					if '0' <= cmd <= '9':
						digits_param+=cmd
					elif cmd == 'a':
						fmt_type	= self.FMT_a
						digits_type = self.DT_LITLE_ALPHA
						break
					elif cmd == 'A':
						fmt_type	= self.FMT_A
						digits_type = self.DT_CAP_ALPHA
						break
					elif cmd == 'b':
						fmt_type	= self.FMT_b
						digits_type = self.DT_b
						break
					elif cmd == 'd':
						fmt_type	= self.FMT_d
						digits_type = self.DT_NUM
						break
					elif cmd == 'o':
						fmt_type	= self.FMT_o
						digits_type = self.DT_o
						break
					elif cmd == 'x':
						fmt_type	= self.FMT_x
						digits_type = self.DT_x
						break
					elif cmd == 'X':
						fmt_type	= self.FMT_X
						digits_type = self.DT_X
						break
					i+=1
				#print("***", len(digits_param))
				if len(digits_param) > 0 :
					params['overflow'] = self.OVERFLOW_ZERO
					digits_num = int(digits_param)
				else:
					params['overflow'] = self.OVERFLOW_AUTO

				#print("***", params['overflow'])

			else: 	# 演算コマンド、制御コマンドの場合,数が正常に入力できるかチェック
					# 入力できなかった場合、コマンド無効
				try:
					val_int = int(val.replace(cmd, ''))

					if cmd == '+':
						params["operation"]   = self.OP_MODE_ADD
						params["coefficient"] = val_int

					elif cmd=='-':
						params["operation"]   = self.OP_MODE_SUM
						params["coefficient"] = val_int

					elif cmd=='*':
						params["operation"]   = self.OP_MODE_MUL
						params["coefficient"] = val_int

					elif cmd=='/' and val_int != 0:
						params["operation"]   = self.OP_MODE_DIV
						params["coefficient"] = val_int

					elif cmd==',':
						params["step_num"]    = val_int

					elif cmd=='.':
						params["period"]      = val_int
						params["repeat"]      = False

					elif cmd=='~':
						params["period"]      = val_int
						params["repeat"]      = True

					elif cmd=='@':
						params["repeat_init"] = val_int
				except: # 例外ここまで
					pass

		#print('test',num_val)
		#初期化数値を計算
		if num_val is not None :
			cmd = num_val[0]
			if cmd != '$':
				params["overflow"]  = self.OVERFLOW_ZERO
			

			else:
				num_val = num_val.replace(cmd,'')

			p = 1
			params['num'] = 0

			for i in range(len(num_val)-1,-1,-1):
				c = num_val[i]

				if len(params['digits_type']) == 0 or params['overflow'] == self.OVERFLOW_AUTO:
					add = 1
				else:
					add = 0

				if fmt_type is not None:

					if fmt_type == self.FMT_X or fmt_type == self.FMT_x :
						if '0' <= c <= '9':
							num = ord(c) - self.CH_CODE_0
						elif 'a' <= c <= 'f':
							num = ord(c) - self.CH_CODE_LITTLE_A + 10
						elif 'A' <= c <= 'F':
							num = ord(c) - self.CH_CODE_CAP_A + 10
						else:
							num = 0
						pp = self.WT_x

					elif fmt_type == self.FMT_o :
						if '0' <= c <= '7':
							num = ord(c) - self.CH_CODE_0
						else:
							num = 0
						pp = self.WT_o
					elif fmt_type == self.FMT_d :
						if '0' <= c <= '9':
							num = ord(c) - self.CH_CODE_0
						else:
							num = 0
						pp = self.WT_NUM
					elif fmt_type == self.FMT_b :
						if '0' <= c <= '1':
							num = ord(c) - self.CH_CODE_0
						else:
							num = 0
						pp = self.WT_b
					elif fmt_type == self.FMT_a :
						if 'a' <= c <= 'z':
							num = ord(c) - self.CH_CODE_LITTLE_A
						elif 'A' <= c <= 'Z':
							num = ord(c) - self.CH_CODE_CAP_A
						else:
							num = 0
						pp = self.WT_ALPHA
					
					params['digits_type'].append(digits_type + add)

				else:
					if '0' <= c <= '9':
						num = ord(c) - self.CH_CODE_0
						pp = self.WT_NUM
						params['digits_type'].append(self.DT_NUM+add)

					elif 'a' <= c <= 'z':
						pp = self.WT_ALPHA
						num = ord(c) - self.CH_CODE_LITTLE_A
						params['digits_type'].append(self.DT_LITLE_ALPHA+add)
					elif 'A' <= c <= 'Z':
						pp = self.WT_ALPHA
						num = ord(c) - self.CH_CODE_CAP_A
						params['digits_type'].append(self.DT_CAP_ALPHA)

				#print("&&&", c, num, p)
				c = num * p
				params['num'] += c
				p *= pp


		if params['num'] is None :
			params['num'] = 0
			#print("---", fmt_type, digits_type)

			if fmt_type is None :
				params['digits_type'] = [self.DT_NUM_ADD]
			else:
				params['digits_type'] = [digits_type+1]
			
		print("dnum", digits_num, len(params['digits_type']))

		while len(params['digits_type']) < digits_num :
			if len(params['digits_type']) == 0 or params['overflow'] == self.OVERFLOW_AUTO:
				add = 1
			else:
				add = 0
			params['digits_type'].append(digits_type + add)


		params['digits_init'] = params['digits_type'][:]
		params['num_init']    = params['num']\
			if params['repeat_init'] is None else params['repeat_init']

		print('keys',params)
		return params


	# When there is word input
	def inputted_word(self, edit, word):
		if word == "":
			return
		self.erase = True

		#check sequence type
		params = self.create_params(word)
		self.insert(edit,params)
		#print(params)
		return

	def undo(self):
		if self.erase:
			sublime.set_timeout(lambda: self.view.run_command('undo'), 0)

	def on_change(self, abbr):
		if not abbr:
			abbr = '$'
		if not abbr and self.erase:
			self.undo()
			self.erase = False
			return

		self.undo()
		
		# restart process with arguments
		def inner_insert():
			self.view.run_command(self.name(), dict(panel_input=abbr))

		sublime.set_timeout(inner_insert, 0)
		

	# callback 'show_input_panel'
	def on_done(self, abbr):
		pass
		

	# entry
	def run(self, edit, panel_input=None):
		self.erase = False

		if panel_input is None:
			v = self.view.window().show_input_panel(
				'Sequence Format:', '',
				self.on_done,
				self.on_change,
				self.undo)
		else:
			# try:
			self.inputted_word(edit, panel_input)
			# except:
				# pass
			return
