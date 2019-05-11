from django.shortcuts import render, HttpResponse
from django.db.models import Sum, Count, Avg, Max
from app01 import models


# Create your views here.
def query(request):
    # ######################基于对象查询(子查询)###############################

    # 一对一 author ----- authordetail
    #                  正向:按字段 authorDetail
    # 一对一   author  ----------------------->  authordetail
    #                 <-----------------------
    #                  反向:按表名 author

    # 正向:查询一个作者的详细信息中的手机号
    # author_obj = models.Author.objects.filter(name='小黑').first()
    # print(author_obj.authorDetail.telephone)

    # 反向:查询地址是某地的作者姓名
    # author_deta = models.AuthorDetail.objects.filter(addr='asdf').first()
    # print(author_deta.author.name)

    # 一对多 book(多,外键) ---  publish(一)

    # 正向查询:关联字段在book表里面，所以book --> publish的查询是正向查询
    # 正向查询按字段:查询一本书的出版社的邮箱
    # python_obj = models.Book.objects.filter(title='python').first()
    # print(python_obj.publish.email)

    # 反向查询按 表名小写_set.all():publish --> book
    # 查询一个出版社对应的所有书籍名称
    # publish_obj = models.Publish.objects.filter(name='橘子出版社').first()
    # for book_obj in publish_obj.book_set.all():
    #     print(book_obj.title)

    # 多对多 book -------- book
    #                正向:按字段（authors.all()）
    # 多对多   book  ----------------------->  author
    #               <-----------------------
    #                  反向:book_set.all()

    # 正向查询:查询某一本书籍的作者的年龄，可能多个作者
    # python_obj = models.Book.objects.filter(title='python').first()
    # for author in python_obj.authors.all():
    #     print(author.name, "---", author.age)

    # 反向查询:查询一个作者出版过的书籍名称
    # author_obj = models.Author.objects.filter(name='小黑').first()
    # for book in author_obj.book_set.all():
    #     print(book.title)

    # ######################基于QuerySet和"__"(双下划线)查询(join查询)###############################
    # 正向查询：表名__按字段  反向查询：表名小写__字段名

    # 一对一
    # 正向:查询一个作者的详细信息中的手机号
    # ret = models.Author.objects.filter(name='小黑').values("authorDetail__telephone")
    # print(ret)

    # 反向:查询地址是某地的作者姓名
    # ret = models.AuthorDetail.objects.filter(addr='asdf').values("author__name")
    # print(ret)

    # 一对多
    # 正向查询:查询一本书的出版社的邮箱
    """
    select publish.email from Book
    left join Publish on book.publish_id =publish.nid
    where book.title='python'
    """
    # ret = models.Book.objects.filter(title='python').values("publish__email")
    # print(ret)

    # 反向查询:查询一个出版社对应的所有书籍名称
    # 方式1:
    # ret = models.Publish.objects.filter(name='橘子出版社').values("book__title")
    # print(ret)
    # 方式2:
    # ret = models.Book.objects.filter(publish__name='橘子出版社').values('title')
    # print(ret)

    # 多对多
    # 正向查询:查询某一本书籍的作者的年龄，可能多个作者
    # ret = models.Book.objects.filter(title='python').values("authors__age")
    # print(ret)

    # 反向查询:查询一个作者出版过的书籍名称
    # ret = models.Author.objects.filter(name='小黑').values("book__title")
    # print(ret)

    # 补充:
    # 查询手机号以151开头的作者出版过的书籍名称以及书籍对应的出版社名称(要使用自己创建的5张表)
    # ret = models.Book.objects.filter(authors__authorDetail__telephone__startswith="151").values('title', 'publish__name')
    # print(ret)

    # ######################################聚合与分组################################################
    # 聚合:aggregate
    # 查询所有书籍的价格和
    # ret = models.Book.objects.all().aggregate(price_sum=Sum('price'))
    # print(ret)

    # 查询所有作者的平均年龄
    # ret = models.Author.objects.all().aggregate(age_avg=Avg('age'))
    # print(ret)

    # 分组:
    """
    ---------------------------------------------------------------------
    emp:
        id     name     age     dept
        1      alex1      22     保安部
        2      alex2      24     保安部
        3      alex3      28     保洁部
        
        sql:
            select Count(id) from emp group by dep
        orm:
            models.emp.objects.values('dep').annotate(c=Count('id'))
    ---------------------------------------------------------------------        
    跨表的分组查询
    emp:
        id      name      age     dep_id
        1       alex1      22        1
        2       alex2      24        1
        3       alex3      28        2
    dep:
        id  name
        1   保安部
        2   保洁部
        -----------------------
        查询每一个部门的名称及对应的人数
        sql:
            select * from emp inner join dep on emp.dep_id=dep.id
            
            id      name      age     dep_id    id  name
            1       alex1      22        1      1   保安部
            2       alex2      24        1      1   保安部
            3       alex3      28        2      2   保洁部
        
            select * from emp inner join dep on emp.dep_id=dep.id group by dep.id,dep.name
        ORM:
            关键点:
                1. queryset对象.annotate()
                2. annotate进行分组统计，按select的字段进行group_by(annotate 前面是什么就按照什么分组)
                3. annotate()返回值依然是queryset对象，增加了分组统计之后的键值对
                
            models.emp.objects.values('dep').annotate(c=Count(id)).values('dept',c)
    """
    # 正向查询
    # ret = models.Person.objects.values('dept_id').annotate(c=Count('dept_id')).values('dept__name', 'c')
    # print(ret)
    # ret = models.Person.objects.values("dept_id").annotate(avg=Avg('salary')).values("dept__name", "avg")
    # print(ret)

    # 反向查询
    # ret = models.Dept.objects.values('name').annotate(c=Count('person__salary')).values('name', 'c')
    # print(ret)

    # 查询每一个作者的名字及出版过的书籍最高价格
    # 反向查询
    # ret = models.Author.objects.values('name').annotate(pri=Max('book__price')).values('name', 'pri')
    # print(ret)
    # 正向查询
    # ret = models.Book.objects.values('authors__name').annotate(pri=Max('price')).values('authors__name', 'pri')
    # print(ret)

    # 查询每一个出版社出版过的书籍的平均价格
    # 正向查询
    # ret = models.Book.objects.values('publish__name').annotate(pri=Avg('price')).values('publish__name', 'pri')
    # print(ret)
    # 反向查询
    # ret = models.Publish.objects.values('name').annotate(pri=Avg('book__price')).values('name', 'pri')
    # print(ret)

    # 查询每一本书籍的作者个数
    # 正向查询
    # ret = models.Book.objects.values('title').annotate(cou=Count('authors__name')).values('title', 'cou')
    # print(ret)
    # 反向查询
    # ret = models.Author.objects.values('book__nid').annotate(coun=Count('name')).values('book__title', 'coun')
    # print(ret)

    # 补充：统计不止一个作者的图书的名称
    ret = models.Book.objects.values('title').annotate(cou=Count('authors__name')).filter(cou__gt=1).values('title',
                                                                                                            'cou')
    print(ret)
    return HttpResponse("ok123")
