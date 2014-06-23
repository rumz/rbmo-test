from django.db import connection
import time
from datetime import datetime

def has_permission(user_id, action, target):
    cursor = connection.cursor()
    query = '''SELECT * FROM user_permissions WHERE
    id = %s AND action=%s AND target=%s
    '''
    cursor.execute(query, [user_id, action, target])
    return cursor.fetchone()>0

def get_allowed_tabs(user_id):
    tabs=[]
    if has_permission(user_id, 'view', 'user'):
        tabs.append({'tag': 'Users', 'link': '/admin/users'})
    if has_permission(user_id, 'view', 'agency information'):
        tabs.append({'tag': 'Agency/Office', 'link': '/admin/agencies'})
    if has_permission(user_id, 'view', 'transaction history'):
        tabs.append({'tag': 'Transaction History', 'link': ''})
    reports = []
    if has_permission(user_id, 'view', 'status of allotment releases'):
        reports.append({'tag': 'Status of Allotment Releases', 'link': ''})
    if has_permission(user_id, 'view', "monthly reports"):
        reports.append({'tag': 'Monthly Reports', 'link': ''})
    if has_permission(user_id, 'view', "analysis report"):
        reports.append({'tag': 'Analysis Reports', 'link': ''})
    if has_permission(user_id, 'view', "fund utilization"):
        reports.append({'tag': 'Fund Utilization Summarry', 'link': ''})
    if has_permission(user_id, 'view', "quarterly report"):
        reports.append({'tag': 'Quarterly Report', 'link': ''})
    if has_permission(user_id, 'view', 'agencies with complete papers'):
        reports.append({'tag': 'List of Agencies with Complete Documents', 'link': ''})
    tabs.append({'tag':'Reports', 'menus':reports})
    return tabs
            
    
def numify(num):
    if num is None:
        return 0
    else:
        return num
