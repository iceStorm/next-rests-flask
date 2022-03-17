from flask_principal import Principal, Permission, RoleNeed, UserNeed, identity_loaded, Need, partial, Identity, AnonymousIdentity
principals = Principal()

# declaring permission Needs
admin_permission = Permission(RoleNeed('admin'))
manager_permission = Permission(RoleNeed('manager'), RoleNeed('admin'))
