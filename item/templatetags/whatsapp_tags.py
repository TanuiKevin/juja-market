from django import template

register = template.Library()

@register.filter(name='whatsapp_link')
def whatsapp_link(whatsapp_number):
    return f"https://wa.me/{whatsapp_number}"

def whatsapp_link(whatsapp_number):
    return f'https://api.whatsapp.com/send?phone={whatsapp_number}'

