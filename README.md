# Django_Budget-app
Ref: https://www.youtube.com/watch?v=W54DF_EMYaQ

### 記錄過程中學到的新東西:
### **1. super()的用法**
在models.py中定義新的Project class(繼承自models.Model)，class中定義method save()，此時使用了super(Project, self).save()這一行來實現父類別models.Model的save() method,不然父類別models.Model的save() method會被新定義的save() method覆蓋。見下面的例子:
```
class Animal(object):
    def __init__(self, name):
        self.name = name
    def greet(self):
        print 'Hello, I am %s.' % self.name

class Dog(Animal):
    def greet(self):
        super(Dog, self).greet()   # Python3 可使用 super().greet(), 在這裡Dog Class的greet() method會保留Aninmal class的greet() method的功能
        print 'WangWang...'
        
>>> dog = Dog('dog')
>>> dog.greet()
Hello, I am dog.
WangWang..        
```
super()最常用的例子是要繼承父類別的__init__(),如下面例子。此時Class A的__init__()也具有Class Base的__init__()裡面的功能
```
class Base(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

class A(Base):
    def __init__(self, a, b, c):
        super(A, self).__init__(a, b)  # Python3 可使用 super().__init__(a, b)
        self.c = c
```
### **2. 自動產生slug**  
```
from django.utils.text import slugify
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget = models.IntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)
```

### **3. get_object_or_404**  
get_object_or_404()是Django shortcut functions的其中一個function(render()也是其中一個function)。  
官方文件說明:  
get_object_or_404(klass, *args, **kwargs):  
Calls get() on a given model manager, but it raises Http404 instead of the model’s DoesNotExist exception.  
klass => A Model class, a Manager, or a QuerySet instance from which to get the object.  
**kwargs => Lookup parameters, which should be in the format accepted by get() and filter().
```
from django.shortcuts import get_object_or_404
project = get_object_or_404(Project, slug=project_slug)
```

### **4. Relationship in models**  
當models之間有建立關係時(e.g. ForeignKey的使用),django提供這些model的instance一些方便的API來取得取得相關的物件。  
```
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    ...

    def __str__(self):
        return self.headline
```
- Forward relationship
```
>>> e = Entry.objects.get(id=1)
>>> e.blog # Returns the Blog object related to e.
```
- Backward relationship
```
>>> b = Blog.objects.get(id=1)
>>> b.entry_set.all() # Returns all Entry objects related to b.
```
### **5. Class-based view (CBV)**
目前學的views都是function-based view, 這個yt教學是用CBV...  
[CBV reference](https://spapas.github.io/2018/03/19/comprehensive-django-cbv-guide/)  
*待研究...*

### **6. Materialize  -- another option rather than bootstrap**  
- Use Materialize to make modal(彈出視窗)


### **7. PUT and DELETE HTTP request with Django**
*待研究...*

### **8. call instance method in template**  
```
# models.py
class Task(models.Model):
    def foo(self):
        return "bar"
```
```
<-- template.html -->
{{ task.foo }}
```  
It is not possible to pass arguments to method calls accessed from within templates. Data should be calculated in views, then passed to templates for display.
