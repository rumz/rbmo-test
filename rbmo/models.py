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
    permission = models.ForeignKey(Permissions)

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
    performance_indicator = models.CharField(max_length = 45)
    q1 = models.IntegerField()
    q2 = models.IntegerField()
    q3 = models.IntegerField()
    q4 = models.IntegerField()
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
    total = models.DecimalField(max_digits = 14, decimal_places = 2)
    
    def __unicode__(self):
        return self.activity

    class Meta:
        db_table = 'budget_allocation'
        permissions = (('record_wfp', 'Enter data from WFP'),
                       ('print_report', 'Print Agency WFP Information')
        )

class FundRelUtil(models.Model):
    budgetallocation = models.ForeignKey(BudgetAllocation)
    month = models.IntegerField(choices=MONTHS)
    date_release = models.DateTimeField()
    amount_rel = models.DecimalField(max_digits=12, decimal_places=2)
    amount_util = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'fund_rel_util'


class MPFR(models.Model):
    year = models.IntegerField()
    agency = models.ForeignKey(Agency)
    jan = models.DateTimeField(null=True)
    feb = models.DateTimeField(null=True)
    mar = models.DateTimeField(null=True)
    apr = models.DateTimeField(null=True)
    may = models.DateTimeField(null=True)
    jun = models.DateTimeField(null=True)
    jul = models.DateTimeField(null=True)
    aug = models.DateTimeField(null=True)
    sept = models.DateTimeField(null=True)
    oct = models.DateTimeField(null=True)
    nov = models.DateTimeField(null=True)
    dec = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.agency.name

    class Meta:
        db_table = 'mpfr'

class Requirements(models.Model):
    SUBMISSION_OPTIONS = (('M', 'Monthly' ), ('Q', 'Quarterly'), ('S', 'Semi Annual'), ('Y', 'Yearly'))
    name = models.CharField(max_length=75)
    subs_opt = models.CharField(max_length = 1, choices = SUBMISSION_OPTIONS)
    requirement_for = models.CharField(max_length=5)

    def __unicode__(self):
        return self.name
        
    class Meta:
        db_table = 'requirements'



class MonthlySubmitted(models.Model):
    year = models.IntegerField()
    date_submitted = models.DateTimeField()
    month = models.IntegerField()
    agency = models.ForeignKey(Agency)
    requirement = models.ForeignKey(Requirements)
    
    def __unicode__(self):
        return self.requirement.name

    class Meta:
        db_table = 'monthly_submitted'
        
    
class QuarterSubmitted(models.Model):
    date_submitted = models.DateTimeField()
    quarter = models.IntegerField()
    agency = models.ForeignKey(Agency)
    requirement = models.ForeignKey(Requirements)

    def __unicode__(self):
        return self.requirement.name

    class Meta:
        db_table = 'quarterly_submitted'
     


class YearlySubmitted(models.Model):
    date_submitted = models.DateTimeField()
    year = models.IntegerField()
    agency = models.ForeignKey(Agency)
    requirement = models.ForeignKey(Requirements)

    def __unicode__(self):
        return self.requirement.name

    class Meta:
        db_table = 'yearly_submitted'


