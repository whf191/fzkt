#coding=utf-8
from  __future__ import unicode_literals
from  django.shortcuts import  HttpResponse
from .models import *
def get_doc_count(request):
    zhuti = request.GET.get("zhuti",None)
    pk = request.GET.get("pk",None)

    if zhuti == "zhuti":
        if pk:
            rs = zhongzi.objects.filter(gengyuns_id=pk)
            rs = len(rs)
            if rs != 0:
                return HttpResponse("0|%s" % rs)
            else:
                return HttpResponse("1|%s" % rs)
        else:
            return HttpResponse("not pk")

    if zhuti == "shipin":
        if pk:
            rs = zhishidian.objects.filter(zhongzi_id=pk)
            rs = len(rs)
            if rs != 0:
                return HttpResponse("0|%s" % rs)
            else:
                return HttpResponse("1|%s" % rs)
        else:
            return HttpResponse("not pk")

    return HttpResponse("not zhuti")


