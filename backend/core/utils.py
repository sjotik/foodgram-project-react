import io

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rest_framework.request import Request

from recipes.models import Recipe


def get_pdf_shopping_list(request: Request) -> io.BytesIO:
    user = request.user
    recipes = Recipe.objects.filter(in_shopping_cart__user=user)
    ingr_total = {}

    for recipe in recipes:
        recipe_ingrs = recipe.with_ingredients.all()
        for ingredient in recipe_ingrs:
            if ingredient.ingredient in ingr_total:
                ingr_total[ingredient.ingredient] += ingredient.amount
            else:
                ingr_total[ingredient.ingredient] = ingredient.amount

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
    textobj = pdf.beginText(inch, inch)
    pdfmetrics.registerFont(TTFont(
        'Verdana', 'core/Verdana.ttf'))
    textobj.setFont('Verdana', 14)

    for ingredient, amount in ingr_total.items():
        textobj.textLine(
            f"{ingredient.name}: {amount} {ingredient.measurement_unit}")

    pdf.drawText(textobj)
    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return buffer
