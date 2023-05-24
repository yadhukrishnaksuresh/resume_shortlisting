from msilib.schema import MIME
import cv2
import pytesseract
import os
import re
import pandas as pd
import streamlit as st
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
st.title("CV SHORTLISTING")
file_path=st.text_input("Enter the folder name")
skill=st.text_input("Enter the skills").split()
if st.button("RUN"):
    # file_path="resumes"
    resume_file_path =os.listdir(file_path)
    resume_file_path=[os.path.join(file_path,i) for i in resume_file_path]
# print(resume_file_path)
    selected=[]
    rejected=[]
    def check_resume(resume_path,job):
        job_match=[]
        resume_img=cv2.imread(resume_path)
        gray=cv2.cvtColor(resume_img,cv2.COLOR_BGR2GRAY)
        resume=pytesseract.image_to_string(gray)
        res=re.sub("[^a-zA-Z]"," ",resume).lower()
        for i in job:
            if ''.join(i.lower().split()) in res:
                job_match.append(i)
            else:
                pass
        percentage_match=(len(job_match)/len(job))*100
        if percentage_match>=50:
            selected.append(resume_path)
        else:
            rejected.append(resume_path)
    # job=['python','c','mysql']
    job=skill
    for i in resume_file_path:
        check_resume(i,job)
# print(selected)
    email=[]
    phone_no=[]
    def email_phone(selected,mail,phone):
        img=cv2.imread(selected)
        grey=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        data=pytesseract.image_to_data(grey,output_type=pytesseract.Output.DICT)
        n=len(data['text'])
        for i in range(n):
            if data['conf'][i]>70:
                if re.search(mail,data['text'][i]):
                    email.append(data['text'][i])
                    break
                if re.search(phone,data['text'][i]):
                    phone_no.append(data['text'][i])
    for i in selected:
        mail=r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+'
        phone=r"(0|91)?[6-9][0-9]{9}"
        email_phone(i,mail,phone)
    print(email)
    print(phone_no)
    selected_resumes=[]
    for i in selected:
        selected_resumes.append(os.path.basename(i))
    names=[]
    for i in selected_resumes:
        names.append(os.path.splitext(i)[0])
    interview_list=pd.DataFrame({'Applicant Name':names,'Email Address':email,"phone number":phone_no})
    st.write("Selected candidates")
    st.write(interview_list)
    st.download_button(label="Download CSV",data=interview_list.to_csv(),mime='text/csv')