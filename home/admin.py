import os
import csv
from home.models import *
from django.contrib import admin
from django.utils import timezone
from reportlab.lib import colors
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image)

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price_usd', 'price_rwf', 'capacity', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('amenities',)
    inlines = [RoomImageInline]

@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ('room', 'created_at')
    search_fields = ('room__name',)

@admin.register(RoomReview)
class RoomReviewAdmin(admin.ModelAdmin):
    list_display = ['room', 'name', 'email', 'location', 'staff', 'cleanliness', 'value_for_money', 'comfort', 'facilities', 'free_wifi', 'status', 'created_at']
    list_filter = ['room', 'status', 'created_at']
    search_fields = ['name', 'email', 'room__name']
    ordering = ['created_at']
    readonly_fields = ['created_at']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "room",
        "name",
        "email",
        "payment_amount",
        "currency",
        "checkInDate",
        "checkOutDate",
        "status",
        "payment_status",
    )
    list_filter = ("status", "payment_status", "room")
    search_fields = ("name", "email", "phone", "transactionId")
    actions = ["export_as_csv", "export_as_pdf"]

    def export_as_csv(self, request, queryset):
        """
        Exports selected bookings as a CSV file.
        """
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response[
            "Content-Disposition"
        ] = f"attachment; filename=bookings_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
        writer = csv.writer(response)

        writer.writerow(field_names)  # Write header
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected as CSV"

    def export_as_pdf(self, request, queryset):
        """
        Exports selected bookings as a professionally styled PDF file.
        """
        # Define the HTTP response with PDF headers
        response = HttpResponse(content_type="application/pdf")
        response[
            "Content-Disposition"
        ] = f"attachment; filename=bookings_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        # Register the Jost font
        font_path_regular = os.path.join(
            os.path.dirname(__file__), "static", "fonts", "Jost-Regular.ttf"
        )
        font_path_bold = os.path.join(
            os.path.dirname(__file__), "static", "fonts", "Jost-Bold.ttf"
        )

        if os.path.exists(font_path_regular) and os.path.exists(font_path_bold):
            pdfmetrics.registerFont(TTFont('Jost-Regular', font_path_regular))
            pdfmetrics.registerFont(TTFont('Jost-Bold', font_path_bold))
            default_font = 'Jost-Regular'
            bold_font = 'Jost-Bold'
        else:
            # Fallback to Helvetica if Jost is not found
            default_font = 'Helvetica'
            bold_font = 'Helvetica-Bold'

        # Create a PDF document with ReportLab
        doc = SimpleDocTemplate(
            response,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
        )
        elements = []

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='JostTitle', fontName=bold_font, fontSize=20, leading=24, alignment=1, textColor="#48351b"))
        styles.add(ParagraphStyle(name='JostNormal', fontName=default_font, fontSize=12, leading=15, textColor="#000000"))
        styles.add(ParagraphStyle(name='JostHeader', fontName=bold_font, fontSize=12, leading=12, textColor="#ffffff"))

        # Company Logo
        logo_path = os.path.join(
            os.path.dirname(__file__), "static", "img", "logo.png"
        )
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=2*inch, height=2*inch)
            elements.append(logo)
        else:
            elements.append(Paragraph("Company Logo", styles['JostTitle']))

        # Company Details
        company_details = """
        <para align=center>
        <b>B&B MOUNTAIN VIEW</b><br/>
        1234567890<br/>
        Kigali Rwanda<br/>
        Phone: +250 788 888 888<br/>
        Email: info@bnb.com
        </para>
        """
        elements.append(Paragraph(company_details, styles['JostNormal']))
        elements.append(Spacer(1, 12))

        # Report Title
        report_title = Paragraph(
            f"Booking Report", styles['JostTitle']
        )
        elements.append(report_title)
        elements.append(Spacer(1, 12))

        # Report Generation Date
        report_date = Paragraph(
            f"Generated on: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles['JostNormal'],
        )
        elements.append(report_date)
        elements.append(Spacer(1, 24))

        # Table Data Preparation
        data = [
            [
                Paragraph("<b>ID</b>", styles['JostHeader']),
                Paragraph("<b>Room</b>", styles['JostHeader']),
                Paragraph("<b>Name</b>", styles['JostHeader']),
                Paragraph("<b>Email</b>", styles['JostHeader']),
                Paragraph("<b>Check-In Date</b>", styles['JostHeader']),
                Paragraph("<b>Check-Out Date</b>", styles['JostHeader']),
                Paragraph("<b>Status</b>", styles['JostHeader']),
                Paragraph("<b>Payment Status</b>", styles['JostHeader']),
            ]
        ]

        for booking in queryset:
            data.append(
                [
                    str(booking.id),
                    str(booking.room),
                    booking.name or "N/A",
                    booking.email or "N/A",
                    booking.checkInDate.strftime("%Y-%m-%d") if booking.checkInDate else "N/A",
                    booking.checkOutDate.strftime("%Y-%m-%d") if booking.checkOutDate else "N/A",
                    booking.get_status_display(),
                    booking.get_payment_status_display(),
                ]
            )

        # Create the table
        table = Table(data, repeatRows=1, hAlign='LEFT')
        table_style = TableStyle(
            [
                # Header background
                ("BACKGROUND", (0, 0), (-1, 0), "#1fb5b4"),
                # Header text color
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                # Font for header
                ("FONTNAME", (0, 0), (-1, 0), bold_font),
                # Font for body
                ("FONTNAME", (0, 1), (-1, -1), default_font),
                # Alignment
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                # Grid
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                # Padding
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
        table.setStyle(table_style)

        # Alternate row colors
        for i in range(1, len(data)):
            if i % 2 == 0:
                bg_color = "#f2f2f2"
                table_style.add("BACKGROUND", (0, i), (-1, i), bg_color)

        elements.append(table)
        elements.append(Spacer(1, 24))

        # Footer with Page Numbers (Advanced: requires a custom Page Template)
        # For simplicity, we'll skip adding footers in this example.

        # Build the PDF
        doc.build(elements)

        return response

    export_as_pdf.short_description = "Export Selected as PDF"

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'created_at', 'updated_at')
    search_fields = ('name', 'position')
    list_filter = ('created_at', 'updated_at')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', )
    list_filter = ('created_at', 'updated_at')

@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'rating']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'position', 'rating']
    ordering = ['created_at']
    readonly_fields = ['created_at']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    # Optional: Make the fields read-only except for the message field if needed
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('email', 'contact_number', 'whatsapp_number', 'address', 'about_title', 'edit_link')

    def has_add_permission(self, request):
        # Only allow adding if there is no instance yet
        return not Setting.objects.exists()

    def edit_link(self, obj):
        from django.utils.html import format_html
        return format_html(
            '<a class="button" href="{}">Edit</a>',
            f'/admin/home/setting/{obj.pk}/change/'
        )
    edit_link.short_description = 'Edit'
    edit_link.allow_tags = True

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price_usd', 'price_rwf', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(FoodOrder)
class FoodOrderAdmin(admin.ModelAdmin):
    list_display = ('food', 'name', 'email', 'created_at')
    search_fields = ('name', 'email', 'food__name')
    list_filter = ('created_at', 'food')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def has_add_permission(self, request):
        return True  # Allow staff to manually add orders if needed
