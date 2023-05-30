from django.shortcuts import render
from .models import Items
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializer import ProductSerializers
from .models import Items
from rest_framework import status
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from datetime import date
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from rest_framework.permissions import IsAuthenticated


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def api_Overview(req):
    over_view ={
        'list_all':'all/'
    }
    return Response({"message":"Api Works","data":over_view})

@permission_classes([IsAuthenticated])
@api_view(["GET"])
def get_all(req):
    products = Items.objects.all()
    serializer = ProductSerializers(products,many=True)
    print(serializer)
    return Response(serializer.data)

@permission_classes([IsAuthenticated])
@api_view(["POST"])
def createItem(req):
    user = ProductSerializers(data=req.data)

    if user.is_valid():
        user.save()

    return Response({"message":"User Create SuccessFully"},status=status.HTTP_201_CREATED)

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def updateItem(req,pk):
    item = Items.objects.get(id=pk)
    itemSerializer = ProductSerializers(instance=item,data=req.data)

    if itemSerializer.is_valid():
        itemSerializer.save()
        return Response(itemSerializer.data)
    

@api_view(["GET"])
def pdf_gen(req):
    iterms = Items.objects.all()
    responce = HttpResponse(content_type="application/pdf")
    responce['Content-Disposition'] = 'attachment; filename="generated_pdf.pdf"'
    doc = SimpleDocTemplate(responce, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Define a custom heading style
    heading_style = ParagraphStyle(
        name='Products',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.black,
        spaceAfter=12,
        alignment=1,
    )

    heading_text = 'Products'
    heading_paragraph = Paragraph(heading_text, heading_style)
    elements.append(heading_paragraph)
    table_data = [['Name', 'Dscripton',]]  # Add headings

    for item in iterms:
        row = [str(item.name), str(item.description)]  # Adjust the fields accordingly
        table_data.append(row)
    
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey), 
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.aliceblue),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), 
        ('FONTSIZE', (0, 0), (-1, 0), 12), 
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.aliceblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black), 
    ])

    table_width = 400
    table = Table(table_data, repeatRows=1,colWidths=[table_width / 3] * 3)
    table.setStyle(table_style)


    cell_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Header cell background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header cell text color
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Header cell alignment
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header cell font
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header cell font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header cell bottom padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Data cell background color
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Data cell text color
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Data cell font
        ('FONTSIZE', (0, 1), (-1, -1), 10),  # Data cell font size
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),  # Data cell bottom padding
    ]
    table.setStyle(TableStyle(cell_style))
    elements.append(table)
    doc.build(elements)
    return responce
