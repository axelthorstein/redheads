from object.detector import Detector
from object.image import Image

BASE_TEST_IMAGE_PATH = "/Users/axelthor/Projects/object/tests/test_images"


def get_product(image_name):
    """Return a product from the image name shorthand.
    """
    image = Image(f"{BASE_TEST_IMAGE_PATH}/{image_name}")
    detector = Detector(image, debug=True)

    return detector.get_product()


def test_detect_circle_black_and_white():
    product = get_product("circle_black_and_white.png")
    assert product


def test_detect_circle_white_and_black():
    product = get_product("circle_white_and_black.png")
    assert product


def test_detect_circle_med_36_square():
    product = get_product("circle_med_36_square.png")

    assert product


def test_detect_circle_med_18_square():
    product = get_product("circle_med_18_square.png")
    assert product


def test_detect_circle_thick_18_square():
    product = get_product("circle_thick_18_square.png")

    assert product


def test_detect_circle_thin_18_square():
    product = get_product("circle_thin_18_square.png")

    assert product


# Off Center Rings:

# def test_detect_circle_thick_18_round():
#     product = get_product("circle_thick_18_round.png")
#     assert product

# def test_detect_circle_med_18_round():
#     product = get_product("circle_med_18_round.png")
#     assert product

# def test_detect_circle_thin_18_round():
#     product = get_product("circle_thin_18_round.png")
#     assert product

# def test_detect_circle_med_36_round():
#     product = get_product("circle_med_36_round.png")
#     assert product

# def test_detect_circle_thin_50_square():
#     # Can't apply the filters because the dashes are too thin.
#     image_path = f"{BASE_TEST_IMAGE_PATH}/circle_thin_50_square.png"
#     detect = Detector(image_path, apply_filters=False)
#     ring = detect.detect()

#     assert product

# Real world tests:

# def test_detect_real_test_circle_1():
#     product = get_product("real_test_circle_1.png")
#     assert product

# def test_detect_real_test_circle_2():
#     product = get_product("real_test_circle_2.png")
#     assert product

# def test_detect_real_test_circle_3():
#     image_path = f"{BASE_TEST_IMAGE_PATH}/real_test_circle_3.png"
#     detect = Detector(image_path, merge_filter=True)
#     ring = detect.detect()

#     assert product

# def test_detect_real_test_circle_4():
#     image_path = f"{BASE_TEST_IMAGE_PATH}/real_test_circle_4.png"
#     detect = Detector(image_path, merge_filter=True)
#     ring = detect.detect()

#     assert product

# def test_detect_real_test_circle_5():
#     product = get_product("real_test_circle_5.png")
#     assert product

# def test_detect_circle_thick_18_square_sim_colors():
#     product = get_product("circle_thick_18_square_sim_colors.png")
#     from pprint import pprint
#     pprint(ring.sequence.sequence)
#     exit()
#     assert product

# def test_detect_circle_peach_merged():
#     product = get_product("peach_merged.png")
#     from pprint import pprint
#     pprint(ring.sequence.sequence)
#     exit()
#     assert product
