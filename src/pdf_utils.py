from flask import make_response
import weasyprint

def generate_pdf(html_content):
    pdf = weasyprint.HTML(string=html_content).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=document.pdf'
    return response