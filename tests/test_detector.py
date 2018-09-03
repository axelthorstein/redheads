from object.detector import Detector

BASE_TEST_IMAGE_PATH = "/Users/axelthor/Projects/object/tests/test_images"


def get_ring(image_name):
    """Return a dashed ring from the image name shorthand.
    """
    detector = Detector(f"{BASE_TEST_IMAGE_PATH}/{image_name}", debug=True)

    return detector.find_ring()


def test_detect_circle_med_36_square():
    ring = get_ring("circle_med_36_square.png")
    assert ring.is_valid()


def test_detect_circle_med_36_round():
    ring = get_ring("circle_med_36_round.png")
    assert ring.is_valid()


def test_detect_circle_med_18_square():
    ring = get_ring("circle_med_18_square.png")
    assert ring.is_valid()


def test_detect_circle_med_18_round():
    ring = get_ring("circle_med_18_round.png")
    assert ring.is_valid()


def test_detect_circle_thick_18_square():
    ring = get_ring("circle_thick_18_square.png")
    assert ring.is_valid()


def test_detect_circle_thick_18_round():
    ring = get_ring("circle_thick_18_round.png")
    assert ring.is_valid()


def test_detect_circle_thin_18_square():
    ring = get_ring("circle_thin_18_square.png")
    assert ring.is_valid()


def test_detect_circle_thin_18_round():
    ring = get_ring("circle_thin_18_round.png")
    assert ring.is_valid()


def test_detect_circle_thin_50_square():
    # Can't apply the filters because the dashes are too thin.
    image_path = f"{BASE_TEST_IMAGE_PATH}/circle_thin_50_square.png"
    detect = Detector(image_path, apply_filters=False)
    ring = detect.find_ring()

    assert ring.is_valid()


def test_detect_real_test_circle_1():
    ring = get_ring("real_test_circle_1.png")
    assert ring.is_valid()


def test_detect_real_test_circle_2():
    ring = get_ring("real_test_circle_2.png")
    assert ring.is_valid()


def test_detect_real_test_circle_3():
    image_path = f"{BASE_TEST_IMAGE_PATH}/real_test_circle_3.png"
    detect = Detector(image_path, merge_filter=True)
    ring = detect.find_ring()

    assert ring.is_valid()


def test_detect_circle_black_and_white():
    ring = get_ring("circle_black_and_white.png")
    assert ring.is_valid()


def test_detect_circle_white_and_black():
    ring = get_ring("circle_white_and_black.png")
    assert ring.is_valid()
