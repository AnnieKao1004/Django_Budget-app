from django.db import models
from django.utils.text import slugify

# Create your models here.
class Project(models.Model):
  name = models.CharField(max_length=100)
  slug = models.SlugField(max_length=100, unique=True, blank=True)
  budget = models.IntegerField()
  
  def save(self, *args, **kwargs):
    self.slug = slugify(self.name)
    super(Project, self).save(*args, **kwargs)

  def budget_left(self):
    expense_list = Expense.objects.filter(project=self)
    total_expense_amount = 0
    for expense in expense_list:
      total_expense_amount += expense.amount
    total_expense_amount = int(total_expense_amount)
    return self.budget - total_expense_amount

  def total_transactions(self):
    expense_list = Expense.objects.filter(project=self)
    return len(expense_list)
 
  def __str__(self):
    return self.name

class Category(models.Model):
  project = models.ForeignKey(Project, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  def __str__(self):
    return self.name

class Expense(models.Model):
  project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="expense")
  title = models.CharField(max_length=100)
  amount = models.IntegerField()
  category = models.ForeignKey(Category, on_delete=models.CASCADE)

  class Meta:
    ordering = ('-amount',)

  def __str__(self):
    return self.title