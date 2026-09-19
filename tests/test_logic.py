"""Unit tests for the analyzer business-logic layer."""

import math

from src.analyzer import logic


class FakeTable:
    """Minimal table double for the logic functions that manipulate tables."""

    def __init__(self, columns, rows):
        self.columns = list(columns)
        self.rows = [list(row) for row in rows]

    def copy(self):
        return FakeTable(self.columns, self.rows)

    def dropna(self):
        return FakeTable(
            self.columns,
            [row for row in self.rows if all(value is not None for value in row)],
        )

    def fillna(self, value):
        return FakeTable(
            self.columns,
            [[value if item is None else item for item in row] for row in self.rows],
        )


def test_gross_amount_normal_and_zero_values():
    """يثبت حساب الإجمالي في الحالة العادية وعند وجود صفر."""
    assert logic.gross_amount(4, 12.5) == 50
    assert logic.gross_amount(0, 12.5) == 0


def test_discount_amount_normal_and_missing_like_zero_values():
    """يثبت حساب الخصم وقبول نسبة صفرية كقيمة حدية."""
    assert logic.discount_amount(200, 0.1) == 20
    assert logic.discount_amount(200, 0) == 0


def test_tax_amount_default_and_zero_rate():
    """يثبت استخدام الضريبة الافتراضية وإمكانية تعطيلها بمعدل صفر."""
    assert logic.tax_amount(200) == 10
    assert logic.tax_amount(200, 0) == 0


def test_region_code_known_unknown_and_missing_values():
    """يثبت تحويل المناطق المعروفة وإرجاع صفر للمجهولة والمفقودة."""
    assert logic.region_code("EU") == 2
    assert logic.region_code("") == 0
    assert logic.region_code(None) == 0


def test_map_label_known_and_unknown_values():
    """يثبت تحويل التصنيفات المعروفة وإرجاع unknown للقيم الحدية وغير المعروفة."""
    assert logic.map_label(2) == "high"
    assert logic.map_label(0) == "low"
    assert logic.map_label(None) == "unknown"


def test_handle_missing_values_drops_rows_with_missing_values():
    """يثبت حذف الصفوف التي تحتوي قيمة مفقودة مع إبقاء الصفوف المكتملة."""
    result = logic.handle_missing_values(FakeTable(["a"], [[1], [None], []]))
    assert result.rows == [[1], []]


def test_normalize_columns_normal_empty_and_duplicate_cases():
    """يثبت تطبيع أسماء الأعمدة، الحفاظ على الجدول الفارغ، ورفض التكرار المتوقع."""
    result = logic.normalize_columns(FakeTable(["Customer Name", ""], []))
    assert result.columns == ["customer_name", ""]

    try:
        logic.normalize_columns(FakeTable(["A-B", "A B"], []))
        assert False, "Expected ValueError for duplicate normalized columns"
    except ValueError:
        pass


def test_cell_as_number_normal_zero_missing_and_invalid_values():
    """يثبت تحويل الأرقام والتعامل مع الصفر والقيمة المفقودة والخطأ كقيمة افتراضية."""
    row = ["12.5", 0, None, "not-a-number"]
    assert logic.cell_as_number(row, 0) == 12.5
    assert logic.cell_as_number(row, 1) == 0
    assert logic.cell_as_number(row, 2, 7.0) == 7.0
    assert logic.cell_as_number(row, 3, 7.0) == 7.0
    assert logic.cell_as_number(row, 99, 7.0) == 7.0


def test_outlier_threshold_normal_and_empty_error():
    """يثبت حساب المتوسط والانحراف للحالة العادية ورفع خطأ للقائمة الفارغة."""
    mean, deviation = logic.outlier_threshold([1, 2, 3])
    assert mean == 2
    assert math.isclose(deviation, math.sqrt(2 / 3))

    try:
        logic.outlier_threshold([])
        assert False, "Expected ZeroDivisionError for empty values"
    except ZeroDivisionError:
        pass


def test_is_outlier_normal_zero_deviation_and_boundary():
    """يثبت كشف القيمة الشاذة، وعدم اعتبارها شاذة عند انحراف صفر أو على الحد."""
    assert logic.is_outlier(10, 0, 1, threshold=2) is True
    assert logic.is_outlier(2, 0, 1, threshold=2) is False
    assert logic.is_outlier(10, 10, 0) is False


def test_enrich_table_normal_empty_and_duplicate_error():
    """يثبت تطبيق التطبيع وحذف القيم المفقودة مع دعم الجدول الفارغ ورفض التكرار."""
    result = logic.enrich_table(FakeTable(["A Column"], [[1], [None]]))
    assert result.columns == ["a_column"]
    assert result.rows == [[1]]

    empty_result = logic.enrich_table(FakeTable([], []))
    assert empty_result.columns == []
    assert empty_result.rows == []

    try:
        logic.enrich_table(FakeTable(["A-B", "A B"], []))
        assert False, "Expected ValueError for duplicate normalized columns"
    except ValueError:
        pass
