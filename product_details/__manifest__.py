# Copyright 2016-2017 Stanislav Krotov <https://www.it-projects.info/team/ufaks>
# Copyright 2016-2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Product Details""",
    "summary": """Allows to add links with describes of products.""",
    "category": "Extra Tools",
    "images": ["static/description/icon.png"],
    "version": "11.0.1.0.0",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "website": "https://it-projects.info",
    "license": "Other OSI approved licence",  # MIT
    # "price": 9.00,
    # "currency": "EUR",
    "depends": ["product", "base_details"],
    "external_dependencies": {"python": [], "bin": []},
    "data": ["views/product_detail.xml"],
    "qweb": [],
    "demo": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "auto_install": False,
    "installable": True,
}
