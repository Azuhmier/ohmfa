mod prepare;
mod lexer;

use std::rc::Rc;
use std::cell::RefCell;
use std::fs::{File};
use std::io::{BufRead, BufReader};
use std::time::{Instant};
use std::collections::HashMap;
use std::fmt::Debug;

fn debug<T: Debug> (arg: &T) {
    println!("{:?}", arg);
    println!("Type: {}", std::any::type_name::<T>());
}

#[derive(Debug, Clone)]
struct Node {
  value: Option<Rc<String>>,
  class: String,
  ln : Option<usize>,
  children: Vec<Rc<RefCell<Node>>>,
}

#[derive(Debug)]
struct Tree {
  root: Rc<RefCell<Node>>,
}

impl Tree {
  pub fn new () -> Self {
    let root_node = Node {
        value: None,
        class: "root".to_string(),
        ln: None,
        children: Vec::<Rc<RefCell<Node>>>::new(),
    };
    Tree {
        root: Rc::new(RefCell::new(root_node)),
    }
  }
}

impl Node {
    pub fn new (value: Option<Rc<String>>, class: String, ln: Option<usize>) -> Self {
        if let Some(LN) = ln {
            if let Some(val) = value {
                Node {
                    value: Some(val),
                    class: class,
                    ln : Some(LN),
                    children: Vec::<Rc<RefCell<Node>>>::new(),
                }
            }
            else {
                Node {
                    value: None,
                    class: class,
                    ln: Some(LN),
                    children: Vec::<Rc<RefCell<Node>>>::new(),
                }
            }
        }
        else {
            if let Some(val) = value {
                Node {
                    value: Some(val),
                    class: class,
                    ln : None,
                    children: Vec::<Rc<RefCell<Node>>>::new(),
                }
            }
            else {
                Node {
                    value: None,
                    class: class,
                    ln : None,
                    children: Vec::<Rc<RefCell<Node>>>::new(),
                }
            }
        }
    }
    pub fn add_child(&mut self, node: Rc<RefCell<Node>> ) {
        self.children.push(node);
    }
}

fn file_to_vec(filename: &str) -> std::io::Result<Vec<String>> {
    let mut lines_out = Vec::new();
    let file_in = File::open(filename).unwrap();

    let reader = BufReader::new(file_in);
    for line in reader.lines() {
        lines_out.push(line?);
    }

    Ok(lines_out)
}

fn main() -> std::io::Result<()> {

    let mut nodes = HashMap::<String, Vec<Rc<RefCell<Node>>>>::new();
    nodes.insert("AUTHOR".to_string(), Vec::<Rc<RefCell<Node>>>::new());
    nodes.insert("TITLE".to_string(), Vec::<Rc<RefCell<Node>>>::new());
    nodes.insert("SERIES".to_string(), Vec::<Rc<RefCell<Node>>>::new());
    nodes.insert("SECTION".to_string(), Vec::<Rc<RefCell<Node>>>::new());
    nodes.insert("CONTAINER_1".to_string(), Vec::<Rc<RefCell<Node>>>::new());
    nodes.insert("CONTAINER_2".to_string(), Vec::<Rc<RefCell<Node>>>::new());
    nodes.insert("URL".to_string(), Vec::<Rc<RefCell<Node>>>::new());
    nodes.insert("DESCRIPTION".to_string(), Vec::<Rc<RefCell<Node>>>::new());
    nodes.insert("LABEL".to_string(), Vec::<Rc<RefCell<Node>>>::new());
    nodes.insert("ATTR".to_string(), Vec::<Rc<RefCell<Node>>>::new());
    nodes.insert("TAG".to_string(), Vec::<Rc<RefCell<Node>>>::new());
    nodes.insert("KEY".to_string(), Vec::<Rc<RefCell<Node>>>::new());
    nodes.insert("root".to_string(), Vec::<Rc<RefCell<Node>>>::new());

    let mut tree  = Tree::new();
    nodes.get_mut(&String::from("root")).unwrap().push(Rc::clone(&tree.root));

    let args: Vec<String> = std::env::args().collect();
    if args.len() > 1 {
        let filename = &args[1];
        let start = Instant::now();

        //Strip leading and trailing whitespace
        let lines = file_to_vec(filename)?;

        //Prepare Lines
        let mut prepared_lines: Vec<String> = vec![];
        for line in lines {
            let prepared_line = prepare::prepare(line);
            prepared_lines.push(prepared_line.to_owned());
        }

        //Lexer & Parser
        //let mut nodes = HashMap::new();
        let mut lexer  = lexer::Lexer::new(&prepared_lines);
        while let Some(token) = lexer.next() {
            match &token {
                lexer::Tokens::LeftBracket(_z,_e,_ln)     => {
                // Group
                    println!("===============================");
                    println!("NODE: GROUP");
                    println!("RAW: [");
                    //let node = Rc::new(RefCell::new(Node::new(Some(Rc::new(word.to_owned())), "TAG".to_string(),Some(*ln))));
                    //nodes.get_mut(&String::from("root")).unwrap().last().unwrap().borrow_mut().add_child(Rc::clone(&node));
                    //nodes.get_mut(&String::from("TAG")).unwrap().push(Rc::clone(&node));
                },
                lexer::Tokens::RightBracket(z,_e,_ln)    => {
                //End Group: Ensure closing brackets
                        if *z != 0 as usize  {
                            println!("===============================");
                            println!("ACTION: END GROUP");
                            println!("RAW: ]");
                            //let node = Rc::new(RefCell::new(Node::new(Some(Rc::new(word.to_owned())), "TAG".to_string(),Some(*ln))));
                            //nodes.get_mut(&String::from("root")).unwrap().last().unwrap().borrow_mut().add_child(Rc::clone(&node));
                            //nodes.get_mut(&String::from("TAG")).unwrap().push(Rc::clone(&node));
                        }
                        else {
                            println!("ERROR {:?}", &token)
                        }
                },
                lexer::Tokens::SemiColon(z,_e,_ln)       => {
                //Container type 1
                        if *z != 0 as usize  {
                            println!("===============================");
                            println!("NODE: CONTAINER_1");
                            println!("RAW: ;");
                            //let node = Rc::new(RefCell::new(Node::new(Some(Rc::new(word.to_owned())), "TAG".to_string(),Some(*ln))));
                            //nodes.get_mut(&String::from("root")).unwrap().last().unwrap().borrow_mut().add_child(Rc::clone(&node));
                            //nodes.get_mut(&String::from("TAG")).unwrap().push(Rc::clone(&node));
                        }
                        else {
                            println!("ERROR {:?}", &token)
                        }
                },
                lexer::Tokens::Comma(z,_e,_ln)           => {
                //Container type 2
                        if *z != 0 as usize  {
                            println!("===============================");
                            println!("NODE: CONTAINER_2");
                            println!("RAW: ,");
                            //let node = Rc::new(RefCell::new(Node::new(Some(Rc::new(word.to_owned())), "TAG".to_string(),Some(*ln))));
                            //nodes.get_mut(&String::from("root")).unwrap().last().unwrap().borrow_mut().add_child(Rc::clone(&node));
                            //nodes.get_mut(&String::from("TAG")).unwrap().push(Rc::clone(&node));
                        }
                        else {
                            println!("ERROR {:?}", &token)
                        }
                },
                lexer::Tokens::Word(word_string, z,_e,ln)    => {
                //Word -> Key, Tag, or Line marker (example: "TITLE")
                    if *z == 0 as usize  {
                    // Line marker (example: "TITLE")
                    // Creats "Generic" Node from the consecutive Literal(s)
                        if word_string.chars().all(|x| x.is_alphanumeric()) {
                            if word_string == "AUTHOR" {
                            // Line Marker: Auther
                            // General Structure: AUTHOR *author1* & *author2*
                            // Capture the first literal as the value for the node and the
                            // first member of the collab vector consecutive literals denoted
                            // by '&' will be pushed to a collab vector for later processing.
                                println!("===============================");
                                println!("NODE: {}", &word_string);
                                let mut collab = Vec::<String>::new();
                                loop {
                                    if let Some(token) = lexer.peek() {
                                        match &token {
                                            lexer::Tokens::Literal(literal_string, _z,_e, next_ln) => {

                                                if next_ln > ln {
                                                    break;
                                                }
                                                else {
                                                    lexer.next();
                                                    collab.push(literal_string.to_owned());
                                                }
                                            }
                                            lexer::Tokens::Amp(_z,_e,next_ln) => {
                                                if next_ln > ln {
                                                    break;
                                                }
                                                else {
                                                    lexer.next();
                                                    println!("TAKE: &");
                                                }
                                            }
                                            lexer::Tokens::Word(word_string,_z,_e,next_ln)     => {
                                                if next_ln > ln {
                                                // Word is on next line
                                                    println!("PEAK: {}", &word_string);
                                                    break;
                                                }
                                                else {
                                                    println!("ERROR: {:?}", &token);
                                                    break;
                                                }
                                            }
                                            lexer::Tokens::LeftBracket(_z,_e,_next_ln)     => {
                                            // Valid token: for Group
                                                println!("PEAK: [");
                                                break;
                                            }
                                            _ => {
                                                println!("ERROR: {:?}", &token);
                                                break;
                                            }
                                        };
                                    }
                                    else {
                                        println!("ERROR: Token is None");
                                        break;
                                    }
                                }
                                if collab.len() > 1 {
                                // Collab Post Processing
                                // Collab vectors with lengths greater than 1 indicate a collab
                                    println!("VAL: {:?}", &collab[0]);
                                    println!("COLLAB: {:?}", &collab);
                                    let node = Rc::new(RefCell::new(Node::new(Some(Rc::new(collab[0].to_owned())), "AUTHOR".to_string(),Some(*ln))));
                                    nodes.get_mut(&String::from("SECTION")).unwrap().last().unwrap().borrow_mut().add_child(Rc::clone(&node));
                                    nodes.get_mut(&String::from("AUTHOR")).unwrap().push(Rc::clone(&node));
                                }
                                else {
                                    println!("VAL: {:?}", &collab[0]);
                                    let node = Rc::new(RefCell::new(Node::new(Some(Rc::new(collab[0].to_owned())), "AUTHOR".to_string(),Some(*ln))));
                                    nodes.get_mut(&String::from("SECTION")).unwrap().last().unwrap().borrow_mut().add_child(Rc::clone(&node));
                                    nodes.get_mut(&String::from("AUTHOR")).unwrap().push(Rc::clone(&node));
                                }
                            }
                            else {
                            //Non Author Line Marker
                                println!("===============================");
                                println!("NODE: {}", &word_string);
                                if let Some(token) = lexer.peek() {
                                // General Structure: MARKER *CONTENT*
                                // Capture the first literal as the value for the node
                                    match &token {
                                        lexer::Tokens::Literal(literal_string, _z,_e,next_ln) => {

                                            if next_ln > ln {
                                                break;
                                            }
                                            else {
                                                let _next_token = lexer.next();
                                                println!("VAL: {}",&literal_string);
                                                let node = Rc::new(RefCell::new(Node::new(Some(Rc::new(literal_string.to_owned())), word_string.to_owned(),Some(*ln))));
                                                nodes.get_mut(&String::from("root")).unwrap().last().unwrap().borrow_mut().add_child(Rc::clone(&node));
                                                nodes.get_mut(&word_string.to_owned()).unwrap().push(Rc::clone(&node));
                                            }
                                        }
                                        lexer::Tokens::Word(word_string,_z,_e,next_ln)     => {
                                            if next_ln > ln {
                                                println!("PEAK: {}", &word_string);
                                                break;
                                            }
                                            else {
                                                println!("ERROR: {:?}", &token);
                                                break;
                                            }
                                        }
                                        // Valid token: for Group
                                        lexer::Tokens::LeftBracket(_z,_e,_next_ln)     => {
                                            println!("PEAK: [");
                                            break;
                                        }
                                        _ => {
                                            println!("ERROR: {:?}", &token);
                                            break;
                                        }
                                    };
                                }
                                else {
                                    println!("ERROR: Token is None");
                                    break;
                                }
                            }

                        }
                        else {
                            // Ignore Token
                        }
                    }
                    else {
                    // Key or Tag
                    // Create node value from consecutive word tokens and determine type
                    // General Structure for Tag: word...word
                    // General Structure for key: word...word:
                    // Two flags: is_tag and is_collab
                        println!("===============================");
                        let mut is_tag : u32 = 1;
                        let mut is_collab: u32 = 0;
                        let mut word = String::from("");
                        let mut collab = Vec::<String>::new();
                        word.push_str(word_string);
                        loop {
                            if let Some(token) = lexer.peek() {
                                match &token {
                                    lexer::Tokens::Word(word_string, _z,_e,next_ln) => {
                                        if next_ln > ln {
                                            break;
                                        }
                                        else {
                                            lexer.next();
                                            word.push_str(&" ".to_string());
                                            word.push_str(&word_string);
                                        }
                                    }
                                    lexer::Tokens::RightBracket(_z,_e,next_ln)     => {
                                        if next_ln > ln {
                                            println!("ERROR: ]");
                                            break;
                                        }
                                        else {
                                            println!("PEEK: ]");
                                            break;
                                        }
                                    }
                                    lexer::Tokens::SemiColon(_z,_e,next_ln)     => {
                                        if next_ln > ln {
                                            println!("ERROR: ;");
                                            break;
                                        }
                                        else {
                                            println!("PEEK: ;");
                                            break;
                                        }
                                    }
                                    lexer::Tokens::Comma(_z,_e,next_ln)     => {
                                        if next_ln > ln {
                                            println!("ERROR: ,");
                                            break;
                                        }
                                        else {
                                            println!("PEEK: ,");
                                            break;
                                        }
                                    }
                                    lexer::Tokens::Colon(_z,_e,next_ln)     => {
                                        if next_ln > ln {
                                            println!("ERROR: :");
                                            break;
                                        }
                                        else {
                                            lexer.next();
                                            if word == "collab".to_string() {
                                            // Is collab key
                                                is_collab = 1;
                                                loop {
                                                    if let Some(token) = lexer.peek() {
                                                        match &token {
                                                            lexer::Tokens::Literal(next_string, _z,_e,next_ln) => {

                                                                if next_ln > ln {
                                                                    break;
                                                                }
                                                                else {
                                                                    lexer.next();
                                                                    collab.push(next_string.to_owned());
                                                                }
                                                            }
                                                            lexer::Tokens::Amp(_z,_e,next_ln) => {
                                                                if next_ln > ln {
                                                                    break;
                                                                }
                                                                else {
                                                                    lexer.next();
                                                                    println!("TAKE: &");
                                                                }
                                                            }
                                                            lexer::Tokens::RightBracket(_z,_e,next_ln)     => {
                                                                if next_ln > ln {
                                                                    println!("ERROR: ]");
                                                                    break;
                                                                }
                                                                else {
                                                                    println!("PEEK: ]");
                                                                    break;
                                                                }
                                                            }
                                                            _ => {
                                                                println!("ERROR: {:?}", &token);
                                                                break;
                                                            }

                                                        }
                                                    }
                                                    else {
                                                        println!("ERROR: Token is None");
                                                        break;
                                                    }
                                                }

                                            }
                                            else {
                                            // Is regular key
                                                is_tag = 0;
                                            }
                                            break;

                                        }
                                    }
                                    _ => {
                                        println!("ERROR: {:?}", &token);
                                        break;
                                    }
                                };
                            }
                            else {
                                println!("ERROR: Token is None");
                                break;
                            }
                        }
                        if is_collab == 1 {
                        // collab key
                                println!("ACTION: COLLAB");
                                println!("COLLAB {:?}", collab);
                        }
                        else {
                            if is_tag == 1 {
                                println!("NODE: TAG");
                                println!("VAL: {:?}",word);
                                let node = Rc::new(RefCell::new(Node::new(Some(Rc::new(word.to_owned())), "TAG".to_string(),Some(*ln))));
                                nodes.get_mut(&String::from("root")).unwrap().last().unwrap().borrow_mut().add_child(Rc::clone(&node));
                                nodes.get_mut(&String::from("TAG")).unwrap().push(Rc::clone(&node));
                            }
                            else {
                           // KEY
                                println!("NODE: KEY");
                                println!("TAKE: :");
                                println!("VAL: {:?}",word);
                                let node =
                                Rc::new(RefCell::new(Node::new(Some(Rc::new(word.to_owned())), "KEY".to_string(),Some(*ln))));
                                nodes.get_mut(&String::from("root")).unwrap().last().unwrap().borrow_mut().add_child(Rc::clone(&node));
                                nodes.get_mut(&String::from("KEY")).unwrap().push(Rc::clone(&node));

                            }
                        }

                    }
                },
                lexer::Tokens::Literal(string, _z,_e,ln) => {
                //Literal -> Attr or Label
                // Create node value from literal
                // General Structure for Attr: literal
                // General Structure for Label: literal=
                // Two flags: is_attr
                    println!("===============================");
                    let mut is_attr : u32 = 1;
                    if let Some(token) = lexer.peek() {
                        match &token {
                            lexer::Tokens::RightBracket(_z,_e,next_ln)     => {
                                if next_ln > ln {
                                    println!("ERROR: ]");
                                }
                                else {
                                    println!("PEEK: ]");
                                }
                            }
                            lexer::Tokens::SemiColon(_z,_e,next_ln)     => {
                                if next_ln > ln {
                                    println!("ERROR: ;");
                                }
                                else {
                                    println!("PEEK: ;");
                                }
                            }
                            lexer::Tokens::Comma(_z,_e,next_ln)     => {
                                if next_ln > ln {
                                    println!("ERROR: ,");
                                }
                                else {
                                    println!("PEEK: ,");
                                }
                            }
                            lexer::Tokens::Equal(_z,_e,next_ln)     => {
                                if next_ln > ln {
                                }
                                else {
                                    lexer.next();
                                    is_attr = 0;
                                }
                            }
                            _ => {
                                println!("ERROR: {:?}", &token);
                            }
                        };
                    }
                    else {
                        println!("ERROR: Token is None");
                    }

                    if is_attr == 1 {
                        println!("NODE: ATTR");
                        println!("VAL: {:?}",&string);
                        let node = Rc::new(RefCell::new(Node::new(Some(Rc::new(string.to_owned())), "ATTR".to_string(),Some(*ln))));
                        nodes.get_mut(&String::from("root")).unwrap().last().unwrap().borrow_mut().add_child(Rc::clone(&node));
                        nodes.get_mut(&String::from("ATTR")).unwrap().push(Rc::clone(&node));
                    }
                    else {
                    // Label
                        println!("NODE: LABEL");
                        println!("TAKE: =");
                        println!("VAL: {:?}",&string);
                        let node = Rc::new(RefCell::new(Node::new(Some(Rc::new(string.to_owned())), "LABEL".to_string(),Some(*ln))));
                        nodes.get_mut(&String::from("root")).unwrap().last().unwrap().borrow_mut().add_child(Rc::clone(&node));
                        nodes.get_mut(&String::from("LABEL")).unwrap().push(Rc::clone(&node));
                    }
                },
                _  => {
                        println!("ERROR: {:?}", token);
                }
            };
        }
        println!("NODAS {:#?}",nodes);
        println!("TREEAS {:#?}",&tree);



        let elapsed = start.elapsed();
        println!("\nelapsed time: {:.2?}\n", elapsed);

        Ok(())

    } else {
        println!("Usage: {} <input>", args[0]);
        Err(std::io::Error::new(std::io::ErrorKind::Other, "Usage: <input>"))
    }
}
/*
   skip line comments: * till * or EOL
   include notes: # 

   (alias/label)(attr/tags)
   X~o
   \


*/
