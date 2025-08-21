import streamlit as st
import base64
import re


def local_css(
        file_name: str
) -> None:
    try:
        with open(file_name) as f:
            st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}")
    except Exception as e:
        st.error(f"Error loading CSS: {e}")

def set_bg_hack(main_bg):
    """
    Set a background image for the Streamlit app.
    
    This function loads an image file, converts it to base64 encoding, and applies it 
    as a full-cover background image to the Streamlit app using CSS injection. The 
    background image will cover the entire app area.
    
    Args:
        main_bg (str): Path to the background image file. Supported formats 
                      include PNG, JPG, JPEG, and GIF. The path should be relative 
                      to the current working directory or an absolute path.
    
    Returns:
        None: This function modifies the Streamlit app's styling but doesn't 
              return any value.
        
    Raises:
        FileNotFoundError: If the specified image file doesn't exist at the given path.
        Exception: For any other errors during file reading, base64 encoding, 
                  or CSS injection (e.g., corrupted image file, permission issues).
        
    Example:
        >>> set_bg_hack("background.png")
        >>> set_bg_hack("assets/hero_image.jpg")
        >>> set_bg_hack("/absolute/path/to/image.gif")
        
    Note:
        - The function automatically detects the image format from the file extension
        - If an unsupported format is detected, it defaults to PNG
        - The background image uses CSS `background-size: cover` for full coverage
        - This function should be called after `st.set_page_config()` for best results
    """
    
    try:
        # Detect file extension
        main_bg_ext = main_bg.split('.')[-1].lower()
        if main_bg_ext not in ['png', 'jpg', 'jpeg', 'gif']:
            main_bg_ext = 'png'  # fallback
        
        with open(main_bg, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        
        st.markdown(
            f"""
             <style>
             .stApp {{
                 background: url(data:image/{main_bg_ext};base64,{img_data});
                 background-size: cover
             }}
             </style>
             """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Error setting background: {e}")


def sort_images_by_number(image_paths):
    """
    Sort image paths by extracting the numeric value from filenames.
    
    Args:
        image_paths (list): List of image file paths
        
    Returns:
        list: Sorted list of image paths by numeric order
    """
    def extract_number(path):
        # Extract number from filename like 'pic01_col.png' or 'pic100_col.png'
        match = re.search(r'pic(\d+)_col\.png', path)
        if match:
            return int(match.group(1))  # Convert to int for proper sorting
        return 0  # fallback for files that don't match pattern
    
    return sorted(image_paths, key=extract_number)


def blend_colors(colors, weights):
    """
    Blend multiple hex colors together using the specified weights.

    Args:
        colors (list of str): List of hex color strings (e.g., ['#FF0000', '#00FF00', '#0000FF']).
        weights (list of float): List of weights for each color. Should be the same length as colors.

    Returns:
        str: The resulting blended color as a hex string (e.g., '#AABBCC').

    Notes:
        - The weights do not need to sum to 1; they will be normalized automatically.
        - Colors are blended in RGB space.
        - If the input lists are empty or mismatched, the function may raise an error.

    Example:
        >>> blend_colors(['#FF0000', '#0000FF'], [0.5, 0.5])
        '#800080'
    """
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb):
        return '#{:02X}{:02X}{:02X}'.format(*rgb)

    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]

    blended = [0, 0, 0]
    for color, weight in zip(colors, normalized_weights):
        rgb = hex_to_rgb(color)
        blended[0] += rgb[0] * weight
        blended[1] += rgb[1] * weight
        blended[2] += rgb[2] * weight

    blended_rgb = tuple(round(c) for c in blended)
    return rgb_to_hex(blended_rgb)