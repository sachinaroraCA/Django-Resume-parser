# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from django.views.decorators.csrf import csrf_exempt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import pyPdf
import pdftotext
import string
import re
from nltk.util import ngrams
from django.shortcuts import render_to_response, redirect
from pdf_parser.models import *
from django.core.files.storage import FileSystemStorage
from resume_parser.settings import MEDIA_ROOT
from django.utils.encoding import smart_str, smart_unicode


def index(request):
    return render(request,'home.html')

def getPdfContent(uploaded_file,upload_file_path):
    result = []
    content = ""
    # Load PDF into pyPDF
    pdf = pyPdf.PdfFileReader(uploaded_file)
    #print pdf.isEncrypted
    # Iterate pages
    for i in range(0, pdf.getNumPages()):
        #print pdf.getPage(i)
        # Extract text from page and add to content
        content += pdf.getPage(i).extractText() + "\n"
        #print i
        #print content
    # for linked in
    if content.strip() == '':
        with open(upload_file_path, "rb") as f:
            pdf_pdf2 = pdftotext.PDF(f)
            for page in pdf_pdf2:
                content = content + page + "\n"
    result.append(content.replace(u"\xa0", " "))
    result.append(" ".join(content.replace(u"\xa0", " ").strip().split()))
    return result



def dataparsing(request):
    try:
        if request.method == "POST":
            uploaded_file = request.FILES.get("pdf_file")
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            upload_file_path = MEDIA_ROOT + '/' +filename
            output_text_dict = getPdfContent(uploaded_file,upload_file_path)
            untrimmed_content = output_text_dict[0]
            content = output_text_dict[1]
            print untrimmed_content
            #print content
            resume_text = content.encode("ascii", "ignore")
            tokens = word_tokenize(resume_text)
            #print tokens
            punctuations = ['(',')',';',':','[',']',',']
            #print punctuations
            stop_words = stopwords.words('english')

            filtered = [w for w in tokens if not w in stop_words and  not w in string.punctuation]

            name  = str(filtered[3])+' ' +str(filtered[4])
            print "Name : " + name
            email = ""
            match_mail = re.search(r'[\w\.-]+@[\w\.-]+', resume_text)
            #handling the cases when mobile number is not given
            if(match_mail != None):
                email = match_mail.group(0)
                print "Email : " + email
            else:
                email = "No EMail ID In Resume" 

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
            name = ""
            try:
                if mobile:
                    name  = str(filtered[3])+ ' ' +str(filtered[4])
                    print "Name :" + name
                else:
                    name = str(filtered[1]) + ' ' + str(filtered[2])
                    print "Name : " + name
            except Exception as ex:
                print "Exception:" + repr(ex)
                
            #Date Of Birth
            date_of_birth = ""
            parsed_resume = ' '.join(filtered)
            # "Parsed Resume in plain Text : ", parsed_resume
            r = str(parsed_resume)    
            shingle = []
            make_shingle = ngrams(filtered,10)
            address = ""

            education = ""
            experience = ""
            h = re.compile('(([^\n]\s+(Experience)[\n]+).*)', re.DOTALL)
            match_exp = re.search(h, untrimmed_content)
            #re.compile(r"^(.+)(?:\n|\r\n?)((?:(?:\n|\r\n?).+)+)", re.MULTILINE)
            
            #print "match exp :", match_exp.groups()
            if(match_exp != None):
                experience = match_exp.group(0)
                experience = experience.split('Education')
                education = experience[1]
                experience= experience[0]
                experience = smart_str(experience)
                
                education = smart_str(education)
                experience = experience[47:]
                print "education::::::::+++++++++++++++++++",education
                #return HttpResponse(exp_data)
                #exp_data  = ' '.join([tup for tup in exp_data])
                #exp_data = exp_data[11:]
                print "experience ::::::::::: " ,  experience
            skills = ""
            h = re.compile('(([^\n]\s+(Summary)[\n]+).*)', re.DOTALL)
            skill_exp = re.search(h, untrimmed_content)
            skill_exp = skill_exp.group(0)
            skill_exp = skill_exp.split('Languages')
            skill_exp = skill_exp[0]
            print 'datatatatatatatta',skill_exp
            skill_exp = skill_exp.split('\n')
            output_skills = ""
            for skill in skill_exp:
                if skill.find('      ')!= -1:
                    print 'Success'
                else:
                    output_skills = output_skills + skill+" "
                    print 'expected_output=============',skill
            print output_skills
            now = datetime.datetime.now()
            data = ParseData.objects.create(added_on = now, name = name , email = email ,mobile = mobile, date_of_birth = date_of_birth,address = address,education = education,experience = experience,parsed_resume = r , shinghles = shingle)
            savein_salesforce(data={"name": name,
                                    "Email__c": email,
                                    "Phone__c": mobile,
                                    "Experience__c": experience,
                                    "Education__c": education})
            data.save()
            return redirect("/resumeinformation/")
            #return HttpResponse('Data Save Successfully')
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

def savein_salesforce(data):
    from .utils.sf_api import SFConnectAPI
    sf = SFConnectAPI()
    sf.create_record(object_name="Resume__c",
                     data=data)
