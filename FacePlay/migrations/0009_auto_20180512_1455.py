# Generated by Django 2.0.5 on 2018-05-12 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FacePlay', '0008_auto_20180512_1230'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_time', models.DateTimeField(auto_now=True)),
                ('p_dir', models.CharField(max_length=100)),
                ('cs_id', models.ForeignKey(on_delete=True, to='FacePlay.C_S')),
            ],
        ),
        migrations.DeleteModel(
            name='USER',
        ),
        migrations.AddField(
            model_name='student',
            name='s_pwd',
            field=models.CharField(default=None, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='s_tel',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='t_pwd',
            field=models.CharField(default=None, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='t_tel',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='s_face',
            field=models.CharField(help_text='存放人脸图片的路径', max_length=100),
        ),
    ]
