from django.views.generic import ListView

from products.models import Product


class SearchProductListView(ListView):
    template_name = 'search/search_view.html'

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.none()
