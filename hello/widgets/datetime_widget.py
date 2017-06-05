from floppyforms import DateInput
from django.utils.safestring import mark_safe


class DateWidget(DateInput):

    class Media:
        css = {
               'all': ('datepicker/css/jquery.datetimepicker.css', 'bootstrap/css/bootstrap.min.css')
              }
        js = ["datepicker/js/jquery.datetimepicker.full.min.js", "datepicker/js/datetime.js"]

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        rendered_widget = super(DateWidget, self).render(name, value, final_attrs)

        return mark_safe("""
                         <p>
                           <label  for="id_date">Date:</label>
                           <input id="id_date" maxlength="200" name="date" type="text" />
                         </p>
                        """)
