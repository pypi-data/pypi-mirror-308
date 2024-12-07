# league-shop-base

Base models and admin for league-shop

## Installation

You can install the package via pip:

```
pip install league-shop-base
```

Add `lsb` to your INSTALLED_APPS.

```
    INSTALLED_APPS = [
        ...
        'lsb',
    ]
```

## To specify top sold skin values parser, add the following settings:

```
LSB_SETTINGS = {
    'top_sold_skin_values': {
        'func': <dotted_module_string_path>,
        'args': <args>,
        'kwargs': <kwargs>
    }
}
For example:

LSB_SETTINGS = {
    'top_sold_skin_values': {
        'func': 'lsb.utils.skins.get_top_sold_skin_values',
        'args': [0, 150],
        'kwargs': {}
    }
}

```
