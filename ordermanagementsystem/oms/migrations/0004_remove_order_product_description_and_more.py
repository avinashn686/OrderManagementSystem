# Generated by Django 4.0.2 on 2022-05-30 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oms', '0003_alter_user_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product_description',
        ),
        migrations.AlterField(
            model_name='order',
            name='product_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_product_id', to='oms.product'),
        ),
    ]