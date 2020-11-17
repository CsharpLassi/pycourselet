from .courselet_element import CourseletElement


class TableColumnBreakElement(CourseletElement):
    def __init__(self, element_id: str):
        super(TableColumnBreakElement, self).__init__(element_id,
                                                      element_type='table_column_break')


class TableRowBreakElement(CourseletElement):
    def __init__(self, element_id: str):
        super(TableRowBreakElement, self).__init__(element_id,
                                                   element_type='table_row_break')
