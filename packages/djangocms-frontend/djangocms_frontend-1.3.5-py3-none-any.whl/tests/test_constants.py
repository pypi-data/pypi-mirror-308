from django.test import TestCase

from djangocms_frontend.settings import (
    ALIGN_CHOICES,
    COLOR_STYLE_CHOICES,
    DEVICE_CHOICES,
    DEVICE_SIZES,
    TAG_CHOICES,
)


class B5ConstantsTestCase(TestCase):
    # make sure to update the documentation
    # when changing any values in these

    def test_constants(self):
        self.assertEqual(
            DEVICE_CHOICES,
            (
                ("xs", "Extra small"),  # default <576px
                ("sm", "Small"),  # default ≥576px
                ("md", "Medium"),  # default ≥768px
                ("lg", "Large"),  # default ≥992px
                ("xl", "Extra large"),  # default ≥1200px
                ("xxl", "Extra-extra large"),
            ),
        )
        self.assertEqual(DEVICE_SIZES, ("xs", "sm", "md", "lg", "xl", "xxl"))
        self.assertEqual(
            TAG_CHOICES,
            (
                ("div", "div"),
                ("section", "section"),
                ("article", "article"),
                ("header", "header"),
                ("footer", "footer"),
                ("aside", "aside"),
            ),
        )
        self.assertEqual(
            COLOR_STYLE_CHOICES,
            (
                ("primary", "Primary"),
                ("secondary", "Secondary"),
                ("success", "Success"),
                ("danger", "Danger"),
                ("warning", "Warning"),
                ("info", "Info"),
                ("light", "Light"),
                ("dark", "Dark"),
            ),
        )
        self.assertEqual(
            ALIGN_CHOICES,
            (
                ("start", "Left"),
                ("center", "Center"),
                ("end", "Right"),
            ),
        )
