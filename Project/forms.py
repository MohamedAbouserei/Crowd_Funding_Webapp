from django.forms import ModelForm 
from django import forms 
from datetime import datetime
from Project.models import * 
import re
class ProjectForm(ModelForm): 
    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super().__init__(*args, **kwargs)
    class Meta: 
        # write the name of models for which the form is made 
            model = Projects         
  
        # Custom fields 
            fields =["cat","title", "totaltarget", "startdate", "enddate","tags","details"] 
    def __str__(self):
            return self.title
    # this function will be used for the validation 
    def clean(self): 
  
        # data from the form is fetched using super function 
        super(ProjectForm, self).clean() 
          
        # extract the username and text field from the data 
        pattern = re.compile("^\w+([\,-]?\w+)+$")
        title = self.cleaned_data.get('title') 
        totaltarget = self.cleaned_data.get('totaltarget')
        startdate = self.cleaned_data.get('startdate') 
        enddate = self.cleaned_data.get('enddate')
        tags = self.cleaned_data.get('tags')
        user_id = self.user_id


            
        

  
        # conditions to be met for the username length 
        if startdate is not None and enddate is not None:
            if  startdate > enddate: 
                self._errors['startdate'] = self.error_class([ 
                    'date error']) 
        if totaltarget is not None:
            if  totaltarget < 1000: 
                self._errors['totaltarget'] = self.error_class([ 
                    'Minimum is 1000 $']) 
        if title is not None:
            if len(title) <5: 
                self._errors['title'] = self.error_class([ 
                    'title Should Contain minimum 5 characters'])
        if tags is not None:
            if not pattern.match(tags):
                 self._errors['tags'] = self.error_class([ 
                    'tags Should Contain char,numbers seprated by ,'])
 
  
        # return any errors if found 
        return self.cleaned_data 

class ImageFileUploadForm(forms.ModelForm):
    class Meta:
        model = Project_pics
        fields = ('picture',) 
