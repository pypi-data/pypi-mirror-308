import pytest

from sphinx.testing import restructuredtext
from sphinx.io import SphinxStandaloneReader
from sphinx import addnodes
from translator import translator

from .utils.test_utils import prepare_app_envs,load_rst_transform_to_doctree

@pytest.mark.sphinx('yaml', testroot='translator-method')
def test_paramDocstringContainingAngleBrackets_checkEncoded(app):
    # Test data definition
    objectToGenXml = 'code_with_docstring.TestClassA.method_param_docstring_contain_angle_bracket'
    objectToGenXmlType = 'function'

    # Arrange
    prepare_app_envs(app, objectToGenXml)
    doctree = load_rst_transform_to_doctree(app, objectToGenXmlType, objectToGenXml)
    
    # Act
    translator(app, '', doctree)

    # Assert
    summary = app.env.docfx_info_field_data[objectToGenXml]['parameters'][0]['description']
    assert (summary == '**paramE** (<xref:str>) -- Test Param E, link [https:/](https:/)/&lt;variable&gt;.foo.net/boo')

@pytest.mark.sphinx('yaml', testroot='translator-method')
def test_docstringContainingAngleBrackets_checkEncoded(app):
    # Test data definition
    objectToGenXml = 'code_with_docstring.TestClassA.method_docstring_contain_angle_bracket'
    objectToGenXmlType = 'function'

    # Arrange
    prepare_app_envs(app, objectToGenXml)
    doctree = load_rst_transform_to_doctree(app, objectToGenXmlType, objectToGenXml)
    
    # Act
    translator(app, '', doctree)

    # Assert
    summary = app.env.docfx_info_field_data[objectToGenXml]['summary']
    assert summary == 'Test Method with param docstring containing angle bracket: link [https:/](https:/)/&lt;variable&gt;.foo.net/boo'