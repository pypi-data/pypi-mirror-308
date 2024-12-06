from pymdgen import doc_class, doc_func, doc_module


def func_a(a, b=None, **kwargs):
    """this is test function a"""
    return


class class_a:
    """this is test class a"""

    def method_a(self, a, b=None, **kwargs):
        """this is test method a"""
        return


def test_doc_func(expected_docs_doc_func_md):
    output = doc_func("func_a", func_a)
    # write_expected("doc_func.md", output)
    assert "\n".join(output) == expected_docs_doc_func_md


def test_doc_class(expected_docs_doc_class_md):
    output = doc_class("class_a", class_a)
    # write_expected("doc_class.md", output)
    assert "\n".join(output) == expected_docs_doc_class_md


def test_doc_module(expected_docs_list):
    output = doc_module("pymdgen.test_module", section_level=3)
    # write_expected("md", output)
    assert output == expected_docs_list
