from django.db import models


class City(models.Model):
    name = models.CharField(
            max_length=50,
            verbose_name='Город',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        

class District(models.Model):
    name = models.CharField(
            max_length=50, 
            verbose_name='Район',
    )

    city = models.ForeignKey(
            City, 
            on_delete=models.PROTECT,
            verbose_name='Город', 
            related_name='districts',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'
        

class Category(models.Model):
    name = models.CharField(
            max_length=50, 
            verbose_name='Категория',
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name='Родительская категория'
    )


    def __str__(self):
        if self.parent:
            return f'{self.parent.name} → {self.name}'
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Estate(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )

    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='products_by_category'
    )

    area = models.DecimalField(
        max_digits=10,
        decimal_places=1,
        verbose_name='Площадь'
    )

    city = models.ForeignKey(
        'City',
        on_delete=models.PROTECT,
        verbose_name='Город',
        related_name='products_by_city'
    )

    district = models.ForeignKey(
        'District',
        on_delete=models.PROTECT,
        verbose_name='Район',
        related_name='products_by_district'
    )

    image = models.ImageField(
        upload_to='images/',
        verbose_name='Изображение'
    )

    geo = models.TextField(
            verbose_name='Местоположение'
    )


    promo_video = models.FileField(
        upload_to='videos/',
        verbose_name='Промо-видео',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно ли объявление'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    def __str__(self):
        return f"{self.name} ({self.city})"

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Image(models.Model):
    estate = models.ForeignKey(
        'Estate',
        on_delete=models.CASCADE,
        verbose_name='Объявление',
        related_name='images'
    )

    image = models.ImageField(
        upload_to='images/',
        verbose_name='Изображения'
    )
