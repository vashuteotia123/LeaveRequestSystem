from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    user_type = models.CharField(choices=[('admin', 'Admin'), ('employee', 'Employee')], max_length=10)

    def __str__(self):
        return self.name


class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(choices=[('casual', 'Casual'), ('sick', 'Sick'), ('earned', 'Earned')], max_length=10)
    leave_from = models.DateField()
    leave_to = models.DateField()
    leave_reason = models.TextField()
    leave_status = models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], max_length=10)

    def __str__(self):
        return self.user.name +  ' ' + self.leave_type + ' ' + str(self.leave_from) + ' -- ' + str(self.leave_to)