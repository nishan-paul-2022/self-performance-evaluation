from django.db import models


class Academic(models.Model):
    year = models.TextField()
    event = models.TextField()
    weight = models.TextField()
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'main_academic'


class Daily(models.Model):
    day = models.TextField()
    n2021 = models.TextField()
    n2022 = models.TextField()

    class Meta:
        managed = False
        db_table = 'main_daily'


class Imonlyhuman(models.Model):
    name = models.TextField()
    classname = models.TextField()
    time = models.TextField()
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'main_imonlyhuman'


class Undergraduate(models.Model):
    code = models.TextField()
    name = models.TextField()
    credit = models.TextField()
    grade = models.TextField()
    gpa = models.TextField()
    level = models.TextField()

    class Meta:
        managed = False
        db_table = 'main_undergraduate'


class ValueYearA(models.Model):
    year = models.TextField()
    event = models.TextField()
    book = models.TextField()
    routine_2am_7am = models.TextField()
    writing = models.TextField()
    study_time = models.TextField()
    response_teacher = models.TextField()
    response_friend = models.TextField()

    class Meta:
        managed = False
        db_table = 'main_value_year_a'


class ValueYearB(models.Model):
    year = models.TextField()
    event = models.TextField()
    pro_contest = models.TextField()
    pro_solving = models.TextField()
    algorithm = models.TextField()
    soft_developing = models.TextField()
    research = models.TextField()
    software = models.TextField()
    online_course = models.TextField()

    class Meta:
        managed = False
        db_table = 'main_value_year_b'


class WeightYearA(models.Model):
    parameter = models.TextField()
    n2004 = models.TextField()
    n2005 = models.TextField()
    n2006 = models.TextField()
    n2007 = models.TextField()
    n2008 = models.TextField()
    n2009 = models.TextField()
    n2010 = models.TextField()
    n2011 = models.TextField()
    n2012 = models.TextField()
    n2013 = models.TextField()
    n2014 = models.TextField()
    n2015 = models.TextField()
    n2016 = models.TextField()
    n2017 = models.TextField()
    n2018 = models.TextField()
    n2019 = models.TextField()
    n2020 = models.TextField()
    n2021 = models.TextField()
    n2022 = models.TextField()

    class Meta:
        managed = False
        db_table = 'main_weight_year_a'


class WeightYearB(models.Model):
    parameter = models.TextField()
    n2017 = models.TextField()
    n2018 = models.TextField()
    n2019 = models.TextField()
    n2020 = models.TextField()
    n2021 = models.TextField()
    n2022 = models.TextField()

    class Meta:
        managed = False
        db_table = 'main_weight_year_b'
