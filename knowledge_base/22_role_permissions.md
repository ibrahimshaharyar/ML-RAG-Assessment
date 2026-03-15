# Role Permissions Reference

Detailed breakdown of what each role can and cannot do.

## Permissions Matrix

| Action | Owner | Admin | Member | Viewer |
|--------|-------|-------|--------|--------|
| Submit queries | ✅ | ✅ | ✅ | ❌ |
| View query history (own) | ✅ | ✅ | ✅ | ✅ |
| View query history (all) | ✅ | ✅ | ❌ | ❌ |
| Create API keys | ✅ | ✅ | ✅ | ❌ |
| Delete API keys (own) | ✅ | ✅ | ✅ | ❌ |
| Delete API keys (others) | ✅ | ✅ | ❌ | ❌ |
| Invite team members | ✅ | ✅ | ❌ | ❌ |
| Remove team members | ✅ | ✅ | ❌ | ❌ |
| Change member roles | ✅ | ✅ | ❌ | ❌ |
| View billing | ✅ | ❌ | ❌ | ❌ |
| Update billing | ✅ | ❌ | ❌ | ❌ |
| Configure SSO | ✅ | ✅ | ❌ | ❌ |
| Configure webhooks | ✅ | ✅ | ❌ | ❌ |
| View audit logs | ✅ | ✅ | ❌ | ❌ |
| Export data | ✅ | ✅ | ❌ | ❌ |
| Delete account | ✅ | ❌ | ❌ | ❌ |
| Transfer ownership | ✅ | ❌ | ❌ | ❌ |

## Changing a Member's Role

1. Settings → Team
2. Click three dots (⋯) next to the member
3. Select **"Change Role"**
4. Choose new role and confirm

Role changes take effect immediately.

## Custom Roles (Enterprise Only)

Enterprise customers can create custom roles with fine-grained permissions:
- Go to **Settings → Team → Custom Roles**
- Define exactly which actions are allowed
- Assign custom roles to team members
