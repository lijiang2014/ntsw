from django.db import models



    

# Create your models here.
class Issue(models.Model):
    system_account = models.CharField(max_length =30)
    conn_email = models.CharField(max_length =30)
    conn2_email = models.CharField(max_length =30)
    tags = models.CharField(max_length =200,blank=True)
    public = models.BooleanField( default=True )
    title = models.CharField(max_length =60)
    description_public = models.TextField( blank=True )    
    description = models.TextField( blank=True )
    issue_time = models.DateTimeField()
    issue_submit_time = models.DateTimeField(  )
    #job = models.ForeignKey( JobIssue , on_delete=models.CASCADE  , blank=True , null=True )
    #jobs = models.ManyToManyField( JobIssue , verbose_name="list of issue jobs" )
    def __str__(self):
        return self.title

class JobIssue(models.Model):
    jobid = models.IntegerField()
    software = models.CharField(max_length =30,blank=True )
    submit_ln = models.CharField(max_length =30,blank=True )
    workdir = models.CharField(max_length =30,blank=True )
    nodelist = models.CharField(max_length =30,blank=True )
    submit_env = models.CharField(max_length =200,blank=True )
    submit_cmd = models.CharField(max_length =200,blank=True )
    submit_time = models.CharField(max_length =200,blank=True )
    error_time = models.DateTimeField(blank=True ,null=True)
    issue = models.ForeignKey( Issue , on_delete=models.CASCADE  , blank=True , null=True )
    
    
class Response(models.Model):
    name = models.CharField(max_length =30)
    submit_time = models.DateTimeField()
    description_public = models.TextField()
    description = models.TextField()
    
    
