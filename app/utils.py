def product_image_path(instance, filename):
    category_title = instance.category.title.lower().replace(' ', '_')
    return f'products/{category_title}/{filename}'


def product_price_filter(filter_type, product=None):
    if filter_type == "expensive":
        return product.order_by("price")
    elif filter_type == "cheap":
        return product.order_by("-price")
    return product