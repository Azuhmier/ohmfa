mod prepare;
mod lexer;

use std::fs::{File};
use std::io::{BufRead, BufReader};
use std::time::{Instant};



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
    let args: Vec<String> = std::env::args().collect();
    if args.len() > 1 {
        let filename = &args[1];
        let startt = Instant::now();
        let lines = file_to_vec(filename)?;

        let mut prepared_lines: Vec<String> = vec![];
        for line in lines {
            let prepared_line = prepare::prepare(line);
            prepared_lines.push(prepared_line.to_owned());
        }

        let mut lexer  = lexer::Lexer::new(&prepared_lines);
        while let Some(token) = lexer.next() {
            //println!("{:?}",&token);
            match &token {
                lexer::Tokens::LeftBracket(z,_e,_ln)     => {
                    println!("===============================");
                    println!("NODE: GROUP");
                    if *z == 5 as usize  {
                        //println!("{:?}",&string);
                        println!("RAW: [");
                    }
                    else {
                        println!("RAW: [");
                    }
                },
                lexer::Tokens::RightBracket(_z,_e,_ln)    => {
                        println!("===============================");
                        println!("ACTION: END GROUP");
                        println!("RAW: ]");
                },
                lexer::Tokens::Colon(_z,_e,_ln)           => {
                        println!("WRONGO :");
                },
                lexer::Tokens::Comma(_z,_e,_ln)           => {
                        println!("===============================");
                        println!("NODE: CONTAINER_2");
                        println!("RAW: ,");
                },
                lexer::Tokens::SemiColon(_z,_e,_ln)       => {
                        println!("===============================");
                        println!("NODE: CONTAINER_1");
                        println!("RAW: ;");
                },
                lexer::Tokens::Equal(_z,_e,_ln)           => {
                        println!("WRONGO =");
                },
                lexer::Tokens::Amp(_z,_e,_ln)             => {
                        println!("WRONGO &");
                },
                lexer::Tokens::Word(string, z,_e,ln)    => {
                    if *z == 0 as usize  {
                        if string.chars().all(|x| x.is_alphanumeric()) {
                            if string == "AUTHOR" {
                                println!("===============================");
                                let mut collab = Vec::<String>::new();
                                println!("NODE: {}", &string);
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
                                            lexer::Tokens::LeftBracket(_z,_e,_next_ln)     => {
                                                break;
                                            }
                                            _ => {
                                                break;
                                            }
                                        };
                                    }
                                    else {
                                        break;
                                        //ERROR
                                    }
                                }
                                if collab.len() > 1 {
                                    println!("VAL: {:?}", &collab[0]);
                                    println!("COLLAB: {:?}", &collab);
                                }
                                else {
                                    println!("VAL: {:?}", &collab[0]);
                                }
                            }
                            else {
                                println!("===============================");
                                println!("NODE: {}", &string);
                                if let Some(token) = lexer.peek() {
                                    match &token {
                                        lexer::Tokens::Literal(next_string, _z,_e,next_ln) => {

                                            if next_ln > ln {
                                                break;
                                            }
                                            else {
                                                let _next_token = lexer.next();
                                                println!("VAL: {}",&next_string);
                                            }
                                        }
                                        _ => {
                                            //ERROR;
                                        }
                                    };
                                }
                                else {
                                    break;
                                    //ERROR
                                }
                            }

                        }
                        else {
                        }
                    }
                    //ATTRS
                    else {
                        println!("===============================");
                        let mut word = String::from("");
                        let mut is_tag : u32 = 1;
                        let mut is_collab: u32 = 0;
                        let mut collab = Vec::<String>::new();
                        word.push_str(string);
                        loop {
                            if let Some(token) = lexer.peek() {
                                match &token {
                                    lexer::Tokens::Word(next_string, _z,_e,next_ln) => {
                                        if next_ln > ln {
                                            break;
                                        }
                                        else {
                                            lexer.next();
                                            word.push_str(&" ".to_string());
                                            word.push_str(&next_string);
                                        }
                                    }
                                    lexer::Tokens::RightBracket(_z,_e,next_ln)     => {
                                        if next_ln > ln {
                                            break;
                                        }
                                        else {
                                            println!("PEEK: ]");
                                            break;
                                        }
                                    }
                                    lexer::Tokens::LeftBracket(_z,_e,next_ln)     => {
                                        if next_ln > ln {
                                            break;
                                        }
                                        else {
                                            println!("PEEK: [");
                                            break;
                                        }
                                    }
                                    lexer::Tokens::SemiColon(_z,_e,next_ln)     => {
                                        if next_ln > ln {
                                            break;
                                        }
                                        else {
                                            //println!("{:?}",&string);
                                            println!("PEEK: ;");
                                            break;
                                        }
                                    }
                                    lexer::Tokens::Comma(_z,_e,next_ln)     => {
                                        if next_ln > ln {
                                            break;
                                        }
                                        else {
                                            //println!("{:?}",&string);
                                            println!("PEEK: ,");
                                            break;
                                        }
                                    }
                                    lexer::Tokens::Colon(_z,_e,next_ln)     => {
                                        if next_ln > ln {
                                            break;
                                        }
                                        else {
                                            lexer.next();
                                            if word == "collab".to_string() {
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
                                                            lexer::Tokens::Word(next_string, _z,_e,next_ln) => {
                                                                if next_ln > ln {
                                                                    break;
                                                                }
                                                                else {
                                                                    println!("WRONGO: {:?}", &next_string);
                                                                    //ERROR
                                                                }
                                                            }
                                                            lexer::Tokens::RightBracket(_z,_e,next_ln)     => {
                                                                if next_ln > ln {
                                                                    break;
                                                                }
                                                                else {
                                                                    println!("PEEK: ]");
                                                                    break;
                                                                }
                                                            }
                                                            lexer::Tokens::LeftBracket(_z,_e,next_ln)     => {
                                                                if next_ln > ln {
                                                                    break;
                                                                }
                                                                else {
                                                                    println!("PEEK: [");
                                                                    break;
                                                                }
                                                            }
                                                            lexer::Tokens::SemiColon(_z,_e,next_ln)     => {
                                                                if next_ln > ln {
                                                                    break;
                                                                }
                                                                else {
                                                                    //println!("{:?}",&string);
                                                                    println!("PEEK: ;");
                                                                    break;
                                                                }
                                                            }
                                                            lexer::Tokens::Comma(_z,_e,next_ln)     => {
                                                                if next_ln > ln {
                                                                    break;
                                                                }
                                                                else {
                                                                    //println!("{:?}",&string);
                                                                    println!("PEEK: ,");
                                                                    break;
                                                                }
                                                            }
                                                            _ => {
                                                                break;
                                                            }

                                                        }
                                                    }
                                                    else {
                                                        break;
                                                    }
                                                }

                                            }
                                            else {
                                                is_tag = 0;
                                            }
                                            break;

                                        }
                                    }
                                    _ => {
                                        break;
                                    }
                                };
                            }
                            else {
                                break;
                                //ERROR
                            }
                        }
                        if is_collab == 1 {
                                println!("ACTION: COLLAB");
                                println!("COLLAB {:?}", collab);
                        }
                        else {
                            if is_tag == 1 {
                                println!("NODE: TAG");
                            }
                            else {
                                println!("NODE: KEY");
                                println!("TAKE: :");
                            }
                            println!("VAL: {:?}",word);
                        }

                    }
                },
                lexer::Tokens::Literal(string, _z,_e,ln) => {
                    println!("===============================");
                    let mut is_attr : u32 = 1;
                    if let Some(token) = lexer.peek() {
                        match &token {
                            lexer::Tokens::RightBracket(_z,_e,next_ln)     => {
                                if next_ln > ln {
                                }
                                else {
                                    println!("PEEK: ]");
                                }
                            }
                            lexer::Tokens::LeftBracket(_z,_e,next_ln)     => {
                                if next_ln > ln {
                                }
                                else {
                                    println!("PEEK: [");
                                }
                            }
                            lexer::Tokens::SemiColon(_z,_e,next_ln)     => {
                                if next_ln > ln {
                                }
                                else {
                                    //println!("{:?}",&string);
                                    println!("PEEK: ;");
                                }
                            }
                            lexer::Tokens::Comma(_z,_e,next_ln)     => {
                                if next_ln > ln {
                                }
                                else {
                                    //println!("{:?}",&string);
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
                            }
                        };
                    }
                    else {
                        //ERROR
                    }
                    if is_attr == 1 {
                        println!("NODE: ATTR");
                    }
                    else {
                        println!("NODE: LABEL");
                        println!("TAKE: =");
                    }
                    println!("VAL: {:?}",&string);
                },
            };
        }



        let elapsed = startt.elapsed();
        println!("\nelapsed time: {:.2?}\n", elapsed);

        Ok(())

    } else {
        println!("Usage: {} <input>", args[0]);
        Err(std::io::Error::new(std::io::ErrorKind::Other, "Usage: <input>"))
    }
}
