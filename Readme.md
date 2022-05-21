# Leave Request System.
<hr>

## Credentials for Employee and admin.

### Employee Credentials: 
```
{
    "email":"vashuteotia123@gmail.com"
    "password":"vishal"
}
```

### Admin Credentials:
```
{
    "email":"vishal@gmail.com"
    "password":"vishal"
}
```

### Admin Panel login credentials:
```
Username: vishal
Password: vishal
```

### Api calls available.

- Employee Login:
`http://127.0.0.1:8000/login?email=vashuteotia123@gmail.com&password=vishal`  
Request Method: GET  

- Admin Login:
`http://127.0.0.1:8000/login?email=vishal@gmail.com&password=vishal`  
Request Method: GET  

- Logout: `http://127.0.0.1:8000/logout`  
Request Method: GET

- Create Leave Request: `http://127.0.0.1:8000/createLeave`
Request Method: POST   
Request Body (JSON):
    ```
    {
        "start_date": "2022-05-21",
        "end_date": "2022-05-23",
        "reason": "doctor",
        "leave_type": "sick"
    }
    ```

- Show all pending leave request to admin: `http://127.0.0.1:8000/showLeaveRequests`
Request Method: GET

- Approve leave (Admin): `http://127.0.0.1:8000/approveLeave`
Request Method: POST
Request Body (JSON):
    ```
    {
        "leave_id": 1
    }
    ```

- Discard Leave Request (Admin): `http://127.0.0.1:8000/rejectLeave`
Request Method: POST
Request Body (JSON):
    ```
    {
        "leave_id": 2
    }
    ```

- Show all leave requests (Employee): `http://127.0.0.1:8000/showEmployeeLeaveRequests`
Request Method: GET
