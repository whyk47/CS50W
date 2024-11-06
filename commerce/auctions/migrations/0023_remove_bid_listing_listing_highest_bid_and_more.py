# Generated by Django 4.2.6 on 2023-10-21 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_bid_listing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='listing',
        ),
        migrations.AddField(
            model_name='listing',
            name='highest_bid',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auctions.bid'),
        ),
        migrations.AddField(
            model_name='listing',
            name='num_bids',
            field=models.IntegerField(default=0),
        ),
    ]
