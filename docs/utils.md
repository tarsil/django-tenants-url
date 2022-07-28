# Utils

## Table of Contents

---

- [Utils](#utils)
    - [Table of Contents](#table-of-contents)
    - [Functions](#functions)

---

## Functions

1. `get_tenant_user_model()` - Return the Tenant User model set 
   in the settings `DTU_TENANT_USER_MODEL`.
2. `get_active_user_tenant()` - Return the active tenant of a given `auth.User`.
3. `get_user_tenants()` - Lists the tenants associated with a user.
4. `get_tenants()` - Returns a list of all tenants.

```python
from django_tenants_url.utils import (
    get_tenant_user_model,
    get_active_user_tenant,
    get_user_tenants,
    get_tenants
)
```
