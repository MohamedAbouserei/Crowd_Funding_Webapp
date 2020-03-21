from django.forms import ModelForm 
from django import forms 
from datetime import datetime
from Project.models import * 
class ProjectForm(ModelForm): 
    class Meta: 
        # write the name of models for which the form is made 
            model = Projects         
  
        # Custom fields 
            fields =["title", "totaltarget", "startdate", "enddate","details"] 
  
    # this function will be used for the validation 
    def clean(self): 
  
        # data from the form is fetched using super function 
        super(ProjectForm, self).clean() 
          
        # extract the username and text field from the data 
        title = self.cleaned_data.get('title') 
        totaltarget = self.cleaned_data.get('totaltarget')
        startdate = self.cleaned_data.get('startdate') 
        startdate=datetime.strptime(startdate, '%m-%d-%Y').date()
        enddate = self.cleaned_data.get('enddate')   
        enddate=datetime.strptime(enddate, '%m-%d-%Y').date()

  
        # conditions to be met for the username length 
        if  startdate < enddate: 
            self._errors['title'] = self.error_class([ 
                'date error']) 
        if  totaltarget < 1000: 
            self._errors['totaltarget'] = self.error_class([ 
                'Minimum is 1000 $']) 
        if len(title) <5: 
            self._errors['title'] = self.error_class([ 
                'Post Should Contain minimum 10 characters']) 
  
        # return any errors if found 
        return self.cleaned_data 