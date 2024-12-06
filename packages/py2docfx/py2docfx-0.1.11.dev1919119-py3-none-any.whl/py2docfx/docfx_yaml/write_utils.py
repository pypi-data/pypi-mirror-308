def is_inline_text_children_of_versionmodified(node):
    if hasattr(node, 'parent') and node.parent is not None:
        if hasattr(node.parent, 'parent') and node.parent.parent is not None:
            if node.parent.parent.tagname == 'versionmodified':
                return True
    return False

def replace_special_unicode(text):
    text = text.replace('\u201c', '"')
    text = text.replace('\u201d', '"')
    text = text.replace('\u2018', "'")
    text = text.replace('\u2019', "'")
    text = text.replace('\u2026', "...")
    return text

def replace_angle_brackets_with_html_entities(text):
    return text.replace('<', '&lt;').replace('>', '&gt;')