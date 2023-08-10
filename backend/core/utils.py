import io

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rest_framework import serializers
from rest_framework.request import Request

from foodgram_backend.settings import FONT_SIZE
from recipes.models import Recipe, RecipeIngredient, RecipeTag


def get_pdf_shopping_list(request: Request) -> io.BytesIO:
    """
    Сбор ингредиентов из рецептов в корзине с суммированием
    количества свопадающих и возврат в pdf.
    """
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
    textobj.setFont('Verdana', FONT_SIZE)

    for ingredient, amount in ingr_total.items():
        textobj.textLine(
            f'{ingredient.name}: {amount} {ingredient.measurement_unit}')

    pdf.drawText(textobj)
    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return buffer


def ingredients_tags_action(recipe: Recipe, ingrs: list, tags: list) -> None:
    """Метод комплексного добавления/обновления ингредиентов и тегов"""

    try:
        recipe.with_ingredients.all().delete()
        batch_ingrs = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            ) for ingredient in ingrs
        ]
        RecipeIngredient.objects.bulk_create(batch_ingrs)

        recipe.with_tags.all().delete()
        batch_tags = [RecipeTag(recipe=recipe, tag=tag) for tag in tags]
        RecipeTag.objects.bulk_create(batch_tags)

    except Exception as ex:
        raise serializers.ErrorDetail(ex)
