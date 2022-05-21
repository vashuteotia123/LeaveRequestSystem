from genericpath import exists
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Leave
import json


@csrf_exempt
def login(request):
    """
    Login function for the user(employee, admin). It checks if the user exists in the database and if the password is correct. 
    """
    if request.method == "GET":
        if  'user' in request.session:
            return JsonResponse({"error": "Already logedin."})

        email = request.GET.get("email")
        password = request.GET.get("password")

        if email is None or password is None:
            return JsonResponse({"error": "Missing email or password."})

        try:
            user = User.objects.get(email = email)
        except:
            user = None

        if user is None:
            return JsonResponse({"error": "No user found with given email address!"})
        
        if user.password != password:
            return JsonResponse({"error": "Wrong credentials, Please try again!"})

        request.session['user'] = email
        request.session['user_type']= user.user_type

        return JsonResponse({"success": True, "message": "User logedin successfully."})
    else:
        return JsonResponse({"error": "400", "message": "Bad Request"})

@csrf_exempt
def logout(request):
    """"
    Logout function for the user(employee, admin). It removes the user from the session.
    """
    try:
        del request.session['user']
        del request.session['user_type']
        return JsonResponse({"message": "Logout Succesfully!"})
    except:
        pass
    return JsonResponse({"message": "No login session found."})

@csrf_exempt
def createLeave(request):
    """
    Create leave request function for the employee. It checks if the user is logged in and if the leave request is valid.
    """
    if request.method == "POST":
        if 'user' not in request.session:
            return JsonResponse({"error": "Please login first."})

        user = request.session['user']
        user_type = request.session['user_type']
        if user_type != "employee":
            return JsonResponse({"error": "Only employee can create leave request."})

        try:
            user = User.objects.get(email = user)
        except:
            user = None

        if user is None:
            return JsonResponse({"error": "No user found with given email address!"})

        data = json.loads(request.body)
        start_date = data["start_date"]
        end_date = data["end_date"]        
        reason = data["reason"]
        leave_type = data["leave_type"]

        print(start_date, end_date, reason, leave_type)

        if not start_date or not end_date or not reason or not leave_type:
            return JsonResponse({"error": "Please fill all the fields."})

        if not re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', start_date) or not re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', end_date):
            return JsonResponse({"error": "Please enter valid date."})

        if start_date > end_date:
            return JsonResponse({"error": "Start date should be less than end date."})

        if leave_type not in ["casual", "sick", "earned"]:
            return JsonResponse({"error": "Please enter valid leave type."})

        try:
            leave = Leave.objects.create(user = user, leave_from = start_date, leave_to = end_date, leave_reason = reason, leave_type = leave_type, leave_status = "pending")
        except:
            return JsonResponse({"error": "Something went wrong. Please try again."})

        return JsonResponse({"success": True, "message": "Leave request created successfully."})
    else:
        return JsonResponse({"error": "400", "message": "Bad Request"})

@csrf_exempt
def showLeaveRequests(request):
    """
    Show all leave requests function for the admin. It checks if the user is logged in and if the user is admin.
    """
    if request.method == "GET":
        if 'user' not in request.session:
            return JsonResponse({"error": "Please login first."})

        user = request.session['user']
        user_type = request.session['user_type']
        if user_type != "admin":
            return JsonResponse({"error": "Only admin can view leave request."})

        try:
            user = User.objects.get(email = user)
        except:
            user = None

        if user is None:
            return JsonResponse({"error": "No user found with given email address!"})

        try:
            leaves = Leave.objects.filter(leave_status = "pending").all()
        except:
            return JsonResponse({"error": "Something went wrong. Please try again."})

        if len(leaves) == 0:
            return JsonResponse({"error": "No leave requests found."})

        data = []
        for leave in leaves:
            data.append({"leave_id": leave.id,"user": leave.user.name, "leave_type": leave.leave_type, "leave_from": leave.leave_from, "leave_to": leave.leave_to, "leave_reason": leave.leave_reason, "leave_status": leave.leave_status})

        return JsonResponse({"success": True, "data": data})
    else:
        return JsonResponse({"error": "400", "message": "Bad Request"})

@csrf_exempt
def approveLeave(request):
    """
    Approve leave request function for the admin. It checks if the user is logged in and if the user is admin.
    """
    if request.method == "POST":
        if 'user' not in request.session:
            return JsonResponse({"error": "Please login first."})

        user = request.session['user']
        user_type = request.session['user_type']
        if user_type != "admin":
            return JsonResponse({"error": "Only admin can approve leave request."})

        try:
            user = User.objects.get(email = user)
        except:
            user = None

        if user is None:
            return JsonResponse({"error": "No user found with given email address!"})

        data = json.loads(request.body)
        if 'leave_id' not in data:
            return JsonResponse({"error": "Please enter leave id."})
        leave_id = data["leave_id"]

        try:
            leave = Leave.objects.get(id = leave_id)
        except:
            return JsonResponse({"error": "Leave request not found."})

        if leave.leave_status != "pending":
            return JsonResponse({"error": "Leave request already approved or rejected."})

        leave.leave_status = "approved"
        leave.save()

        return JsonResponse({"success": True, "message": "Leave request approved successfully."})
    else:
        return JsonResponse({"error": "400", "message": "Bad Request"})

@csrf_exempt
def rejectLeave(request):
    """
    Reject leave request function for the admin. It checks if the user is logged in and if the user is admin.
    """
    if request.method == "POST":
        if 'user' not in request.session:
            return JsonResponse({"error": "Please login first."})

        user = request.session['user']
        user_type = request.session['user_type']
        if user_type != "admin":
            return JsonResponse({"error": "Only admin can reject leave request."})

        try:
            user = User.objects.get(email = user)
        except:
            user = None

        if user is None:
            return JsonResponse({"error": "No user found with given email address!"})

        data = json.loads(request.body)
        if 'leave_id' not in data:
            return JsonResponse({"error": "Please enter leave id."})
        leave_id = data["leave_id"]

        try:
            leave = Leave.objects.get(id = leave_id)
        except:
            return JsonResponse({"error": "Leave request not found."})

        if leave.leave_status != "pending":
            return JsonResponse({"error": "Leave request already approved or rejected."})

        leave.leave_status = "rejected"
        leave.save()

        return JsonResponse({"success": True, "message": "Leave request rejected successfully."})
    else:
        return JsonResponse({"error": "400", "message": "Bad Request"})

@csrf_exempt
def showEmployeeLeaveRequests(request):
    """
    Show all leave requests function for the employee. It checks if the user is logged in and if the user is employee.
    """
    if request.method == "GET":
        if 'user' not in request.session:
            return JsonResponse({"error": "Please login first."})

        user = request.session['user']
        user_type = request.session['user_type']
        if user_type != "employee":
            return JsonResponse({"error": "Only employee can view leave request."})

        try:
            user = User.objects.get(email = user)
        except:
            user = None

        if user is None:
            return JsonResponse({"error": "No user found with given email address!"})

        try:
            leaves = Leave.objects.filter(user = user).all()
        except:
            return JsonResponse({"error": "Something went wrong. Please try again."})

        if len(leaves) == 0:
            return JsonResponse({"error": "No leave requests found."})

        data = []
        for leave in leaves:
            data.append({"leave_id": leave.id,"user": leave.user.name, "leave_type": leave.leave_type, "leave_from": leave.leave_from, "leave_to": leave.leave_to, "leave_reason": leave.leave_reason, "leave_status": leave.leave_status})

        return JsonResponse({"success": True, "data": data})
    else:
        return JsonResponse({"error": "400", "message": "Bad Request"})
