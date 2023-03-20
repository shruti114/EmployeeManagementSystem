import streamlit as st
import datetime
import pandas as pd
import mysql.connector
st.markdown("<html><h1><center>EMPLOYEE MANAGEMENT SYSTEM</center></h1></html>",unsafe_allow_html=True)
st.write("This is a data management application developed by Shruti as a prt of learning")
choice=st.sidebar.selectbox("My Menu",("HOME","LOGIN"))
if choice=="HOME":
    st.markdown("<center><h1>WELCOME</h1></center>",unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/New_office.jpg/640px-New_office.jpg")
    st.video("https://www.youtube.com/watch?v=yqqphr4S-i0&t=64s")
elif choice=="LOGIN":
    if 'login' not in st.session_state:
        st.session_state['login']=False
    uid=st.text_input("Enter employee id")
    pwd=st.text_input("Enter password")
    btn=st.button("Login")
    if btn:
        mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="ems")
        c=mydb.cursor()
        c.execute("select * from login")
        for row in c:
            if uid==row[0] and pwd==row[1]:
                st.session_state['login']=True
                break
        if(st.session_state['login']==False):
           st.header("Incorrect ID or password")
    if st.session_state['login']:
        st.header("Login Successful")
        select=st.selectbox("My Menu",("Employee","Leave","Manager","Project"))
        if select=="Leave":
            mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="ems")
            c=mydb.cursor()
            lid=0
            c.execute("select lid from leave_planner order by lid desc limit 1")
            for data in c:
                lid=int(data[0])
                break
            lid+=1
            ename=st.text_input("Enter employee name")
            startdate=st.date_input("From when you are starting your leave date?",datetime.date(2023,1,1))
            enddate=st.date_input("When are you retirning?",datetime.date(2023,1,1))
            if startdate > enddate:
                st.header("Invalid date")
            leavetype=st.selectbox("Type",("SickLeave","Vacation"))
            no_of_days=st.text_input("Enter no odf days of leave")
            btn=st.button("Update Leave")
            if btn:
                c.execute("insert into leave_planner values(%s,%s,%s,%s,%s,%s)",(lid,ename,startdate,enddate,leavetype,no_of_days))
                mydb.commit()
                st.header("Leave Updated Successfully.")
        elif select=="Project":
            choice=st.selectbox("Project",("Add","Delete","Update","View Project"))
            if choice=="View Project":
                mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="ems")
                c=mydb.cursor()
                c.execute("select * from project")
                l=[]
                for r in c:
                    l.append(r)
                df=pd.DataFrame(data=l,columns=["Pid","Pname","startdate","Expenditure"])
                st.dataframe(df)
            elif choice=="Add":
                if 'add' not in st.session_state:
                    st.session_state['add']=False
                mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="ems")
                c=mydb.cursor()
                pid=0
                c.execute("select pid from project order by pid desc limit 1")
                for data in c:
                    pid=int(data[0])
                pid+=1
                pname=st.text_input("Enter project name")
                c.execute("select pname from project")
                for p in c:
                    if p[0]==pname:
                        st.header("This Project is already there in the database, continue only if ou want to add it.")
                startdate=st.date_input("Enter the commencement date of the project",datetime.date(2023,1,1))
                expense=st.text_input("Enter expenditure")
                btn1=st.button("Add")
                if btn1:
                    c.execute("insert into project values(%s,%s,%s,%s)",(pid,pname,startdate,expense))
                    mydb.commit()
                    st.header("Data Added Successfully.")         
            elif choice=="Delete":
                mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="ems")
                c=mydb.cursor()
                pname=st.text_input("Enter project name")
                c.execute("select pid from project where pname=%s",(pname,))
                pid=0
                for data in c:
                    pid=data[0]
                    break
                c.execute("select ename,eid from employee where pid=(%s)",(pid,))
                l=[]
                flag=0
                for data in c:
                    eid=data[1]
                    ename=data[0]
                    l.append(data[1])
                    st.subheader(ename)
                    flag=1
                if flag:
                    st.subheader("is/are working on this project.")
                delete=st.button("Delete")
                if delete:
                    if flag==1:
                        for data in l:
                            c.execute("update employee set pid=%s where eid=%s",('None',data))
                            mydb.commit()
                    c.execute("delete from project where pid=(%s)",(pid,))
                    mydb.commit()
                    st.header("Data deleted successfully")
            elif choice=="Update":
                mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="ems")
                c=mydb.cursor()
                pname=st.text_input("Enter project name")
                c.execute("select pid from project where pname=%s",(pname,))
                pid=0
                for data in c:
                    pid=data[0]
                    break
                expenditure=st.text_input("Enter expenditure to update")
                update=st.button("Update")
                if update:
                    c.execute("update project set expenditure=(%s) where pid=(%s)",(expenditure,pid))
                    mydb.commit()
                    st.header("Data updated successfully")
        elif select=="Manager":
            choice=st.selectbox("Manager",("Add","Delete","View Managers"))
            if choice=="View Managers":
                mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="ems")
                c=mydb.cursor()
                c.execute("select * from manager")
                l=[]
                for r in c:
                    l.append(r)
                df=pd.DataFrame(data=l,columns=["ManagerID","ManagerName"])
                st.dataframe(df)
            elif choice=="Add":
                mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="ems")
                c=mydb.cursor()
                mid=0
                c.execute("select mid from manager order by mid desc limit 1")
                for data in c:
                    mid=int(data[0])
                mid+=1
                mname=st.text_input("Enter Manager name")
                btn2=st.button("Add")
                if btn2:
                    c.execute("insert into manager values(%s,%s)",(mid,mname))
                    mydb.commit()
                    st.header("Data Added Successfully.")
            elif choice=="Delete":
                mid=st.text_input("Enter manager id")
                delete=st.button("Delete")
                if delete:
                    mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="ems")
                    c=mydb.cursor()
                    c.execute("delete from manager where mid=(%s)",(mid,))
                    mydb.commit()
                    st.header("Data deleted successfully")
        elif select=="Employee":
            s=st.selectbox("My Menu",("ADD","DELETE","Employee Details"))
            if s=="Employee Details":
                mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="ems")
                c=mydb.cursor()
                c.execute("select distinct e.eid,e.ename,d.address from employee e,employee_detail d where e.eid=d.eid")
                l=[]
                for r in c:
                    l.append(r)
                df=pd.DataFrame(data=l,columns=["Id","Name","Address"])
                st.dataframe(df)
            elif s=='ADD':
                mid=0
                pid=[]
                ename=st.text_input("Enter employee name")
                mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="ems")
                c=mydb.cursor()
                c.execute("select pname from project")
                l=[]
                for data in c:
                        l.append(data[0])
                pname=st.multiselect("Projects",tuple(l))
                c.execute("select * from project")
                projects=[]
                i=0
                for data in c:
                    projects.append(data)
                df=pd.DataFrame(data=projects,columns=["pid","pname","startdate","expenditure"])
                pnames=df["pname"]
                pids=df["pid"]
                i=0
                for data in pnames:
                    if data in pname:
                        pid.append(pids[i])
                        break
                    i+=1
                oname=st.selectbox("Organzation",("None","Onleitechnologies"))
                oid="1"
                salary=st.text_input("Enter salary")
                c.execute("select mname from manager")
                l=[]
                for data in c:
                    for char in data:
                        if char=="," or char=="'":
                            continue
                        l.append(char)
                mname=st.selectbox("Manager",tuple(l))
                c.execute("select * from manager")
                l=[]
                for row in c:
                    l.append(row)
                df=pd.DataFrame(data=l,columns=["mid","mname"])
                mnames=df["mname"]
                mids=df["mid"]
                i=0
                for data in mnames:
                    if mname==data:
                        mid=mids[i]
                        break
                    i+=1
                joining_date=st.date_input("When did you joined the oraganization?",datetime.date(2023,1,1))
                is_working=st.radio("Are you working today? enter Yes or No",("Yes","No"))
                if is_working.upper()=="YES":
                    is_working=1
                else:
                    is_working=2
                address=st.text_input("Enter Address")
                btn=st.button("Add")
                eid=did=0
                c.execute("select eid from employee order by eid desc limit 1")
                for data in c:
                    eid=int(data[0])
                c.execute("select did from employee_detail order by did desc limit 1")
                for data in c:
                    did=int(data[0])
                did=did+1
                if btn:
                    i=0
                    for data in pname:
                        eid=eid+1
                        pid=pids[i]
                        c.execute("insert into employee values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(eid,ename,pid,mid,oid,'2099-12-31',joining_date,salary,is_working))
                        mydb.commit()
                        i=i+1
                    c.execute("insert into employee_detail values(%s,%s,%s,%s)",(did,eid,ename,address))
                    mydb.commit()
                    st.header("Data Added Successfully.")
            if s=='DELETE':
                mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="ems")
                c=mydb.cursor()
                ename=st.text_input("Enter employee name to be deleted")
                pname=st.text_input("Enter corresponding project")
                c.execute("select pid from project where pname=%s",(pname,))
                pid=eid=did=0
                for data in c:
                    pid=data[0]
                    break
                c.execute("select eid from employee where pid=%s and ename=%s",(pid,ename)) 
                delete=st.button("Delete")
                for data in c:
                    did=eid=data[0]
                if delete:
                    c.execute("delete from employee where eid=(%s)",(eid,))
                    mydb.commit()
                    c.execute("delete from employee_detail where did=(%s)",(eid,))
                    mydb.commit()
                    btnn=st.button("DeleteDetail")
                    if btnn:
                        c.execute("delete from employee_detail where did=(%s)",(did,))
                        mydb.commit()
                    st.header("Data deleted successfully")