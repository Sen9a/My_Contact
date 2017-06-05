from floppyforms import ClearableFileInput
from django.utils.safestring import mark_safe


class ImageFieldWidget(ClearableFileInput):

    class Media:
        css = {
               'all': ('image_upload/css/fileinput.min.css', 'image_upload/css/few_style.css')
              }
        js = ["image_upload/js/fileinput.min.js", "image_upload/js/image_script.js"]

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        rendered_widget = super(ImageFieldWidget, self).render(name, value, final_attrs)

        return mark_safe("""
            <span>
                <div id="kv-avatar-errors-1" class="center-block" style="width:500px;display:none"></div>
                    <div class="kv-avatar center-block" style="width:500px">
                        <label for="id_image">Avatar :</label>
                        <input id="id_image" name="image" type="file" class="file-loading">
                    </div>
            </span>
           """)
