from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

class TrafficViolationReport:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.styleN = self.styles['Normal']
        self.styleH = self.styles['Heading1']
        self.data = {}

    def set_data(self, datetime, car_id, violation_type, car_image_path, scene_image_path, speed=None):
        self.data = {
            "DateTime": datetime,
            "Car ID": car_id,
            "Car Image": car_image_path,
            "Scene Image": scene_image_path,
            "Violation Type": violation_type,
            "Speed": speed
        }

    def load_image(self, path, width=2*inch, height=2*inch):
        try:
            img = Image(path, width=width, height=height)
            return img
        except Exception as e:
            return Paragraph(f"Error loading image: {str(e)}", self.styleN)

    def generate_pdf(self, save_path):
        # Create the PDF document
        document = SimpleDocTemplate(save_path, pagesize=A4)
        elements = []

        # Title
        title = Paragraph("Traffic Violation Report", self.styleH)
        elements.append(title)
        elements.append(Spacer(1, 12))

        # DateTime
        date_time = Paragraph(f"Date & Time: {self.data['DateTime']}", self.styleN)
        elements.append(date_time)
        elements.append(Spacer(1, 12))

        # Violation Type
        violation_type = Paragraph(f"Violation Type: {self.data['Violation Type']}", self.styleN)
        elements.append(violation_type)
        elements.append(Spacer(1, 12))

        # Speed (if applicable)
        if self.data.get("Speed"):
            speed = Paragraph(f"Speed: {self.data['Speed']} km/h", self.styleN)
            elements.append(speed)
            elements.append(Spacer(1, 12))

        # Car ID and Image
        car_id_paragraph = Paragraph(f"Car ID: {self.data['Car ID']}", self.styleN)
        car_image = self.load_image(self.data["Car Image"], width=2*inch, height=2*inch)

        # Creating a table-like layout for the Car ID and Car Image
        car_info_table = Table(
            [[car_id_paragraph, car_image]],
            colWidths=[2*inch, 2*inch],
            style=TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0)
            ])
        )

        elements.append(Paragraph("Car Details:", self.styleN))
        elements.append(car_info_table)
        elements.append(Spacer(1, 12))

        # Scene Image
        elements.append(Paragraph("Scene Image:", self.styleN))
        scene_image = self.load_image(self.data["Scene Image"], width=6*inch, height=3*inch)
        elements.append(scene_image)

        # Description of scene
        elements.append(Paragraph("Description of Scene:", self.styleN))
        if self.data["Violation Type"] == "Traffic Light Violation":
            description = "The vehicle was detected crossing the line when the traffic light was red."
        elif self.data["Violation Type"] == "Speed Violation":
            description = "The vehicle was detected exceeding the speed limit."
        elif self.data["Violation Type"] == "Pedestrian Crossing Violation":
            description = "The vehicle was detected crossing a pedestrian crossing when a pedestrian is detected to be crossing."
        else:
            description = "No description available."
        elements.append(Paragraph(description, self.styleN))
        
        # if folder does not exist, create it
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        # Build the PDF
        document.build(elements)
        print(f"PDF report generated and saved at {save_path}")

