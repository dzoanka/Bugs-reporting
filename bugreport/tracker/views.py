from django.shortcuts import render, redirect
from .models import Bug
from .models import PROJECT
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import TrackTicketForm
from django.core.mail import send_mail

def index(request):
    """View function for home page of site."""

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

    return render(request, 'tracker/bug_list.html', context=context)

class BugDetailView(generic.DetailView):
    model = Bug

    def get_context_data(self, **kwargs):
        context = super(BugDetailView, self).get_context_data(**kwargs)
        if 'project' in self.kwargs:
            context["project"] = self.kwargs['project']
        return context

    def bug_detail_view(request, primary_key):
        bug = get_object_or_404(Bug, pk=primary_key)
        return render(request, 'tracker/bug_detail.html', context={'bug': bug})

def send_query_email(full_name, ticket_number, email):
    send_mail(
        'Query to ' + full_name + ' system',
        'You added a query to ' + full_name +  ' system. The ticket number is ' + ticket_number + '. You can track or edit your query by providing the ticket number.',
        'joanna_len@iwonka.med.virginia.edu',
        [email],
        fail_silently=False,
    )

class BugCreate(CreateView):
    model = Bug
    fields = ['project', 'description', 'screenshot_or_attachment', 'first_name', 'last_name', 'affiliation', 'location', 'email', 'query_type']
    initial={'project': 'o'}

    def get_context_data(self, **kwargs):
        context = super(BugCreate, self).get_context_data(**kwargs)
        if 'project' in self.kwargs:
            context["project"] = self.kwargs['project']
            context["project_full"] = [v for (k,v) in PROJECT if k == self.kwargs['project']][0]
        return context

    def form_valid(self, form):
        if 'project' in self.kwargs:
            full_name = [v for (k,v) in PROJECT if k == self.kwargs['project']][0]
            if form.instance.email != None:
                send_query_email(full_name, str(form.instance.ticket_number), form.instance.email)
            obj = form.save(commit=False)
            obj.project = self.kwargs['project']
            obj.save()
            try:
                bug = Bug.objects.get(ticket_number=obj.ticket_number)
                return redirect('bug-detail', pk=bug.id, project=bug.project)
            except Bug.DoesNotExist:
                return redirect('/')
        else:
            full_name = [v for (k,v) in PROJECT if k == form.instance.project][0]
            if form.instance.email != None:
                send_query_email(full_name, str(form.instance.ticket_number), form.instance.email)
        # call the parents class method
        return super().form_valid(form)

def track_ticket(request):
    context = {}

    if request.method == 'POST':
        form = TrackTicketForm(request.POST)
        if Bug.objects.filter(ticket_number = request.POST['ticket_number']).exists():
            return redirect('bug-update', request.POST['ticket_number'])
        else:
            form = TrackTicketForm()
            form.error = "A query with given ticket number does not exist!"
    else:
        form = TrackTicketForm()

    context['form'] = form
    return render(request, 'tracker/track_ticket.html', context=context)

def track_ticket_project(request, project):
    context = {}

    if request.method == 'POST':
        form = TrackTicketForm(request.POST)
        bug_found = Bug.objects.filter(ticket_number = request.POST['ticket_number'])
        if bug_found.exists():
            if bug_found.get().project == project:
                return redirect('bug-update', request.POST['ticket_number'], project)
            else:
                return redirect('bug-update', request.POST['ticket_number'])
        else:
            form = TrackTicketForm()
            form.error = "A query with given ticket number does not exist!"
    else:
        form = TrackTicketForm()

    context['form'] = form
    context['project'] = project
    return render(request, 'tracker/track_ticket.html', context=context)

class BugUpdate(UpdateView):
    model = Bug
    fields = ['project', 'description', 'screenshot_or_attachment', 'first_name', 'last_name', 'affiliation', 'location', 'email', 'query_type']

    def get_object(self, queryset=None):
        obj = Bug.objects.get(ticket_number=self.kwargs['uuid'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(BugUpdate, self).get_context_data(**kwargs)
        context['bug'] = self.get_object()
        if 'project' in self.kwargs:
            context["project"] = self.kwargs['project']
            context["project_full"] = [v for (k,v) in PROJECT if k == self.kwargs['project']][0]
        return context

    def get_template_names(self):
        self.template_name_suffix = '_form_track'
        return super(BugUpdate, self).get_template_names()
