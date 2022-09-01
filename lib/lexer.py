import sys
import re
import copy




class lexer :


################################################
# Public {{{1
################################################

    def getToken(self): #{{{2
    # The public interface for getting tokens. Handles EOF flags, Line Buffer updating, and
    # UID/header computation. It's basically the pre-configuration of the whole token retireval and
    # the while loop in the private function of the same name. It's basically stablizes the starting
    # point for the coming while loop.

        #----------- Initiate Token Variable ------------ #

        # Initiate or clear the token in preperation for the next the next token
        self.token = {
            'uid'        : None,  #  Unique Identification Number
            'name'       : None,  #  Token Name
            'match'      : None,  #  String that was matched
            'z_txt'      : None,  #  'z' of match in txt
            'z_line'     : None,  #  'z' of match on line
            'e_line'     : None,  #  'e' of match on line
            'LineNumber' : None,  #  line number where match was found
            'type'       : None,  #  token type
            'EOF'        : False, #  EOF
        }

        if not self.f_EOF :
        # Keeps the token from doing any more work when the EOF flag was set after the last token
        # retrieval. This is different than the EOF flag of the token of which serves as the actual
        # return value to tell the parser that or whoever that the EOF was reached and no more
        # tokens can be found. Henceforth, this if statment is only ever false after the last token
        # reached the EOF, for the EOF flag of the lexer is set after this statment, and thus, this
        # statment is to ensure that any further attemtps to get a token after the last one will
        # give a token will null values and it's own EOF flag set


            #----------- LINEBUFFER CHECK ------------ #

            self.TokenNumber += 1  # incrment token number


            self.__verbose(0, "Getting Token %d " % self.TokenNumber, False)
            self.__verbose(0, "-" * 80)
            self.__verbose(1, "---POS: line:%-4s z:%-3s size:%-3s abs:%s" % (self.LineNumber, self.z_line, self.SizeOfLineBuffer, self.z_txt))
            self.__verbose(1, "---TEXT BUFFER    :%s" % self.LineBuffer)
            self.__verbose(1, "---TEXT BUFFER(@z):%s" % self.LineBuffer[self.z_line:])

            if self.SizeOfLineBuffer == self.z_line:
            # Line Buffer is empty

                self.__UpdateLineBuffer()
                # Fill line buffer with the next line if it exists

                if self.TokenNumber != 1 :
                # set the EOL flag, unless the token number is 1. When the lexer is initiated the
                # linebuffer will be empty by default, but this is not the EOL.

                    self.f_EOL = True

                self.__verbose(1, "!! TEXT BUFFER IS EMPTY")
                self.__verbose(1, "---POS: line:%-4s z:%-3s size:%-3s abs:%s" % (self.LineNumber, self.z_line, self.SizeOfLineBuffer, self.z_txt))
                self.__verbose(1, "---TEXT BUFFER    :%s" % self.LineBuffer)
                self.__verbose(1, "---TEXT BUFFER(@z):%s" % self.LineBuffer[self.z_line:])

            self.__verbose(1, "---CURRENT headers LIST: %s" % str(self.headers))


            #----------- COMPUTE UID FROM HEADER ------------ #

            if len(self.headers) :
            # headers list is not empty

                self.token['uid'] = self.headers[-1]
                # set token UID to last head in header list

            else :
                # headers list is empty

                self.token['uid'] = '0'
                # set uid to '0'

            self.__getToken()
            # The meat of the token getting. It's basically a while loop. It doesn't return the
            # token but sets the token variable of the lexer.

        else :
        # EOF FLAG was set, this only means that the last token attempt reached the end of the file.

            self.token['EOF'] = True
            # EOF flag of token to let the parser or whoever know to stop asking for more tokens

            self.__verbose(0,"END OF FILE REACHED")

        return self.token







################################################
# PRIVATE  {{{1
################################################

    def __init__(self, txt, LexerConfig, f_VerboseEnabled=False) : #{{{2


        #----------- TXT ------------ #
        self.txt          = txt
        self.z_txt        = 0


        #----------- LINE BUFFER ------------ #
        ##- Line Buffer
        self.LineBuffer        = ''
        self.z_line            = 0
        self.SizeOfLineBuffer  = 0


        #----------- COUNT TRACKERS ------------ #
        self.TokenNumber  = 0
        self.LineNumber   = 1


        #----------- FLAGS ------------ #
        self.f_EOF            = False
        self.f_EOL            = False
        self.f_VerboseEnabled = f_VerboseEnabled


        #----------- REGEX FOR SKIPPING WHITESPACE ------------ #
        self.re_newline               = re.compile('\n')
        self.re_whitespace            = re.compile('([^\S\n]+)|(\n)')
        self.re_NonNewline_whitespace = re.compile('[^\S\n]+')


        #----------- TOKENSTATES AND TOKEN REGEX COMPILATION ------------ #
        self.TokenStates = LexerConfig
        for uid in self.TokenStates :
            tokenState = self.TokenStates[uid]
            for n in '12' :
                if  tokenState['pat' + n] :
                    uncompiled_regex = tokenState['pat' + n]
                    compiled_regex   = re.compile( uncompiled_regex )
                    tokenState['pat' + n]  = compiled_regex


        #----------- DEFAULT TOKEN STATES ------------ #
        self.DefaultTokenStates = copy.deepcopy(self.TokenStates)


        #----------- TOKEN HISTORY ------------ #
        self.TokenHistory = {
            0: [
                {
                    'uid': '-1'
                }
            ]
        }
        for uid in self.TokenStates.keys() :
            pntr = uid.split('.')
            lvl = len(pntr)
            if lvl not in self.TokenHistory :
                self.TokenHistory[lvl] = [
                    {
                        'uid': '-1'
                    }
                ]


        #----------- HEADERS ------------ #
        self.headers      = []




    def __getToken(self) :#{{{2
    # The loop I was talking about. It cannot loop forever, it either gets a match or throws an
    # error. The match property of the token is set by the post match, and once you reach post match
    # you have already have a token to return and after returning from post match the program will
    # exit out of the while loop

        while not self.token['match'] :
        # Token Match has not been found

            uid        = self.token['uid']     # UID of current token
            tokenState = self.TokenStates[uid] # token state

            pat1 = "/" + tokenState['pat1'].pattern +"/"if tokenState['pat1'] else None  #verbose
            pat2 = "/" + tokenState['pat2'].pattern +"/" if tokenState['pat2'] else None #verbose
            self.__verbose(2, "Trying with token %s %s %s %s" % (uid, tokenState['name'], str(pat1),str(pat2)))
            self.__verbose(3, "...Checking if Enabled: ",False)


            #----------- ENABLED? ------------ #

            if tokenState['enabled'] :
            # Token is enabled

                pat, n = self.__GetPattern()
                # get pattern and pattern number for token

                self.__verbose(0, "ENABLED!")
                patString = pat1 if n == 1 else pat2 #verbose
                self.__verbose(3, "using pat %s" % str(patString))
                self.__verbose(3, "...Checking if Valid: ", False)


                #----------- VALID TO TRY? ------------ #

                if self.__isValid() :
                # Token is Valid to try

                    TokenMatch = None
                    # Declare Token match varible. This is done just so we can send a none value
                    # into the post match for containtainers than are EOL terminating

                    self.__verbose(0, "VALID!")
                    self.__verbose(3, "...Matching: ", False)


                    #----------- MATCH FOR EOL FLAG ------------ #

                    if self.f_EOL and tokenState['f_eolt'] and tokenState['f_c'] :
                    # Token is EOL terminanting and the lexer EOL flag is set

                        self.__PostMatch(TokenMatch)
                        # DO post match with null match object. The post match is done regardless of
                        # the lexer position, so certain soubroutines will be disabled. A match for
                        # a token in the current line buffer will be done next time the lexer is
                        # called

                        self.__verbose(0, "SUCCESS!")


                    #----------- MATCH IN LINE BUFFER ------------ #

                    else :

                        TokenMatch = pat.match(self.LineBuffer, self.z_line)
                        # Begin Match

                        if TokenMatch:
                        # Match Succesful

                            self.__PostMatch(TokenMatch)
                            # Do post match with match object

                            self.__verbose(0, "SUCCESS!")


                        else: # verbose
                            self.__verbose(0, "FAIL!")
                else: # verbose
                    self.__verbose(0, "INVALID!")
            else :# verbose
                self.__verbose(0, "DISABLED!")


            #----------- NO MATCH ------------ #

            if not self.token['match'] :
            # match failed.

               self.__ed_Optional()
               # check if token had optional ed condition, and set them off as if the token was
               # matched

               self.__TryAnotherToken()
               # try another token. This is where the system will throw an error if it could not
               # resolve a token match. If there are no EOL terminating tokens for the lexer EOL
               # flag it will be resolved here and the current line buffer will be used for matching




    def __isValid(self, uid=None) :#{{{2

        retu = False

        if not uid :
            uid = self.token['uid']

        tokenState = self.TokenStates[uid]

        if tokenState['enabled'] :

            if tokenState['pat1'] and (tokenState['pat2'] or tokenState['f_eolt']) :
            # bicontainer

                if tokenState['f_c'] :
                # active

                    if not (tokenState['f_eolt'] != self.f_EOL):
                    #Active EOL terminating token at EOL or Active non EOL terminating token not at
                    # EOL

                        retu = True

                else :
                # not active

                    retu = True

            elif tokenState['f_c'] and not tokenState['pat1']:
            # delim

                retu = True

            else:
            # regular

                retu = True

        return retu




    def __computeType(self, uid=None) :#{{{2

        Type = None

        if not uid :
            uid = self.token['uid']

        tokenState = self.TokenStates[uid]

        if tokenState['pat1'] and (tokenState['pat2'] or tokenState['f_eolt']) :
        # bicontainer

            if tokenState['f_c'] :
            # active

                Type = 'bicontainer-end'

            else :
            # not active

                Type = 'bicontainer-start'
        elif tokenState['f_c'] and not tokenState['pat1']:
        #delim

            Type = 'delim'

        else:
        #regular

            Type = 'regular'

        return Type




    def __GetPattern(self, uid=None) : #{{{2

        if not uid :
            uid = self.token['uid']

        tokenState = self.TokenStates[uid]

        if tokenState['f_c'] :
            pat = tokenState['pat2']
            n = 2

        else :
            pat = tokenState['pat1']
            n = 1

        return pat, n




    def __UpdateLineBuffer(self) :#{{{2
    # When the line buffer is empty it has to be filled with the next line if exists. To do this it
    # matches whitespace (blank spaces and newlines) until it reaches a non-white space character or
    # the End of the file. The last newline found determines the start of the linebuffer, any
    # trailing blank spaces determine the 'z_line' or where the lexer will start looking for tokens
    # within the line buffer. Then the next newline is searched for, its positon determines the
    # length of the line buffer or its end within the txt.
    #
    # The behavior of this subroutine when the EOF is reached is dependent on whether or not the
    # file ends in a new line or not. The difference being that in the former the last line is
    # always an empty line, while this is not the case with the latter. This difference will
    # manifest is an incrment of the linecount and z_txt before the EOF is reached as the EOF is
    # only reached as far as this subroutine is concerned when the resulting linebuffer size and
    # z_line are equal


        #----------- POSITION PRESETS ------------ #

        self.z_line = 0              # Put 'z_line' at start of line buffer
        self.SizeOfLineBuffer = None # Length of new line buffer is unkown, set it to 'None'

        self.__verbose(2, "...Filling Line Buffer With the Next Line")
        self.__verbose(3, "----------------------------POS: line:%-4s z:%-3s size:%-3s abs:%s" % (self.LineNumber, self.z_line, self.SizeOfLineBuffer, self.z_txt))


        #----------- SKIP WHITSPACES ------------ #

        WhiteSpaceMatch = self.re_whitespace.match( self.txt, self.z_txt )
        # Match whitspace including newline at 'z_txt' of txt. The first match will always be a
        # newline (unless the End Of File was reaced) since trailing non-newline whitespaces would
        # of been skipped elsewhere in the lexer.

        while ( WhiteSpaceMatch ) :
        # If match, update the lexer positions, and keep matching until no match if found indicating
        # The next non-whitespace character or the EOF.

            if WhiteSpaceMatch.group(2) :
            # A newline was matched

                self.LineNumber += 1      # Increment line cnt
                self.z_line      = 0      # Set 'z_line' to start of line

                self.z_txt  += 1
                # Increment z_txt by 1, moving it past the newline found an at the start of
                # the next line. The line buffer does not incororate newlines since they are
                # skipped; this is why the 'z_line' could be set at 0 and not be on a newline.

                self.__verbose(3, "!! Next Line Found..........",False)
                self.__verbose(0, "POS: line:%-4s z:%-3s size:%-3s abs:%s" % (self.LineNumber, self.z_line, self.SizeOfLineBuffer, self.z_txt))


            else:
            # Leading spaces were found

                z_txt_OfLeadingSpaces = WhiteSpaceMatch.span()[0] # z_txt of leading space(s)
                e_txt_OfLeadingSpaces = WhiteSpaceMatch.span()[1] # e_txt of leading space(s)

                self.z_txt   = e_txt_OfLeadingSpaces
                # Set 'z_txt' after the leading space(s)

                self.z_line += (e_txt_OfLeadingSpaces - z_txt_OfLeadingSpaces)
                # Set 'z_line' after the leading space(s). To nomralize the e_txt of the spaces we
                # subtract from it its z_txt, so that both the z_line and the z_txt of the leading
                # spacing are refference to 0.

                self.__verbose(3, "!! leading space(s) found...",False)
                self.__verbose(0, "POS: line:%-4s z:%-3s size:%-3s abs:%s" % (self.LineNumber, self.z_line, self.SizeOfLineBuffer, self.z_txt))

            WhiteSpaceMatch = self.re_whitespace.match( self.txt, self.z_txt )
            # Look for more matches


        #----------- FIND SIZE OF LINE BUFFER ------------ #

        self.__verbose(2, "...Seaching for the beginning of the next line")

        NextLineMatch = self.re_newline.search( self.txt, self.z_txt )
        # Search for the next  newline, so we know where the current line ends

        if NextLineMatch:
        # Found the next newline

            z_txt_OfNextNewLine = NextLineMatch.span()[0]
            # z_txt of the next newline

            z_line_MaxChange = (z_txt_OfNextNewLine - self.z_txt)
            self.SizeOfLineBuffer = z_line_MaxChange + self.z_line
            # The size of the line buffer is computed by finding the max possible z_line which is
            # the current z_txt (corresponds to the first position of a non leading space in the
            # line buffer) subtracted by the z_txt of the next new line. This gives us a normalized
            # max of how much the z_line can change in the current buffer. Since the line buffer
            # includes leading spaces the z_line can be non-zero meaning to find the actual length
            # of the linebuffer we need to add the z_line and the max z_line change to get the
            # actual size of the line buffer.

            self.__verbose(3, "!! Found........................",False)
            self.__verbose(0, "POS: line:%-4s z:%-3s size:%-3s abs:%s" % (self.LineNumber, self.z_line, self.SizeOfLineBuffer, self.z_txt))

        else :
        # Last line of the file

            self.SizeOfLineBuffer = len( self.txt[ self.z_txt : ] ) + self.z_line
            # Since we are on the last line, the line buffer size is just the length from z_txt to
            # the last position in the txt plus the z_line to account for the leading whitespaces
            # missed.

            self.__verbose(3, "!! Not found, last line reached")

            if self.SizeOfLineBuffer == self.z_line :
            # Length of line buffer is equal to the z_line

                self.f_EOF = True # End OF File flag

                self.__verbose(2, "!! End Of File reached")


        #----------- FILL THE LINE BUFFER WITH THE NEW POSITIONS ------------ #

        z_txt_OfLineBuffer = self.z_txt - self.z_line
        # The position where the linbuffer starts in the txt. The z_line is subtracted
        # from the z_txt to include the leading spaces that were skipped

        e_txt_OfLineBuffer = z_txt_OfLineBuffer + self.SizeOfLineBuffer
        # The position just after the last character of the line buffer in the txt. Found by just
        # adding the the starting postiong of the line buffer in the text with its size.

        self.LineBuffer = self.txt[ z_txt_OfLineBuffer : e_txt_OfLineBuffer ]
        # Fill the line buffer setting it to slice in the txt.




    def __TryAnotherToken(self) : #{{{2
    # the current token failed, try another one. If we can't find another one try whitespace. If
    # that fails see if the EOL flag is set. If the EOL flag is set the lexer basically went through
    # all the tokens as specified by the header and none of them had an EOL terminating flag set, so 
        if self.__TryChild() :
            return 1

        elif self.__TryNextSybling() :
            return 1

        elif self.__TryWhiteSpace() :
            return 1

        elif self.f_EOL:

            #----------- RESETING TOKEN UID TO LAST HEADER ------------ #
            # The lexer was freaking out trying out all these childs and syblings, turns out it was
            # just an un claimed EOL flag, so reset the uid to the last header

            if len(self.headers) > 0 :
                self.__verbose(4, "!! No tokens had an 'EOL terminating' condition")
                self.__verbose(4, "...reseting UID to last header and begin matching in the line buffer")

                self.token['uid'] = self.headers[-1]

            else:
                self.token['uid'] = '0'

            self.f_EOL = False

        else:
        # The Lexer did its best but in the end it could not achieve its task. The Lexer did not
        # fail you, YOU failed it! Shame on you for giving the lexer and impossible task. Check your
        # lexer_config and try again.

            sys.exit('Error: no match')




    def __ed_Optional(self) : #{{{2
    # Some tokens have an 'ed_optnl' flag wich just means run the 'ed' condition even when it
    # doesn't match

        self.__verbose(4, "__ed_Optional()")

        uid  = self.token['uid']
        tokenState = self.TokenStates[uid]


        #----------- DO THE ED THING ------------ #

        if tokenState['ed_optnl'] :
            self.__EdCheck()




    def __EdCheck(self) : #{{{2
    # Every token has a 'ed_enbl' and 'ed_dsbl' that when the token is matched, tells the lexer to
    # enable and disable these tokens repsectively

        self.__verbose(4, "__EdCheck()")

        uid        = self.token['uid']     # UID of current token
        tokenState = self.TokenStates[uid] # token state


        #----------- ENABLE TOKENS ------------ #

        for UID in tokenState['ed_enbl']:
            self.TokenStates[UID]['enabled'] = True
            self.__verbose(5, "...enabling %s" % UID)


        #----------- DISABLE TOKENS ------------ #

        for UID in tokenState['ed_dsbl']:
            self.TokenStates[UID]['enabled'] = False
            self.__verbose(5, "...disabling %s" % UID)




    def __SwitchcaseCheck(self) : #{{{2
    # Check if 'sc_en' flag is enabled if so disable all other tokens in 'sc' besides the current
    # token

        uid = self.token['uid']            # UID of current token
        tokenState = self.TokenStates[uid] # token state

        self.__verbose(4, "__SwitchcaseCheck()")
        self.__verbose(5, "checking sc_en...", False)


        #----------- DISABLE ALL OTHER TOKENS ------------ #

        if tokenState['sc_en'] :

            self.__verbose(0, "TRUE")

            for UID in tokenState['sc']:
                if UID != uid :
                    self.TokenStates[UID]['enabled'] = False

                    self.__verbose(5, "...disabling %s" % UID)

        else: #verbose
            self.__verbose(0, "FALSE")




    def __CfCompute(self) : #{{{2v
    # Only bicontainer tokens will have their f_c flag changed, besides that all containers with
    # f_c flag set will have the state of all their child tokens reset to default.

        uid = self.token['uid']            # UID of current token
        tokenState = self.TokenStates[uid] # token state

        self.__verbose(4, "__CfCompute()")
        self.__verbose(5, "...checking f_c flag...", False)

        if tokenState['f_c'] :
        # Is token an active container?

            self.__verbose(0, "...TRUE")
            self.__verbose(5, "...checking token is a bicontainer...", False)

            if tokenState['pat1']:
            # Is token an bicontainer?

                self.__verbose(0, "...TRUE")
                self.__verbose(4, "---current headers: %s" % str(self.headers))
                self.__verbose(4, "...popping headers")


                #----------- SET F_C FLAG TO FALSE ------------ #

                tokenState['f_c'] = False
                # set f_c to false, since when it is true when a bicontainer is matched, it means we
                # have reached its end and it is no longer active


                #----------- POPPING HEADERS ------------ #

                head_uid = None
                while head_uid != self.token['uid'] :
                    head_uid = self.headers[-1]
                    self.headers.pop()
                    if len(self.headers) == 0 :
                        break

                self.__verbose(4, "---updated headers: %s" % str(self.headers))


            #----------- RESETING CHILD TOKEN STATES ------------ #
            lvl = len(uid)
            for UID in self.TokenStates.keys() :
               if not len(UID) <= lvl and UID[:lvl] == uid :
               # Token Children are determined by tokens with UID lvls higher than the token and a
               # UID matching the parent UID at the parent UID's lvl
               #    EX:
               #        Token = 4.3.5    Parent
               #        Token = 4        Not a child, UID lvl not greater than parent token
               #        Token = 4.6.2.4  Not a child, UID does not match parent at parent lvl
               #        Token = 4.3.5.3  This is a child

                   self.TokenStates[UID] = copy.deepcopy(self.DefaultTokenStates[UID])
                   self.__verbose(4, "...resetting %s" % UID)


        elif not tokenState['f_c'] and (tokenState['pat2'] or tokenState['f_eolt']) :
        # Elif token is a container if a f_c flag set to false. THe second part of the boolean
        # captures EOL terminating bicontainers. A delim container can never get this condition to
        # be true for its f_c flag is always set. Appending the header just tells the lexer where to
        # start and where it is restricted to. You cannot match tokens that are outside of an active
        # bicontainer

            self.__verbose(0, "...FALSE")
            self.__verbose(4, "---current headers: %s" % str(self.headers))
            self.__verbose(4, "...appending headers")


            #----------- APPENDING HEADERS ------------ #

            self.headers.append( tokenState['uid'] )
            tokenState['f_c'] = True

            self.__verbose(4, "---updated headers: %s" % str(self.headers))




    def __GiveCompute(self, TokenMatch) : #{{{2
    #If the token does not have a 'f_give' flag set, update the line buffer positions so that the
    # lexer starts looking for the next token after the last match. When the 'f_give' is set it
    # looks in the same position that the last match was found.

       uid  = self.token['uid']           # UID of current token
       tokenState = self.TokenStates[uid] # token state

       self.__verbose(4, "__GiveCompute()")
       self.__verbose(5, "...checking (f_giv flag & f_EOL)...",False)

       if not tokenState['f_give'] and not self.f_EOL :
       # Check 'f_give' flag, also check for EOL lexer flag, we don't want an EOL terminating token
       # chaning the linebuffer position because its token retrieval is irrelevant of the line
       # buffer and only depends on the lexer EOL flag

           e_line_OfTokenMatch  = TokenMatch.span()[1]
           z_line_OfTokenMatch  = TokenMatch.span()[0]
           self.z_line         += (e_line_OfTokenMatch-z_line_OfTokenMatch)
           self.z_txt          += (e_line_OfTokenMatch-z_line_OfTokenMatch)
           # Just adding the difference b/w the e_line and z_line of the match both of the 'z' values
           # will put the lexer after the last character of the token match.

           self.__verbose(0, "FALSE")
           self.__verbose(5, "...updating POS")
           self.__verbose(5, "---POS: line:%-4s z:%-3s size:%-3s abs:%s" % (self.LineNumber, self.z_line, self.SizeOfLineBuffer, self.z_txt))

       else: #verbose
           self.__verbose(0, "TRUE")
           self.__verbose(5, "...POS remains unchanged")




    def __TryChild(self) : #{{{2
    # See if token has a child, if so make that the new token. The subroutine checks the existance of
    # the UID of the first child if the token has childs

        self.__verbose(4,"...looking for chilren")

        success  = False
        uid      = self.token['uid']
        tokState = self.TokenStates[uid]

        if tokState['f_c'] :
            pntr = self.__uid2pntr(uid)
            pntr.append(0)
            UID = self.__pntr2uid(pntr)

            if UID in self.TokenStates.keys() :
                success            = True
                self.token['uid']  = UID
                self.token['name'] = self.TokenStates[UID]['name']

                self.__verbose(5,"SUCCESS: child exits at " + UID)

        return success




    def __TryNextSybling(self) : #{{{2
    # Incrment the number of the last lvl of the token UID to get the next sybling if it exists
        self.__verbose(4,"...looking for next sybling")

        success  = False
        uid      = self.token['uid']
        tokState = self.TokenStates[uid]

        if not tokState['f_c'] and tokState['pat1'] :

            pntr = self.__uid2pntr(uid)
            pntr[-1] += 1
            UID = self.__pntr2uid(pntr)

            if UID in self.TokenStates.keys() :

                success            = True
                self.token['uid']  = UID
                self.token['name'] = self.TokenStates[UID]['name']

                self.__verbose(5,"SUCCESS: sybling exits at " + UID)

        return success




    def __TryWhiteSpace(self) : #{{{2
    # If child and sybling don't exists this is the last line of defence: match non-newline
    # whitespace at current lexer position

        self.__verbose(4,"...trying whitespace")

        success                     = False
        NonNewline_whitespace_Match = self.re_NonNewline_whitespace.match( self.LineBuffer, self.z_line)

        if NonNewline_whitespace_Match :

            success = True
            e_line_OfNonNewline_whitespace = NonNewline_whitespace_Match.span()[1]
            z_line_OfNonNewline_whitespace = NonNewline_whitespace_Match.span()[0]
            length                         = e_line_OfNonNewline_whitespace - z_line_OfNonNewline_whitespace

            self.__verbose(5,"SUCCESS: whitespace at " + str(self.z_txt) + " with length of " + str(length))

            self.z_line += (length)
            self.z_txt  += (length)


            #----------- RESETING TOKEN UID TO LAST HEADER ------------ #
            # The lexer was freaking out trying out all these childs and syblings, turns out it was
            # just a whitespace, so reset the uid to the last header

            if len(self.headers) > 0 :
                self.token['uid'] = self.headers[-1]
            else:
                self.token['uid'] = '0'

        return success




    def __MaxCheck(self) : #{{{2
    # Compute the absolute, consecutive, and consecutive group match counts of
    #   every token and disable token if the max of either of them have been
    #   reached. When a 'container-end' token is reached all of its token
    #   children will have their match counts reset to 0.

        uid      = self.token['uid']     # UID of token
        tokState = self.TokenStates[uid] # State of token

        pat2undefined = not tokState['pat2']      # Is pattern 2 not defined?
        notEOLt       = not tokState['f_eolt']    # Is f_EOLt flag not  set?
        regular_token = pat2undefined and notEOLt # Is token a regular?

        self.__verbose(4, "__MaxCheck()")

        if tokState['f_c'] or regular_token :
        # Container flag is  set or token is regular

            self.__verbose(5, "---Max Register:           %s %s %s" % (str(tokState['max'][0]),str(tokState['max'][1]),str(tokState['max'][2])))
            self.__verbose(5, "---Count Register:         %d %d %d" % (tokState['cnt'][0],tokState['cnt'][1],tokState['cnt'][2]))


            maxreg         = tokState['max'] # Max register
            absMax         = maxreg[0]       # Absolute max
            cnsctvMax      = maxreg[1]       # Consecutive max
            cnsctvgrpMax   = maxreg[2]       # Consecutive Group max

            tokState['cnt'][0] += 1      # Increment absolute match count
            absCnt = tokState['cnt'][0]  # Absolute match count


            #----------- ABSOLUTE MAX ------------ #

            if absMax is not None :
            # Absolute max is defined

                if absMax == absCnt :
                # Absolute max reached

                    tokState['enabled'] = False # Disable token

                    self.__verbose(5, "!! Absolute Match Max Reached")
                    self.__verbose(5, "...disabling token")


            pntr = self.__uid2pntr(uid) # Pntr of token  computed from UID
            lvl  = len(pntr)            # Token lvl

            prvlvlUID = self.TokenHistory[lvl][-1]['uid']
            # UID of previous token with the  same lvl


            #----------- CONSECUTIVE MAX ------------ #

            if prvlvlUID == uid  and absCnt > 1:
            # Previous token on the same lvl had the same UID and the absolute match count is
            # greater than 1 meaning the previous UID was in the current parent contaner

                tokState['cnt'][1] += 1
                # Increment concecutive match count

                cnsctvCnt = tokState['cnt'][0]
                # Concecutive match count

                if cnsctvMax is not None :
                # Concecutive match max is defined

                    if cnsctvMax == cnsctvCnt :
                    # Consecutive match max reached

                        tokState['enabled'] = False # Disable token

                        self.__verbose(5, "!! Consecutive Match Max Reached")
                        self.__verbose(5, "...disabling token")



            #----------- CONSECUTIVE GROUP MAX ------------ #

            if self.TokenNumber > 1  :
            # Not the first token asked for

                if  prvlvlUID != uid and absCnt > 1 :
                # Previous token on the same lvl did not have the same UID and the absolute match
                # count is greater than 1 meaning the previous UID was in the current parent

                    tokState['cnt'][2] += 1
                    # Increment Consecutive group match count

                    if cnsctvgrpMax is not None :
                    # Consecutive Group match count

                        cnsctvgrpCnt = tokState['cnt'][0]
                        # Consecutive Group match max is defined

                        if cnsctvgrpMax == cnsctvgrpCnt :
                        # Consecutive Group match max reached

                            tokState['enabled'] = False # Disable token

                            self.__verbose(5, "!! Consecutive Group Match Max Reached")
                            self.__verbose(5, "...disabling token")

            self.__verbose(5, "---Updated Count Register: %d %d %d" % (tokState['cnt'][0],tokState['cnt'][1],tokState['cnt'][2]))

        else : #verbose
            self.__verbose(5, "!! Token is is not regular or active bicontainer")




    def __PostMatch(self, TokenMatch) : #{{{2

        uid        = self.token['uid']
        tokenState = self.TokenStates[uid]

        self.token['type']  = self.__computeType()
        # get token type


        #----------- POST MATCH ROUTINES ------------ #

        TokenMatch = self.__OverMatch(TokenMatch)
        self.__EdCheck()
        self.__SwitchcaseCheck()
        self.__MaxCheck()
        self.__CfCompute()

        #----------- INSERT TOKEN INFORMATION ------------ #

        self.token['name']    = tokenState['name']

        if not self.f_EOL :
            self.token['z_txt']       = self.z_txt
            self.token['z_line']      = self.z_line
            self.token['LineNumber']  = self.LineNumber
            self.token['e_line']      = TokenMatch.span()[1]
            self.token['match']       = TokenMatch.group()
        else :
        # You just matched an EOL terminating token. It has a z_line and e_line of zero for it's
        # match, but its z_txt is is 1 minus the start of the line buffer pos in the txt because the
        # newline actually takes up a character, we just skip it when updating the line buffer

            self.token['z_txt']       = self.z_txt - self.z_line - 1
            self.token['z_line']      = 0

            self.token['LineNumber']  = self.LineNumber - 1
            # Even thought the line buffer is already at the next line, we are still checking if any
            # tokens terminate at the end of the last line so deincrement that line number

            self.token['e_line']      = 0
            self.token['match']       = '\\n'

        if self.f_EOF :
            self.token['EOF'] = True


        #----------- TOKEN HISTORY ------------ #
        lvl = len(uid.split('.'))
        self.TokenHistory[0].append(copy.deepcopy(self.token))
        self.TokenHistory[lvl].append(copy.deepcopy(self.token))


        #----------- DO WE UPDATE THE LINE BUFFER? ------------ #
        self.__GiveCompute(TokenMatch)


        #----------- EOL FLAG ------------ #
        self.f_EOL = False if self.f_EOL else False


        self.__verbose(2,"Token: %s " % self.token)




    def __OverMatch(self, TokenMatch) : #{{{2
    # Search for parent container token matches in the line buffer to
    # determined if they are located within the span of the  token match. If so
    # change the token e_line to the smallest z_line of the parent container
    # tokens.

        uid        = self.token['uid']
        tokenState = self.TokenStates[uid]
        pntr       = self.__uid2pntr(uid)

        if not (tokenState['f_eolt'] and self.f_EOL) :

            if len(pntr) > 1:

                e_line = TokenMatch.span()[1]
                # 'e' of token match in the line buffer

                self.__verbose(4, "__OverMatch() at  %s e_line:%s" % (uid, str(e_line)) )
                self.__verbose(5, "pntr = %s" % str(pntr) )
                self.__verbose(5, "...popping pntr..." , False)

                pntr.pop()
                # Remove the last item of the pntr, corresponds with getting the pntr of the
                # parent token

                self.__verbose(0, str(pntr) )

                #----------- LOOK FOR PARENT TOKEN TO OVERMATCH AND OVERMATCH------------ #
                while len(pntr) > 0 :
                # Find the 'z' of every parent token in the line buffer

                    puid = self.__pntr2uid( pntr )
                    # UID of parent token from its pntr

                    self.__verbose(5, "...checking %s validity..." % puid, False )

                    if self.__isValid( puid ) :
                    # Valididty check on parent token

                        self.__verbose(0, "TRUE" )

                        pat, n = self.__GetPattern( puid )
                        # Get pattern and pattern number according to the state of the parent token

                        self.__verbose(5, "...matching  %s with pat %s..." % (puid, str(pat)), False)

                        string = self.LineBuffer # Line Buffer
                        start  = self.z_line     # 'z' of token match in the line buffer

                        ParentMatch = pat.search(string, start)
                        # Match object of the parent token


                        #----------- OVERMATCH FOUND ------------ #

                        if ParentMatch :
                        # If match was successful

                            z_lineOfParent = ParentMatch.span()[0]
                            # 'z' of parent token match in the line buffer

                            self.__verbose(0, "SUCCESS" )
                            self.__verbose(5, "matched at Parent Container z_line: " + str(z_lineOfParent))

                            if e_line > z_lineOfParent:
                            # Overmatch Found: 'z' of parent token match is less than 'e' of token
                            # match in the line buffer

                                e_line = z_lineOfParent
                                # set 'e' of token match to 'e' of parent token in the line buffer

                                self.__verbose(5, "!! Parent Container's z_line less than e_line: " + str(e_line))
                                self.__verbose(5, "e_line is now : " + str(e_line))

                        else : #verbose
                            self.__verbose(0, "FAIL" )
                    else :  #verbose
                        self.__verbose(0, "False" )


                    #-----------  GET NEXT PARENT TOKEN TO OVERMATCH------------ #

                    if uid == self.headers[-1] :
                    # Cannot go to parents beyond an a parent token that is an active biocontainer

                        self.__verbose(5, "!! Active Bicotainer, Cannot Pop Pntr Any Further" )

                        break # finish looking for overmatches

                    self.__verbose(5, "...popping pntr..." , False)

                    pntr.pop()
                    # Remove the last item of the pntr, corresponds with getting the pntr of the parent token.

                    self.__verbose(0, "...%s" % str(pntr) )


                #-----------  OVERMATCH POST PROCESS ------------ #

                if e_line != TokenMatch.span()[1] :
                # An overmatch was found

                    if self.z_line != e_line :

                        self.__verbose(5, "!! smaller e_line of %s found" % str(e_line) )
                        self.__verbose(5, "...generating new match object with the LineBuffer truncated at e_line:%s" % str(e_line) )

                        pat, n = self.__GetPattern(uid)
                        # Get pattern and pattern number according to the state of the parent token

                        string = self.LineBuffer[:e_line] 
                        # Line buffer, truncated at the smallest 'z' of an overmatch found

                        start = self.z_line
                        # 'z' of token match in the line buffer

                        TokenMatch = pat.match(string, start) 
                        # Recompute the token match object with truncated line buffer

                    else:
                    # Overmatch consumed the entire token match

                       puid = self.__pntr2uid(pntr)
                       # UID of the parent token in the overmatch

                       error_msg = ("ERROR: token %s consumed the" # Error Message
                                    "entire match of token %s"
                                   )

                       sys.exit(error_msg % (puid, uid))           # Throw Error

                else :
                    self.__verbose(5, "!! smaller e_line not found" )

        return TokenMatch # Return new Token Match






################################################
# UTILITILES  {{{1
################################################

    def __verbose(self, tabn, string, newline=True) : #{{{2
        if self.f_VerboseEnabled :
            tabs = "    " * tabn
            if newline :
                print(tabs + string)
            else :
                print(tabs + string, end='')




    def __uid2pntr(self, uid) :#{{{2
        pntr = uid.split('.')
        pntr = [int(i) for i in pntr]
        return pntr




    def __pntr2uid(self, pntr) : #{{{2
        pntr = [str(i) for i in pntr]
        uid = '.'.join(pntr)
        return uid






################################################
# DOC {{{1
################################################
pod = """

========================
== TERMS
line buffer
txt buffer
z
e
span
newline
match
search
Overmatching
whitespace
child
sybling
token
token definition
max
absolute match
consecutive match
group matches
ed
sc
sc_en
type
absolute position
headers
delim
regular
bicotainer
bicontainer start
bicontainer end
container
container_flag
eol flag
eof flag
reset
active
pattern 1
pattern 2
tnct
ed_optnl
f_give
tokenState
pntr
token lvl
top lvl
uid
name
eol_t
f_ed_enbl
ed_enbl
ed_dsbl
valid
enabled




"""
