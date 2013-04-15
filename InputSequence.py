"""
    InputSequenceCommand
    - Twitter: @kope_88
    
    This plug-in will output a sequence numbers in
    mulutiple caret position.
    
    ver 1.1 - 2013.04.15
    """

import sublime, sublime_plugin

class InputSequenceCommand(sublime_plugin.TextCommand):
    
	CH_CODE_SMALL_A = ord(u'a')
	CH_CODE_SMALL_Z = ord(u'z')
	CH_CODE_BIG_A = ord(u'A')
	CH_CODE_BIG_Z = ord(u'Z')
	CH_CODE_0 = ord(u'0')
	CH_CODE_9 = ord(u'9')
    
    
	# return '0' or 'A' or 'a' or '(SPACE)' or 0
	def check_char(self, ch) :
		ch_num = ord(ch)
		if self.CH_CODE_0         <= ch_num and self.CH_CODE_9       >= ch_num :
			return self.CH_CODE_0
		elif self.CH_CODE_BIG_A   <= ch_num and self.CH_CODE_BIG_Z   >= ch_num :		# big character
			return self.CH_CODE_BIG_A
		elif self.CH_CODE_SMALL_A <= ch_num and self.CH_CODE_SMALL_Z >= ch_num :		# small character
			return self.CH_CODE_SMALL_A
		
		return 0
    
    
    
	def on_done(self, word):
        
		if word == "":
			return;
        
		# check sequence type
		charlist = list(word)
		digits = len(charlist)
        
		# set decriment flag
		decriment = False
		overflow = False
		if charlist[0] == u'-' :
			decriment = True
			charlist = charlist[1:digits]
			digits -= 1
		elif charlist[0] == u'$' :
			overflow = True
			charlist = charlist[1:digits]
			digits -= 1
        
		# set digits type list
		digitTypes = []
		counter = []
		for ch in charlist :
			ch_base = self.check_char(ch)
			digitTypes.append(ch_base)
			counter.append(ord(ch) - ch_base)
        
		edit = self.view.begin_edit();
        
		# get caret position
		for region in self.view.sel():
            
			# set insert text
			insert_str = u''.join(charlist)
            
			if region.empty():	# non select word
				self.view.insert(self.edit, region.a, insert_str)
			
			else:				# select word
				self.view.replace(edit, region, insert_str)
            
			# incriment word
			for i in range(digits-1, -1 , -1) :
                
				carry = False
                
				# set ch_max
				if digitTypes[i] == self.CH_CODE_0:
					ch_max = self.CH_CODE_9 - self.CH_CODE_0
				elif digitTypes[i] == self.CH_CODE_BIG_A:
					ch_max = self.CH_CODE_BIG_Z - self.CH_CODE_BIG_A
				elif digitTypes[i] == self.CH_CODE_SMALL_A:
					ch_max = self.CH_CODE_SMALL_Z - self.CH_CODE_SMALL_A
				else:
					continue
                
				# incriment or decriment
				counter[i] += 1 if not decriment else -1
                
				if counter[i] < 0 :
					counter[i] = ch_max
					carry = True
				elif counter[i] > ch_max :
					counter[i] = 0
					carry = True
                
				charlist[i] =  chr(digitTypes[i] + counter[i])
                
				#Carry decision
				if not carry:
					break
                
                
				#Add judgment of digits
				if i == 0 and overflow:
					digitTypes.insert(0, digitTypes[0] if digitTypes[0]!=0 else self.CH_CODE_0);
					counter.insert(0, 1 if digitTypes[0] == self.CH_CODE_0 else 0);
					charlist.insert(0,chr(digitTypes[0]+counter[0]))
					digits+=1
					break
        
        
        
		self.view.end_edit(edit)
    
    
    
	def run(self, edit):
		self.edit = edit
		self.view.window().show_input_panel('Sequence Type (alphabet or number):', '$0', self.on_done, None,None)
