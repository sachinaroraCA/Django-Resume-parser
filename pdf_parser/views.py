# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from django.shortcuts import render
from django.http import HttpResponse
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
    if request.method == "POST":
        uploaded_file = request.FILES.get("pdf_file")
        content = getPdfContent(uploaded_file)
        resume_text = content.encode("ascii", "ignore")
        tokens = word_tokenize(resume_text)
        punctuations = ['(',')',';',':','[',']',',']
        stop_words = stopwords.words('english')
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
        match_mobile = re.search(r'((?:\(?\+91\)?)?\d{9})',resume_text)
        #handling the cases when mobile number is not given
        if(match_mobile != None):
            mobile = match_mobile.group(0)
            print "Mobile : " +  mobile

        parsed_resume = ' '.join(filtered)
        print "Parsed Resume in plain Text : ", parsed_resume
        r = str(parsed_resume)    
        print r
        shingle = []
        # form n-grams - basically the singles for LSH
        make_shingle = ngrams(filtered,10)
        #print the shingles
        for s in make_shingle:
            shingle.append(s)  

                          
        print "Shingles for the resume : ",shingle
        
        #add the new entries to the table
        now = datetime.datetime.now()
        data = ParseData.objects.create(added_on = now, name = name , email = email ,mobile = mobile, parsed_resume = r , shinghles = shingle)
        #r = parsed_resume(name = name,email = email, mobile = mobile, parsed_resume = r, shingles = shingle)
        #commit the changes
        data.save()
        return redirect("/resumeinformation/")
        
        
        
        return HttpResponse('Data Save Successfully')
    else:
        return HttpResponse('Please Upload A File')


def resumeinformation(request):
    resume_data = ParseData.objects.all()
    return render(request, "datatable.html", {'resume_data': resume_data})

def resume_data_delete(request):
    data = ParseData.objects.all()[0].delete()
    return redirect("/resumeinformation/")

