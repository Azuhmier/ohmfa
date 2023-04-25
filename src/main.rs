use std::fs::{File};
use std::io::{BufRead, BufReader};
use std::path::Path;
use std::time::{Instant};

#[derive(Debug, PartialEq)]
enum LineEnding {
    Unix,
    Dos,
    Unknown
}

fn file_to_vec<P: AsRef<Path>, E>(filename: P) -> Result<(Vec<String>, LineEnding), E> {
    let file_in = File::open(&filename);
    let reader = BufReader::new(file_in);
    let mut lines_out = Vec::new();
    let mut last_char = None;
    let mut line_ending = LineEnding::Unknown;

    for line_result in reader.lines() {
        let line = line_result?;
        if let Some(c) = line.chars().last() {
            last_char = Some(c);
            if line_ending == LineEnding::Unknown {
                if c == '\n' {
                    line_ending = LineEnding::Unix;
                } else if c == '\r' {
                    line_ending = LineEnding::Dos;
                }
            }
        }
        lines_out.push(line);
    }

    // Determine newline at EOF
    if last_char == Some('\n') {
        println!("Newline at EOF");
    } else {
        println!("No newline at EOF");
    }

    // Print line ending type
    match line_ending {
        LineEnding::Unknown => println!("No line endings detected"),
        LineEnding::Unix => println!("UTF-8 is Unix"),
        LineEnding::Dos => println!("UTF-8 is DOS"),
    }

    Ok((lines_out, line_ending))
}

fn extract_whitespace(line: String) -> (String, u32, u32) {
    let mut cleaned_line: String = line.trim().to_owned();
    let mut leading_spaces = 0;
    let mut trailing_spaces = 0;

    if line.trim().is_empty() {
        leading_spaces += line.len() as u32;

        ("\n".to_owned(), leading_spaces, trailing_spaces)
    } else {
        let first_char = cleaned_line.chars().next().unwrap();
        let last_char = cleaned_line.chars().last().unwrap();

        for curr_char in line.chars() {
            if first_char != curr_char && curr_char.is_whitespace() {
                leading_spaces += 1;
            } else {
                break;
            }
        }

        for curr_char in line.chars().rev() {
            if last_char != curr_char && curr_char.is_whitespace() {
                trailing_spaces += 1;
            } else {
                break;
            }
        }

        cleaned_line.push('\n');

        (cleaned_line, leading_spaces, trailing_spaces)
    }
}

fn main() -> std::io::Result<()> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() > 1 {
        let filename = &args[1];
        let lines = file_to_vec(filename)?;

        let mut results: Vec<(String, u32,  u32)> = vec![];

        let start = Instant::now();

        for line in lines {
            results.push(extract_whitespace(line));
        }

        let mut trimmed_lines: Vec<String> = vec![];

        println!("\n[Tuple]");
        for result in results {
            println!("{:?}", result);
            trimmed_lines.push(result.0);
        }

        println!("\n[Trimmed File]:");
        for line in trimmed_lines {
            print!("{}", line);
        }
        println!("---");

        let elapsed = start.elapsed();

        println!("\nelapsed time: {:.2?}\n", elapsed);

        Ok(())
    } else {
        println!("Usage: {} <input>", args[0]);
        Err(std::io::Error::new(std::io::ErrorKind::Other, "Usage: <input>"))
    }
}
