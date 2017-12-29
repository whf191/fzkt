# coding=utf-8
from  __future__ import unicode_literals
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from .models import gengyuns, zhongzi, zhishidian
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # 导入django自带的分页工具
import datetime, os
from  django.contrib.auth.decorators import  login_required

# Create your views here.


daohangtiao = {'导航': [["url", "飞机"]]}

daohangtiao = None


# 首页文章数据展示
def shouye_gengyun(limit=10):
    dhl_list = gengyuns.objects.all().order_by('-pk')

    p = Paginator(dhl_list, limit)  # 默认2行为一列并反转列表
    return p


# 获取种子分页
def zhongzi_gengyun(pk, limit=10):
    rs_zz = getZhongzi(pk)
    if rs_zz:
        p = Paginator(list(reversed(rs_zz)), limit)  # 默认2行为一列并反转列表
        return p
    p = Paginator([], limit)
    return p


# gengyun单个获取
def getGengyun(pk):
    try:
        pk = int(pk)
    except Exception, e:
        print e
        return False
    try:
        gy = gengyuns.objects.get(pk=pk)
        return gy
    except Exception, e:
        print e
        return False


# gengyun_zhongzi获取
def getZhongzi(pk):
    try:
        pk = int(pk)
    except Exception, e:
        print e
        return False

    try:
        zz = zhongzi.objects.filter(gengyuns_id=pk)
        return zz
    except Exception, e:
        print e
        return False


# zhongzi_open单个打开
def getZhongziOpen(pk):
    try:
        pk = int(pk)
        zo = zhongzi.objects.get(pk=pk)
        return zo
    except Exception, e:
        print e
        return False


def gengyun_index(request):
    # 获取分页对象
    fenye_duixiang = shouye_gengyun()
    page = request.GET.get('page', None)
    if not page:
        page = 1
    try:
        huoqu_mouye_jilu = fenye_duixiang.page(page)
    except PageNotAnInteger:
        huoqu_mouye_jilu = fenye_duixiang.page(1)
    except EmptyPage:
        huoqu_mouye_jilu = fenye_duixiang.page(fenye_duixiang.num_pages)  # 取最后一条记录

    return render_to_response("index.html",
                              {"daohangtiao": daohangtiao, 'huoqu_mouye_jilu': huoqu_mouye_jilu, 'request': request})


def gengyun_zhongzi(request):
    page = request.GET.get('page', None)
    pk = request.GET.get("pk", None)

    if pk:
        rs_gy = getGengyun(pk)
        fenye_duixiang = zhongzi_gengyun(pk)
        if rs_gy:
            if not page:
                page = 1
            try:
                huoqu_mouye_jilu = fenye_duixiang.page(page)
            except PageNotAnInteger:
                huoqu_mouye_jilu = fenye_duixiang.page(1)
            except EmptyPage:
                huoqu_mouye_jilu = fenye_duixiang.page(fenye_duixiang.num_pages)  # 取最后一条记录
            return render_to_response("gengyun_zhongzi.html",
                                      {"daohangtiao": daohangtiao, "rs_gy": rs_gy, "huoqu_mouye_jilu": huoqu_mouye_jilu,
                                       'request': request})

    # return render_to_response("zhongzi.html",{"daohangtiao":daohangtiao})
    return HttpResponseRedirect("/gengyun_index/")


# getZhiShiDian获取
def getZhiShiDian(pk):
    try:
        pk = int(pk)
    except Exception, e:
        print e
        return False

    try:
        zz = zhishidian.objects.filter(zhongzi_id=pk)
        return zz
    except Exception, e:
        print e
        return False

#课程附件
def getfujian(zz):
    l2 = []
    for i in zz:
        isi = i.fujian_set.all()
        if isi:
            for i2 in isi:
                l2.append(i2)
    return l2

# 获取种子分页
def sanji_gengyun(pk, limit=10):
    rs_zz = getZhiShiDian(pk)
    if rs_zz:
        p = Paginator(list(reversed(rs_zz)), limit)  # 默认2行为一列并反转列表
        return p
    p = Paginator([], limit)
    return p


def zhongzi_open(request):
    page = request.GET.get('page', None)
    pk = request.GET.get("pk", None)
    if pk:
        rs_gy = getZhongziOpen(pk)
        rs_zz = getZhiShiDian(pk)
        rs_zz = getfujian(rs_zz)
        fenye_duixiang = sanji_gengyun(pk)
        if rs_gy:
            if not page:
                page = 1
            try:
                huoqu_mouye_jilu = fenye_duixiang.page(page)
            except PageNotAnInteger:
                huoqu_mouye_jilu = fenye_duixiang.page(1)
            except EmptyPage:
                huoqu_mouye_jilu = fenye_duixiang.page(fenye_duixiang.num_pages)  # 取最后一条记录
            return render_to_response("zhongzi.html",
                                      {"daohangtiao": daohangtiao, "rs_gy": rs_gy, "huoqu_mouye_jilu": huoqu_mouye_jilu,
                                       'request': request ,'rs_zz':rs_zz})

    return HttpResponseRedirect("/gengyun_index/")


# ckeditor 图片粘贴上传部分

def datetime_image_name():
    d1 = datetime.datetime.today()
    d1 = "%s%s%s%s%s%s%s " % (d1.year, d1.month, d1.day, d1.hour, d1.minute,
                              d1.second, d1.microsecond)

    return d1 + ".png"


def get_static_lujing(image_name=None):
    #static = os.path.dirname(os.path.abspath(__file__))
    static = "/usr/local/nginx/html/static2/images"
    static = static + os.sep

    if image_name:
        return static + os.sep + image_name
    else:
        return static

@login_required
def uploader(request):
    image = request.FILES.get("upload")
    image_name = datetime_image_name()
    white_image = get_static_lujing(image_name)

    with  open(white_image, "wb") as f:
        f.write(image.read())

    tupian = """{"uploaded": 1,"fileName": "%s","url": "/static/images/%s"} """ % (image_name, image_name)

    return HttpResponse(tupian)


def liulan(request):
    print request
    print request.GET
    print request.POST
    CKEditorFuncNum = request.GET.get("CKEditorFuncNum", None)
    print CKEditorFuncNum

    rs = """
    <script type="text/javascript">
        window.parent.CKEDITOR.tools.callFunction(%s,"/static/files/foo.jpg")


        </script>


    """ % CKEditorFuncNum

    return HttpResponse(rs)
