//Mon 04/24/23 07:35:07
/*
--------------------------------------------------------------
[
   [
       "[bB]y\s(.*)"
   ],
   [
       ">\s*(.*)"
   ],
   [
       "(https[^ ]+)"
   ]
]

--------------------------------------------------------------
[
   [
       "[bB]y\s(.*)"
   ],
   [
       ">\s*(.*)"
   ],
   [
       "(\[.*)"
       [
           \[([^\)\(]*)\],
           [
               [^ ,]*([^, ].*)*,
               [
                   ([^,]*),*
               ]
            ]
        ]
   ],
   [
       "(https[^ ]+)"
   ],
]




--------------------------------------------------------------
[
   [
       "[bB]y\s(.*)"
       [
           "([^`]+)`([^`]+)
           [
               "[^ ]"
           ]
           [
               \(([^\)\(]*)\),
           ]
       ]
   ],
   [
       ">\s*(.*)"
   ],
   [
       "(\[.*)"
       [
           \[([^\)\(]*)\],
           [
               [^ ,]*([^, ].*)*,
               [
                   ([^,]*),*
               ]
            ]
        ]
   ],
   [
       "(https[^ ]+)"
   ],
]



--------------------------------------------------------------
[
   [
       "[bB]y\s(.*)"
       [
           "([^`]+)`([^`]+)
           [
               "[^ ]"
           ]
           [
               \(([^\)\(]*)\),
           ]
       ]
       [
           "[^ ]"
       ]
   ],
   [
       ">\s*(.*)"
   ],
   [
       "(\[.*)"
       [
           \[([^\)\(]*)\],
           [
               [^ ,]*([^, ].*)*,
               [
                   ([^,]*),*
               ]
            ]
        ]
   ],
   [
       "(https[^ ]+)"
   ],
]



--------------------------------------------------------------
[
   [
       "[bB]y\s(.*)"
       [
           SEPERATOR('`')
           [
               WORD
           ]
           [
               BRACKET('(',')'),
           ]
       ]
       [
           WORD
       ]
   ],
   [
       ">\s*(.*)"
   ],
   [
       "(\[.*)"
       [
           BRAKET('[',']',
           [
               DELIM(',')
           ]
        ]
   ],
   [
       "(https[^ ]+)"
   ],
]



--------------------------------------------------------------
[
   [
       "[bB]y\s(.*)",
       [
           SEPERATOR('`', mask=1)
           [
               WORD
           ]
           [
               BRACKET('(',')'),
           ]
       ]
   ],
   [
       ">\s*(.*)"
   ],
   [
       "(\[.*)",
       [
           BRAKET('[',']',
           [
               DELIM(',')
           ]
        ]
   ],
   [
       "(https[^ ]+)"
   ],
]

--------------------------------------------------------------
[
   [ "[bB]y\s(.*)",
       [ SEPERATOR('`', mask=1)
           [ WORD
           ]
           [ BRACKET('(',')'),
           ]
       ]
   ],
   [ ">\s*(.*)"
   ],
   [ "(\[.*)",
       [ BRAKET('[',']',
           [ DELIM(',')
           ]
       ]
   ],
   [ "(https[^ ]+)"
   ],
]

--------------------------------------------------------------
[
   [ "[bB]y\s(.*)",
       [ SEPERATOR('`', mask=1)
           [ WORD ]
           [ BRACKET('(',')'), ]
       ]
   ],
   [ ">\s*(.*)" ],
   [ "(\[.*)",
       [ BRAKET('[',']',
           [ DELIM(',') ]
       ]
   ],
   [ "(https[^ ]+)" ],
]

--------------------------------------------------------------
[
   [ "[bB]y\s(.*)",
       [ SEPERATOR('`', mask=1),
           [ WORD ],
           [ BRACKET('(',')') ]]],
   [ ">\s*(.*)" ],
   [ "(\[.*)",
       [ BRAKET('[',']',
           [ DELIM(',') ]]],
   [ "(https[^ ]+)" ],
]
*/