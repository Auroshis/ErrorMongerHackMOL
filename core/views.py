from django.contrib.auth.models import User
#from django.contrib.auth import authenticate
#from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm
from django import forms
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Problem, Solution
from django.db.models import F


def home(request):
    return render(request,'home.html')

# registration method of new users method
def register(request):
    # User registration data can be sent only if the request method is 'POST' else it will keep redirecting an empty form
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        # If all the fields are filled up in the correct format then retrieve data from each field
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            # Checking if the user is an existing user or a new user, creating neew account and logging in a new user
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return render(request, 'home.html')    
            else:
                # Redirect to login page if username or email already exists
                return render(request, 'login.html')
                
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form' : form})

# login_required decorator ensures you can not access these functionalities without logging in
@login_required
def search(request):
    keyword = request.GET.get('Search', 'default')
    #print('keyword', type(keyword))
    # Searching for keyword using wildcards in db across various db fields
    try:
        problems = Problem.objects.filter(user_id = request.user.id,pro_lang__contains=keyword)|Problem.objects.filter(user_id = request.user.id, framework_library__contains=keyword)|Problem.objects.filter(user_id = request.user.id, error_name__contains=keyword) #lazy evaluation the next uery will be executed if the previous one fails
        if problems:
            return render(request, 'problem_list.html', {'problems': problems, 'empty_queryset':False, 'message':''})
        else:
            return render(request, 'problem_list.html', {'problems': problems, 'empty_queryset':True, 'message':"Sorry no matches found 😅"})
    except:
        return render(request, 'error.html')

@login_required
def delete_problem(request, pk):
    try:
        if request.method == 'POST':
            problem = Problem.objects.get(pk=pk)
            problem.delete()
        return redirect('home')
    except:
        return redirect('home')

@login_required
def delete_solution(request, pk):
    try:
        if request.method == 'POST':
            solution = Solution.objects.get(pk=pk)
            solution.delete()
        return redirect('home')
    except:
        return redirect('home')

@login_required
def recent_problem_list(request):
    try:
        # Get all the Problems added by the user in sorted order by date i.e, most recent Problem at the top
        problems = Problem.objects.filter(user_id = request.user.id).order_by('date_time').reverse()
        if problems:# if the queryset is not empty
            return render(request, 'problem_list.html', {'problems': problems, 'empty_queryset':False, 'message':""})
        else:# if empty queryset i.e, no records to show
            return render(request, 'problem_list.html', {'problems': problems, 'empty_queryset':True, 'message':"You haven't added any Errors yet!"})
    except:
        return render(request, 'error.html', {'message': "We encountered an error while fetching your recent problems😣"})

@login_required
def common_problem_list(request):
    #print('user id -> ', request.user.id)
    # Get all the Problems added by the user in sorted order by the number of counts in a decreasing order
    try:
        problems = Problem.objects.filter(user_id = request.user.id).order_by('count').reverse()
        if problems:
            return render(request, 'problem_list.html', {'problems': problems, 'empty_queryset':False, 'message':''})
        else:
            return render(request, 'problem_list.html', {'problems': problems, 'empty_queryset':True, 'message':"You haven't added any Errors yet!"})
    except:
        return render(request, 'error.html', {'message': "We encountered an error while fetching your common problems😣"})


# Get all the solutions for a particular problem
@login_required
def solution_list(request, pk):
    # The below method takes 3 database hits
    try:
        current_problem = Problem.objects.get(pk=pk) #  db hit 1
        # Update the count of the number of times a particular problem is visited by +1
        current_problem.count = F('count') + 1
        current_problem.save() # db hit 2
        solutions = Solution.objects.filter(problem = current_problem) # db hit 3 
        #solutions = Problem.objects.filter(user_id=request.user.id, pk=pk).select_related('solution_link').order_by('date_time')
        if solutions:
            return render (request, 'solution_list.html',{'solutions': solutions, 'empty_queryset':False})
        else:
            return render (request, 'solution_list.html',{'solutions': solutions, 'empty_queryset':True})
        # optimise the number of database hits
    except:
        return render(request, 'error.html', {'message': "We encountered an error while fetching Solution to your Problem😣"})

# Function to add new Errors/Problems and a solution
@login_required
def add_problem(request):
    if request.method == 'POST':
        if request.POST.get('prolang') and request.POST.get('error_name'):
            user_id = request.user.id
            programming_language = request.POST.get('prolang')
            framework_library = request.POST.get('frlib')
            solution_link = request.POST.get('sollink')
            text_sol = request.POST.get('code')
            remark = request.POST.get('remark')
            error_name = request.POST.get('error_name')
            problem = Problem(pro_lang = programming_language, framework_library = framework_library, error_name=error_name, user_id = user_id)
            problem.save()
            solution = Solution(problem = problem, solution_link = solution_link, remark = remark, text_sol = text_sol, user_id = user_id)
            solution.save()
            print('saving into db')
            return render(request, 'add_problem.html', {'alert_value': True, 'type':'success'})
    else:
            return render(request, 'add_problem.html', {'alert_value': True, 'type':'danger'})

@login_required
def new_problem(request):
    return render(request, 'add_problem.html')

@login_required
def new_solution(request,pk):
    return render(request, 'add_solution.html', {'pk':pk})

@login_required
def add_solution(request):
    if request.method == 'POST':
        if request.POST.get('sollink'):
            solution_link = request.POST.get('sollink')
            text_sol = request.POST.get('code')
            remark = request.POST.get('remark')
            problem_pk = request.POST.get('problem_pk')
            problem = Problem.objects.get(pk=problem_pk)
            solution = Solution(problem = problem, solution_link = solution_link, remark = remark, text_sol = text_sol, user_id = request.user.id)
            solution.save()
            #print('saving into db')
            #return reverse("solution_list", kwargs={"id":pk})aA
            return render(request, 'add_solution.html', {'alert_value': True, 'type':'success'})# add a toast error added successfully
    else:
            return render(request, 'add_solution.html', {'alert_value': True, 'type':'danger'})# add a toast to fill again