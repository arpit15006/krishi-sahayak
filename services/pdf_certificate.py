"""
PDF Certificate Generator for Digital Crop Passports
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
import qrcode
from datetime import datetime
import os

def generate_certificate_pdf(passport_data, farmer_data, qr_data):
    """Generate a professional PDF certificate"""
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkgreen,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=10,
        textColor=colors.darkgreen,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    # Header
    elements.append(Paragraph("🌾 DIGITAL CROP PASSPORT", title_style))
    elements.append(Paragraph("Blockchain Verified Agricultural Certificate", subtitle_style))
    elements.append(Spacer(1, 20))
    
    # Certificate Info
    cert_info = [
        ['Certificate ID:', passport_data.get('nft_token_id', 'N/A')],
        ['Issue Date:', datetime.now().strftime('%B %d, %Y')],
        ['Status:', '✅ VERIFIED & AUTHENTICATED'],
        ['Blockchain:', 'MONAD Testnet'],
    ]
    
    cert_table = Table(cert_info, colWidths=[2*inch, 3*inch])
    cert_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(cert_table)
    elements.append(Spacer(1, 20))
    
    # Farmer Information
    elements.append(Paragraph("👨‍🌾 FARMER INFORMATION", header_style))
    
    farmer_info = [
        ['Name:', farmer_data.get('name', 'N/A')],
        ['Location:', farmer_data.get('place', 'N/A')],
        ['PIN Code:', farmer_data.get('pincode', 'N/A')],
        ['Phone:', farmer_data.get('phone', 'N/A')],
        ['Experience:', f"{farmer_data.get('farming_experience_years', 0)} years"],
    ]
    
    farmer_table = Table(farmer_info, colWidths=[2*inch, 3*inch])
    farmer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(farmer_table)
    elements.append(Spacer(1, 20))
    
    # Crop Information
    elements.append(Paragraph("🌾 CROP INFORMATION", header_style))
    
    crop_info = [
        ['Crop Type:', passport_data.get('crop_type', 'N/A')],
        ['Season:', passport_data.get('season', 'N/A')],
        ['Quality Grade:', 'Grade A Premium'],
        ['Farming Practices:', 'Sustainable, Organic'],
        ['Certification:', '✅ Quality Assured'],
    ]
    
    crop_table = Table(crop_info, colWidths=[2*inch, 3*inch])
    crop_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgreen),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(crop_table)
    elements.append(Spacer(1, 20))
    
    # QR Code Section
    elements.append(Paragraph("📱 VERIFICATION QR CODE", header_style))
    
    # Generate QR code image
    qr_img_buffer = BytesIO()
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(qr_img_buffer, format='PNG')
    qr_img_buffer.seek(0)
    
    # Create QR code table
    qr_table_data = [
        [Image(qr_img_buffer, width=1.5*inch, height=1.5*inch), 
         Paragraph("Scan this QR code to verify the authenticity of this certificate on the blockchain. This certificate is cryptographically secured and publicly verifiable.", normal_style)]
    ]
    
    qr_table = Table(qr_table_data, colWidths=[2*inch, 3.5*inch])
    qr_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('ALIGN', (1, 0), (1, 0), 'LEFT'),
    ]))
    
    elements.append(qr_table)
    elements.append(Spacer(1, 30))
    
    # Footer
    footer_text = f"""
    <para align=center>
    <b>🌱 Krishi Sahayak - AI Farming Platform</b><br/>
    This certificate is issued by Krishi Sahayak and is blockchain verified.<br/>
    Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
    <i>Empowering farmers with technology for sustainable agriculture</i>
    </para>
    """
    
    elements.append(Paragraph(footer_text, normal_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and return it
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data