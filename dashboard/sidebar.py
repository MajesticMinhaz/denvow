def create_section(id: int, name: str, url: str) -> dict:
    """
    Helper function to create a section dictionary.

    Parameters:
    - id (int): The ID of the section.
    - name (str): The name of the section.
    - url (str): The URL associated with the section.

    Returns:
    dict: Section dictionary.
    """
    return {'id': id, 'name': name, 'url': url}


def create_menu_item(id: int, name: str, icon: str, url: str, sections: list = None) -> dict:
    """
    Helper function to create a menu item dictionary.

    Parameters:
    - id (int): The unique identifier for the menu item.
    - name (str): The name of the menu item.
    - icon (str): The icon associated with the menu item.
    - url (str): The URL associated with the menu item.
    - sections (List[Dict[str, str]]): Optional list of sections under the menu item.

    Returns:
    dict: Menu item dictionary.
    """
    menu_item = {'id': id, 'name': name, 'icon': icon, 'url': url}
    if sections:
        menu_item['sections'] = sections
    return menu_item


def sidebar_data(section_active_id: int = 1, sub_section_active_id: int = 1) -> dict:
    """
    Generates sidebar data with optional highlighting of the active menu item.

    Parameters:
    - section_active_id (int): The ID of the active menu item. Default is 1.
    - sub section_active_id (int): The ID of the active sub item. Default is 1.

    Returns:
    dict: Sidebar data dictionary.
    """
    data = dict(
        general=[
            create_menu_item(
                id=1, name='Dashboard', icon='bi bi-grid', url='dashboard'
            ),

            create_menu_item(
                id=2, name='Sales', icon='bi bi-speedometer2', url=None, sections=[
                    create_section(id=1, name='POS', url='dashboard'),
                    create_section(id=2, name='Orders', url='dashboard'),

                ]
            ),

            create_menu_item(
                id=3, name='Product Management', icon='bi bi-cart3', url=None, sections=[
                    create_section(id=1, name='Categories', url='categories'),
                    create_section(id=2, name='Sub Categories', url='sub_categories'),
                    create_section(id=3, name='Products', url='products'),
                ]
            ),

            create_menu_item(
                id=4, name='Inventory Management', icon='bi bi-shield-plus', url='dashboard'
            ),

            create_menu_item(
                id=5, name='People Management', icon='bi bi-people', url=None, sections=[
                    create_section(id=1, name='Customer', url='dashboard'),
                    create_section(id=2, name='Suplier', url='dashboard'),

                ]
            ),

            create_menu_item(
                id=6, name='Wallet', icon='bi bi-wallet2', url='dashboard'
            ),

            create_menu_item(
                id=7, name='Subscription', icon='bi bi-credit-card', url='dashboard'
            ),

            create_menu_item(
                id=8, name='Reports', icon='bi bi-journal-medical', url=None, sections=[
                    create_section(id=1, name='Sales Report', url='dashboard'),
                    create_section(id=2, name='Customer Report', url='dashboard'),
                    create_section(id=3, name='Dues Report', url='dashboard'),
                    create_section(id=4, name='Stock Report', url='dashboard'),
                ]
            ),
        ],
        
        pages=[
            create_menu_item(
                id=9, name='Profile', icon='bi bi-person', url='profile'
            ),

            create_menu_item(
                id=10, name='Settings', icon='bi bi-gear', url=None, sections=[
                    create_section(id=1, name='Change Password', url='account_change_password')
                ]
            ),
        ]
    )

    for menu_item in data['general'] + data['pages']:
        menu_item['collapsed'] = menu_item['id'] != section_active_id

        if not menu_item["collapsed"]:
            if menu_item.get('sections'):

                for section in menu_item.get('sections'):
                    section["active"] = section['id'] == sub_section_active_id 
    
    return data
