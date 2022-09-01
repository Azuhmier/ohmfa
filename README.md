!! This Read Me and the information in it is outdated and will be updaated soon!
# OHMFA  (WIP!!!!!!!!!)
Omni Hashing Masterbin File Application

## Description

OHMFA  copies a masterbin file to a generated directory called '{name}.ohmfi', where, based on user specifications, it is parsed and converted into a SQL database. From here the contents of the database can be queried, manipulated, and used to generated formed outputs. Several '{name}.ohmfi' directories can be grouped in a master directory called '{name}.ohmfa' to extend analysis and share configurations.

## Introduction
**What is a masterbin?**
A pseudo or strictly structured txt file of urls, such as a 'list' of online stories.

**What are its limitations?**
This application is not meant to replace the time and effort expended meticulously to maintain a masterbin, rather it aims to greatly improve it the process. It's better to incomplete or partially organized data than WRONG data. With this in mind one should not expect to be able to write up OHMFA parse configurations that will work 'as is' on any masterbin. OHMFA aims to give feedback and analysis tools in cases where this expectation is not met to help the user edit the masterbin file till it is suitable to parse.

**What is the use case? Practically?**
OHMFA is based on previous experience with working with and maintaining masterbins with over 1000+ urls with associated authors, story titles, and tags. These elements eventually needed to be parsed to ensure tag consistency, check for duplicates, get urls for scrapping, and generate formatted outputs for public ease of access to the contents of the masterbin. The program (proto-OHMFA), or rather series of scripts, created for this were robust but 'patchy'. The 'final straw' was the 'great pastebin purge'. Masterbins were forcefully deleted causing replacement masterbins to be created in a myriad of formats such as 'googledocs', 'mega', 'ghostbin', and 'rentry'. Their associated urls (especially for story urls) became highly decentralized in their site domains resulting in several url(s) to represent the same content on each of the new popular domains (Ex: 'hardbin', 'googledocs', 'ghostbin', 'rentry'). This 'chaos' also caused masterbins to have new maintainer(s), which was a real 'wake-up call' to the quite real possibility of a masterbin being abandoned by their maintainer(s). In conclusion, their was a real urgent need to create a program that not only assists in maintaining masterbins in such dynamic environments, but one that is not too eccentric that another individual can take control of a masterbin and it's supplementary files and formatted versions after another maintainer's leave. Since it is based off of traditional masterbin keeping (typing into a txt file), parsing is heavily used to transfer to a SQL database.

## Architecture (WIP)

### Precursor
The 'proto-OHMFA' program consisted of the masterbin, configuration files, and a directory where they were all kept. It was written in perl and the only command line interface was simply '% perl do_thing.pl' that would make a hash structure of the contents of the masterbin based on a file called 'dspt.json' that held all the regular expression patterns for each class of match (Ex: url, title) as well as to where to put their matches in generated hash structure. The parsing and said hash structure was validated by writing the masterbin file back with the hash structure with the use of another configuration file called 'drsr.json'. A 'txt diff' (the bash utility 'diff' was used) was done on the original and generated masterbin file, and no difference mean it was successful. Updates (changes) to the masterbin file were 'validated' by both a 'txt diff' and a 'hash diff' which was just a 'txt diff' between the sorted previous hash structure and the new generated one. With the prior process, the validation was determined by the user by looking at the 'diff' output and hitting 'y/n' on whether the program should commit the new masterbin and hash structure. For formatted versions of the masterbin a configuration file called 'mask.json' was used. It contained the verbatim cmdline statement (Ex: the one used to upload a txt file to rentry.org), locations of passwords, headers, and suppressions of certain types of data. With all these configuration files, another script/program called the 'Boiler Plate Generator' was created to validate configuration file and provide their default values. It was a dynamic in nature able to recursively validate and provide defaults for each 'match class' found in the context of their hierarchical placement in the generated hash structure. Analysis and editing tools of this 'proto OHMFA' program consisted of the generation of additional outputs called 'paged files'. These were files containing a list of matches and their line numbers in the masterbin and their was a file for each 'class' of match such as 'title', 'url', 'author', and 'tag'. It was utilize with Vim using a vimscript that would allow a user through a series of key mappings to quickly go to the match under the cursor in these paged files.

In conclusion the 'proto-ohmfa' was a series of scripts whose behavior were determined by a myriad of configuration files with a masterbin editing interface created and applied in Vim via a vimscript.

### Modular
##### _Input Parser & Handler_
Instead of editing configuration json file manually, it is done in an input or make file depending on the context.
##### _Boiler Plate Generator (BPG)_
Provide default and validation for the configuration files and any other framework that is meticulous meticulous as well as dynamic
##### _ohmfi/ohmfa Handler_
The '{name}.ohmfi' Keeps track of the masterbin file, configurations, and supplementary files. It's akin to how a .docx file is just a 'zipped' up directory, except in this case it won't be zipped. The '{name}.ohmfa' groups the '{name}.ohmfi' files together so one can share configuration files and other information.
##### _Lexer_
It tokenizes the masterbin file. It receives lexer arguments and the txt fragment to be lexed (given by the parser). And then it gives back the tokens.
##### _Parser_
Takes tokens by the lexer and creates a parse tree and/or hash structure
##### _IFL generator/validator_
Post processing of hash structure to get it ready to be turned into an sql database
##### _IFL to SQL_
Pretty much what the name says for now
##### _Writer_
Writes back masterbin file or creates formatted versions of it.
##### _History/file deltas_
Pretty much what the name says for now along with some automation/validation/interfacing. Something more robust than using 'diff' on an old and new file.

### MISC/OTHER
##### _OHMFA Main Controller_
...
##### _Command Line Interface_
...
##### _Additional Interface_
...
##### _Distribution/Installation_
...

## To Do
a lot

