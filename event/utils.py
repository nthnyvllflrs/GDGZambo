import random, string

from django.utils.text import slugify

DONT_USE = ['create', 'speaker', 'upcoming', 'past', 'info', 'draft-save', 'rsvp', 'sponsor', 'statistics']
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
	if new_slug is not None:
		slug = new_slug
	else:
		try: slug = slugify(instance.title)
		except: slug = slugify(instance.name)

	if slug in DONT_USE:
		new_slug = "{slug}-{randstr}".format(slug=slug, randstr=random_string_generator(size=4))
		return unique_slug_generator(instance, new_slug=new_slug)
	Klass = instance.__class__
	qs_exists = Klass.objects.filter(slug=slug).exists()
	if qs_exists:
		new_slug = "{slug}-{randstr}".format(
		slug=slug,
		randstr=random_string_generator(size=4)
		)
		return unique_slug_generator(instance, new_slug=new_slug)
	return slug


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None