# -*- coding: utf-8 -*-

# Relation Extraction Skeleton
# ==========================================
#
# Author: Jianbin Qin <jqin@cse.unsw.edu.au>

from relation import Relation
import re

def extract_date_of_birth(sentence):
    data = sentence['annotation']
    predicate = "DateOfBirth"
    results = []
    string = ""
    rel = Relation("","","")
    for items in data:
        word = items[1]
        type = items[4]
        new = word + "(" + type + ") " 
        string += new
        
    quoteObj = re.search("(\"\(I-PERSON\)) (\w*)\(I-PERSON\) (\"\(I-PERSON\))", string)
    if quoteObj is not None:
        quote1 = str(quoteObj.group(1))
        quote1 = re.sub('\(I-PERSON\)', '', quote1)
        name = str(quoteObj.group(2))
        quote2 = str(quoteObj.group(3))
        quote2 = re.sub('\(I-PERSON\)', '', quote2)
        enclosedName = quote1 + name + quote2 + "(I-PERSON)"
        string = re.sub("(\"\(I-PERSON\)) (\w*)\(I-PERSON\) (\"\(I-PERSON\))", enclosedName, string)
    
    fullDateObj = re.search(r'(\w*\.*\(B-PERSON\)) (\"*\w*\.*\"*\(I-PERSON\))? ?(\"*\w*\.*\"*\(I-PERSON\))? ?(\"*\w*\.*\"*\(I-PERSON\))?.*born.*?(\w*\(B-DATE\)) ?(.*\(I-DATE\))?', string)
    if fullDateObj is not None:
        firstName = str(fullDateObj.group(1))
        secondName = str(fullDateObj.group(2))
        thirdName = str(fullDateObj.group(3))
        fourthName = str(fullDateObj.group(4))
        
        month = str(fullDateObj.group(5))
        day_Year = str(fullDateObj.group(6))
                 
        firstName = re.sub(r'\(B-PERSON\)', '', firstName)
        secondName = re.sub(r'\(I-PERSON\)', '', secondName)
        thirdName = re.sub(r'\(I-PERSON\)', '', thirdName)
        fourthName = re.sub(r'\(I-PERSON\)', '', fourthName)
        fullName = firstName + " " + secondName + " " + thirdName + " " + fourthName
        fullName = fullName.replace(" None", "")

        month = re.sub(r'\(B-DATE\)| ','', month)
        day_Year = re.sub(r'\(I-DATE\)','', day_Year)
        day_Year = re.sub(r' , ',', ', day_Year)
        day_Year = day_Year[0:20]
        day_YearObj = re.search(r'^(.*?[0-9]{4}).*', day_Year)
        if day_YearObj is not None:
            day_Year = str(day_YearObj.group(1))
        monthObj = re.search(r'(^[0-9]{4}).*', month)
        if monthObj is not None:
            day_Year = "None"
        DOB = month + " " + day_Year
        DOB = DOB.replace(" None", "")

        rel = Relation(fullName, predicate, DOB)
        results.append(rel)
    return results

def extract_has_parent(sentence):
    predicate = "HasParent"
    results = []
    data = sentence['annotation']
    string = ""
    for items in data:
        word = items[1]
        type = items[4]
        new = word + "(" + type + ") " 
        string += new
    
    quoteObj = re.search("(\"\(I-PERSON\)) (\w*)\(I-PERSON\) (\"\(I-PERSON\))", string)
    if quoteObj is not None:
        quote1 = str(quoteObj.group(1))
        quote1 = re.sub('\(I-PERSON\)', '', quote1)
        name = str(quoteObj.group(2))
        quote2 = str(quoteObj.group(3))
        quote2 = re.sub('\(I-PERSON\)', '', quote2)
        enclosedName = quote1 + name + quote2 + "(I-PERSON)"
        string = re.sub("(\"\(I-PERSON\)) (\w*)\(I-PERSON\) (\"\(I-PERSON\))", enclosedName, string)
        
    fullParentObj = re.search(r'(\"*\w*\.*\"*\(B-PERSON\)) (\"*\w*\.*\"*\(I-PERSON\))?' + 
                              ' ?(\"*\w*\.*\"*,*\(I-PERSON\))? ?(\"*\w*\.*\"*,*\(I-PERSON\))? ?(\"*\w*\.*\"*,*\(I-PERSON\))?' +
                              '.*born.*?[to|of].*?( \"*\w*\"*\(B-PERSON\)) ?(\"*\w*\.*\"*,*\(I-PERSON\))?' +
                              ' ?(\"*\w*\.*\"*,*\(I-PERSON\))? ?(\"*\w*\.*\"*,*\(I-PERSON\))? ?(\"*\w*\.*\"*,*\(I-PERSON\))?', string)

    if fullParentObj is not None:
        firstName = str(fullParentObj.group(1))
        secondName = str(fullParentObj.group(2))
        thirdName = str(fullParentObj.group(3))
        fourthName = str(fullParentObj.group(4))
        fifthName = str(fullParentObj.group(5))
        
        p1firstName = str(fullParentObj.group(6))
        p1secondName = str(fullParentObj.group(7))
        p1thirdName = str(fullParentObj.group(8))
        p1fourthName = str(fullParentObj.group(9))
        p1fifthName = str(fullParentObj.group(10))
        
        parent1FullName = (p1firstName + " " + p1secondName + " " + 
                           p1thirdName + " " + p1fourthName + " " + 
                           p1fifthName)

        subjectFullName = (firstName + " " + secondName + " " + 
                           thirdName + " " + fourthName + " " + fifthName)
        
        subjectFullName = re.sub(r'\(B-PERSON\)', '', subjectFullName)
        subjectFullName = re.sub(r'\(I-PERSON\)', '', subjectFullName)
        subjectFullName = re.sub(r' None', '', subjectFullName)
        subjectFullName = re.sub(r' ,', ',', subjectFullName)
        
        parent1FullName = re.sub(r'\(B-PERSON\)', '', parent1FullName)
        parent1FullName = re.sub(r'\(I-PERSON\)', '', parent1FullName)
        parent1FullName = re.sub(r' None', '', parent1FullName)
        parent1FullName = re.sub(r' ,', ',', parent1FullName)
        parent1FullName = re.sub(r'Sr$', 'Sr.', parent1FullName)
        parent1FullName = re.sub(r'Sr .', 'Sr.', parent1FullName)
        parent1FullName = parent1FullName.lstrip()
        
        rel1 = Relation(subjectFullName, predicate,  parent1FullName)
        results.append(rel1)
        
        secondParentObj = re.search(r'and\(O\) (\"*\w*\.*\"*\(B-PERSON\)) (\"*\w*\.*\"*\(I-PERSON\))?' + 
                                    ' ?(\"*\w*\.*\"*,*\(I-PERSON\))? ?(\"*\w*\.*\"*,*\(I-PERSON\))? ' +
                                    '?(\"*\w*\.*\"*,*\(I-PERSON\))?', string)
        if secondParentObj is not None:
            p2firstName = str(secondParentObj.group(1))
            p2secondName = str(secondParentObj.group(2))
            p2thirdName = str(secondParentObj.group(3))
            p2fourthName = str(secondParentObj.group(4))
            p2fifthName = str(secondParentObj.group(5))
            
            p2FullName = (p2firstName + " " + p2secondName + " " +
                         p2thirdName + " " + p2fourthName + " " +
                         p2fifthName)                
            p2FullName = re.sub(r'\(B-PERSON\)', '', p2FullName)
            p2FullName = re.sub(r'\(I-PERSON\)', '', p2FullName)
            p2FullName = re.sub(r' None', '', p2FullName)
            p2FullName = re.sub(r' ,', ',', p2FullName)
            p2FullName = p2FullName.lstrip()
            p2FullName = re.sub(r'Sr', 'Sr.', p2FullName)
            p2FullName = re.sub(r'Sr .', 'Sr.', p2FullName)
            p2FullName = re.sub(r'Sr. .', 'Sr.', p2FullName)
            rel2 = Relation(subjectFullName, predicate,  p2FullName)
            results.append(rel2)
  
    return results
