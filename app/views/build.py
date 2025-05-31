from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from ..mixins import JSONResponseMixin
from ..models import Build, Processor, ProcessorCooler, GraphicsCard, Case, CaseFan, Motherboard, Memory, Storage, \
    PowerSupply


class BuildListView(ListView, JSONResponseMixin):
    model = Build
    template_name = 'pickpcparts/build/list.html'
    context_object_name = 'builds'
    paginate_by = 12

    def get_queryset(self):
        # Show user's builds first, then others
        if self.request.user.is_authenticated:
            user_builds = Build.objects.filter(author=self.request.user)
            other_builds = Build.objects.exclude(author=self.request.user)
            return user_builds.union(other_builds)
        return Build.objects.all()

    def render_to_response(self, context, **response_kwargs):
        if self.request.accepts('text/html') or 'html' in self.request.GET:
            return super().render_to_response(context, **response_kwargs)
        return self.render_to_json_response(context, **response_kwargs)


class BuildDetailView(DetailView, JSONResponseMixin):
    model = Build
    template_name = 'pickpcparts/build/detail.html'
    context_object_name = 'build'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = self.can_edit_build(self.object)
        return context

    def can_edit_build(self, build):
        if not self.request.user.is_authenticated:
            return False
        return self.request.user == build.author or self.request.user.is_staff

    def render_to_response(self, context, **response_kwargs):
        if self.request.accepts('text/html') or 'html' in self.request.GET:
            return super().render_to_response(context, **response_kwargs)
        return self.render_to_json_response(context, **response_kwargs)


class BuildForm(ModelForm):
    class Meta:
        model = Build
        fields = ['name', 'notes', 'processor', 'processor_cooler', 'graphics_card',
                  'case', 'case_fans', 'motherboard', 'memory', 'storage', 'power_supply']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['processor'].queryset = Processor.objects.all()
        self.fields['processor_cooler'].queryset = ProcessorCooler.objects.all()
        self.fields['graphics_card'].queryset = GraphicsCard.objects.all()
        self.fields['case'].queryset = Case.objects.all()
        self.fields['case_fans'].queryset = CaseFan.objects.all()
        self.fields['motherboard'].queryset = Motherboard.objects.all()
        self.fields['memory'].queryset = Memory.objects.all()
        self.fields['storage'].queryset = Storage.objects.all()
        self.fields['power_supply'].queryset = PowerSupply.objects.all()

    def clean(self):
        cleaned = super().clean()

        processor = cleaned.get('processor')
        processor_cooler = cleaned.get('processor_cooler')
        motherboard = cleaned.get('motherboard')
        case = cleaned.get('case')
        power_supply = cleaned.get('power_supply')

        if processor:
            if motherboard and processor.socket != motherboard.socket:
                self.add_error('motherboard',
                               _('Incompatible motherboard socket ({ms}) and processor socket ({ps}).').format(
                                   ms=motherboard.socket, ps=processor.socket))
            if processor_cooler and processor.socket not in processor_cooler.socket.all():
                self.add_error('processor_cooler',
                               _('Incompatible cooler socket (cs}) and processor socket ({ps}).').format(
                                   cs=', '.join([x[1] for x in processor_cooler.socket.all().values_list()]),
                                   ps=processor.socket
                               ))

        if case:
            if motherboard and motherboard.formfactor != case.formfactor:
                self.add_error('motherboard',
                               _('Incompatible motherboard form factor ({mf}) and case form factor ({cf}).').format(
                                   mf=motherboard.formfactor, cf=case.formfactor))
            if power_supply and power_supply.formfactor != case.formfactor:
                self.add_error('power_supply',
                               _('Incompatible power supply ({pf}) and case form factor ({cf}).').format(
                                   pf=power_supply.formfactor, cf=case.formfactor))


class BuildCreateView(LoginRequiredMixin, CreateView):
    model = Build
    form_class = BuildForm
    template_name = 'pickpcparts/build/form.html'
    success_url = reverse_lazy('builds')
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _('Build created successfully!'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create New Build')
        context['submit_text'] = _('Create Build')
        return context


class BuildUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Build
    form_class = BuildForm
    template_name = 'pickpcparts/build/form.html'
    login_url = '/login/'

    def test_func(self):
        build = self.get_object()
        return self.request.user == build.author or self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, _('Build updated successfully!'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Update Build: {name}').format(name=self.object.name)
        context['submit_text'] = _('Update Build')
        return context

    def get_success_url(self):
        return reverse_lazy('build-detail', kwargs={'pk': self.object.pk})


class BuildDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Build
    template_name = 'pickpcparts/build/delete.html'
    success_url = reverse_lazy('builds')
    context_object_name = 'build'
    login_url = '/login/'

    def test_func(self):
        build = self.get_object()
        return self.request.user == build.author or self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Build deleted successfully!'))
        return super().delete(request, *args, **kwargs)
