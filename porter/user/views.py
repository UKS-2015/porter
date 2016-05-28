from abc import ABCMeta
from core.forms import UserForm, PorterUserForm, UserPasswordForm
from core.mixins import PorterAccessMixin
from core.models import PorterUser, Project
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView


class UserProfileAbstract(PorterAccessMixin, DetailView):
    __metaclass__ = ABCMeta
    model = User
    success_url = reverse_lazy('list')

    def get_context_data(self, **kwargs):
        context = super(UserProfileAbstract, self).get_context_data(**kwargs)
        user = self.get_object()

        try:
            porteruser = PorterUser.objects.get(user=user)
            context['projects'] = Project.objects.filter(users=user)
            context['object'] = porteruser.to_dict()
            context['user'] = user
            context['picture'] = porteruser.picture
        except (Project.DoesNotExist, PorterUser.DoesNotExist):
            context['projects'] = []
        return context


class UserProfile(UserProfileAbstract):
    model = User
    success_url = reverse_lazy('list')
    template_name = 'user/profile.html'

    def get_object(self):
        user = self.request.user
        return user


class UserDetail(UserProfileAbstract):
    model = User
    success_url = reverse_lazy('list')
    template_name = 'user/detail.html'

    def get_object(self):
        return User.objects.get(pk=self.kwargs['pk'])


class UserPassword(PorterAccessMixin, UpdateView):
    model = User
    success_url = reverse_lazy('profile')
    template_name = 'user/password.html'
    form_class = UserPasswordForm

    def get_form_kwargs(self, **kwargs):
        data = super(UserPassword, self).get_form_kwargs(**kwargs)
        data['user'] = self.get_object()
        return data

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def form_valid(self, form):
        form.save()
        return super(UserPassword, self).form_valid(form)

    def get_object(self):
        user = self.request.user
        return user


class UserChange(PorterAccessMixin, UpdateView):
    model = User
    success_url = reverse_lazy('user:profile')
    template_name = 'user/change.html'
    form_class = UserForm

    def get_object(self):
        user = self.request.user
        return user

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        try:
            porter_user = PorterUser.objects.get(user=self.object)
            porter_user_form = PorterUserForm(instance=porter_user)
        except PorterUser.DoesNotExist:
            porter_user_form = PorterUserForm()

        return self.render_to_response(
            self.get_context_data(form=form, porter_user_form=porter_user_form)
        )

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        try:
            porter_user = PorterUser.objects.get(user=self.object)
        except PorterUser.DoesNotExist:
            porter_user = PorterUser()
            porter_user.user = self.object

        porter_user_form = PorterUserForm(self.request.POST, request.FILES, instance=porter_user)

        if form.is_valid() and porter_user_form.is_valid():
            return self.form_valid(form, porter_user_form)
        else:
            return self.form_invalid(form, porter_user_form)

    def form_valid(self, form, porter_user_form):
        """
        Called if all forms are valid. Creates a User instance along with
        associated PorterUser and then redirects to a success page.
        """
        self.object = form.save()
        porter_user_form.save()
        return redirect(reverse('profile'))

    def form_invalid(self, form, porter_user_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  porter_user_form=porter_user_form)
        )
