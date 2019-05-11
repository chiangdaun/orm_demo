#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "duan"
# Date: 2019/5/3

import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_demo.settings")
    import django

    django.setup()

    from app01 import models
    from django.db.models import Avg

    # # ORM分組查詢,每個部門名稱及部門的平均工資
    # ret = models.Employee.objects.all()
    # """
    # SELECT `employee`.`id`, `employee`.`name`, `employee`.`age`, `employee`.`salary`, `employee`.`province`, `employee`.`dept` FROM `employee`
    # <QuerySet [<Employee: 张三>, <Employee: 李四>, <Employee: 王五>, <Employee: 赵六>]>
    # """
    # print(ret)
    #
    # ret = models.Employee.objects.all().values("dept")
    # """
    # SELECT `employee`.`dept` FROM `employee`
    # <QuerySet [{'dept': '财务部'}, {'dept': '人事部'}, {'dept': '人事部'}, {'dept': '教学部'}]>
    # """
    # print(ret)
    #
    # ret = models.Employee.objects.all().values("dept", "age")
    # """
    # SELECT `employee`.`dept`, `employee`.`age` FROM `employee`
    # <QuerySet [{'dept': '财务部', 'age': 23}, {'dept': '人事部', 'age': 34}, {'dept': '人事部', 'age': 45}, {'dept': '教学部', 'age': 56}]>
    # """
    # print(ret)
    #
    # # ORM中values或者values_list 里面写什么字段，就相当于select 什么字段
    #
    # ret = models.Employee.objects.values("dept").annotate(a=Avg("salary")).values("dept", "a")
    # """
    # SELECT `employee`.`dept`, AVG(`employee`.`salary`) AS `a` FROM `employee` GROUP BY `employee`.`dept` ORDER BY NULL
    # <QuerySet [{'dept': '财务部', 'a': 2000.0}, {'dept': '人事部', 'a': 5000.0}, {'dept': '教学部', 'a': 8000.0}]>
    # """
    # print(ret)
    # # annotate 前面是什么就按照什么分组！
    #
    # # ORM連表查詢
    # ret = models.Person.objects.values("dept_id")
    # """
    # SELECT `person`.`dept_id` FROM `person`
    # <QuerySet [{'dept_id': 1}, {'dept_id': 1}, {'dept_id': 2}, {'dept_id': 3}, {'dept_id': 3}]>
    # """
    # print(ret)
    #
    # ret = models.Person.objects.values("dept_id").annotate(avg=Avg('salary')).values("dept__name", "avg")
    # """
    # SELECT `dept`.`name`, AVG(`person`.`salary`) AS `avg` FROM `person` INNER JOIN `dept` ON (`person`.`dept_id` = `dept`.`id`) GROUP BY `person`.`dept_id`, `dept`.`name` ORDER BY NULL
    # <QuerySet [{'dept__name': '保安部', 'avg': 3000.0}, {'dept__name': '保洁部', 'avg': 2000.0}, {'dept__name': '影视部', 'avg': 2600.0}]>
    # """
    # print(ret)
    #
    # # 查詢person表,判斷工資是否大於2000
    # ret = models.Person.objects.all().extra(
    #     select={"gt": "salary>2000"}
    # )
    # """
    # SELECT (salary>2000) AS `gt`, `person`.`id`, `person`.`name`, `person`.`salary`, `person`.`dept_id` FROM `person`
    # """
    # # print(ret)
    # for i in ret:
    #     print(i.name, i.gt)
    #
    # # 執行原生SQL
    # from django.db import connection, connections
    #
    # cursor = connection.cursor()  # cursor = connections['default'].cursor()
    # cursor.execute("""SELECT * from person where id = %s""", [1])
    # ret = cursor.fetchone()
    # """
    # SELECT * from person where id = 1
    # (1, '小黑', 2000, 1)
    # """
    # print(ret)
