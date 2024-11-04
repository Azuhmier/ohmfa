use regex::Regex;
use lazy_static::lazy_static;
//use std::time::{Instant};

pub fn prepare(line: String) -> String {

    lazy_static! {
        static ref RE_AUTHOR      : Regex  = Regex::new(r"^\s*[bB]y\s+([^`]+)(?:`([^`]+))*").unwrap();
        static ref RE_AUTHOR_AMP  : Regex  = Regex::new(r"[^&]+").unwrap();
        static ref RE_LB          : Regex  = Regex::new(r"\(").unwrap();
        static ref RE_RB          : Regex  = Regex::new(r"\)").unwrap();
        static ref RE_TITLE       : Regex  = Regex::new(r"^\s*>([^`]+)(?:`([^`]+))*").unwrap();
        static ref RE_DSCP        : Regex  = Regex::new(r"^\s*#(.+)").unwrap();
        static ref RE_SECTION     : Regex  = Regex::new(r"\s*%+([^%]+)[% ]*").unwrap();
        static ref RE_SERIES      : Regex  = Regex::new(r"=+/([^=+]+)/=+").unwrap();
        static ref RE_TAGS        : Regex  = Regex::new(r"^\s*(\[.*\])([^\[\]]*)$").unwrap();
        static ref RE_URL         : Regex  = Regex::new(r"^\s*(http[^ ]+)\s*(?:`([^`]+))*").unwrap();
        static ref RE_COMMENT     : Regex  = Regex::new(r"^\s*~(.+)").unwrap();
        static ref RE_EXCL        : Regex  = Regex::new(r"[xX]").unwrap();
        static ref RE_O           : Regex  = Regex::new(r"[oO0]").unwrap();
    }

    if RE_AUTHOR.is_match(&line) {
        let mut new_line = String::from("AUTHOR ");
        let delim = String::from(" & ");
        let literal = String::from("*");
        let cap = RE_AUTHOR.captures(&line).unwrap();
        for (i, cap2) in RE_AUTHOR_AMP.captures_iter(&cap[1]).enumerate() {

            if i >= 1 {
                new_line.push_str(&delim);
            }
            new_line.push_str(&literal);
            new_line.push_str(&cap2[0]);
            new_line.push_str(&literal);
        }
        if cap.get(2).is_some() {
             let space = String::from(" ");
             let attr = RE_LB.replace_all(&cap[2], "[").to_string();
             let attr2 = RE_RB.replace_all(&attr, "]").to_string();
             new_line.push_str(&space);
             new_line.push_str(&attr2);
        }
        new_line
    }
    else if RE_TITLE.is_match(&line) {
        let cap = RE_TITLE.captures(&line).unwrap();
        let mut new_line = String::from("TITLE ");
        let literal = String::from("*");
        new_line.push_str(&literal);
        new_line.push_str(&cap[1]);
        new_line.push_str(&literal);
        if cap.get(2).is_some() {
             let space = String::from(" ");
             let attr = RE_LB.replace_all(&cap[2], "[").to_string();
             let attr2 = RE_RB.replace_all(&attr, "]").to_string();
             new_line.push_str(&space);
             new_line.push_str(&attr2);
        }
        new_line
    }
    else if RE_TAGS.is_match(&line) {
        let cap = RE_TAGS.captures(&line).unwrap();
        let mut new_line = String::from("");
        new_line.push_str(&cap[1]);
        if cap.get(2).is_some() {
             let ops = RE_O.replace_all(&cap[2], "$").to_string();
             let ops2 = RE_EXCL.replace_all(&ops, "#").to_string();
             new_line.push_str(&ops2);
        }
        new_line
    }
    else if RE_COMMENT.is_match(&line) {
        let cap = RE_COMMENT.captures(&line).unwrap();
        let mut new_line = String::from("// ");
        new_line.push_str(&cap[1]);
        new_line
    }
    else if RE_URL.is_match(&line) {
        let cap = RE_URL.captures(&line).unwrap();
        let mut new_line = String::from("URL ");
        let literal = String::from("*");
        new_line.push_str(&literal);
        new_line.push_str(&cap[1]);
        new_line.push_str(&literal);
        if cap.get(2).is_some() {
             let space = String::from(" ");
             let attr = RE_LB.replace_all(&cap[2], "[").to_string();
             let attr2 = RE_RB.replace_all(&attr, "]").to_string();
             new_line.push_str(&space);
             new_line.push_str(&attr2);
        }
        new_line
    }
    else if RE_DSCP.is_match(&line) {
        let cap = RE_DSCP.captures(&line).unwrap();
        let mut new_line = String::from("DESCRIPTION ");
        let literal = String::from("*");
        new_line.push_str(&literal);
        new_line.push_str(&cap[1]);
        new_line.push_str(&literal);
        new_line
    }
    else if RE_SECTION.is_match(&line) {
        let cap = RE_SECTION.captures(&line).unwrap();
        let mut new_line = String::from("SECTION ");
        let literal = String::from("*");
        new_line.push_str(&literal);
        new_line.push_str(&cap[1]);
        new_line.push_str(&literal);
        new_line
    }
    else if RE_SERIES.is_match(&line) {
        let cap = RE_SERIES.captures(&line).unwrap();
        let mut new_line = String::from("SERIES ");
        let literal = String::from("*");
        new_line.push_str(&literal);
        new_line.push_str(&cap[1]);
        new_line.push_str(&literal);
        new_line
    }
    else {
        line
    }

}
