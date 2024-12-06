class TestClassA():
    """Test Class A
    some summary to ensure class parameters and constructor parametes are put in two field lists 

    """
    def __init__(self) -> None:
        pass
    
    def method_param_docstring_contain_angle_bracket(self):
        """Test Method with param docstring containing angle bracket
        
        :param str paramE: Test Param E, link https://<variable>.foo.net/boo
        """
        pass

    def method_docstring_contain_angle_bracket(self):
        """Test Method with param docstring containing angle bracket: link https://<variable>.foo.net/boo
        """
        pass