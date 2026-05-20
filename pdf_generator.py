from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO

def generate(input_data):
    print('PDF Input Data', input_data)
    fileName = 'sample.pdf'
    documentTitle = 'sample'
    title = 'Sample Title!'
    subTitle = input_data['address']
    
    textLines = [
        f"Roundtrip Efficiency = {input_data['SAM_data']['battery']['average_battery_roundtrip_efficiency']:.2f}%",
        f"System Power Generated = {input_data['SAM_data']['grid']['gen'][0]:.2f} kWh",
        f"Bill Peak Demand Charge = ${input_data['SAM_data']['utilityrate']['monthly_tou_demand_charge_w_sys'][1][1]:,.2f}",
        f"Cash Flow = ${input_data['SAM_data']['cashloan']['cf_after_tax_cash_flow'][1]:,.2f}"
    ]

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)
    pdf.setTitle(documentTitle)
    
    pdf.setFont('Helvetica-Bold', 36)
    pdf.drawCentredString(300, 770, title)

    pdf.setFillColorRGB(0, 0, 255)
    pdf.setFont('Courier-Bold', 24)
    pdf.drawCentredString(290, 720, subTitle)

    pdf.line(30, 710, 550, 710)

    text = pdf.beginText(40, 680)
    text.setFont('Courier', 18)
    text.setFillColor(colors.red)

    for line in textLines:
        text.textLine(line)

    pdf.drawText(text)

    pdf.save()
    
    buffer.seek(0)
    return buffer

if __name__ == '__main__':
    generate({'address': 'None'})