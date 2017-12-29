#coding=utf-8
from django.contrib import admin
from  .models import  gengyuns,zhongzi,zhishidian,fujian
from django.utils.translation import ugettext_lazy as _
from datetime import date
# Register your models here.


class DecadeBornListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _(u'班级')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 't_banji'
    _

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        print model_admin

        return (
            ('80s', _('in the eighties')),
            ('90s', _('in the nineties')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        print self.value()



        return queryset.filter(pk=6)


#附件内联
class fujianInline(admin.TabularInline):
    model = fujian

class zdy_fujian(admin.ModelAdmin):
    list_display = ['id','name','upfile']
    def upfile(self,obj):
        return """<a href=http://zxzx.hui1983.top%s>  %s </a>""" % (obj.up_file.name[4:],obj.name)

    upfile.short_description = "下载附件"
    upfile.allow_tags = True





class zyd_zhongzi(admin.ModelAdmin):
    list_filter = [DecadeBornListFilter,]

class zdy_zhidianshi(admin.ModelAdmin):
    inlines = [fujianInline, ]

admin.site.register(gengyuns)

admin.site.register(zhongzi,zyd_zhongzi)
admin.site.register(zhishidian,zdy_zhidianshi)

admin.site.register(fujian,zdy_fujian)