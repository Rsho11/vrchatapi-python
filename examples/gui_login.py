import tkinter as tk
from tkinter import messagebox

import vrchatapi
from vrchatapi.api import authentication_api
from vrchatapi.exceptions import UnauthorizedException, ApiException
from vrchatapi.models.two_factor_auth_code import TwoFactorAuthCode
from vrchatapi.models.two_factor_email_code import TwoFactorEmailCode


def login():
    username = entry_username.get()
    password = entry_password.get()

    config = vrchatapi.Configuration(username=username, password=password)
    try:
        with vrchatapi.ApiClient(config) as api_client:
            api_client.user_agent = "GuiExample/0.0.1"
            auth_api = authentication_api.AuthenticationApi(api_client)
            try:
                current_user = auth_api.get_current_user()
            except UnauthorizedException as e:
                if e.status == 200:
                    code = entry_2fa.get()
                    if "Email 2 Factor Authentication" in e.reason:
                        auth_api.verify2_fa_email_code(
                            two_factor_email_code=TwoFactorEmailCode(code)
                        )
                    elif "2 Factor Authentication" in e.reason:
                        auth_api.verify2_fa(
                            two_factor_auth_code=TwoFactorAuthCode(code)
                        )
                    current_user = auth_api.get_current_user()
                else:
                    raise
            messagebox.showinfo("Success", f"Logged in as: {current_user.display_name}")
    except (UnauthorizedException, ApiException) as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("VRChat Login")

# Username field
tk.Label(root, text="Username").grid(row=0, column=0, padx=5, pady=5)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=5, pady=5)

# Password field
tk.Label(root, text="Password").grid(row=1, column=0, padx=5, pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=5, pady=5)

# 2FA field
tk.Label(root, text="2FA Code (if required)").grid(row=2, column=0, padx=5, pady=5)
entry_2fa = tk.Entry(root)
entry_2fa.grid(row=2, column=1, padx=5, pady=5)

# Login button
login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
