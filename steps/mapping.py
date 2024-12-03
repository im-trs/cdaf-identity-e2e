from page_objects.confused_page import ConfusedPage

PAGE_OBJECTS = {
    'confused_page': ConfusedPage,

    # add more page objects here as needed
}


def get_page_object(page_name):
    if page_name not in PAGE_OBJECTS:
        raise ValueError(f"Invalid page_name: {page_name}")

    page_object_class = PAGE_OBJECTS[page_name]
    return page_object_class()


def get_element(page_name, element_name, text=""):
    el = None
    po = get_page_object(page_name)
    el = po.get_element(element_name, text)
    return el

