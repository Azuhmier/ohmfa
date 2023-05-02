# OHMFA  (WIP!!!!!!!!!)
Omni Hashing Masterbin File Application

## Description
Ohmfa takes a masterbin file, parses it, and converts it to sql. In this format the database can be manipulated and 'written' in traditional masterbin text format.

## Introduction
**What is a masterbin?**
A pseudo or strictly structured txt file of urls, such as a 'list' of online stories.

**What are its limitations?**
This application is not meant to replace the time and effort expended meticulously to maintain a masterbin, rather it aims to greatly improve it the process. It's better to incomplete or partially organized data than WRONG data. With this in mind one should not expect to be able to write up OHMFA parse configurations that will work 'as is' on any masterbin. OHMFA aims to give feedback and analysis tools in cases where this expectation is not met to help the user edit the masterbin file till it is suitable to parse.

**What is the use case? Practically?**
OHMFA is based on previous experience with working with and maintaining masterbins with over 1000+ urls with associated authors, story titles, and tags. These elements eventually needed to be parsed to ensure tag consistency, checked for duplicates, updated with urls for scrapping, and used to generate formatted outputs for public ease of access. The program (proto-OHMFA), a collection of perl scripts, was created for this. Even though it was robust, it was 'patchy' at best. The 'final straw' that lead to the development of a new program was the 'Great Pastebin Purge'. Masterbins were forcefully deleted causing replacement masterbins to be created in a myriad of formats such as 'googledocs', 'mega', 'ghostbin', and 'rentry'. Their associated urls (especially for story urls) became highly decentralized in their site domains resulting in several url(s) to represent the prior ones on each of the new popular domains (Ex: 'hardbin', 'googledocs', 'ghostbin', 'rentry'). This 'chaos' also caused masterbins to have new maintainer(s), which was a real 'wake-up call' to the quite real possibility of a masterbin becoming too overwhelming to maintain for their current maintainer(s). In conclusion, their was a real urgent need to create a program that not only assists in maintaining masterbins in such dynamic environments, but one that is not too eccentric that other individuals can't aid in the maintenance or take control of the masterbin(s) and it's supplementary files and formatted versions after dramatic changes in events or an ever increasingly complicated environment. Since it is based off of traditional masterbin keeping (typing into a txt file), parsing is heavily used to transfer the contents of a masterbin to an SQL database.

## To Do
a lot

