app_name = "lms_custom"
app_title = "Lms Custom"
app_publisher = "Admin"
app_description = "LMS Custom Injector"
app_email = "admin@example.com"
app_license = "mit"

# These run whenever standard bench commands trigger
after_install = "lms_custom.setup_lms.inject_lms_customizations"
after_migrate = "lms_custom.setup_lms.inject_lms_customizations"
