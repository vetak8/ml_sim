import utils
from skimage import data

def test_rotated_image():
    '''
    Test function
    '''
    img = data.rocket()
    img_shape = img.shape

    rotated_img = utils.rotated_image(img)
    rotated_img_shape = rotated_img.shape

    assert img_shape == rotated_img_shape
