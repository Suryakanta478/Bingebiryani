from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['home']   # ⚠️ yaha tera URL name hona chahiye

    def location(self, item):
        return reverse(item)
