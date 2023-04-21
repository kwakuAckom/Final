import json
from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ExpenseForm, CreateProjectForm
from .models import Project, Category, Expense
from django.views.generic import CreateView
from  django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Project, Expense

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Project, Expense
from django.views.decorators.csrf import csrf_exempt  # import the decorator
from django.core.exceptions import ValidationError


# Create your views here.
#OKAY
@login_required
def project_list(request):
    project_list = Project.objects.all()
    paginator = Paginator(project_list,6)
    print(request.GET)
    page = request.GET.get('page')
    try:
        project_list = paginator.page(page)
    except PageNotAnInteger:
        project_list = paginator.page(1)
    except EmptyPage:
        project_list = paginator.page(paginator.num_pages)
    return render(request, 'budget/project-list.html', {'project_list':project_list})

@login_required
@csrf_exempt
def project_detail(request, project_slug):
    print("details ---")
    project = get_object_or_404(Project, slug=project_slug)
    if request.method == 'POST':
        print("adding---")
        form = ExpenseForm(request.POST)
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        print(title, amount, category_name)
        category, _ = Category.objects.get_or_create(name=category_name, project=project)
        _save = Expense.objects.create(
            project=project,
            title=title,
            amount=amount,
            category=category,
            description=description,
            priority=priority
        )
        _save.save()
        return redirect('detail', project_slug=project_slug)
    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id=id)
        expense.delete()
        return HttpResponse('')
    else:
        expenses = Expense.objects.filter(project=project).order_by('-priority', '-date')
        context = {'project': project, 'expense_list': expenses, 'form': ExpenseForm()}
        return render(request, 'budget/project-detail.html', context)


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'budget/add-project.html'
    fields = ('name','budget')

    def form_valid(self, form):
        #project = Project()
        self.object = form.save(commit=False)
        self.object.save()
        categories = self.request.POST['categoriesString'].split(',')
        for category in categories:
            Category.objects.create(
                project = Project.objects.get(id=self.object.id),
                name = category
            ).save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('list')

""" def add_expense(request, project_id):
    print("in -- 7")
    project = Project.objects.get(id=project_id)
    print("in")
    if request.method == 'POST':
        print(1)
        form = ExpenseForm(request.POST)
        print(form)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.project = project
            expense.save()
            return redirect('project_detail', project_id=project_id)
    else:
        form = ExpenseForm()
    return render(request, 'add-expense.html', {'form': form, 'project': project}) """



""" def add_expense(request, project_slug):
    print("in -- 7")
    project = get_object_or_404(Project, slug=project_slug)
    print("in")
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.project = project
            expense.save()
            return redirect('project_detail', project_slug=project_slug)
    else:
        form = ExpenseForm()
    return render(request, 'budget/project-detail.html',{'project': project}) """