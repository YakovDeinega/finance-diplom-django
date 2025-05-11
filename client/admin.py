from django.contrib import admin

from client.models import UserInformation, Portfolio, PortfolioAsset

# Register your models here.
admin.site.register(UserInformation)
admin.site.register(Portfolio)
admin.site.register(PortfolioAsset)