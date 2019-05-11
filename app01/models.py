from django.db import models


# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=32, verbose_name="姓名")
    age = models.IntegerField(verbose_name='年龄')
    salary = models.IntegerField(verbose_name='工资')
    province = models.CharField(max_length=32, verbose_name="省份")
    dept = models.CharField(max_length=32, verbose_name="部门")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "employee"
        verbose_name = "员工"
        verbose_name_plural = verbose_name


class Dept(models.Model):
    """
    部門表
    """
    name = models.CharField(max_length=32, verbose_name="部門名稱")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "dept"
        verbose_name = "部門"
        verbose_name_plural = verbose_name


class Person(models.Model):
    """
    員工表
    """
    name = models.CharField(max_length=32, verbose_name="姓名")
    salary = models.IntegerField(verbose_name="工資", default=None)
    dept = models.ForeignKey(to='Dept')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'person'
        verbose_name = "人員"
        verbose_name_plural = verbose_name


class Author(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    age = models.IntegerField()

    # 与AuthorDetail建立一对一的关系
    authorDetail = models.OneToOneField(to="AuthorDetail", on_delete=models.CASCADE)


class AuthorDetail(models.Model):
    nid = models.AutoField(primary_key=True)
    birthday = models.DateField()
    telephone = models.BigIntegerField()
    addr = models.CharField(max_length=64)


class Publish(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    email = models.EmailField()


class Book(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    publishDate = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    # 与Publish建立一对多的关系,外键字段建立在多的一方
    publish = models.ForeignKey(to="Publish", to_field="nid", on_delete=models.CASCADE)
    # 与Author表建立多对多的关系,ManyToManyField可以建在两个模型中的任意一个，自动创建第三张表
    authors = models.ManyToManyField(to='Author', )
