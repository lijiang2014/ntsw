from django.shortcuts import render
from django.http import HttpResponse , FileResponse , StreamingHttpResponse ,HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from .models import Issue , JobIssue
from django.core import serializers
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import hashlib
from django.conf import settings

email_conn_class = settings.ISSUE_CONF['email_conn_class']


class IssueForm(ModelForm):
    title = forms.CharField( label = '问题标题 Issue title' ,help_text='glyphicon glyphicon-pencil' , widget=forms.TextInput( attrs={'class' :'form-control' , 'placeholder' : '问题标题' } )  )
    system_account = forms.CharField( label = '系统账号 System Account' ,help_text='glyphicon glyphicon-user' , widget=forms.TextInput( attrs={'class' :'form-control' , 'placeholder' : '系统账号' } ) )
    conn_email = forms.EmailField( label = '联系邮件 E-Mail' ,help_text='glyphicon glyphicon-envelope' , widget=forms.EmailInput( attrs={'class' :'form-control' , 'placeholder' : 'E-Mail Address' } ) ) 
    #issue_time = forms.DateTimeField(  label = 'Issue time' ,help_text='glyphicon glyphicon-time' , widget=forms.DateTimeInput( format="%Y-%m-%dT%H:%M", attrs={'class' :'form-control' , 'placeholder' : 'E-Mail Address' , 'type' : 'datetime-local' } )   ) #forms.DateTimeField( required=True , input_formats="%Y-%m-%dT%H:%M" )
    issue_time = forms.CharField(  label = '问题发生时间 Issue time' ,help_text='glyphicon glyphicon-time' , widget=forms.DateTimeInput( format="%Y-%m-%dT%H:%M", attrs={'class' :'form-control' , 'placeholder' : '问题发生的时间' , 'type' : 'datetime-local' } )   ) #forms.DateTimeField( required=True , input_formats="%Y-%m-%dT%H:%M" )
    conn2_email = forms.TypedChoiceField( label='问题分类 Issue Class'  ,  empty_value="..." ,choices=email_conn_class ,  help_text='glyphicon glyphicon-list',widget=forms.Select( 
        attrs={
            'class' :'form-control'
        }
    ))
    public = forms.ChoiceField(label='是否公开此问题 Do you want to public this issue ?'  , choices=(
        ( True , "True" ) ,
        ( False, "False") ,
    ) , help_text='none' , widget=forms.RadioSelect(     ) )
    description_public = forms.CharField( required=False  ,  label='可公开问题信息 Public Description' , widget=forms.Textarea( attrs={'class' :'form-control' , 'placeholder' : '可公开的问题描述' } )  )
    description = forms.CharField( required=False ,  label='私密问题信息 Private Description' , widget=forms.Textarea( attrs={'class' :'form-control' , 'placeholder' : '其他问题描述' } )  )
    isjob = forms.ChoiceField(label='是否是作业问题 Is this a job issue ?'  , choices=(
        ( True , "True" ) ,
        ( False, "False") ,
    ) , help_text='none' , widget=forms.RadioSelect(     ) )
 
    class Meta :
        model = Issue
        fields = [       'title' , 'system_account' ,  'conn_email',
                    'conn2_email' , # 'tags' ,
                     'public' , 'description_public' ,
                     'description' ,
                   'issue_time' ,
 ]

class JobIssueForm(ModelForm) :
    jobid = forms.CharField( required=False ,label = '作业id Job ID' ,help_text='glyphicon glyphicon-pencil' , widget=forms.TextInput( attrs={'class' :'form-control' , 'placeholder' : '作业ID号(*)' } )  )
    software = forms.CharField( required=False , label = '所用软件 software' ,help_text='glyphicon glyphicon-pencil' , widget=forms.TextInput( attrs={'class' :'form-control' , 'placeholder' : '使用的软件' } )  )
    submit_ln = forms.CharField(required=False , label = '提交节点 submit node' ,help_text='glyphicon glyphicon-pencil' , widget=forms.TextInput( attrs={'class' :'form-control' , 'placeholder' : '提交作业的节点' } )  )
    workdir = forms.CharField(required=False , label = '工作路径 work dir' ,help_text='glyphicon glyphicon-pencil' , widget=forms.TextInput( attrs={'class' :'form-control' , 'placeholder' : '工作路径' } )  )
    submit_env = forms.CharField( required=False ,label = '作业运行环境 Job Env' ,help_text='glyphicon glyphicon-pencil' , widget=forms.TextInput( attrs={'class' :'form-control' , 'placeholder' : '作业环境设置' } )  )
    submit_cmd = forms.CharField( required=False ,label = '作业命令 Job CMD' ,help_text='glyphicon glyphicon-pencil' , widget=forms.TextInput( attrs={'class' :'form-control' , 'placeholder' : '作业提交命令' } )  )
    class Meta :
        model = JobIssue
        fields = [   'jobid' ,  'software' ,
    'submit_ln' , 'workdir',   # 'nodelist',
     'submit_env', 'submit_cmd', # 'submit_time',
   # 'error_time'  , 
   ] 

    


# Create your views here.


email_host = settings.ISSUE_CONF['email_host']
email_user = settings.ISSUE_CONF['email_user']
email_pass = settings.ISSUE_CONF['email_pass']
#email_ = ''

def email_send( title , recivers , content  ) :
    try :
        title = "[AutoMail][NewIssue]" + title 
        msg = MIMEText(content)
        msg['Subject'] = title
        msg['From'] = email_user
        msg['To'] = ','.join(recivers)
        smtp = smtplib.SMTP( email_host )
        smtp.login( email_user , email_pass  )
        smtp.sendmail(email_user , recivers , msg.as_string() )
        smtp.close()
    except Exception as e :
        print("email_send error:" , e )


def index(request) :
    return HttpResponse("hello!")

def new(request):
    #return HttpResponse("hello! try to create new issue. ")
    message_error = ""
    if request.method == 'POST' :
        form = IssueForm(request.POST ,prefix = 'issue' )
        jform = JobIssueForm( request.POST , prefix = 'jobissue' )
        #print(request.POST)
        #print(form)
        if form.is_valid():
            print("form is valid")
            job = None
            err = False
            #print(form.cleaned_data["isjob"] , type( form.cleaned_data["isjob"] ))
            if form.cleaned_data["isjob"] == "True" :
                if jform.is_valid():
                    print("job is valid")
                    job = jform.save( commit =False )
                    print(  serializers.serialize( "json" , [job] ) )
                    if not job.jobid:
                        message_error="need jobid!"
                        err = True 
                else:
                    err = True
            if not err :
                newissue = form.save( commit=False )
                print("time" ,newissue.issue_time  )
                #try :
                #    newissue.issue_time = datetime.strptime( form.cleaned_data["issue_time"] ,      "%Y-%m-%dT%H:%M" )
                #except Exception as e :
                #    pass
                newissue.issue_submit_time = datetime.now()
                newissue.save()
                jsonstring = ""
                if job :
                    job.issue = newissue 
                    job.save()
                    #print(  serializers.serialize( "json" , [job] ) )
                    jsonstring += serializers.serialize( "json" , [job] )
                #print(  serializers.serialize( "json" , [newissue] ) )
                jsonstring += serializers.serialize( "json" , [newissue] )
                print( "Sucess return " )
                issue_token = issue_gentoken( newissue.pk  )
                # try to send email 
                issue_url = reverse( 'getissue' , args=( newissue.pk ,) ) + '?token=' + issue_token 
                content = "new issue  %d \n url : %s \n json: %s" % ( newissue.pk , issue_url ,jsonstring )
                email_send( newissue.title , [ newissue.conn_email , newissue.conn2_email  ] , content  )
                return HttpResponseRedirect( reverse( 'getissue' , args=( newissue.pk ,) ) + '?token=' + issue_token   )
        else :
            pass
        #if jform.is_valid():
        #    print("jform is valid")
    else :
        form = IssueForm( prefix = 'issue'  )
        jform = JobIssueForm( prefix = 'jobissue' )
    print( form.is_bound )
    #form['title'].classx = 'aaa'
    #print( form['title'].css_classes())
    return render(request , 'issues/new.html' , {'form':form , 'jform' : jform , 'message_error' : message_error }  )

def issue_gentoken(issue_id) :
    issue = Issue .objects.get(pk= issue_id)
    issue_json =  serializers.serialize( "json" , [issue] ) 
    m2 = hashlib.md5()
    m2.update( (issue_json ).encode('utf-8'))
    issue_md5 = m2.hexdigest()
    return issue_md5[:5]

def result(request , issue_id ):
    issue = Issue .objects.filter(pk= issue_id)
    job = JobIssue.objects.filter( issue=issue_id )
    if len( issue ):
        issue = issue[0]
    else :
        issue = None 
    if len( job ):
        job = job[0]
    else :
        job = None

    token = request.GET.get('token','')
    token_pass = False
    user_pass = False 
    if token and issue :
        issue_token = issue_gentoken( issue_id )
        print(issue_token)
        if token == issue_token :
            print("token pass")
            token_pass = True
    if  request.user.is_authenticated() :
        if ( request.user.is_staff ) :
            user_pass = True 
    private_right = user_pass or token_pass

    if issue.public or private_right :
        return render(request , 'issues/issue.html' , {'issue':issue , 'job':job , 'private_right' : private_right }  )
    else :
        return HttpResponse("Resource is not available for you! you need to login or have the token for this issue")