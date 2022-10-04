

def detect_user(user):
    if user.role == 1:
        redirect_url = 'VendorDashboard'
        return redirect_url
    elif user.role == 2:
        redirect_url = 'CustomerDashboard'
        return redirect_url
    elif user.role is None and user.is_superadmin:
        redirect_url = '/admin'
        return redirect_url
