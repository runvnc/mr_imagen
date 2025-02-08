def get_closest_image_size(w, h):
    # Available image size options for Imagen
    # Note: These are typical sizes that work well with Imagen
    sizes = {
        "square_hd": (1024, 1024),
        "square": (512, 512),
        "portrait": (768, 1024),
        "landscape": (1024, 768)
    }

    # Calculate aspect ratio and total pixels of input
    input_ratio = w / h
    input_pixels = w * h

    # Find the closest match
    closest_size = min(sizes.items(), key=lambda x: (
        abs(input_ratio - (x[1][0] / x[1][1])) +  # Aspect ratio difference
        abs(input_pixels - (x[1][0] * x[1][1])) / 1000000  # Total pixels difference (normalized)
    ))

    return closest_size[1]  # Return the actual dimensions instead of name
