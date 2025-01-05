from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Profile, Language
from .forms import ProfileForm
from django.db.models import Q

class ProfileListView(ListView):
    model = Profile
    template_name = 'users/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 6

    def get_queryset(self):
        queryset = Profile.objects.filter(is_public=True).select_related(
            'user'
        ).prefetch_related('languages')

        # Recherche
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(user__username__icontains=q) |
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q) |
                Q(bio__icontains=q)
            )

        # Filtres
        language = self.request.GET.get('language')
        if language:
            queryset = queryset.filter(languages__code=language)

        status = self.request.GET.get('status')
        if status == 'verified':
            queryset = queryset.filter(verified=True)
        elif status == 'unverified':
            queryset = queryset.filter(verified=False)

        level = self.request.GET.get('level')
        if level:
            if level == 'expert':
                queryset = queryset.filter(reputation_score__gte=1000)
            elif level == 'advanced':
                queryset = queryset.filter(reputation_score__gte=500, reputation_score__lt=1000)
            elif level == 'intermediate':
                queryset = queryset.filter(reputation_score__gte=100, reputation_score__lt=500)
            elif level == 'beginner':
                queryset = queryset.filter(reputation_score__lt=100)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = Language.objects.all()
        return context

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'

class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'users/profile_form.html'
    success_url = reverse_lazy('profile-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'users/profile_form.html'
    success_url = reverse_lazy('profile-list')

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'users/profile_confirm_delete.html'
    success_url = reverse_lazy('profile-list')