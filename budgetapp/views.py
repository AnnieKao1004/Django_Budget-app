from django.shortcuts import render, get_object_or_404
from .models import Project, Category, Expense
from .forms import ProjectForm, ExpenseForm
from django.views.generic import CreateView
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView


# Create your views here.
def project_list(request):
  project_list = Project.objects.all()
  return render(request,'project-list.html', locals())

def addProjectandCategory(request):
  if request.method == "POST":
    add_project_form = ProjectForm(request.POST) #create a form instance from POST data
    if add_project_form.is_valid() and request.POST['categoriesString'] != '':
      project = add_project_form.save() # this is an Project instance
      catArray = request.POST['categoriesString'].split(',')
      for category in catArray:
        Category.objects.create(project=project, name=category)
    url = '/{}'.format(project.slug)
    return HttpResponseRedirect(url)
  else:
    add_project_form = ProjectForm()
  return render(request, 'add-project.html', locals())

def project_detail(request, project_slug):
  #fetching the specific project
  project = get_object_or_404(Project, slug=project_slug) # get a project object
  expense_list = project.expense.all()
  
  if request.method == 'GET':
    form = ExpenseForm(project=project, slug=project_slug)
    return render(request,'project-detail.html', locals())
  elif request.method == 'POST':
    form = ExpenseForm(request.POST, project=project, slug=project_slug) # modelForm 裡面有foreign key的話,接收POST產生instance的時候,參數也要傳進去
    form.save()
      
  return HttpResponseRedirect('/{}'.format(project_slug))

def delete_expense(request, id):
  expense = get_object_or_404(Expense, id=id)
  project_slug = expense.project.slug
  expense.delete()
  return HttpResponseRedirect('/{}'.format(project_slug))

class ProjectDelete(DeleteView):
  model = Project
  success_url = reverse_lazy('list')