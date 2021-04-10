# Generated by Django 3.1.2 on 2021-04-10 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20210404_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnerpreference',
            name='about_partner',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='age_from',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='age_to',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='caste',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.caste'),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='height_from',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='height_to',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='highest_education',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.educationcategory'),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='income_from',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='income_to',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='mother_tongue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.mothertongue'),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='occupation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.occupationcategory'),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='raasi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.raasi'),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='religion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.religion'),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='star',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.star'),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='sub_caste',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.subcaste'),
        ),
    ]
