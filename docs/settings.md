# Settings

Default settings are provided with `django-tenants-url`.

## Table of Contents

---

- [Settings](#settings)
    - [Table of Contents](#table-of-contents)
    - [Defaults](#defaults)
    - [HEADER_NAME](#header_name)
    - [TENANT_USER_MODEL](#tenant_user_model)
    - [Example](#example)

---

## Defaults

```python
# settings.py
...

DTU_TENANT_NAME = "Public"
DTU_TENANT_SCHEMA = "public"
DTU_DOMAIN_NAME = "localhost"
DTU_PAID_UNTIL = "2100-12-31"
DTU_ON_TRIAL = False
DTU_HEADER_NAME = "HTTP_X_REQUEST_ID"
DTU_AUTO_CREATE_SCHEMA = True
DTU_AUTO_DROP_SCHEMA = False
DTU_TENANT_USER_MODEL = None

```

- `DTU_TENANT_NAME` - Default tenant name for the public schema.
- `DTU_TENANT_SCHEMA` - Default schema name for the public.
- `DTU_DOMAIN_NAME` - Public schema defaults to localhost (production server, for example).
- `DTU_PAID_UNTIL` - Default paid_until date. The package can be used for subscription models.
- `DTU_ON_TRIAL` - Defaults to `false`. With `paid_until` this flag can be activated
   for subscription models.
- `DTU_HEADER_NAME` - Name of the header to be sent with the calls and route to the schema.
- `DTU_AUTO_CREATE_SCHEMA` - When disabled, a tenant schema is not created on `save()`.
- `DTU_AUTO_DROP_SCHEMA` - If disabled, a tenant when removed the schema is not delated on `delete()`.
- `DTU_TENANT_USER_MODEL` - Required field pointing to the model mapping a tenant with a user.

## HEADER_NAME

Probably the one of the most important configurations.
The `HEADER_NAME` is what will be used to be read/sent from the requests hitting the back-end server
and map the current user with a schema.

This field can be overritten to any value of choice **but be careful when changing**.

## TENANT_USER_MODEL

This field is **crucial** to be updated in the settings ([see installation instructions](./index.md)).

The model will facilitate the mapping between a tenant and a user.
The [middleware](./middleware.md) doesn't lookup at this model but it's specially useful
if the [permissions](./permissions.md) are used.

The [middleware](./middleware.md) looks at the [Tenant model](./models.md#tenantmixin).

## Example

When updating the settings, specially `HEADER_NAME` that can be done via `settings.py`.

```python
# settings.py

...

DTU_HEADER_NAME = `HTTP_X_UNIQUE_ID"

```

```cURL
curl --header "X_UNIQUE_ID: <UNIQUE_UUID>" -v http://localhost:8000/my-view
```
