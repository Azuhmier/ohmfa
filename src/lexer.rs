use std::fmt::{Debug};

#[derive(Debug, Clone)]
pub enum Tokens {
    LeftBracket(usize, usize, usize),
    RightBracket(usize, usize, usize),
    Colon(usize, usize, usize),
    Comma(usize, usize, usize),
    SemiColon(usize, usize, usize),
    Equal(usize, usize, usize),
    Amp(usize, usize, usize),
    Word(String, usize, usize, usize),
    Literal(String, usize, usize, usize),
}

//impl Copy for Tokens { }

#[derive(Debug)]
pub struct Lexer<'a> {
    chars: std::iter::Peekable<std::iter::Enumerate<std::str::Chars<'a>>>,
    lines:&'a Vec<String>,
    ln: usize,
    token_buffer: Vec<Tokens>,
}

impl<'a> Lexer<'a> {
    pub fn new(lines: &Vec<String>) -> Lexer{
        let tb = Vec::<Tokens>::new();

        Lexer {
            lines: lines,
            chars: lines[0].chars().enumerate().peekable(),
            ln: 0 as usize,
            token_buffer: tb,
        }
    }

    pub fn next(&mut self) -> Option<Tokens>{

        let len = self.lines.len();
        let mut retu :Option<Tokens> = None;
        if self.token_buffer.is_empty() {

            loop {
                if let Some(token) = self._next_token() {
                    retu = Some(token.clone());
                    break;
                }

                else if (len - 1) > self.ln {
                    self._next_line()
                }

                else  {
                    break;
                }
            }
        retu
        }
        else {
            Some(self.token_buffer.pop().unwrap())
        }
    }

    pub fn peek(&mut self) -> Option<Tokens>{

        let len = self.lines.len();
        let mut retu :Option<Tokens> = None;
        if self.token_buffer.is_empty() {

            loop {
                if let Some(token) = self._next_token() {
                    self.token_buffer.push(token.clone());
                    retu = Some(token);
                    break;
                }

                else if (len - 1) > self.ln {
                    self._next_line()
                }

                else  {
                    break;
                }
            }
        retu
        }
        else {
            let token = self.token_buffer.last().unwrap();
            Some(token.clone())
        }
    }

    fn _next_line(&mut self) {
        let len = self.lines.len();
        if (len - 1) > self.ln {
            self.ln += 1;
            self.chars =  self.lines[self.ln].chars().enumerate().peekable();
        }
    }

    fn _next_token(&mut self) -> Option<Tokens> {

        let mut token: Option<Tokens> = None;
        let not_words: [char; 9] = [']','[','*',':','=',' ',',',';','&'];

        while token.is_none() {
            if let Some(c) = self.chars.next() {
                token = match c.1 {
                    ' ' => {
                        continue;
                    }
                    '*' => {
                        let mut literal = String::new();
                        let mut z: usize = c.0;
                        while let Some(&c) = self.chars.peek() {
                            if c.1 != '*' {
                                literal.push(self.chars.next().unwrap().1);
                                z = c.0;
                            } else {
                                self.chars.next();
                                break;
                            }
                        }
                        Some(Tokens::Literal(literal, c.0 + 1, z, self.ln.to_owned()))
                    }
                    '[' => {
                        Some(Tokens::LeftBracket(c.0, c.0, self.ln.to_owned()))
                    }
                    ']' => {
                        Some(Tokens::RightBracket(c.0, c.0, self.ln.to_owned()))
                    }
                    ':' => {
                        Some(Tokens::Colon(c.0, c.0, self.ln.to_owned()))
                    }
                    ',' => {
                        Some(Tokens::Comma(c.0, c.0, self.ln.to_owned()))
                    }
                    '=' => {
                        Some(Tokens::Equal(c.0, c.0, self.ln.to_owned()))
                    }
                    ';' => {
                        Some(Tokens::SemiColon(c.0, c.0, self.ln.to_owned()))
                    }
                    '&' => {
                        Some(Tokens::Amp(c.0, c.0, self.ln.to_owned()))
                    }
                    _ => {
                        let mut ident = String::new();
                        let mut z: usize = c.0;
                        ident.push(c.1);

                        while let Some(&c) = self.chars.peek() {
                            if !(not_words.contains(&c.1)) {
                                ident.push(self.chars.next().unwrap().1);
                                z = c.0.to_owned();
                            } else {
                                break;
                            }
                        }
                        Some(Tokens::Word(ident, c.0, z , self.ln.to_owned()))
                    }
                };
            }
            else {
                break
            }

        }
        token

    }
}
