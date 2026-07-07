def product_image_path(instance, filename):
    category_title = instance.category.title.lower().replace(' ', '_')
    return f'products/{category_title}/{filename}'
