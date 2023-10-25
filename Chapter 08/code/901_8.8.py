from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# Create a new PDF document with 1 page
pdf = canvas.Canvas('Wind_Turbine_Maintenance_Manual.pdf', pagesize=letter)
# Add content to the page
pdf.setFont("Helvetica-Bold", 20)
pdf.drawCentredString(300, 700, "Wind Turbine Maintenance Manual")
pdf.setFont("Helvetica", 12)
pdf.drawString(50, 650, "Introduction:")
pdf.drawString(50, 620, "This manual provides guidelines for maintaining the wind turbine to ensure optimal performance and prevent breakdowns. It covers all aspects of the turbine's operation, from routine inspections to major repairs.")
pdf.drawString(50, 580, "Thresholds for Preventive Maintenance:")
pdf.drawString(50, 550, "- Temperature: The temperature of the turbine should not exceed 20°C. If it exceeds this threshold, maintenance is required to prevent overheating.")
pdf.drawString(50, 520, "- Wind Speed: The turbine should be shut down if wind speeds exceed 25 meters per second. If the turbine operates in high wind conditions, it may cause damage to the blades and other components.")
pdf.drawString(50, 490, "- Power Output: If the power output drops by more than 20%, it may indicate a problem with the turbine. Maintenance should be performed to identify and resolve any issues.")
pdf.drawString(50, 450, "These are general guidelines and may vary based on the specific model of the turbine. Please refer to the manufacturer's manual for detailed maintenance instructions.")
# Save the PDF document
pdf.save()
