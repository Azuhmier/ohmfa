import sys
import re
import copy

class lexer :




# Public {{{1
################################################
    def get_token(self): #{{{2

        self.token = {
            'controller_uid'  : None,
            'controller_type' : None,
            'controller_name' : None,
            'type'            : None,
            'match'           : None,
            'line_number'     : None,
            'z_line'   : None,
            'e_line'   : None,
            'z_data'          : None,
        }

        self.__get_token()

        return self.token




# PRIVATE  {{{1
################################################
    def __init__(self, data, config, verbose=False) : #{{{2

        #----------- TOKEN CONTROLLERS ------------ #
        self.token_uid         =0
        self.token_controllers =config
        self.__setup_token_controllers()

        #----------- DEFAULT TOKEN CONTROLLERS ------------ #
        self.Default_token_controllers =copy.deepcopy(self.token_controllers)

        #----------- TOKEN HISTORY ------------ #
        self.token_history ={}
        self.__setup_token_history()

        #----------- HEADERS ------------ #
        self.headers =[]

        #----------- LINE BUFFER ------------ #
        self.data                =data
        self.z_data              =0
        self.line_buffer         =''
        self.line_number         =1
        self.z_line       =0
        self.size_of_line_buffer =0

        #----------- FLAGS ------------ #
        self.f_EOF   =False
        self.f_EOL   =False
        self.verbose =verbose

        #----------- REGEX FOR SKIPPING WHITESPACE ------------ #
        self.re_newline =re.compile('\n')
        self.re_spaces  =re.compile('[^\S\n]+')




    def __get_token(self) : #{{{2
        self.token_uid +=1
        self.token['controller_uid'] =self.__get_head()
        self.__check_line_buffer()

        while self.token['match'] is None :
            if self.f_EOF :
                self.token_uid               =-1
                self.token['controller_uid'] ='-1'
                break

            controller_uid =self.token['controller_uid']
            controller =self.token_controllers[controller_uid]

            if controller['enabled'] :
                if self.__is_token_EOL_terminating(controller_uid) == self.f_EOL :
                    pattern =self.__get_pattern(controller_uid)
                    token_match =pattern.match(self.line_buffer, self.z_line)
                    if token_match :
                        self.__post_match(token_match)
            ## No Match
            if self.token['match'] is None :
               self.__ed_trigger_on_no_match_too()
               if not self.__try_child() :
                   if not self.__try_next_sybling() :
                       if self.f_EOL :
                           self.__check_line_buffer()
                           self.token['controller_uid'] = self.__get_head()
                       else :
                           sys.exit('Error: Next token could not be obtained.')




    def __check_line_buffer(self) : #{{{2
        self.__skip_spaces()
        if self.size_of_line_buffer == self.z_line :
            if (self.f_EOL) or (self.token_uid == 1) :
                 self.f_EOL =False
                 self.__update_line_buffer()
            else :
                self.f_EOL =True




    def __skip_spaces(self) : #{{{2
        spaces_match = self.re_spaces.match( self.line_buffer, self.z_line )
        if spaces_match :
            z_line_spaces  =spaces_match.span()[0]
            e_line_spaces  =spaces_match.span()[1]
            self.z_line    =e_line_spaces
            self.z_data          +=(e_line_spaces - z_line_spaces)




    def __update_line_buffer(self) : #{{{2
        self.size_of_line_buffer =None
        newline_match =self.re_newline.match(self.data, self.z_data)
        if newline_match :
            self.line_number   +=1
            self.z_line  =0
            self.z_data        +=1
            next_line_buffer_match =self.re_newline.search(self.data, self.z_data)
            if next_line_buffer_match:
                z_data_of_next_line_buffer =next_line_buffer_match.span()[0]
                self.size_of_line_buffer =(z_data_of_next_line_buffer - self.z_data)
            else :
                self.size_of_line_buffer =len(self.data[ self.z_data:])
                if self.z_line == self.size_of_line_buffer  :
                    self.f_EOF =True

            e_data =(self.z_data + self.size_of_line_buffer)
            self.line_buffer =self.data[self.z_data:e_data]

            self.__skip_spaces()
            if self.size_of_line_buffer == self.z_line :
                 self.__update_line_buffer()




#---------------------------- POST MATCH ----------------------------#
    def __post_match(self, token_match) : #{{{2
        controller_uid =self.token['controller_uid']
        controller =self.token_controllers[controller_uid]

        ## Overmatch
        token_match =self.__overmatch(token_match)

        ## Assign Information to The Token
        self.token['controller_name'] =controller['name']
        self.token['controller_type'] =self.__compute_controller_type(controller_uid)
        self.token['type']            =self.__compute_token_type(controller_uid)
        if not self.f_EOL :
            self.token['match']         =token_match.group()
            self.token['line_number']   =self.line_number
            self.token['z_line'] =self.z_line
            self.token['e_line'] =token_match.span()[1]
            self.token['z_data']        =self.z_data
        else :
            self.token['match']         =token_match.group()
            self.token['line_number']   =self.line_number
            self.token['z_line'] =0
            self.token['e_line'] =0
            self.token['z_data']        =(self.z_data - self.z_line - 1)

        self.__ed()
        self.__sc_controllers()
        self.__max()
        self.__f_active_container()
        self.__f_do_not_update_line_buffer_for_match(token_match)

        ## Update Token History
        lvl =len(controller_uid.split('.'))
        self.token_history[0].append(copy.deepcopy(self.token))
        self.token_history[lvl].append(copy.deepcopy(self.token))




    def __overmatch(self, token_match) : #{{{2
        controller_uid  =self.token['controller_uid']
        controller      =self.token_controllers[controller_uid]
        pntr            =self.__controller_uid2pntr(controller_uid)
        new_token_match = None

        if (not self.f_EOL) and (len(pntr) > 1) :
            e_line     =token_match.span()[1]
            new_e_line_buffer =e_line
            pntr.pop()

            while len(pntr) > 0 :

                parent_controller_uid =self.__pntr2controller_uid(pntr)
                parent_pattern        =self.__get_pattern(parent_controller_uid)
                parent_match          =parent_pattern.search(self.line_buffer, self.z_line)

                if (parent_match) and (not self.__is_token_EOL_terminating(parent_controller_uid)) :
                    parent_z_line_buffer =parent_match.span()[0]
                    if new_e_line_buffer > parent_z_line_buffer :
                        new_e_line_buffer =parent_z_line_buffer

                if parent_controller_uid == self.headers[-1] : # parent_controller_uid is the current head
                    break
                pntr.pop()

            if new_e_line_buffer != e_line :
                if self.z_line != new_e_line_buffer :
                    pattern = self.__get_pattern(controller_uid)
                    new_token_match =pattern.match(self.line_buffer[:new_e_line_buffer], self.z_line)
                    if not new_token_match :
                        print(self.z_line)
                        print(self.line_buffer[:new_e_line_buffer])
                        print(new_e_line_buffer)
                        print(parent_match)
                        print(token_match)
                        sys.exit('Error')
                    else :
                        token_match = new_token_match
                else :
                   parent_controller_uid =self.__pntr2controller_uid(pntr)
                   error_msg =("ERROR: token %s consumed the entire match of token %s")
                   sys.exit(error_msg % (parent_controller_uid, controller_uid))

        return token_match




    def __max(self) : #{{{2
        controller_uid =self.token['controller_uid']
        controller =self.token_controllers[controller_uid]
        if not self.__is_inactive_bi_container(controller_uid) :
            cnt  =controller['cnt']
            maxx =controller['max']
            ## Absolute Max
            cnt[0] += 1
            if (maxx[0] is not None) and (maxx[0] == cnt[0]) :
                controller['enabled'] =False
            ## Compute previous controller_uid of the same level from token history
            pntr =self.__controller_uid2pntr(controller_uid)
            lvl =len(pntr)
            prv_lvl_controller_uid =self.token_history[lvl][-1]['controller_uid']
            ## Consecutive Max
            if maxx[1] is not None:
                if (prv_lvl_controller_uid == controller_uid) and (cnt[0] > 1):
                    cnt[1] += 1
                    if (maxx[1] is not None) and (maxx[1] == cnt[1]) :
                        controller['enabled'] =False
            ## Consecutive Group Max
            if self.token_uid > 1  :
                if maxx[2] is not None:
                    if  (prv_lvl_controller_uid != controller_uid) and (cnt[0] > 1) :
                        cnt[2] += 1
                        if (maxx[2] is not None) and (maxx[2] == cnt[2]) :
                                controller['enabled'] =False




    def __ed(self) : #{{{2
        controller_uid =self.token['controller_uid']
        controller =self.token_controllers[controller_uid]
        if not self.__is_active_bi_container(controller_uid) :
            for controller_uid in controller['ed_enable_these_controllers']:
                self.token_controllers[controller_uid]['enabled'] =True
            for controller_uid in controller['ed_disable_these_controllers']:
                self.token_controllers[controller_uid]['enabled'] =False




    def __sc_controllers(self) : #{{{2
        controller_uid =self.token['controller_uid']
        controller =self.token_controllers[controller_uid]
        if not self.__is_active_bi_container(controller_uid) :
            if controller['sc_enabled'] :
                for controller_uid in controller['sc_controllers'] :
                    if controller_uid != controller_uid :
                        self.token_controllers[controller_uid]['enabled'] =False




    def __f_active_container(self) : #{{{2
        controller_uid =self.token['controller_uid']
        controller =self.token_controllers[controller_uid]
        if controller['f_active_container'] :
            if self.__compute_controller_type(controller_uid) =='bi-container' :
                controller['f_active_container'] =False
                head_controller_uid =None
                while head_controller_uid != self.token['controller_uid'] :
                    head_controller_uid =self.headers[-1]
                    self.headers.pop()
                    if len(self.headers) == 0 :
                        break
            lvl =len(controller_uid)
            for child_controller_uid in self.token_controllers.keys() :
               if not len(child_controller_uid) <= lvl and child_controller_uid[:lvl] == controller_uid :
                   self.token_controllers[child_controller_uid] =copy.deepcopy(self.Default_token_controllers[child_controller_uid])
        elif self.__compute_controller_type(controller_uid) =='bi-container':
            self.headers.append(controller['uid'])
            controller['f_active_container'] =True




    def __f_do_not_update_line_buffer_for_match(self, token_match) : #{{{2
       controller_uid =self.token['controller_uid']
       controller =self.token_controllers[controller_uid]
       if not controller['f_do_not_update_line_buffer_for_match'] and not self.f_EOL :
           e_line_of_token_match  =token_match.span()[1]
           z_line_of_token_match  =token_match.span()[0]
           self.z_line +=(e_line_of_token_match-z_line_of_token_match)
           self.z_data +=(e_line_of_token_match-z_line_of_token_match)




#---------------------------- NO MATCH ----------------------------#
    def __ed_trigger_on_no_match_too(self) : #{{{2
        controller_uid =self.token['controller_uid']
        controller =self.token_controllers[controller_uid]
        if controller['ed_trigger_on_no_match_too'] :
            self.__ed()




    def __try_child(self) : #{{{2
        success =False
        controller_uid =self.token['controller_uid']
        controller =self.token_controllers[controller_uid]
        if controller['f_active_container'] :
            pntr =self.__controller_uid2pntr(controller_uid)
            pntr.append(0)
            child_controller_uid =self.__pntr2controller_uid(pntr)
            if child_controller_uid in self.token_controllers.keys() :
                success =True
                self.token['controller_uid'] =child_controller_uid
        return success




    def __try_next_sybling(self) : #{{{2
        success =False
        controller_uid =self.token['controller_uid']
        controller =self.token_controllers[controller_uid]

        if not self.__is_active_bi_container(controller_uid) :
            pntr =self.__controller_uid2pntr(controller_uid)
            pntr[-1] += 1
            sybling_controller_uid =self.__pntr2controller_uid(pntr)

            if sybling_controller_uid in self.token_controllers.keys() :
                success =True
                self.token['controller_uid'] =sybling_controller_uid

        return success




# UTILITILES  {{{1
################################################
    def __get_pattern(self, controller_uid) : #{{{2
        controller =self.token_controllers[controller_uid]
        if controller['f_active_container'] :
            pattern =controller['pattern_2']
        else :
            pattern =controller['pattern_1']
        return pattern




    def __is_token_EOL_terminating(self, controller_uid) : #{{{2
        controller =self.token_controllers[controller_uid]
        if controller['f_active_container'] and controller['f_EOL_terminating'] :
            return True
        else :
            return False




    def __compute_token_type(self, controller_uid) :#{{{2
        Type =None
        controller =self.token_controllers[controller_uid]
        if controller['pattern_1'] and controller['pattern_2'] :
            if controller['f_active_container'] :
                Type ='end'
            else :
                Type ='start'
        elif not controller['pattern_1'] and controller['pattern_2'] :
            Type ='delim'
        else :
            Type ='regular'
        return Type




    def __compute_controller_type(self, controller_uid) :#{{{2
        Type =None
        controller =self.token_controllers[controller_uid]
        if controller['pattern_1'] and controller['pattern_2'] :
            Type ='bi-container'
        elif not controller['pattern_1'] and controller['pattern_2'] :
            Type ='mono-container'
        else :
            Type ='member'
        return Type




    def __get_head(self) : #{{{2
        if len(self.headers) :
            return self.headers[-1]
        else :
            return '0'




    def __verbose(self, tabn, string, newline=True) : #{{{2
        if self.verbose :
            tabs ="    " * tabn
            if newline :
                print(tabs + string)
            else :
                print(tabs + string, end='')




    def __controller_uid2pntr(self, controller_uid) :#{{{2
        pntr =controller_uid.split('.')
        pntr =[int(i) for i in pntr]
        return pntr




    def __pntr2controller_uid(self, pntr) : #{{{2
        pntr =[str(i) for i in pntr]
        controller_uid ='.'.join(pntr)
        return controller_uid




    def __is_active_bi_container(self, controller_uid) : #{{{2
        retu =False
        controller =self.token_controllers[controller_uid]
        if self.__compute_controller_type(controller_uid) == 'bi-container' :
            if  controller['f_active_container'] :
                retu =True
        return retu




    def __is_inactive_bi_container(self, controller_uid) : #{{{2
        retu =False
        controller =self.token_controllers[controller_uid]
        if self.__compute_controller_type(controller_uid) == 'bi-container':
            if not controller['f_active_container'] :
                retu =True
        return retu




    def __setup_token_controllers(self) : #{{{2
        for controller in self.token_controllers.values() :
            ## pattern 1
            if  controller['pattern_1'] :
                controller['pattern_1'] =re.compile(controller['pattern_1'])
            ## pattern 2
            if  controller['pattern_2'] :
                controller['pattern_2'] =re.compile(controller['pattern_2'])
            elif controller['f_EOL_terminating'] :
                controller['pattern_2'] =re.compile('')




    def __setup_token_history(self) : #{{{2
        self.token_history[0] =[{'controller_uid':'-1'}]
        for controller_uid in self.token_controllers.keys() :
            pntr =controller_uid.split('.')
            lvl =len(pntr)
            self.token_history[lvl] =[{'controller_uid':'-1'}]




