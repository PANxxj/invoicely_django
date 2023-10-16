from io import BytesIO
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
import pdfkit
from .serializers  import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import PermissionDenied
from rest_framework import status,authentication,permissions
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from team.models import Team
from .utils import render_to_pdf
from django.core.mail import EmailMultiAlternatives
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class InvoiceView(ModelViewSet):
    serializer_class=InvoiceSerializer
    queryset=Invoice.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        team=self.request.user.team.first()
        invoice_number=team.first_invoice_number
        team.first_invoice_number=invoice_number+1
        team.save()
        serializer.save(created_by=self.request.user,team=team,invoices=invoice_number,modified_by=self.request.user,bank_account=team.bank_account)

    def perform_update(self, serializer):
        obj=self.get_object()
        if self.request.user!=obj.created_by:
            raise PermissionDenied('wrong object owner')
        serializer.save()

class ItemView(ModelViewSet):
    serializer_class=ItemSerializer
    queryset=Item.objects.all()

    def get_queryset(self):
        id=self.request.GET.get('invoice_id',0)
        return self.queryset.filter(invoice__id=id)
    
@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def generate_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, created_by=request.user)
    team = Team.objects.filter(created_by=request.user).first()

    template_name = 'pdf.html'

    if invoice.is_credit_for:
        template_name = 'pdf_creditnote.html'

    template = get_template(template_name)
    html = template.render({'invoice': invoice, 'team': team})
    # pdf = pdfkit.from_string(html, False, options={})
    pdf = render_to_pdf('pdf.html', {'invoice': invoice, 'team': team})
    response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response

@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def send_remainder(request, invoice_id):
    invoice=get_object_or_404(Invoice,pk=invoice_id,created_by=request.user)
    team=Team.objects.filter(created_by=request.user).first()

    # subject='Unpaid Invoice'
    # from_email=team.email
    # to=[invoice.client.email]
    # text_content='You have an Unpaid Invoice. invoice number : #'+str(invoice.invoices)
    # html_content='You have an Unpaid Invoice. invoice number : #'+str(invoice.invoices)

    # msg=EmailMultiAlternatives(subject,text_content,from_email,to)
    # msg.attach_alternative(html_content,'text/html')

    # template=get_template('pdf.html')
    # html=template.render({'invoice':invoice,'team':team})
    # pdf = render_to_pdf('pdf.html', {'invoice': invoice, 'team': team})

    # if pdf:
    #     name=f'invoice_{ invoice.invoices}.pdf'
    #     msg.attach(name,pdf,'application/pdf')

    # msg.send()
    #----------------------------------

    template = get_template('pdf.html')
    html  = template.render({'invoice': invoice, 'team': team})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    pdf = result.getvalue()
    filename = f'invoice_{ invoice.invoices}.pdf'

    mail_subject = 'Unpaid Invoice'
    html_message = render_to_string('pdf.html',{'invoice': invoice, 'team': team})
    message = strip_tags(html_message)
    from_email=team.email
    recipient_list = [invoice.client.email]
    email = EmailMultiAlternatives(mail_subject,message,from_email,recipient_list)
    email.attach_alternative(html_message,"text/html")
    email.attach(filename,pdf,'application/pdf')
    email.send(fail_silently=True)

    return Response()

