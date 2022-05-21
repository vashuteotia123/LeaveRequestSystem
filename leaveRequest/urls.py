from django.urls import path
from .views import *

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('createLeave', createLeave, name='createLeave'),
    path("showLeaveRequests", showLeaveRequests, name="showLeaveRequests"),
    path("approveLeave", approveLeave, name="approveLeave"),
    path("rejectLeave", rejectLeave, name="rejectLeave"),
    path("showEmployeeLeaveRequests", showEmployeeLeaveRequests, name="showEmployeeLeaveRequests"),
]