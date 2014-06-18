from django.db import models
from django.contrib.auth.models import User

MONTHS = ((1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), 
          (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'),
          (10, 'October'), (11, 'November'), (12, 'December'))


class Permissions(models.Model):
    action = models.CharField(max_length=10)
    target = models.CharField(max_length=45)

    def __unicode__(self):
        return self.action + ' ' + self.target
        
    class Meta:
        db_table = 'permissions'


class Groups(models.Model):
    name = models.CharField(max_length=45)

    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = 'groups'

class GroupPermissions(models.Model):
    group = models.ForeignKey(Groups)
    permisssion = models.ForeignKey(Permissions)

    def __unicode__(self):
        return self.group+' '+self.permission

    class Meta:
        db_table = 'group_perm'

class UserGroup(models.Model):
    user = models.OneToOneField(User)
    group = models.ForeignKey(Groups)

    def __unicode__(self):
        return self.user + ' ' + self.group

    class Meta:
        db_table = 'user_group'

class UserActivity(models.Model):
    user = models.ForeignKey(User)
    action = models.CharField(max_length = 100)
    act_date = models.DateTimeField()
    target = models.CharField(max_length = 100)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'user_activity'
    
    
class Sector(models.Model):
    name = models.CharField(max_length = 100)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'sector'


class Agency(models.Model):
    name = models.CharField(max_length = 200)
    sector = models.ForeignKey(Sector)
    email = models.EmailField()
    acces_key = models.CharField(max_length = 150)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'agency'

#its either PS, MOOE, or CO
class Allocation(models.Model):
    name = models.CharField(max_length = 100)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'allocation'


class BudgetAllocation(models.Model):
    year = models.IntegerField()
    activity = models.CharField(max_length = 200)
    agency = models.ForeignKey(Agency)
    allocation = models.ForeignKey(Allocation)
    performane_indicator = models.CharField(max_length = 45)
    q1 = models.DecimalField(max_digits = 12, decimal_places = 2)
    q2 = models.DecimalField(max_digits = 12, decimal_places = 2)
    q3 = models.DecimalField(max_digits = 12, decimal_places = 2)
    q4 = models.DecimalField(max_digits = 12, decimal_places = 2)
    jan = models.DecimalField(max_digits = 12, decimal_places = 2)
    feb = models.DecimalField(max_digits = 12, decimal_places = 2)
    mar = models.DecimalField(max_digits = 12, decimal_places = 2)
    apr = models.DecimalField(max_digits = 12, decimal_places = 2)
    may = models.DecimalField(max_digits = 12, decimal_places = 2)
    jun = models.DecimalField(max_digits = 12, decimal_places = 2)
    jul= models.DecimalField(max_digits = 12, decimal_places = 2)
    aug = models.DecimalField(max_digits = 12, decimal_places = 2)
    sept = models.DecimalField(max_digits = 12, decimal_places = 2)
    oct = models.DecimalField(max_digits = 12, decimal_places = 2)
    nov = models.DecimalField(max_digits = 12, decimal_places = 2)
    dec = models.DecimalField(max_digits = 12, decimal_places = 2)
    
    def __unicode__(self):
        return self.activity

    class Meta:
        db_table = 'budget_allocation'
        permissions = (('record_wfp', 'Enter data from WFP'),
                       ('print_report', 'Print Agency WFP Information')
        )


class AllotmentReleases(models.Model):
    agency = models.ForeignKey(Agency)
    month = models.CharField(max_length = 3, choices = MONTHS)
    amount = models.DecimalField(max_digits = 12, decimal_places = 2)
    allocation = models.ForeignKey(Allocation)
    date_release = models.DateTimeField()

    def __unicode__(self):
        self.amount
        
    class Meta:
        db_table = 'allotment_releases'

class Documents(models.Model):
    doc_name = models.CharField(max_length=100)
    
    def __unicode__():
        return self.doc_name

    class Meta:
        db_table = 'documents'
        

class DocsSubmitted(models.Model):
    date_submitted = models.DateTimeField()
    agency = models.ForeignKey(Agency)
    doc = models.ForeignKey(Documents)

    def __unicode__(self):
        return self.doc.doc_name
        
    class Meta:
        db_table = 'docs_submitted'



