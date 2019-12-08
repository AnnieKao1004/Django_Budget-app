from django import forms
from . import models

class ProjectForm(forms.ModelForm):
  class Meta:
    model = models.Project
    fields = ['name', 'budget',]

  def __init__(self, *args, **kwargs):
    super(ProjectForm, self).__init__(*args, **kwargs)
    self.fields['name'].label = 'Project Name (enter with English and number)'
    self.fields['budget'].label = 'Budget'

class ExpenseForm(forms.ModelForm):
  class Meta:
    model = models.Expense  
    fields = ['project', 'title', 'amount', 'category']

  def __init__(self, *args, **kwargs):
    project = kwargs.pop('project','')
    slug = kwargs.pop('slug','')
    super(ExpenseForm, self).__init__(*args, **kwargs)
    
    self.fields['title'].label = 'Title'
    self.fields['amount'].label = 'Amount'
    self.fields['category'].label = 'Category'
    self.fields['category'] = forms.ModelChoiceField(queryset=models.Category.objects.filter(project=project))
    self.fields['project'] = forms.ModelChoiceField(queryset=models.Project.objects.filter(slug=slug), empty_label=None)  
