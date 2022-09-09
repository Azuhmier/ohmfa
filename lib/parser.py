import re
import sys
import copy




class parser :


#######################
# Public {{{1
#######################
    def parse_next_token(self) :

        self.token = self.lexer.next_token()
        self.__populate_node()
        self.__add_node_to_tree()






#######################
# Private {{{1
#######################
    def __init__(self, config, f_verbose=False): #{{{2
        self.DataController   = config['data']
        self.f_verboe  = f_verbose
        self.token     = None
        self.default_node      = {
            'puid' : None,
            'name' : None,
            'type' : None,
            'subtype' : None,
            'pos' : {
                'z_txt'      : None,
                'z_line'     : None,
                'e_line'     : None,
                'LineNumber' : None,
            },
            'childs' : {
            },
        }
        self.config = {
            'uid' : None,
            'puid': None,
            'stop_puid': None,
            'parent_puid': [
                {
                    'puid' : None,
                    'limit' : None,
                    'direction' : None,
                }
            ]
        }

        self.__populate_node()
        self.__add_node_to_tree()


    def __add_node_to_tree(self) :
        uid = self.token['uid']

        #-------------GET PARENT PUID-----------#
        parent_puid = None
        LN = self.node['pos']['z_txt']
        for parent in self.config[uid]['parent_puid'] :
            parent_puid = parent['puid']
            limit        = parent['limit']
            direction    = parent['direction']

            if direction :
                parentNode = self.table[puid][-idx]
            else :
                parentNode =  self.table[+puid][idx]
            z_txt      = parentNode['pos']['z_txt']
            if z_txt < pz_txt :
                parent_uid = parent_puid


        #-------------ADD NODE TO PARENT -----------#


#######################
# Utilities {{{1
#######################
    def __populate_pos(self) :
        self.node['pos']['z_txt']       = self.token['z_txt']
        self.node['pos']['z_line']      = self.token['z_line']
        self.node['pos']['e_line']      = self.token['e_line']
        self.node['pos']['LineNumber']  = self.token['LineNumber']

    def __populate_node(self) :
       token_uid    = self.token['uid']
       #start
       #stop
       #delim
       #regular

       #reff
       #data
       #drsr
       #none
       puids = self.DataController[token_uid]

       self.node = copy.deepcopy(self.defualt_node)
       self.node['name']    = self.config['parse'][parse_uid]['name']
       self.node['uid']     = self.config['parse'][parse_uid]['uid']
       self.node['type']    = self.config['parse'][parse_uid]['type']
       self.node['subtype'] = self.config['parse'][parse_uid]['subtype']
       self.__populate_pos()
       self.__populate_node_with_child_keys()

       if len(self.table["+" + puid]) :
           self.node = self.table["+" + puid][0]
           self.table["+" + puid].pop()
       self.table[puid].append(self.node)

    def __populate_node_with_child_keys(self) :
        for child_parse_uid in self.getChilds() :
            self.node['childs'][child_parse_uid] = {}


    def __getChilds(self,parse_uid = None) :
        child_parse_uids = []

        if not parse_uid :
            parse_uid = self.node['parse_uid']

        parse_uids = [config[i]['parse_uid'] for i in config.keys() ]
        parse_uid_lvl = len(parse_uid)
        for child_canidaate_parse_uid_ in parse_uids :
            if len(child_canidate_parse_uid) == (parse_uid_lvl + 1 )
                child_canidate_pntr = child_canidate_parse_uid.split('.')
                pntr                = parse_uid.split('.')
                if child_pntr[:parse_uid_lvl] == pntr :
                    child_parse_uids.append(child_parse_uid)
       return child_parse_uids







#######################
# doc {{{1
#######################
pod = """

0 (0.X1 (+/-0.X1.0 ) 0.X2 (0.X2.0 (0.0.X2.0.0) ) +0.X3)
    0.0   (0.0.X1` (+/-0.0.X1.0) 0.0.X2 (+/-0.0.X2.0) +0.0.X3 +0.0.X4)
        0.0.0 (0.0.0.X1 (+/-0.0.0.X1.0) )

author (attr (label ) url (attr (label) ) !section)
    title  (attr (label) tag (label) !description !series)
        url    (attr (label) )

token_a     0
token_b     0.X1
token_c     +/-0.X1.0
token_d     0.X2
token_e     0.X2.0
token_f     0.0.X2.0.0
token_g     +0.X3
token_h     0.0
token_i     0.0.X1
token_j     +/-0.0.X1.0
token_k     0.0.X2
token_l     +/-0.0.X2.0
token_m     +0.0.X3
token_n     +0.0.X4
token_o     0.0.0
token_p     0.0.0.X1
token_q     +/-0.0.0.X1.0



0                author
0.X1             attr
+/-0.X1.0        label
0.X2             url
0.X2.0           attr
0.0.X2.0.0       label
+0.X3            section
0.0              title
0.0.X1           attr
+/-0.0.X1.0      label
0.0.X2           tag
+/-0.0.X2.0      label
+0.0.X3          description
+0.0.X4          series
0.0.0            url
0.0.0.X1         attr
+/-0.0.0.X1.0    label

0                author
0.X1             author_attr
+/-0.X1.0        author_attr_label
0.X2             author_url
0.X2.0           author_url_attr
0.0.X2.0.0       author_url_attr_label
+0.X3            author_section
0.0              title
0.0.X1           title_attr
+/-0.0.X1.0      title_attr_label
0.0.X2           title_tag
+/-0.0.X2.0      title_tag_label
+0.0.X3          title_description
+0.0.X4          title_series
0.0.0            url
0.0.0.X1         url_attr
+/-0.0.0.X1.0    url_attr_label

0           author
0.1         attr
0.1.0       label
0.2         url
0.2.0       attr
0.0.2.0.0   label
0.3         section
0.0         title
0.0.1       attr
0.0.1.0     label
0.0.2       tag
0.0.2.0     label
0.0.3       description
0.0.4       series
0.0.0       url
0.0.0.1     attr
0.0.0.1.0   label

0           author
0.1         author_attr
0.1.0       author_attr_label
0.2         author_url
0.2.0       author_url_attr
0.0.2.0.0   author_url_attr_label
0.3         author_section
0.0         title
0.0.1       title_attr
0.0.1.0     title_attr_label
0.0.2       title_tag
0.0.2.0     title_tag_label
0.0.3       title_description
0.0.4       title_series
0.0.0       url
0.0.0.1     url_attr
0.0.0.1.0   url_attr_label

"%title(attr ? %author.attr.label='collab')                              ""

 line-section.part-section

 line-author.part-author
 line-author.container-attributes
 line-author.container-attributes.part-label
 line-author.container-attributes.part-attr
 line-author.container-attributes.container-literal.literal
 line-author.container-attributes.attributeflag
 line-author.container-attributes.delim-tag=';'
 line-author.container-attributes

 line-series.part-series

 line-title.part-title
 line-title.container-attributes
 line-title.container-attributes.part-attr
 line-title.container-attributes.part-label
 line-title.container-attributes.attributeflag
 line-title.container-attributes.delim-tag=';'
 line-title.container-attributes.container-literal

 line-tags.container-tags
 line-tags.container-tags.part-label
 line-tags.container-tags.part-tag
 line-tags.container-tags.container-literal.literal
 line-tags.container-tags.tagflag
 line-tags.container-tags.delim-tag=';'
 line-tags.taglineflag

 line-url.url
 line-author.container-attributes
 line-url.container-attributes.part-label
 line-url.container-attributes.part-attr
 line-url.container-attributes.attributeflag
 line-url.container-attributes.delim-tag=';'
 line-author.container-attributes.container-literal.literal

 line-description.entire_line

line-section.part-section                                            section          +author

line-author.part-author                                              author           -root
line-author.container-attributes                                     label            -attribute
line-author.container-attributes.part-label                          label            +attribute
line-author.container-attributes.part-attr                           attribute        -author
line-author.container-attributes.container-literal.literal           label            -author
line-author.container-attributes.attributeflag                       label            -attribute
line-author.container-attributes.delim-tag=';'                       label            +attribute

line-series.part-series                                              series           +author

line-title.part-title                                                title            -author
line-title.container-attributes                                      label            -attribute
line-title.container-attributes.part-label                           label            +attribute
line-title.container-attributes.part-attr                            attribute        -author
line-title.container-attributes.attributeflag                        label            -author
line-title.container-attributes.delim-tag=';'                        label            -attribute
line-title.container-attributes.container-literal                    label            +attribute

line-tags.container-tags                                             label            -title
line-tags.taglineflag                                                label            -attribute
line-tags.container-tags.part-label                                  label            +attribute
line-tags.container-tags.part-tag                                    tag              -title
line-tags.container-tags.container-literal.literal                   tag              -title
line-tags.container-tags.tagflag                                     label            -attribute
line-tags.container-tags.delim-tag=';'                               label            +attribute

line-url.url                                                         url              -author -title
line-url.container-attributes                                        label            +attribute
line-url.container-attributes.part-label                             label            =attribute
line-url.container-attributes.part-attr                              attribute        -url
line-author.container-attributes.container-literal.literal           attribute        -url
line-url.container-attributes.attributeflag                          label            -attribute
line-url.container-attributes.delim-tag=';'                          label            +attribute

line-description.entire_line                                         description      -title


-root            0           author
-author          0.1         author_attr
+author_attr     0.1.0       author_attr_label
-author_attr     0.1.0       author_attr_label
-author          0.2         author_url
-author_url      0.2.0       author_url_attr
+author_url_attr 0.0.2.0.0   author_url_attr_label
-author_url_attr 0.0.2.0.0   author_url_attr_label
+author          0.3         author_section
+author          0.0         title
-title           0.0.1       title_attr
+title_attr      0.0.1.0     title_attr_label
-title_attr      0.0.1.0     title_attr_label
-title           0.0.2       title_tag
-title           0.0.2.0     title_tag_label
-title           0.0.2.0     title_tag_label
-title           0.0.3       title_description
+title           0.0.4       title_series
-author          0.0.0       url
-url             0.0.0.1     url_attr
+url_attr        0.0.0.1.0   url_attr_label
-url_attr        0.0.0.1.0   url_attr_label
