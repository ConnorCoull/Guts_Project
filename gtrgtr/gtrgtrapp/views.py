from .models import Guitars
from django.views.generic import ListView
# Create your views here.
class IndexView(ListView):
    model = Guitars
    context_object_name = 'guitars'
    paginate_by = 21
    template_name = 'index.html'

