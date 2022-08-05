#!/usr/bin/env python3
# ============================================================
#
# File:    bpg.py
#
# Usage:   ./bpg.py
#
# Date:    Sun 07/31/22 03:08:25
# Version: 1.0
# Project: ohmfa
# Author:  Azuhmier (aka taganon), azuhmier@gmail.com
#
# Description:
# ============================================================

import sys
import os
from pydoc import locate
import copy
import glob
from datetime import datetime
import traceback
import pprint
pp = pprint.PrettyPrinter(indent=4,sort_dicts=True,depth=1,compact=False,)
self = {}
self['paths']={}
self['paths']['cwd']=os.getcwd()
self['bpm'] = {#{{{
    ## OPGET
    ## SCRAPE
    'scrape' : {#{{{
        'init' : { #{{{
            'DEFAULT' : {
                'config' : {
                    'DEFAULT' : {
                        'dspt' : {
                            'DEFAULT' : {
                            }
                        },
                        'login' : {
                            'DEFAULT' : {
                            }
                        },
                        'extern' : {
                            'DEFAULT' : {
                            }
                        }
                    }
                },
                'IFL' : {
                    'DEFAULT' : {},
                },
                'meta' : {
                    'DEFAULT' : {},
                },
                'flags' : {  #{{{
                    'DEFAULT' : {
                        'plhd' : {
                            'DEFAULT' : 0,
                        },
                        'prsv' : {
                            'DEFAULT' : 0,
                        },
                    },
                },#}}}
                'opts' : { #{{{
                    'DEFAULT' : {
                        'plhd' : {
                            'DEFAULT' : {},
                        },
                    },
                },#}}}
                'status' : { #{{{
                    'DEFAULTS' : {
                        'base' : {
                            'DEFAULT' : 0,
                        },
                        'dspt' : {
                            'DEFAULT' : 0,
                        },
                        'init' : {
                            'DEFAULT' : 0,
                        },
                        'matches' : {
                            'DEFAULT' : 0,
                        },
                        'state_is_ok' : {
                            'DEFAULT' : 0,
                        },
                        'sync' : {
                            'DEFAULT' : 0,
                        },
                        'valid_file' : {
                            'DEFAULT' : 0,
                        },
                        'valid_hash' : {
                            'DEFAULT' : 0,
                        },
                    },
                },#}}}
            },
        },#}}}
        'IFL' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'DEFAULT' : 'scrape'
                },#}}}
                'struct_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : 'IFL'
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT' : {},
                    'FILL' : [
                        [ 'SELF', 'value', ['urls','list'] ],
                        {
                            'DEFAULT' : {
                                'url' : {
                                    'TYPE' : 'str',
                                    'DEFAULT' : None,
                                },
                                'domain' : {
                                    'TYPE' : 'str',
                                    'DEFAULT' : None,
                                },
                                'html' : {
                                    'TYPE' : 'str',
                                    'DEFAULT' : None,
                                },
                                'content' : {
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        [ 'ARG_CP', [ 'key']],
                                        {
                                            'DEFAULT' : {
                                                'kind' : {
                                                    'TYPE' : 'str',
                                                    'DEFAULT' : None,
                                                },
                                                'content' : {
                                                    'TYPE' : 'list',
                                                    'DEFAULT' : None,
                                                },
                                            },
                                        },
                                    ],
                                },
                            }
                        }
                    ],
                }#}}}
            },
        }, #}}}
        'dspt' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'struct_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT' : {},
                    'FILL' : [
                        [ 'SELF', [ 'key', ['url','domains'] ] ],
                        {
                            'DEFAULT' : {
                                'story' : {
                                    'content' : {
                                        'DEFAULT' : [],
                                    },
                                    'description' : {
                                        'DEFAULT' : [],
                                    },
                                    'tags' : {
                                        'DEFAULT' : [],
                                    },
                                    'published' : {
                                        'DEFAULT' : [],
                                    },
                                    'updated' : {
                                        'DEFAULT' : [],
                                    },
                                    'comments' : {
                                        'DEFAULT' : [],
                                    },
                                    'index' : {
                                        'default' : [],
                                    },
                                },
                                'author' : {
                                    'stories' : {
                                        'DEFAULT' : [],
                                    },
                                    'joined' : {
                                        'DEFAULT' : [],
                                    },
                                    'activity' : {
                                        'DEFAULT' : [],
                                    },
                                },
                            }
                        }
                    ],
                }#}}}
            },
        }, #}}}
        'login' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'struct_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT' : {
                        'domain' : {
                            'TYPE' : 'str',
                            'DEFAULT' : None,
                        },
                        'login' : {
                            'TYPE' : 'str',
                            'DEFAULT' : None,
                        },
                        'usr' : {
                            'TYPE' : 'str',
                            'DEFAULT' : None,
                        },
                        'pwd' : {
                            'TYPE' : 'str',
                            'DEFAULT' : None,
                        },
                        'token' : {
                            'TYPE' : 'str',
                            'DEFAULT' : None,
                        },
                    }
                }#}}}
            },
        }, #}}}
    },#}}}
    'hasher' : {#{{{
        'init' : { #{{{
            'DEFAULT' : {
                'IFL_objs' : { #{{{
                    'DEFAULT' : {},
                    'FILL' : [
                        ['ARG_CP', ['key'] ],
                        {
                            'DEFAULT' : {
                                'commit' : {#{{{
                                    'DEFAULT': {
                                        'schema' : {#{{{
                                            'EXPR' : True,
                                            'DEFAULT' : [ 'BPC', ['hasher', 'schema'], ],
                                        },#}}}
                                        'mfile' : {#{{{
                                            'EXPR' : True,
                                            'DEFAULT' : [ 'BPC', ['hasher', 'mfile'], ],
                                        },#}}}
                                        'IFL' : { #{{{
                                            'EXPR' : True,
                                            'DEFAULT' : [ 'BPC', ['hasher', 'IFL'], ],
                                        },#}}}
                                        'matches' : { #{{{
                                            'EXPR' : True,
                                            'DEFAULT' : [ 'BPC', ['hasher', 'matches'], ],
                                        },#}}}
                                        'outputs' : { #{{{
                                            'DEFAULT' : {
                                                'paged' : {#{{{
                                                    'EXPR' : True,
                                                    'DEFAULT' : [ 'BPC', ['hasher', 'paged'], ],
                                                },#}}}
                                                'dfile' : {#{{{
                                                    'DEFAULT' : [],
                                                    'FILL' : [
                                                        ['ARG_CP', ['key']],
                                                        {
                                                            'EXPR' : True,
                                                            'DEFAULT' : [ 'BPC', ['dfile'], ],
                                                        }
                                                    ]
                                                }#}}}
                                            },
                                        },#}}}
                                        'meta' : { #{{{
                                            'EXPR' : True,
                                            'DEFAULT' : [ 'BPC', ['meta'], ],
                                        },#}}}
                                    }
                                },#}}}
                                'stack' : {#{{{
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        ['ARG_CP', ['key'] ],
                                        {
                                            'DEFAULT': {
                                                'schema' : {#{{{
                                                    'DEFAULT' : [],
                                                    'FILL' : [
                                                        [ 'ARG_CP', [ 'key' ] ],
                                                        {
                                                            'EXPR' : True,
                                                            'DEFAULT' : [ 'BPC', ['schema'], ],
                                                        },
                                                    ],
                                                },#}}}
                                                'mfile' : {#{{{
                                                    'DEFAULT' : [],
                                                    'FILL' : [
                                                        [ 'ARG_CP', [ 'key' ] ],
                                                        {
                                                            'EXPR' : True,
                                                            'DEFAULT' : [ 'BPC', ['mfile'], ],
                                                        }
                                                    ],
                                                },#}}}
                                                'IFL' : { #{{{
                                                    'DEFAULT' : [],
                                                    'FILL' : [
                                                        [ 'ARG_CP', [ 'key' ] ],
                                                        {
                                                            'EXPR' : True,
                                                            'DEFAULT' : [ 'BPC', ['IFL'], ],
                                                        }
                                                    ],
                                                },#}}}
                                                'matches' : { #{{{
                                                    'DEFAULT' : [],
                                                    'FILL' : [
                                                        [ 'ARG_CP', [ 'key' ] ],
                                                        {
                                                            'EXPR' : True,
                                                            'DEFAULT' : [ 'BPC', ['matches'], ],
                                                        }
                                                    ],
                                                },#}}}
                                                'outputs' : { #{{{
                                                    'DEFAULT' : {
                                                        'paged' : {#{{{
                                                            'DEFAULT' : [],
                                                            'FILL' : [
                                                                [ 'ARG_CP', [ 'key' ] ],
                                                                {
                                                                    'EXPR' : True,
                                                                    'DEFAULT' : [ 'BPC', ['paged'], ],
                                                                }
                                                            ],
                                                        },#}}}
                                                        'dfile' : {#{{{
                                                            'DEFAULT' : [],
                                                            'FILL' : [
                                                                [ 'ARG_CP', [ 'key' ] ],
                                                                {
                                                                    'EXPR' : True,
                                                                    'DEFAULT' : [ 'BPC', ['dfile'], ],
                                                                }
                                                            ],
                                                        }#}}}
                                                    },
                                                },#}}}
                                                'meta' : { #{{{
                                                    'DEFAULT' : [],
                                                    'FILL' : [
                                                        [ 'ARG_CP', [ 'key' ] ],
                                                        {
                                                            'EXPR' : True,
                                                            'DEFAULT' : [ 'BPC', ['meta'], ],
                                                        }
                                                    ],
                                                },#}}}
                                            }
                                        }
                                    ]
                                }#}}}
                            }
                        }
                    ],
                },#}}}
                'config' : {  #{{{
                    'DEFAULT' : {
                        'main' : {#{{{
                            'DEFAULT': {
                                'extern' : {#{{{
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        [ 'ARG_CP', ['value'] ],
                                        {
                                            'DEFAULT' : [],
                                            #'EXPR' : True,
                                            #'DEFAULT' : [ 'BPC', ['hasher',  'extern' ] ],
                                        }
                                    ]
                                },#}}}
                            }
                        },#}}}
                        'IFL' : {#{{{
                            'DEFAULT' : {
                                'dspt' : {#{{{
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        [ 'ARG_CP', ['value'] ],
                                        {
                                            'EXPR' : True,
                                            'DEFAULT' : [ 'BPC', ['hasher', 'IFL', 'dspt'], ],
                                        }
                                    ]
                                },#}}}
                                'drsr' : {#{{{
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        [ 'ARG_CP', ['value'] ],
                                        {
                                            'EXPR' : True,
                                            'DEFAULT' : [ 'BPC', ['hasher', 'drsr'], ],
                                        }
                                    ]
                                },#}}}
                                'mask' : {#{{{
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        [ 'ARG_CP', ['value'] ],
                                        { 'EXPR' : True, 'DEFAULT' : [ 'BPC', ['hasher', 'mask'], ], }
                                    ]
                                },#}}}
                                'injection' : {#{{{
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        [ 'ARG_CP', ['value'] ],
                                        { 'EXPR' : True, 'DEFAULT' : [ 'BPC', ['hasher', 'injection'], ], }
                                    ]
                                },#}}}
                                'launch' : {#{{{
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        [ 'ARG_CP', ['value'] ],
                                        {
                                            'EXPR' : True,
                                            'DEFAULT' : [ 'BPC', ['hasher', 'launch'], ],
                                        }
                                    ]
                                },#}}}
                            }
                        },#}}}
                        'scrape' : {#{{{
                            'DEFAULT': {
                                'dspt' : {#{{{
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        [ 'ARG_CP', ['value'] ],
                                        {
                                            'EXPR' : True,
                                            'DEFAULT' : [ 'BPC', ['hasher', 'mask'], ],
                                        }
                                    ]
                                },#}}}
                                'login' : {#{{{
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        [ 'ARG_CP', ['value'] ],
                                        {
                                            'EXPR' : True,
                                            'DEFAULT' : [ 'BPC', ['hasher', 'mask'], ],
                                        }
                                    ]
                                },#}}}
                            }
                        },#}}}
                        'OPs' : {#{{{
                            'DEFAULT': {
                                'dspt' : {#{{{
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        [ 'ARG_CP', ['value'] ],
                                        {
                                            'EXPR' : True,
                                            'DEFAULT' : [ 'BPC', ['hasher', 'IFL', 'mask'], ],
                                        }
                                    ]
                                },#}}}
                            }
                        }#}}}
                    }
                },#}}}
                'properties' : {#{{{
                    'DEFAULT' : {
                        'flags' : {  #{{{
                            'DEFAULT' : {
                                'plhd' : {
                                    'DEFAULT' : 0,
                                },
                                'prsv' : {
                                    'DEFAULT' : 0,
                                },
                                'launch' : {
                                    'DEFAULT' : 0,
                                },
                                'commit' : {
                                    'DEFAULT' : 0,
                                },
                                'writable' : {
                                    'DEFAULT' : 0,
                                },
                            },
                        },#}}}
                        'paths' : {  #{{{
                            'DEFAULT' : {
                                'cwd' : {
                                    'DEFAULT' : [ 'SELF', ['value', ['paths','cwd'] ] ],
                                    'EXPR' : True,
                                },
                                'drsr' : {
                                    'DEFAULT' : './.ohmfi/self/drsr.json',
                                },

                                'dspt' : {
                                    'DEFAULT' : './.ohmfi/self/dspt.json'
                                },

                                'input' : {
                                    'DEFAULT' : './.ohmfi/self/input.txt',
                                },

                                'mask' : {
                                    'DEFAULT' : './.ohmfi/self/mask.json',
                                },

                                'hash' : {
                                    'DEFAULT' : './.ohmfi/self/hash.json',
                                },

                                'smask' : {
                                    'DEFAULT' : [ 'GLOB', [ './.ohmfi/self/smask/*' ] ],
                                    'EXPR' : True,
                                },

                                'sdrsr' : {
                                    'DEFAULT' : [ 'GLOB', [ './.ohmfi/self/sdrsr/*' ] ],
                                    'EXPR' : True,
                                },

                                'extern' : {
                                    'DEFAULT' : [ 'GLOB', [ './.ohmfi/self/extern/*' ] ]
                                },

                            },
                        },#}}}
                        'opts' : { #{{{
                            'DEFAULT' : {
                                'plhd' : {
                                    'DEFAULT' : {},
                                },
                            },
                        },#}}}
                        'status' : { #{{{
                            'DEFAULTS' : {
                                'base' : {
                                    'DEFAULT' : 0,
                                },
                                'dspt' : {
                                    'DEFAULT' : 0,
                                },
                                'init' : {
                                    'DEFAULT' : 0,
                                },
                                'matches' : {
                                    'DEFAULT' : 0,
                                },
                                'state_is_ok' : {
                                    'DEFAULT' : 0,
                                },
                                'sync' : {
                                    'DEFAULT' : 0,
                                },
                                'valid_file' : {
                                    'DEFAULT' : 0,
                                },
                                'valid_hash' : {
                                    'DEFAULT' : 0,
                                },
                                'config' : {
                                    'DEFAULT' : {},
                                },
                                'meta' : {
                                    'DEFAULT' : {},
                                },
                                'parse' : {
                                    'DEFAULT' : {},
                                },
                                'sweep' : {
                                    'DEFAULT' : {},
                                },
                                'write' : {
                                    'DEFAULT' : {},
                                },
                                'opts' : {
                                    'DEFAULT' : {},
                                },
                            },
                        }#}}}
                    },
                },#}}}
                'actions' : {#{{{
                    'DEFAULT' : {
                        'parser' : {#{{{
                            'DEFAULT' : {},
                        },#}}}
                        'ohmfi' : {#{{{
                            'DEFAULT' : {},
                        },#}}}
                        'sweeper' : {#{{{
                            'DEFAULT' : {},
                        },#}}}
                        'composer' : {#{{{
                            'DEFAULT' : {},
                        },#}}}
                        'validater' : {#{{{
                            'DEFAULT' : {},
                        },#}}}
                        'DB_interface' : {#{{{
                            'DEFAULT' : {},
                        },#}}}
                    },
                }, #}}}
            },
        },#}}}
        'schema' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'DEFAULT' : 'hasher'
                },#}}}
                'struct_type' : {#{{{
                    'DEFAULT' : 'schema'
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT' : [],
                    'FILL' : [
                        [ 'ARG_CP', ['value'] ],
                        {
                            'DEFAULT' : {
                                'type' : {
                                    'TYPE' : 'str',
                                    'DEFAULT' : None
                                },
                                'dspt' : {
                                    'TYPE' : 'str',
                                    'DEFAULT' : None
                                },
                                'drsr' : {
                                    'TYPE' : 'str',
                                    'DEFAULT' : None
                                },
                                'mask' : {
                                    'TYPE' : 'str',
                                    'DEFAULT' : None
                                },
                                'extern' :  {
                                    'TYPE' : 'str',
                                    'DEFAULT' : None
                                },
                                'launch':  {
                                    'TYPE' : 'str',
                                    'DEFAULT' : None
                                },
                                'injection':  {
                                    'TYPE' : 'str',
                                    'DEFAULT' : None
                                }
                            }
                        }
                    ]
                }#}}}
            },
        }, #}}}
        'mfile' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'struct_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT' : [],
                }#}}}
            },
        }, #}}}
        'IFL' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'struct_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT' : {
                        'UID' : {
                            'DEFAULT' : '00000000',
                        },
                        'config_UID' : {
                            'DEFAULT' : '00',
                        },
                        'class' : {
                            'NO_OVERRIDE' : True,
                            'DEFAULT' : 'root'
                        },
                        'val' : {
                            'DEFAULT' : None,
                            'TYPE': 'str'
                        },
                        'LN' : {
                            'DEFAULT' : None,
                            'TYPE': 'int'
                        },
                        'childs' : {
                            'DEFAULT' : {},
                            'FILL' : [
                                [ 'ARG_CP', ['key'] ],
                                {
                                    'EXPR' : True,
                                    'DEFAULT' : [ 'BPC', ['hasher', 'IFL_obj']
                                    ]
                                }
                            ]
                        },
                        'props' : { #{{{
                            'DEFAULT' : {
                                'supress' : {
                                    'DEFAULT' : False,
                                }
                            }
                        } #}}}
                    },
                }#}}}
            },
        }, #}}}
        'IFL_obj' : { #{{{
            'DEFAULT' : {
                'UID' : {
                    'DEFAULT' : None,
                    'TYPE': 'str'
                },
                'config_UID' : {
                    'DEFAULT' : None,
                    'TYPE': 'str'
                },
                'class' : {
                    'DEFAULT' : None,
                    'TYPE': 'str'
                },
                'val' : {
                    'DEFAULT' : None,
                    'TYPE': 'str'
                },
                'LN' : {
                    'DEFAULT' : None,
                    'TYPE': 'int'
                },
                'childs' : {
                    'DEFAULT' : {},
                    'FILL' : [
                        [ 'ARG_CP', ['key'] ],
                        {
                            'EXPR' : True,
                            'DEFAULT' : [ 'BPC', ['hasher', 'IFL_obj']
                            ]
                        }
                    ]
                },
                'props' : { #{{{
                    'DEFAULT' : {
                        'supress' : {
                            'DEFAULT' : 0,
                        }
                    }
                } #}}}
            },
        }, #}}}
        'matches' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'DEFAULT' : 'hasher'
                },#}}}
                'struct_type' : {#{{{
                    'DEFAULT' : 'matches'
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT' : {},
                    'FILL' : [
                        [ 'SELF', [ 'key', ['config','IFL', 'dspt'], ['root'] ] ],
                        {
                            'DEFAULT' : {
                                'total' : {
                                    'DEFAULT' : 0,
                                },
                                'contents' : {
                                    'DEFAULT': [],
                                }
                            }
                        }
                    ],
                }#}}}
            },
        }, #}}}
        'paged' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'struct_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT': {
                        'lists' : {
                            'DEFAULT' : {},
                            'FILL' : [
                                ['self',['key', ['config','IFL','dspt','data'], ['root']]],
                                {
                                    'DEFAULT' : []
                                }
                            ]
                        },
                        'paged_lists' : {
                            'DEFAULT' : {},
                            'FILL' : [
                                ['self',['key', ['config','IFL','dspt','data'], ['root']]],
                                {
                                    'DEFAULT' : [
                                        {
                                            'DEFAULT' : None,
                                            'TYPE' : 'int',
                                        },
                                        {
                                            'DEFAULT' : None,
                                            'TYPE' : 'str',
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }#}}}
            },
        }, #}}}
        'dfile' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'struct_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT' : [],
                }#}}}
            },
        }, #}}}
        'dspt' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'struct_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT' : {
                        'root' : { #{{{
                            'NO_OVERRIDE' : True,
                            'DEFAULT' : {
                                'UID' : { #{{{
                                    'DEFAULT' : '00',
                                }#}}}
                            }
                        }, #}}}
                        'miss' : { #{{{
                            'NO_OVERRIDE' : True,
                            'DEFAULT' : {
                                'UID' : { #{{{
                                    'DEFAULT' : 'ff',
                                },#}}}
                                'parent' : {#{{{
                                    'DEFAULT' : [':all'],
                                },#}}}
                            }
                        } #}}}
                    },
                    'FILL' : [
                        [ 'SELF', [ 'key', ['config','IFL', 'dspt'], ['root','miss'], 1, ['myobj']]],
                        {
                            'EXPR' : True,
                            'DEFAULT': [ 'BPC', [ 'hasher', 'dspt_obj' ] ]
                        }
                    ]
                }#}}}
            },
        }, #}}}
        'dspt_obj' : { #{{{
            'DEFAULT' : {
                'class' : {#{{{
                    'DEFAULT' : 'node',
                },#}}}
                'parse' : {#{{{
                    'DEFAULT' : {
                        'mode' : {#{{{
                            'DEFAULT' : 're',
                        },#}}}
                        're' : {#{{{
                            'DEFAULT' : {
                                'pattern' : {#{{{
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        ['ARG_CP', ['value'],[],1,[0]],
                                        {
                                            'DEFAULT': {
                                                'str' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str'
                                                },#}}}
                                                'seleciton' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str'
                                                },#}}}
                                                'min' : {#{{{
                                                    'DEFAULT' : 'split',
                                                    'TYPE' : 'str',
                                                },#}}}
                                                'max' : {#{{{
                                                    'DEFAULT' : 'split',
                                                    'TYPE' : 'str',
                                                }#}}}
                                            }
                                        }
                                    ]
                                }#}}}
                            }
                        },#}}}
                        'substr' : {#{{{
                            'DEFAULT' : {
                                'pattern' : {#{{{
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        ['ARG_CP', ['value'],[],1,[0]],
                                        {
                                            'DEFAULT': {
                                                'str' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str'
                                                },#}}}
                                                'keep' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str'
                                                },#}}}
                                                'seleciton' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str'
                                                },#}}}
                                                'ignore' : {#{{{
                                                    'DEFAULT' : ' ',
                                                    'TYPE' : 'str',
                                                },#}}}
                                                'min' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str',
                                                },#}}}
                                                'max' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str',
                                                },#}}}
                                                'direction' : {#{{{
                                                    'DEFAULT' : 'left',
                                                    'TYPE' : 'str',
                                                },#}}}
                                            }
                                        }
                                    ]
                                }#}}}
                            }
                        },#}}}
                        'bracketing' : {#{{{
                            'DEFAULT' : {
                                'pattern' : {#{{{
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        ['ARG_CP', ['value'],[],1,[0]],
                                        {
                                            'DEFAULT': {
                                                'left_str' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str'
                                                },#}}}
                                                'right_str' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str',
                                                },#}}}
                                                'left_keep' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str',
                                                },#}}}
                                                'right_keep' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str',
                                                },#}}}
                                                'selection' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str',
                                                },#}}}
                                                'ignore' : {#{{{
                                                    'DEFAULT' : ' ',
                                                    'TYPE' : 'str',
                                                },#}}}
                                                'min' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str',
                                                },#}}}
                                                'max' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str',
                                                },#}}}
                                            }
                                        }
                                    ]
                                }#}}}
                            }
                        },#}}}
                        'delims' : {#{{{
                            'DEFAULT' : {
                                'pattern' : {#{{{
                                    'DEFAULT' : [],
                                    'FILL' : [
                                        ['ARG_CP', ['value'],[],1,[0]],
                                        {
                                            'DEFAULT': {
                                                'str' : {#{{{
                                                    'DEFAULT' : [],
                                                    'FILL' : [
                                                        [ 'ARG_CP', ['value'] ],
                                                        {
                                                            'DEFAULT' : None,
                                                            'TYPE' : 'str',
                                                        }
                                                    ]
                                                },#}}}
                                                'selection' : {#{{{
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'str',
                                                },#}}}
                                                'min' : {#{{{
                                                    'DEFAULT' : 'split',
                                                    'TYPE' : 'str',
                                                },#}}}
                                                'max' : {#{{{
                                                    'DEFAULT' : 'split',
                                                    'TYPE' : 'str',
                                                }#}}}
                                            }
                                        }
                                    ]
                                }#}}}
                            }
                        }#}}}
                    }
                },#}}}
                'parent' : {#{{{
                    'DEFAULT' : [],
                    'FILL' : [
                        ['ARG_CP', ['value']],
                        {
                            'DEFAULT' : None,
                            'TYPE' : 'str',
                        }
                    ]
                },#}}}
                'UID' : { #{{{
                    'DEFAULT' : '10',
                },#}}}
                'childs' : {#{{{
                    'DEFAULT' : {},
                    'FILL' : [
                        ['ARG_CP', [ 'key' ] ],
                        {
                            'EXPR' : True,
                            'DEFAULT' : [ 'BPC', ['hasher', 'dspt_obj'] ]
                        }
                    ]
                },#}}}
            }
        }, #}}}
        'drsr' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'struct_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT' : {},
                    'FILL' : [
                        [ 'SELF', [ 'key', ['config','IFL','dspt', 'data']]],
                        {
                            'EXPR' : True,
                            'DEFAULT' : [ 'BPC', ['hasher', 'drsr_obj'] ]
                        }
                    ],
                }#}}}
            },
        }, #}}}
        'drsr_obj' : {#{{{
            'DEFAULT' : {
                'lb' : {#{{{
                    'DEFAULT' : [],
                    'FILL' : [
                        [ 'ARG_CP', ['value'] ],
                        {
                            'DEFAULT' : {
                                'txt': {
                                    'DEFAULT' : ''
                                },
                                'disable': {
                                    'DEFAULT' : {
                                        'after' : {
                                            'DEFAULT' : [],
                                            'FILL' : [
                                                [ 'ARG_CP', ['value'] ],
                                                {
                                                    'DEFAULT' : {
                                                        'class' : {
                                                            'DEFAULT' : True,
                                                        },
                                                        'not' : {
                                                            'DEFAULT' : True,
                                                        }
                                                    }
                                                }
                                            ]
                                        },
                                        'before' : {
                                            'DEFAULT' : [],
                                            'FILL' : [
                                                [ 'ARG_CP', ['value'] ],
                                                {
                                                    'DEFAULT' : {
                                                        'class' : {
                                                            'DEFAULT' : True,
                                                        },
                                                        'not' : {
                                                            'DEFAULT' : True,
                                                        }
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                }
                            }
                        }
                    ]
                },#}}}
                'rb' : {#{{{
                    'DEFAULT' : [],
                    'FILL' : [
                        [ 'ARG_CP', ['value'] ],
                        {
                            'DEFAULT' : {
                                'txt': {#{{{
                                    'DEFAULT' : ''
                                },#}}}
                                'disable': {#{{{
                                    'DEFAULT' : {
                                        'after' : {#{{{
                                            'DEFAULT' : [],
                                            'FILL' : [
                                                [ 'ARG_CP', ['value'] ],
                                                {
                                                    'DEFAULT' : [
                                                        {
                                                            'DEFAULT' : None,
                                                            'TYPE' : 'str',
                                                        },
                                                        {
                                                            'DEFAULT' : None,
                                                            'TYPE' : 'str',
                                                        }
                                                    ]
                                                }
                                            ]
                                        },#}}}
                                        'before' : {#{{{
                                            'DEFAULT' : [],
                                            'FILL' : [
                                                [ 'ARG_CP', ['value'] ],
                                                {
                                                    'DEFAULT' : [
                                                        {
                                                            'DEFAULT' : None,
                                                            'TYPE' : 'str',
                                                        },
                                                        {
                                                            'DEFAULT' : None,
                                                            'TYPE' : 'str',
                                                        }
                                                    ]
                                                }
                                            ]
                                        }#}}}
                                    }
                                }#}}}
                            }
                        }
                    ]
                },#}}}
                'childs' : {#{{{
                    'TYPE' : 'dict',
                    'DEFAULT' : None,
                    'FILL' : [
                        ['ARG_CP', ['key'] ],
                        {
                            'EXPR' : True,
                            'DEFAULT' : [ 'BPC', ['hasher', 'drsr_obj'] ]
                        }
                    ]
                }#}}}
            },
        },#}}}
        'mask' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'struct_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT' : {
                        'root' : { #{{{
                            'NO_OVERRIDE' : 1,
                            'DEFAULT' : {
                                'cmd' : {
                                    'DEFAULT' : None,
                                    'TYPE': 'str'
                                },
                                'type' : {
                                    'DEFAULT' : 'mask',
                                },
                                'scripts' : {
                                    'DEFAULT' : [],
                                },
                                'pwds' : {
                                    'DEFAULT' : [],
                                },
                                'name' : {
                                    'DEFAULT' : None,
                                    'TYPE': 'str'
                                },
                                'injection' : {
                                    'DEFAULT' : None,
                                    'TYPE': 'str'
                                },
                            },
                        },#}}}
                    },
                    'FILL' : [
                        [
                            'SELF',
                            [
                                'key',
                                ['config','IFL', 'dspt'],
                                ['root','miss']
                            ],
                        ],
                        {
                            'DEFAULT' : {
                                'supress' : { #{{{
                                    'DEFAULT' : {
                                        'all' : {
                                            'DEFAULT' : 0,
                                        },
                                        'vals' : {
                                            'DEFAULT' : [],
                                        },
                                    },
                                }, #}}}
                                'sort' : {#{{{
                                    'DEFAULT' : 0,
                                },#}}}
                                'plhd_enable' : { #{{{
                                    'DEFAULT' : '0'
                                },#}}}
                                'plhds' : { #{{{
                                    'DEFAULT' : {},
                                    'FILL' : [
                                        [   'ARG_CP', ['key', ['childs'] ] ],
                                        {
                                            'TYPE' : 'str',
                                            'DEFAULT' : None,
                                        }
                                    ]
                                },#}}}
                                'childs' : { #{{{
                                    'DEFAULT' : {},
                                    'FILL' : [
                                        ['ARG_CP', ['key']],
                                        {
                                            'EXPR' : True,
                                            'DEFAULT' : ['BPC', ['hasher', 'mask_obj']]
                                        }
                                    ]
                                }#}}}
                            },
                        },
                    ]
                }#}}}
            },
        }, #}}}
        'mask_obj' : { #{{{
            'FILL' : [
                [
                    'SELF', [ 'key', ['config','IFL', 'dspt'] ],
                ],
                {
                    'DEFAULT' : {
                        'supress' : { #{{{
                            'DEFAULT' : {
                                'all' : {
                                    'DEFAULT' : 0,
                                },
                                'vals' : {
                                    'DEFAULT' : [],
                                },
                            },
                        }, #}}}
                        'sort' : {#{{{
                            'DEFAULT' : {
                                'enable' : {
                                    'DEFAULT': False,
                                },
                                'mode' :{
                                    'DEFAULT': 'alphabetically',
                                }
                            }
                        },#}}}
                        'plhd' : { #{{{
                            'DEFAULT' : {
                                'enable' : {
                                    'DEFAULT' : 0,
                                },
                                'value' : {
                                    'DEFAULT' : '',
                                },
                            },
                        }#}}}
                    },
                },
            ],

        },#}}}
        'injection' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'struct_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT' : {
                        'injection' : {
                            'DEFAULT' : None,
                            'TYPE' : 'list',
                            'FILL' : [
                                [ 'ARG_CP', ['value'], ],
                                {
                                    'DEFAULT' : {
                                        'injection_type' : {
                                            'TYPE' : 'str',
                                            'DEFAULT' : None
                                        },
                                        'txt' : {
                                            'DEFAULT' : []
                                        },
                                        'range': {
                                            'DEFAULT' : [
                                                {
                                                    'DEFAULT' : 0
                                                },
                                                {
                                                    'DEFAULT' : 0
                                                },
                                                {
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'int'
                                                },
                                                {
                                                    'DEFAULT' : None,
                                                    'TYPE' : 'int'
                                                }
                                            ]
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }#}}}
            },
        }, #}}}
        'launch' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'struct_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT' : {
                        'cmds' : {#{{{
                            'DEFAULTS' : [],
                            'FILL' : [
                                [ 'ARG_CP', ['value'] ],
                                {
                                    'DEFAULT' : None,
                                    'type' : 'str'
                                }
                            ]
                        },#}}}
                        'pwds' : {#{{{
                            'DEFAULTS' : {},
                            'FILL' : [
                                [ 'ARG_CP', ['key'] ],
                                {
                                    'DEFAULT' : {
                                        'fname' :{
                                            'DEFAULT' : None,
                                            'type' : 'str'
                                        },
                                        'ftype' :{
                                            'DEFAULT' : None,
                                            'type' : 'str'
                                        },
                                        'parse_args' :{
                                            'DEFAULT' : [],
                                            'FILL' : [
                                                [ 'ARG_CP', ['value'] ],
                                                {
                                                    'TYPE' : 'str',
                                                    'DEFAULT' : None
                                                }
                                            ]
                                        }
                                    }
                                }
                            ]
                        },#}}}
                    }
                }#}}}
            },
        }, #}}}
    },#}}}
    'main' : {#{{{
        'extern' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'DEFAULT' : 'main'
                },#}}}
                'struct_type' : {#{{{
                    'DEFAULT' : 'extern'
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'EXPR' : 1,
                    'DEFAULT' : [ 'BPC', ['hasher', 'injection_data'], ],
                }#}}}
            },
        }, #}}}
        'config' : { #{{{
            'DEFAULT' : {
                'ohmfa_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'config_type' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'name' : {#{{{
                    'TYPE' : 'str',
                    'DEFAULT' : None
                },#}}}
                'version' : {#{{{
                    'DEFAULT' : 0
                },#}}}
                'data' : {#{{{
                    'DEFAULT' : {}
                }#}}}
            },
        }, #}}}
        'ohmfi' : { #{{{
            'DEFAULT' : {
                'config': {#{{{
                    'DEFAULT' : {
                        'main': {#{{{
                            'DEFAULT' : {
                                'extern' : {#{{{
                                    'DEFAULT' : {},
                                    'FILL' :[
                                        [ 'ARG_CP', ['key'] ],
                                        {
                                            'DEFAULT' : 'json'
                                        }
                                    ]
                                },#}}}
                            }
                        },#}}}
                        'IFL': {#{{{
                            'DEFAULT' : {
                                'dspt' : {#{{{
                                    'DEFAULT' : {},
                                    'FILL' :[
                                        [ 'ARG_CP', ['key'] ],
                                        {
                                            'DEFAULT' : 'json'
                                        }
                                    ]
                                },#}}}
                                'drsr': {#{{{
                                    'DEFAULT' : {},
                                    'FILL' :[
                                        [ 'ARG_CP', ['key'] ],
                                        {
                                            'DEFAULT' : 'json'
                                        }
                                    ]
                                },#}}}
                                'mask' : {#{{{
                                    'DEFAULT' : {},
                                    'FILL' :[
                                        [ 'ARG_CP', ['key'] ],
                                        {
                                            'DEFAULT' : 'json'
                                        }
                                    ]
                                },#}}}
                                'injection' : {#{{{
                                    'DEFAULT' : {},
                                    'FILL' :[
                                        [ 'ARG_CP', ['key'] ],
                                        {
                                            'DEFAULT' : 'json'
                                        }
                                    ]
                                },#}}}
                                'launch': {#{{{
                                    'DEFAULT' : {},
                                    'FILL' :[
                                        [ 'ARG_CP', ['key'] ],
                                        {
                                            'DEFAULT' : 'json'
                                        }
                                    ]
                                },#}}}
                            }
                        },#}}}
                        'scrape': {#{{{
                            'DEFAULT' : {
                                'dspt': {#{{{
                                    'DEFAULT' : {},
                                    'FILL' :[
                                        [ 'ARG_CP', ['key'] ],
                                        {
                                            'DEFAULT' : 'json'
                                        }
                                    ]
                                },#}}}
                                'login': { #{{{
                                    'DEFAULT' : {},
                                    'FILL' :[
                                        [ 'ARG_CP', ['key'] ],
                                        { 'DEFAULT' : 'json' }
                                    ]
                                }#}}}
                            }
                        },#}}}
                        'OPs': {#{{{
                            'DEFAULT' : {
                                'dspt': {#{{{
                                    'DEFAULT' : {},
                                    'FILL' :[
                                        [ 'ARG_CP', ['key'] ],
                                        { 'DEFAULT' : 'json' }
                                    ]
                                },#}}}
                            }
                        }#}}}
                    }
                },#}}}
                'IFL_objs' : {#{{{
                    'DEFAULT' : {},
                    'FILL' :[
                        [ 'ARG_CP', ['key'] ],
                        {
                            'DEFAULT' : {
                                'scehma' : {#{{{
                                    'DEFAULT' : 'json'
                                },#}}}
                                'mfile' : {#{{{
                                    'DEFAULT' : 'txt'
                                },#}}}
                                'IFL' : {#{{{
                                    'DEFAULT' : 'json'
                                },#}}}
                                'matches' : {#{{{
                                    'DEFAULT' : 'json'
                                },#}}}
                                'outputs' : { #{{{
                                    'DEFAULT' : {
                                        'paged' : {#{{{
                                            'DEFAULT' : {},
                                            'FILL' :[
                                                [ 'ARG_CP', ['key'] ],
                                                {
                                                    'EXPR' : 1,
                                                    'DEFAULT' : {}
                                                }
                                            ]
                                        },#}}}
                                        'dfile' : {#{{{
                                            'DEFAULT' : {},
                                            'FILL' :[
                                                [ 'ARG_CP', ['key'] ],
                                                { 'DEFAULT' : 'txt' }
                                            ]
                                        },#}}}
                                    },
                                },#}}}
                            }
                        }
                    ]
                }#}}}
            }
        },#}}}
        'DEFAULTS' : { #{{{
            'DEFAULT' : {
                'hasher_objs' : {#{{{
                    'DEFAULT' : [
                        'IFL',
                        'container',
                        'group'
                    ]
                },#}}}
                'obj_terms' : {#{{{
                    'DEFAULT' : [
                        'uobjs',
                        'lobjs',
                        'iobjs',
                        'wobjs',
                        'root'
                    ]
                },#}}}
                'config' : {#{{{
                    'DEFAULT' : [
                        'dspt',
                        'drsr',
                        'mask',
                        'extern',
                        'sdrsr',
                        'smask',
                        'credentials'
                    ]
                },#}}}
                'input_types' : {#{{{
                    'DEFAULT' : [
                        'mfile',
                        'extern'
                    ]
                },#}}}
                'output_types' : {#{{{
                    'DEFAULT' : [
                        'dfile',
                        'delta',
                        'paged'
                    ]
                },#}}}
                'pwd_file_type' : {#{{{
                    'DEFAULT' : [
                        'csv'
                    ]
                }#}}}
            }
        }, #}}}
    },#}}}
    'utilities' : {#{{{
        'bpc' : { #{{{
            'REQUIRED': {#{{{
                'DEFAULT' : False
            },#}}}
            'NO_OVERRIDE': {#{{{
                'DEFAULT' : False
            },#}}}
            'EXPR': {#{{{
                'DEFAULT' : False
            },#}}}
            'DEFAULT' : {#{{{
                'REQUIRED': True,
                'DEFAULT' : None,
                #'TYPE' : ':all'
                'TYPE' : 'str'
            },#}}}
            'TYPE' : {#{{{
                'DEFAULT' : None,
                'TYPE' : ['list', 'str']
            },#}}}
            'FILL' :{#{{{
                'DEFAULT': [
                    {
                        'DEFAULT' : [
                            {
                                'DEFAULT' : None,
                                'TYPE' : 'str'
                            },
                            {
                                'DEFAULT' : [],
                            }
                        ],
                    },
                    {
                        'DEFAULT' : {},
                    }
                ],
            }#}}}
        },#}}}
        'EXPR' : { #{{{
            'BPC': {#{{{
                'DEFAULT' : [
                    {
                        'DEFAULT' : None,
                        'TYPE' : 'str'
                    },
                ],
            },#}}}
            'SELF': {#{{{
                'DEFAULT' : [
                    {
                        'DEFAULT' : None,
                        'TYPE' : 'str'
                    },
                    {
                        'DEFAULT' : [],
                        'FILL' : [
                            ['ARG_CP', ['value']],
                            {
                                'DEFAULT' : None,
                                'TYPE' : 'str',
                            }
                        ]
                    },
                    {
                        'DEFAULT' : [],
                        'FILL' : [
                            ['ARG_CP', ['value']],
                            {
                                'DEFAULT' : None,
                                'TYPE' : 'str',
                            }
                        ]
                    },
                    {
                        'DEFAULT' : False,
                    },
                    {
                        'DEFAULT' : None,
                        'TYPE' : ['str','int']
                    },
                ],
            },#}}}
            'ARG' : {#{{{
                'DEFAULT' : [
                    {
                        'DEFAULT' : None,
                        'TYPE' : 'str'
                    },
                    {
                        'DEFAULT' : [],
                        'FILL' : [
                            ['ARG_CP', ['value']],
                            {
                                'DEFAULT' : None,
                                'TYPE' : 'str',
                            }
                        ]
                    },
                    {
                        'DEFAULT' : [],
                        'FILL' : [
                            ['ARG_CP', ['value']],
                            {
                                'DEFAULT' : None,
                                'TYPE' : 'str',
                            }
                        ]
                    },
                    {
                        'DEFAULT' : False,
                    },
                    {
                        'DEFAULT' : None,
                        'TYPE' : ['str','int']
                    },
                ],
            },#}}}
            'ARG_CP' : {#{{{
                'DEFAULT' : [
                    {
                        'DEFAULT' : None,
                        'TYPE' : 'str'
                    },
                    {
                        'DEFAULT' : [],
                        'FILL' : [
                            ['ARG_CP', ['value']],
                            {
                                'DEFAULT' : None,
                                'TYPE' : 'str',
                            }
                        ]
                    },
                    {
                        'DEFAULT' : [],
                        'FILL' : [
                            ['ARG_CP', ['value']],
                            {
                                'DEFAULT' : None,
                                'TYPE' : 'str',
                            }
                        ]
                    },
                    {
                        'DEFAULT' : False,
                    },
                    {
                        'DEFAULT' : None,
                        'TYPE' : ['str','int']
                    },
                ],
            },#}}}
            'GLOB' :{#{{{
                'DEFAULT' : [
                    {
                        'DEFAULT' : None,
                        'TYPE' : 'str'
                    },
                    {
                        'DEFAULT' : [],
                        'FILL' : [
                            ['ARG_CP', ['value']],
                            {
                                'DEFAULT' : None,
                                'TYPE' : 'str',
                            }
                        ]
                    },
                    {
                        'DEFAULT' : [],
                        'FILL' : [
                            ['ARG_CP', ['value']],
                            {
                                'DEFAULT' : None,
                                'TYPE' : 'str',
                            }
                        ]
                    },
                    {
                        'DEFAULT' : False,
                    },
                    {
                        'DEFAULT' : None,
                        'TYPE' : ['str','int']
                    },
                ],
                'DEFAULT': [
                    {
                        'DEFAULT' : [],
                        'FILL' : [
                            ['ARG_CP', ['value']],
                            {
                                'DEFAULT' : None,
                                'TYPE' : 'str',
                            }
                        ]
                    },
                ],
            }#}}}
        },#}}}
    }#}}}

}#}}}

def getBpc(self,group,bpc_name,arg=None) : #{{{
    bpm = self['bpm']
    return copy.deepcopy(bpm[group][bpc_name])
#}}}

def genFromBp(self,group,bpc_name,arg=None) : #{{{
    bpm = self['bpm']
    bpc = getBpc(self,group,bpc_name,arg)
    arg = __bpg_recurse(self,bpc,arg,arg,arg,None)
    return arg

#}}}

def __bpg_recurse(self,bpc,arg,rarg,prarg,key) : #{{{

    print('-------------BPC')
    pp.pprint(bpc)
    bpc = __computeDefault(self, bpc, arg, rarg)
    print('-------------BPC after CD')
    pp.pprint(bpc)
    print('-------------rarg')
    pp.pprint(rarg)
    retu = __params_check(self, bpc, arg, rarg)
    if key is not None :
        prarg[key] = retu
    if rarg is None :
        rarg = retu
    if arg is None :
        arg = rarg
    print('-------------rarg after PC')
    pp.pprint(rarg)
    bpc = __expandBPC(self, bpc, arg, rarg)
    print('-------------EXPANDED BPC',)
    pp.pprint(bpc)
    if isinstance(bpc,list) and len(bpc) > 0 and isinstance(bpc[0],dict) and 'DEFAULT' in bpc[0]:
        for n, item in enumerate(bpc) :
            if n+1 > len(rarg) :
                item['REQUIRED'] = False  if 'REQUIRED' not in item else item['REQUIRED']
                if  item['REQUIRED'] :
                    traceback.print_stack()
                    sys.exit('ERROR: fuck you')
                else :
                    rarg.append(None)
            print('=========== IDX: ',end='')
            print(n)
            __bpg_recurse(self,item,arg,rarg[n],rarg,n )
    elif isinstance(bpc,dict) and 'DEFAULT' :
        for key in bpc :
            if 'DEFAULT' not in bpc[key] :
                break
            if key not in rarg :
                bpc[key]['REQUIRED'] = False  if 'REQUIRED'  not in bpc[key] else bpc[key]['REQUIRED']
                if  bpc[key]['REQUIRED'] :
                    traceback.print_stack()
                    sys.exit('ERROR: fuck you')
                else :
                    rarg[key] = None
            print('============ KEY: ',end='')
            print(key)
            __bpg_recurse(self,bpc[key],arg, rarg[key], rarg,key)
    return rarg
#}}}

def __computeDefault (self, bpc, arg, rarg) : #{{{
    default = copy.deepcopy(bpc['DEFAULT'])
    if 'EXPR' in bpc and bpc['EXPR'] is True :
        bpc['EXPR'] = False
        expr = bpc['DEFAULT']
        default = __computeExpr(self, expr, arg, rarg)
    bpc['DEFAULT'] = default
    return bpc
#}}}

def __computeExpr(self,expr,arg,rarg) : #{{{
    print('     -------------COMPUTE EXPR')
    print('     ',end='')
    print(expr)
    expr_name = expr[0]
    expr_args = expr[1]
    if expr_name == 'BPC' :
        result = copy.deepcopy(getBpc(self,expr_args[0],expr_args[1]))
        result = __expandBPC(self, result, arg, rarg)
        print('     -------------COMPUTED BPC')
        print('     ',end='')
        pp.pprint(result)
    elif expr_name == 'GLOB':
        result = __glob(self,expr_args)
    else :
        result = __get_items(self, arg, rarg, expr_name, expr_args)
        print('     -------------COMPUTED ITEMS')
        print('     ',end='')
        pp.pprint(result)
    return result
#}}}

def __get_items(self ,arg, rarg, expr_name, expr_args): #{{{
    print('    ------------ EXPR_NAME:')
    print('     ',end='')
    print(expr_name)

    if expr_name != 'ARG_CP' :
        if expr_name == 'SELF' :
            narg = self
        elif expr_name == 'ARG' :
            narg = arg
        else :
            traceback.print_stack()
            sys.exit('ERROR: fuck you')
        keys   = expr_args[1]
        n=0
        while n < len(keys) :
            narg = narg[keys[n]]
            n+=1
        del expr_args[1]

    else :
        narg = rarg

    print('     -------------NARG after')
    print('     ',end='')
    print('     EXPR_NAME: ',end='')
    print(expr_name)
    print('     ',end='')
    pp.pprint(narg)
    item_type = expr_args[0]
    enablePlhd = 0
    List = []
    if len(expr_args) == 4 :
        enablePlhd = expr_args[2]
        plhd = expr_args[3]
    if enablePlhd :
        List = plhd
        List = range(0,len(plhd),1)
    else :
        if isinstance(narg, dict) :
            if item_type == 'key' :
                List = narg.keys()
            elif item_type == 'value':
                List = narg.values()
            else:
                traceback.print_stack()
                sys.exit('ERROR: fuck you')
        elif isinstance(narg, list) :
            if item_type == 'value' :
                List = range(0,len(narg),1)
            else :
                traceback.print_stack()
                sys.exit('ERROR: fuck you')
        elif narg is None:
            List = []
        else :
            List = [narg]
    if len(expr_args) >=2 :
        notList   = expr_args[1]
    else :
        notList = []
    result    = [item for item in List if item not in notList]
    return result
#}}}


def __glob(self,expr_args): #{{{
    result = []
    for i in expr_args :
        result.append(glob.glob(i))
    return result
#}}}

def __params_check(self, bpc, arg, rarg) : #{{{
    bpc['NO_UNDEF']    = False  if 'NO_UNDEF'    not in bpc else bpc['NO_UNDEF']
    bpc['NO_OVERRIDE'] = False  if 'NO_OVERRIDE' not in bpc else bpc['NO_OVERRIDE']
    if 'TYPE' in bpc :
        if isinstance(bpc['TYPE'],list) :
            allowed_types = bpc['TYPE']
        else :
            allowed_types = [bpc['TYPE']]
    elif bpc['DEFAULT'] is not  None :
        allowed_types = [type(bpc['DEFAULT']).__name__]
    else :
        traceback.print_stack()
        sys.exit('ERROR: fuck you')

    allowed_types = [locate(x) for x in allowed_types]
    if rarg is None :
        if bpc['NO_UNDEF'] :
            traceback.print_stack()
            sys.exit('ERROR: fuck you')
        if isinstance( bpc['DEFAULT'], list) :
            rarg = []
        elif isinstance( bpc['DEFAULT'], dict) :
            rarg = {}
        else :
            rarg = copy.deepcopy(bpc['DEFAULT'])
    elif not isinstance(rarg, tuple(allowed_types)) :
        traceback.print_stack()
        sys.exit('ERROR: fuck you')
        if bpc['NO_OVERRIDE'] and bpc['DEFAULT'] != arg :
            traceback.print_stack()
            sys.exit('ERROR: fuck you')
    return rarg
#}}}

def __expandBPC (self, bpc, arg, rarg) : #{{{
    retu = copy.deepcopy(bpc['DEFAULT'])
    if 'FILL' in bpc :
        if isinstance(retu, dict) :
            retu.update(__addFill(self,bpc,arg,rarg,'dict'))
        if isinstance(retu, list) :
            retu.extend(__addFill(self,bpc,arg,rarg,'list'))
    return retu
#}}}

def __addFill (self, bpc, arg, rarg, Type) : #{{{
    fill = bpc['FILL']
    expr = fill[0]
    fill_list = __computeExpr(self, expr, arg, rarg)
    fill_bpc = fill[1]
    fill_bpc = __computeDefault (self, fill_bpc, arg, rarg)
    print('     -------------fillBPC')
    print('     ',end='')
    pp.pprint(fill_bpc)


    print('     -------------FILL_LIST')
    print('     ',end='')
    pp.pprint(fill_list)
    if Type == 'list' :
        filler=[]
        for item in fill_list :
            filler[item] = copy.deepcopy(fill_bpc)
    elif Type == 'dict' :
        filler={}
        for item in fill_list :
            filler[item] = copy.deepcopy(fill_bpc)
    print('     -------------FILLER')
    print('     ',end='')
    pp.pprint(filler)
    return filler
#}}}



self = genFromBp(self,'hasher','init',self)
print('=====================genFromBp')
pp = pprint.PrettyPrinter(indent=4,sort_dicts=True,compact=False,depth=3)
pp.pprint(self)
print('=====================genFromBp')
pp = pprint.PrettyPrinter(indent=4,sort_dicts=True,depth=1,compact=False,)
stuff = genFromBp(self,'hasher','dspt')
pp = pprint.PrettyPrinter(indent=4,sort_dicts=True,compact=False,)
pp.pprint(stuff)
#--------------------------------
# DOC {{{1
#--------------------------------
# ==OBJECTIVE
#----------------------
# TERMS
#----------------------
# == GENERAL
# bpc
# bp = DEFAULT + FILL
# arg
# == PARAM_CHECKING KEYS
# DEFAULT [:all]
# FILL [list]
# EXPR  [{expr_name},[expr_args]]
# NO OVERRIDE [bool]
# PROHIBIT_UNDEF [bool]
# REQUIRED [bool]
# == FILLIST
# KEY
# VALUE
# == TYPES
# :all
# str
# obj
# None
# list
# dict
# bool
# int
# == EXPRESSIONS (EXPR)
# ARG
# ARG_CP
# BPC
# GLOB
# == workflow
# bpc = params
# bp  = computed_params
# arg = ref
# bp = default + fill
#.a.b
# bpc = { 'DEFAULT' : value/bpc, ... }
# None = f(TYPE)
# ''   = bpc = DEFAULT
# {}   = bpc = DEFAULT + FILL(keys(self,arg,bp,args))
#   - {key_n : bpc_n}
# []   = bpc = DEFAULT + FILL(values(self,arg,bp,args))
#   - [bpc_n]
# ==PARAM CHECKING
# ==KEY FILLING
