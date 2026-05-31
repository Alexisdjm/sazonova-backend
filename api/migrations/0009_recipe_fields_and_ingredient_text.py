from django.db import migrations, models


def merge_ingredient_fields(apps, schema_editor):
    Ingredient = apps.get_model('api', 'Ingredient')
    for ingredient in Ingredient.objects.all():
        quantity = (ingredient.quantity or '').strip()
        name = (ingredient.name or '').strip()
        if quantity and name:
            ingredient.text = f'{quantity} de {name}'
        elif quantity:
            ingredient.text = quantity
        else:
            ingredient.text = name
        ingredient.save(update_fields=['text'])


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_distributorrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.TextField(blank=True, verbose_name='Descripción'),
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='recipe_image',
            new_name='card_image',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='card_image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='recipes/cards/',
                verbose_name='Imagen para la tarjeta',
            ),
        ),
        migrations.AddField(
            model_name='recipe',
            name='detailed_image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='recipes/details/',
                verbose_name='Imagen para la página de detalle',
            ),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='text',
            field=models.CharField(
                blank=True,
                max_length=300,
                verbose_name='Ingrediente (ej: 2 dientes de ajo picados)',
            ),
        ),
        migrations.RunPython(merge_ingredient_fields, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='ingredient',
            name='name',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='text',
            field=models.CharField(
                max_length=300,
                verbose_name='Ingrediente (ej: 2 dientes de ajo picados)',
            ),
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['id']},
        ),
    ]
