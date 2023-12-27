def page_title_data(name: str, path_sequence: list) -> dict:
    """
    Generates data for a page title, including the name and path sequence.

    Parameters:
    - name (str): The name of the page title.
    - path_sequence (list): The sequence of the path to the current page.
      Each element in the list can be a string representing a path segment or a dictionary
      containing both the path segment and its URL.

    Returns:
    dict: Page title data dictionary with 'name' and 'path_sequence' keys.
    """
    return dict(
        name=name,
        path_sequence=path_sequence
    )
