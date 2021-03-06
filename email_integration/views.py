import logging
logger = logging.getLogger(__name__)
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from .forms import VerifyEmailForm
from .models import EmailAddress, EmailProfile
from email_bot.views import OLContextMixin




class VerifyEmailFormView(OLContextMixin, FormView):
    form_class = VerifyEmailForm
    template_name = 'verify_form.html'
    success_url = '/introductions'
    heading = "Verify a new email address"

    def form_valid(self, form):
        form.send_email()
        return super(VerifyEmailFormView, self).form_valid(form)

class VerifyEmailView(OLContextMixin, DetailView):
    model = EmailAddress
    slug_field = 'verification_hash'
    queryset = EmailAddress.objects.filter(verification_complete=False)
    heading = "Gotcha!"

    def get(self, request, *args, **kwargs):
        if not request.user:
            return None
        self.object = self.get_object()
        self.object.user_profile, created = EmailProfile.objects.get_or_create(user=request.user)
        self.object.verification_complete = True
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)





