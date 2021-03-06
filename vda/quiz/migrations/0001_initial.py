# Generated by Django 2.0.2 on 2018-09-02 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('answer_id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Button',
            fields=[
                ('button_id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ButtonAction',
            fields=[
                ('button_action_id', models.AutoField(primary_key=True, serialize=False)),
                ('button', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Button')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('imgname', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('page_id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(max_length=1000)),
                ('step', models.PositiveSmallIntegerField(default=0)),
                ('page_score', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=50)),
                ('worth_points', models.BooleanField(default=False)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Page')),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('quote_id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=200)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Page')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('current_score', models.PositiveSmallIntegerField(default=0)),
                ('current_step', models.PositiveSmallIntegerField(default=0)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Page')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('title_id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=100)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Page')),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Page'),
        ),
        migrations.AddField(
            model_name='buttonaction',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Page'),
        ),
        migrations.AddField(
            model_name='button',
            name='next_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Page'),
        ),
        migrations.AddField(
            model_name='answer',
            name='next_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Page'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Question'),
        ),
    ]
