from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wishlist", "0003_alter_wishlist_unique_together_wishlist_product_and_more"),
        ("products", "0003_category_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wishlist",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="wishlisted_by",
                to="products.product",
            ),
        ),
    ]