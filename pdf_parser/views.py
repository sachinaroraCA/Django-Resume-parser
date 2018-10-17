# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import pyPdf
import docx
import string
import re
from nltk.util import ngrams
from django.db.models import *
from pdf_parser.models import *
from django.shortcuts import render_to_response, redirect


def index(request):
    return render(request,'home.html')

def getPdfContent(uploaded_file):
    content = ""
    # Load PDF into pyPDF
    pdf = pyPdf.PdfFileReader(uploaded_file)
    # Iterate pages
    for i in range(0, pdf.getNumPages()):
        # Extract text from page and add to content
        content += pdf.getPage(i).extractText() + "\n"
        # Collapse whitespace
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content

def dataparsing(request):
    try:
        if request.method == "POST":
            uploaded_file = request.FILES.get("pdf_file")
            content = getPdfContent(uploaded_file)
            print content
            resume_text = content.encode("ascii", "ignore")
            print resume_text
            tokens = word_tokenize(resume_text)
            #print tokens
            punctuations = ['(',')',';',':','[',']',',']
            print punctuations
            stop_words = stopwords.words('english')
            print stop_words
            #storing the cleaned resume
            filtered = [w for w in tokens if not w in stop_words and  not w in string.punctuation]
            print "removing the stop words....\nCleaning the resumes....\nExtracting Text ......."
            print filtered
            #get the name from the resume
            name  = str(filtered[0])+' ' +str(filtered[1])
            print "Name : " + name
            email = ""
            match_mail = re.search(r'[\w\.-]+@[\w\.-]+', resume_text)
            #handling the cases when mobile number is not given
            if(match_mail != None):
                email = match_mail.group(0)
                print "Email : " + email

            #mobile number
            mobile = ""
            if mobile:
                match_mobile = re.search(r'((?:\(?\+91\)?)?\d{9})',resume_text)
                #handling the cases when mobile number is not given
                if(match_mobile != None):
                    mobile = match_mobile.group(0)
                    print "Mobile : " +  mobile
            else:
                match_mobile = re.search(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',resume_text)
                if(match_mobile != None):
                    mobile = match_mobile.group(0)
                    print "Mobile : " +  mobile
            #Date Of Birth
            date_of_birth = ""
            #if date_of_birth:
            dob = re.findall(r'(\d+/\d+/\d+)',resume_text,re.I)[0]
            print dob
            if(dob != None):
                date_of_birth = dob
                print "Date Of birth:" + date_of_birth
            #else:
            #    dob = re.findall(r'\d\d\w\w\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}', resume_text,re.I)[0]
            #    print dob
            #    if(dob != None):
            #        date_of_birth = dob
            #        print "Date Of Birth:" + date_of_birth
            #return HttpResponse(date_of_birth)
            parsed_resume = ' '.join(filtered)
            print "Parsed Resume in plain Text : ", parsed_resume
            r = str(parsed_resume)    
            print r
            shingle = []
            education_shingle = []
            make_edu = ngrams(filtered,23)
            # form n-grams - basically the singles for LSH
            for s in make_edu:
                education_shingle.append(s)
            print "Shingles for the education: ",education_shingle
            make_shingle = ngrams(filtered,10)
            #print the shingles
            for s in make_shingle:
                shingle.append(s)  

                              
            print "Shingles for the resume : ",shingle
            address = ""
            if(address != None):
                add = [item for item in shingle if item[0] == "Address"]
                add = add[0]
                address = ' '.join([tup for tup in add])
                address = address[8:]
                print "address:" + address
            #add the new entries to the table
            education = ""
            if(education != None ):
                edu = [item for item in education_shingle if item[0] == "Education"]
                edu = edu[0]
                education  = ' '.join([tup for tup in edu]) 
                education = education[11:]
                print "education :" + education
        
            experience = ""
            if(experience != None):
                list = []
                exp_1 = [item for item in shingle if item[0] == "Present"]
                exp_1 = exp_1[2]
                exp_1 = exp_1[2:]
                exp_2 = [item for item in shingle if item[0] == "Designation"]
                exp_2 = exp_2[0]
                list.append(exp_1 + exp_2)
                list = list[0]
                experience  = ' '.join([tup for tup in list])
                print "experience :" + experience

            now = datetime.datetime.now()
            data = ParseData.objects.create(added_on = now, name = name , email = email ,mobile = mobile, date_of_birth = date_of_birth,address = address,education = education,experience = experience,parsed_resume = r , shinghles = shingle)
            #r = parsed_resume(name = name,email = email, mobile = mobile, parsed_resume = r, shingles = shingle)
            #commit the changes
            data.save()
            return redirect("/resumeinformation/")
            
            
            
            return HttpResponse('Data Save Successfully')
        else:
            return HttpResponse('Missing Some Data Field')
    except Exception as ex:
        print "Exception:" + repr(ex)
    return HttpResponseRedirect('/dataparsing/')


def resumeinformation(request):
    resume_data = ParseData.objects.all()
    return render(request, "datatable.html", {'resume_data': resume_data})

def resume_data_delete(request):
    data = ParseData.objects.all()[0].delete()
    return redirect("/resumeinformation/")

