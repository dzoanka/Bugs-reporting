from django.shortcuts import render, redirect
from .models import Book, Author, BookInstance, Genre, Bug
from .models import PROJECT
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import TrackTicketForm

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    # num_books = Book.objects.all().count()
    # num_instances = BookInstance.objects.all().count()
    #
    # # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    #
    # # The 'all()' is implied by default.
    # num_authors = Author.objects.count()
    #
    # context = {
    #     'num_books': num_books,
    #     'num_instances': num_instances,
    #     'num_instances_available': num_instances_available,
    #     'num_authors': num_authors,
    # }

    bug_list = Bug.objects.all()
    context = {
        'bug_list': bug_list,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BugListView(generic.ListView):
    model = Bug
    paginate_by = 15

def displayBugsForProject(request, project):
    bug_list = Bug.objects.all().filter(project = project)

    context = {
        'project': project,
        'bug_list': bug_list,
        'project_full': [v for (k,v) in PROJECT if k == project][0]
    }

    return render(request, 'tracker/project_bug_list.html', context=context)


class BugDetailView(generic.DetailView):
    model = Bug

    def bug_detail_view(request, primary_key):
        bug = get_object_or_404(Bug, pk=primary_key)
        return render(request, 'tracker/bug_detail.html', context={'bug': bug})

class BugCreate(CreateView):
    model = Bug
    fields = ['project', 'description', 'screenshot_or_attachment']

class ProjectBugCreate(CreateView):
    template_name = 'tracker/bug_form_project.html'
    model = Bug
    fields = ['description', 'screenshot_or_attachment']

    def get_context_data(self, **kwargs):
        context = super(ProjectBugCreate, self).get_context_data(**kwargs)
        context["project"] = self.kwargs['project']
        context["project_full"] = [v for (k,v) in PROJECT if k == self.kwargs['project']][0]
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.project = self.kwargs['project']
        obj.save()
        try:
            bug = Bug.objects.get(ticket_no=obj.ticket_no)
            return redirect('bug-detail', pk=bug.id)
        except Bug.DoesNotExist:
            return redirect('/')

def track_ticket(request):
    context = {}
    form = TrackTicketForm(request.POST or None)
    context['form'] = form
    return render(request, 'tracker/track_ticket.html', context=context)

class BugUpdate(UpdateView):
    #template_name = 'tracker/bug_form_project.html'
    model = Bug
    fields = ['description', 'screenshot_or_attachment'] #"__all__"

    def get_object(self, queryset=None):
        obj = Bug.objects.get(ticket_no=self.kwargs['uuid']) # instead of self.request.GET or self.request.POST
        return obj

class BugDelete(DeleteView):
    model = Bug
    success_url = reverse_lazy('bug')

#TUTORIAL:

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'tracker/book_detail.html', context={'book': book})


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2


class AuthorDetailView(generic.DetailView):
    model = Author

    def author_detail_view(request, primary_key):
        author = get_object_or_404(Author, pk=primary_key)
        return render(request, 'tracker/author_detail.html', context={'author': author})

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
