
import numpy as np
import os
from PIL import Image

NUM_CHANNELS = 3


# --------------------------------------------------------------------------- #

def img_read_helper(path):
    """
    Creates an RGBImage object from the given image file
    """
    # Open the image in RGB
    img = Image.open(path).convert("RGB")
    # Convert to numpy array and then to a list
    matrix = np.array(img).tolist()
    return RGBImage(matrix)


def img_save_helper(path, image):
    """
    Saves the given RGBImage instance to the given path
    """
    # Convert list to numpy array
    img_array = np.array(image.get_pixels())
    # Convert numpy array to PIL Image object
    img = Image.fromarray(img_array.astype(np.uint8))
    # Save the image object to path
    img.save(path)


# --------------------------------------------------------------------------- #

# Part 1: RGB Image #passes terminal tests 
class RGBImage:
    """
    Represents an image in RGB format
    """

    def __init__(self, pixels): #passes terminal tests
        """
        Initializes a new RGBImage object

        # Test with non-rectangular list
        >>> pixels = [
        ...              [[255, 255, 255], [255, 255, 255]],
        ...              [[255, 255, 255]]
        ...          ]
        >>> RGBImage(pixels)
        Traceback (most recent call last):
        ...
        TypeError

        # Test instance variables
        >>> pixels = [
        ...              [[255, 255, 255], [0, 0, 0]]
        ...          ]
        >>> img = RGBImage(pixels)
        >>> img.pixels
        [[[255, 255, 255], [0, 0, 0]]]
        >>> img.num_rows
        1
        >>> img.num_cols
        2
        """

        # Raise exceptions here
        # Check if pixels is a list and isn't empty
        if not isinstance(pixels, list) or len(pixels) == 0:
            raise TypeError()

        # Finding number of rows and columns
        num_rows = len(pixels)
        num_cols = len(pixels[0])

        for row in pixels:
        # Check if each row is a list and if #row elements = #column elements
            if not isinstance(row, list) or len(row) != num_cols:
                raise TypeError()
            
            # Check if each pixel in each row is a list and each pixel len = 3
            for pixel in row:
                if not isinstance(pixel, list) or len(pixel) != 3:
                    raise TypeError()
            
                # Check that each pixel value is an integer and lies b/w 0-255 range
                for intensity in pixel:
                    if not isinstance(intensity, int) or not (0 <= intensity <= 255):
                        raise ValueError()

        self.pixels = pixels
        self.num_rows = num_rows
        self.num_cols = num_cols

    def size(self): #passes terminal tests
        """
        Returns the size of the image in (rows, cols) format

        # Make sure to complete __init__ first
        >>> pixels = [
        ...              [[255, 255, 255], [0, 0, 0]]
        ...          ]
        >>> img = RGBImage(pixels)
        >>> img.size()
        (1, 2)
        """
        return (self.num_rows, self.num_cols)

    def get_pixels(self): #passes terminal tests
        """
        Returns a copy of the image pixel array

        # Make sure to complete __init__ first
        >>> pixels = [
        ...              [[255, 255, 255], [0, 0, 0]]
        ...          ]
        >>> img = RGBImage(pixels)
        >>> img_pixels = img.get_pixels()

        # Check if this is a deep copy
        >>> img_pixels                               # Check the values
        [[[255, 255, 255], [0, 0, 0]]]
        >>> id(pixels) != id(img_pixels)             # Check outer list
        True
        >>> id(pixels[0]) != id(img_pixels[0])       # Check row
        True
        >>> id(pixels[0][0]) != id(img_pixels[0][0]) # Check pixel
        True
        """
        return [[[pixel for pixel in channel] \
        for channel in row] for row in self.pixels]


    def copy(self): #passes terminal tests
        """
        Returns a copy of this RGBImage object

        # Make sure to complete __init__ first
        >>> pixels = [
        ...              [[255, 255, 255], [0, 0, 0]]
        ...          ]
        >>> img = RGBImage(pixels)
        >>> img_copy = img.copy()

        # Check that this is a new instance
        >>> id(img_copy) != id(img)
        True
        """
        copied = self.get_pixels()
        return RGBImage(copied)


    def get_pixel(self, row, col): #passes terminal tests
        """
        Returns the (R, G, B) value at the given position

        # Make sure to complete __init__ first
        >>> pixels = [
        ...              [[255, 255, 255], [0, 0, 0]]
        ...          ]
        >>> img = RGBImage(pixels)

        # Test with an invalid index
        >>> img.get_pixel(1, 0)
        Traceback (most recent call last):
        ...
        ValueError

        # Run and check the returned value
        >>> img.get_pixel(0, 0)
        (255, 255, 255)
        """
        # Check that row and col are integers
        if not isinstance(row, int) or not isinstance(col, int):
            raise TypeError()
        # Check row/col index
        if row < 0 or row >= self.num_rows or \
        col < 0 or col >= self.num_cols:
            raise ValueError()
        pixel = self.pixels[row][col]
        return tuple(pixel)



    def set_pixel(self, row, col, new_color): #passes terminal tests
        """
        Sets the (R, G, B) value at the given position

        # Make sure to complete __init__ first
        >>> pixels = [
        ...              [[255, 255, 255], [0, 0, 0]]
        ...          ]
        >>> img = RGBImage(pixels)

        # Test with an invalid new_color tuple
        >>> img.set_pixel(0, 0, (256, 0, 0))
        Traceback (most recent call last):
        ...
        ValueError

        # Check that the R/G/B value with negative is unchanged
        >>> img.set_pixel(0, 0, (-1, 0, 0))
        >>> img.pixels
        [[[255, 0, 0], [0, 0, 0]]]
        """
        # tested all exceptions
        
        # Check if row and col are integers
        if not isinstance(row, int) or not isinstance(col, int):
            raise TypeError()
        
        # Check if row and col have valid index entry 
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            raise ValueError()
        
        # Check if new_color is a tuple with 3 entries
        if not isinstance(new_color, tuple) or len(new_color) != 3:
            raise ValueError()

        # Check if new_color entries are integers and if each entry is <= 255
        for pixel_intensity in new_color:
            if pixel_intensity > 255:
                raise ValueError()
            if not isinstance(pixel_intensity, int):
                raise TypeError()
        
        original_color = self.pixels[row][col]
        updated = [
            new_intensity if new_intensity >= 0 else current_intensity
            for current_intensity, new_intensity in zip(original_color, new_color)
        ]
        self.pixels[row][col] = updated


# Part 2: Image Processing Template Methods #
class ImageProcessingTemplate:
    """
    Contains assorted image processing methods
    Intended to be used as a parent class
    """

    def __init__(self): #passes terminal tests
        """
        Creates a new ImageProcessingTemplate object

        # Check that the cost was assigned
        >>> img_proc = ImageProcessingTemplate()
        >>> img_proc.cost
        0
        """
        self.cost = 0

    def get_cost(self): #passes terminal tests
        """
        Returns the current total incurred cost

        # Check that the cost value is returned
        >>> img_proc = ImageProcessingTemplate()
        >>> img_proc.cost = 50 # Manually modify cost
        >>> img_proc.get_cost()
        50
        """
        return self.cost

    def negate(self, image):
        """
        Returns a negated copy of the given image

        # Check if this is returning a new RGBImage instance
        >>> img_proc = ImageProcessingTemplate()
        >>> pixels = [
        ...              [[255, 255, 255], [0, 0, 0]]
        ...          ]
        >>> img = RGBImage(pixels)
        >>> img_negate = img_proc.negate(img)
        >>> id(img) != id(img_negate) # Check for new RGBImage instance
        True

        # The following is a description of how this test works
        # 1 Create a processor
        # 2/3 Read in the input and expected output
        # 4 Modify the input
        # 5 Compare the modified and expected
        # 6 Write the output to file
        # You can view the output in the img/out/ directory
        >>> img_proc = ImageProcessingTemplate()                            # 1
        >>> img = img_read_helper('img/gradient_16x16.png')                 # 2
        >>> img_exp = img_read_helper('img/exp/gradient_16x16_negate.png')  # 3
        >>> img_negate = img_proc.negate(img)                               # 4
        >>> img_negate.pixels == img_exp.pixels # Check negate output       # 5
        True
        >>> img_save_helper('img/out/gradient_16x16_negate.png', img_negate)# 6
        """
        # Retrieve pixel matrix
        pixels = image.get_pixels()
        max_value = 255
        
        # Then calculate the negation values by subtracting it from the orginal matrix
        negation = [[[max_value - intensity for intensity in pixel] \
                    for pixel in row] for row in pixels]
        
        # negation = [[(255 - pixel[i]) for i in range(3) for pixel in pixels]]
        
        negated_img = RGBImage(negation)
        return negated_img


    def grayscale(self, image): #passes terminal tests
        """
        Returns a grayscale copy of the given image

        # See negate for info on this test
        # You can view the output in the img/out/ directory
        >>> img_proc = ImageProcessingTemplate()
        >>> img = img_read_helper('img/gradient_16x16.png')
        >>> img_exp = img_read_helper('img/exp/gradient_16x16_gray.png')
        >>> img_gray = img_proc.grayscale(img)
        >>> img_gray.pixels == img_exp.pixels # Check grayscale output
        True
        >>> img_save_helper('img/out/gradient_16x16_gray.png', img_gray)
        """
        pixels = image.get_pixels()
        gray_pixels = [[[sum(pixel)//3] * 3 for pixel in row] for row in pixels]
        grayed_image = RGBImage(gray_pixels)
        return grayed_image

    def rotate_180(self, image): #passes terminal tests
        """
        Returns a rotated version of the given image

        # See negate for info on this test
        # You can view the output in the img/out/ directory
        >>> img_proc = ImageProcessingTemplate()
        >>> img = img_read_helper('img/gradient_16x16.png')
        >>> img_exp = img_read_helper('img/exp/gradient_16x16_rotate.png')
        >>> img_rotate = img_proc.rotate_180(img)
        >>> img_rotate.pixels == img_exp.pixels # Check rotate_180 output
        True
        >>> img_save_helper('img/out/gradient_16x16_rotate.png', img_rotate)
        """
        # Get new instance of og matrix
        pixels = image.get_pixels()
        transposed_pixels = [row[::-1] for row in pixels[::-1]]
        flipped = RGBImage(transposed_pixels)
        return flipped
        

    def get_average_brightness(self, image): #passes terminal tests
        """
        Returns the average brightness for the given image

        >>> img_proc = ImageProcessingTemplate()
        >>> img = img_read_helper('img/gradient_16x16.png')
        >>> img_proc.get_average_brightness(img)
        133
        """
        # pixels = image.get_pixels()
        # total_brightness = sum([sum([max(pixel) for pixel in row]) for row in pixels])
        # average_brightness = total_brightness // (image.num_rows + image.num_cols)
        # return average_brightness

        pixels = image.get_pixels()
        total_brightness = sum(sum(pixel) for row in pixels for pixel in row)
        average_brightness = total_brightness // (3  * image.num_rows * image.num_cols)
        return average_brightness


    def adjust_brightness(self, image, intensity): #passes terminal tests
        """
        Returns a new image with adjusted brightness level

        >>> img_proc = ImageProcessingTemplate()
        >>> img = img_read_helper('img/gradient_16x16.png')
        >>> img_exp = img_read_helper('img/exp/gradient_16x16_adjusted.png')
        >>> img_adjust = img_proc.adjust_brightness(img, 75)
        >>> img_adjust.pixels == img_exp.pixels # Check adjust_brightness
        True
        >>> img_save_helper('img/out/gradient_16x16_adjusted.png', img_adjust)
        """
        bound_value = 255
        
        # Check that intensity is an integer
        if not isinstance(intensity, int):
            raise TypeError()
        
        # Check that intensity is b/w -255 to +255
        if intensity > bound_value or intensity < - bound_value:
            raise ValueError()

        # Retrieve the pixel matrix 
        pixels = image.get_pixels()

        # Adjust the pixels
        adjusted_pixels = [[[max(0, min(bound_value, pixel[i] + intensity)) \
        for i in range(3)] for pixel in row] for row in pixels]
        return RGBImage(adjusted_pixels)
        


    def blur(self, image):
        """
        Returns a new image with the pixels blurred

        >>> img_proc = ImageProcessingTemplate()
        >>> img = img_read_helper('img/gradient_16x16.png')
        >>> img_exp = img_read_helper('img/exp/gradient_16x16_blur.png')
        >>> img_adjust = img_proc.blur(img)
        >>> img_adjust.pixels == img_exp.pixels # Check blur
        True
        >>> img_save_helper('img/out/gradient_16x16_blur.png', img_adjust)
        """
        pixels = image.get_pixels()
        blurred_image = [[pixel for pixel in row] for row in pixels]

        for row in range(image.num_rows):
            for col in range(image.num_cols):
                red_sum = 0
                green_sum = 0
                blue_sum = 0
                counter = 0

                for i in range(max(0, row-1), min(image.num_rows, row + 2)):
                    for j in range(max(0, col-1), min(image.num_cols, col + 2)):
                        red_sum += pixels[i][j][0]
                        green_sum += pixels[i][j][1]
                        blue_sum += pixels[i][j][2]
                        counter += 1

                r_avg = red_sum // counter
                g_avg = green_sum // counter
                b_avg = blue_sum // counter

                blurred_image[row][col] = [r_avg, g_avg, b_avg]

        return RGBImage(blurred_image)


# Part 3: Standard Image Processing Methods # #passes terminal tests
class StandardImageProcessing(ImageProcessingTemplate):
    """
    Represents a standard tier of an image processor
    """

    def __init__(self):
        """
        Creates a new StandardImageProcessing object

        # Check that the cost was assigned
        >>> img_proc = ImageProcessingTemplate()
        >>> img_proc.cost
        0
        """
        super().__init__()
        self.cost = 0
        self.free = 0

    def negate(self, image):
        """
        Returns a negated copy of the given image

        # Check the expected cost
        >>> img_proc = StandardImageProcessing()
        >>> img_in = img_read_helper('img/square_16x16.png')
        >>> negated = img_proc.negate(img_in)
        >>> img_proc.get_cost()
        5

        # Check that negate works the same as in the parent class
        >>> img_proc = StandardImageProcessing()
        >>> img = img_read_helper('img/gradient_16x16.png')
        >>> img_exp = img_read_helper('img/exp/gradient_16x16_negate.png')
        >>> img_negate = img_proc.negate(img)
        >>> img_negate.pixels == img_exp.pixels # Check negate output
        True
        """
        negated_image = super().negate(image)  
        if self.free > 0:
            self.cost += 0
            self.free -= 1
        else:
            self.cost += 5
        return negated_image

    def grayscale(self, image):
        """
        Returns a grayscale copy of the given image

        """
        grayed_img = super().grayscale(image)
        if self.free > 0:
            self.cost += 0
            self.free -= 1
        else:
            self.cost += 6
        return grayed_img

    def rotate_180(self, image):
        """
        Returns a rotated version of the given image
        """
        rotated_img = super().rotate_180(image)
        if self.free > 0:
            self.cost += 0
            self.free -= 1
        else:
            self.cost += 10
        return rotated_img


    def adjust_brightness(self, image, intensity):
        """
        Returns a new image with adjusted brightness level
        """
        adjusted_img = super().adjust_brightness(image)
        if self.free > 0:
            self.cost += 0
            self.free -= 1
        else:
            self.cost += 1
        return adjusted_img


    def blur(self, image):
        """
        Returns a new image with the pixels blurred
        """
        blurred_img = super().blur(image)
        if self.free > 0:
            self.cost += 0
            self.free -= 1
        else:
            self.cost += 5
        return blurred_img


    def redeem_coupon(self, amount):
        """
        Makes the given number of methods calls free

        # Check that the cost does not change for a call to negate
        # when a coupon is redeemed
        >>> img_proc = StandardImageProcessing()
        >>> img = img_read_helper('img/gradient_16x16.png')
        >>> img_proc.redeem_coupon(1)
        >>> img = img_proc.rotate_180(img)
        >>> img_proc.get_cost()
        0
        """
        if amount <= 0:
            raise ValueError()
        if not isinstance(amount,int):
            raise TypeError()
        # for i in range(amount):
        self.free += amount


# Part 4: Premium Image Processing Methods #
class PremiumImageProcessing(ImageProcessingTemplate):
    """
    Represents a paid tier of an image processor
    """

    def __init__(self):
        """
        Creates a new PremiumImageProcessing object

        # Check the expected cost
        >>> img_proc = PremiumImageProcessing()
        >>> img_proc.get_cost()
        50
        """
        super().__init__()
        self.cost = 50

    def chroma_key(self, chroma_image, background_image, color): #passes terminal tests
        """
        Returns a copy of the chroma image where all pixels with the given
        color are replaced with the background image.

        # Check output
        >>> img_proc = PremiumImageProcessing()
        >>> img_in = img_read_helper('img/square_16x16.png')
        >>> img_in_back = img_read_helper('img/gradient_16x16.png')
        >>> color = (255, 255, 255)
        >>> img_exp = img_read_helper('img/exp/square_16x16_chroma.png')
        >>> img_chroma = img_proc.chroma_key(img_in, img_in_back, color)
        >>> img_chroma.pixels == img_exp.pixels # Check chroma_key output
        True
        >>> img_save_helper('img/out/square_16x16_chroma.png', img_chroma)
        """

        if not isinstance(chroma_image, RGBImage) or not \
            isinstance(background_image, RGBImage):
            raise TypeError()

        # Check image sizes
        if chroma_image.size() != background_image.size():
            raise ValueError()

        # Create a new image to store the result
        new_image = RGBImage(chroma_image.get_pixels())

        # Loop over each pixel in the chroma_image
        for i in range(chroma_image.num_rows):
            for j in range(chroma_image.num_cols):
                # Get the pixel values from the chroma and background images
                chroma_pixel = chroma_image.get_pixel(i, j)
                background_pixel = background_image.get_pixel(i, j)

                # Check if the pixel color matches the specified color
                if chroma_pixel == color:
                    # Replace the pixel with the corresponding pixel from the background image
                    new_image.set_pixel(i, j, background_pixel)

        return new_image


    def sticker(self, sticker_image, background_image, x_pos, y_pos): #passes terminal tests
        """
        Returns a copy of the background image where the sticker image is
        placed at the given x and y position.

        # Test with out-of-bounds image and position size
        >>> img_proc = PremiumImageProcessing()
        >>> img_sticker = img_read_helper('img/square_6x6.png')
        >>> img_back = img_read_helper('img/gradient_16x16.png')
        >>> x, y = (15, 0)
        >>> img_proc.sticker(img_sticker, img_back, x, y)
        Traceback (most recent call last):
        ...
        ValueError

        # Check output
        >>> img_proc = PremiumImageProcessing()
        >>> img_sticker = img_read_helper('img/square_6x6.png')
        >>> img_back = img_read_helper('img/gradient_16x16.png')
        >>> x, y = (3, 3)
        >>> img_exp = img_read_helper('img/exp/square_16x16_sticker.png')
        >>> img_combined = img_proc.sticker(img_sticker, img_back, x, y)
        >>> img_combined.pixels == img_exp.pixels # Check sticker output
        True
        >>> img_save_helper('img/out/square_16x16_sticker.png', img_combined)
        """
        # Checks that sticker_image and background_image are RGBImage instances
        if not isinstance(sticker_image, RGBImage) or not \
        isinstance(background_image, RGBImage):
            raise TypeError() 

        # Check sticker size smaller than background size
        if (sticker_image.num_cols > background_image.num_cols
            or sticker_image.num_rows > background_image.num_rows):
            raise ValueError()

        # Check x_pos and y_pos types
        if not isinstance(x_pos, int) or not isinstance(y_pos, int):
            raise TypeError()

        # Check if sticker will fit at the x/y
        if (sticker_image.num_rows + y_pos > background_image.num_rows
            or sticker_image.num_cols + x_pos > background_image.num_cols):
            raise ValueError()

        # Create a new image to store the result
        new_image = RGBImage(background_image.get_pixels())

        # Loop over each pixel in the sticker image
        for i in range(sticker_image.num_rows):
            for j in range(sticker_image.num_cols):
                # Calculate the position in the background
                back_row = y_pos + i
                back_col = x_pos + j

                # Get  pixel values from  sticker and background
                sticker_pixel = sticker_image.get_pixel(i, j)
                background_pixel = background_image.get_pixel(back_row, back_col)

                # Replace corresponding pixels
                new_image.set_pixel(back_row, back_col, sticker_pixel)

        return new_image      



    def edge_highlight(self, image):
        """
        Returns a new image with the edges highlighted
        # Check output
        >>> img_proc = PremiumImageProcessing()
        >>> img = img_read_helper('img/gradient_16x16.png')
        >>> img_edge = img_proc.edge_highlight(img)
        >>> img_exp = img_read_helper('img/exp/gradient_16x16_edge.png')
        >>> img_exp.pixels == img_edge.pixels # Check edge_highlight output
        True
        >>> img_save_helper('img/out/gradient_16x16_edge.png', img_edge)
        """

        # Create a new image to store the result
        edge_img = image.get_pixels()

        for row in range(len(edge_img)):
            for col in range(len(edge_img[0])):
                avg = sum(edge_img[row][col])//3
                edge_img[row][col] = avg        
        output = []

        # The kernel
        kernel = [
            [ -1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]
        ]
        # Apply kernel to each pixel
        for w in range(len(edge_img)):
            new_lst = [0 for i in range(len(edge_img[0]))]
            for h in range(len(edge_img[0])):

                # Apply kernel to neighboring pixels
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        # Fact check that pixel is within image bounds
                        if 0 <= w + i < len(edge_img) and 0 <= h + j < len(edge_img[0]):
                            # pixel_pos = edge_img.get_pixel(w + i, h + j)
                            m_value = kernel[i+1][j+1]
                            # new_lst.append[pixel_pos[0]*m_value]
                            new_lst[h] += edge_img[w+i][h+j] * m_value

                if new_lst[h] < 0:
                    new_lst[h] = [0, 0, 0]
                elif new_lst[h] > 255:
                    new_lst[h] = [255, 255, 255]
                else:
                    new_lst[h] = [new_lst[h], new_lst[h], new_lst[h]]


                # if new_lst[h] < 0:
                #     new_lst[h] = [0, 0, 0]
                # else:
                #     new_lst[h] = [255, 255, 255]

            output.append(new_lst)
        # print(output)
        return RGBImage(output)

# img_proc = PremiumImageProcessing()
# img = img_read_helper('img/gradient_16x16.png')
# img_edge = img_proc.edge_highlight(img)
# # for w in range(img.num_rows):
# #     for h in range(img.num_cols):      
# #         if sum(img.pixels[w][h]) != sum(img_edge.pixels[w][h]):
# #             print(w, h)

# img_exp = img_read_helper('img/exp/gradient_16x16_edge.png')
# img_exp.pixels == img_edge.pixels
# img_save_helper('img/out/gradient_16x16_edge.png', img_edge)


# Part 5: Image KNN Classifier #
class ImageKNNClassifier:
    """
    Represents a simple KNNClassifier
    """

    def __init__(self, k_neighbors):
        """
        Creates a new KNN classifier object
        """
        self.k_neighbors = k_neighbors
        self.data = []


    def fit(self, data):
        """
        Stores the given set of data and labels for later
        """
        if len(data) < self.k_neighbors:
            raise ValueError()
        self.data = data


    def distance(self, image1, image2): #passes terminal tests
        """
        Returns the distance between the given images

        >>> img1 = img_read_helper('img/steve.png')
        >>> img2 = img_read_helper('img/knn_test_img.png')
        >>> knn = ImageKNNClassifier(3)
        >>> knn.distance(img1, img2)
        15946.312896716909
        """

        # Check if both images are RGBImage instances
        if not isinstance(image1, RGBImage) or not isinstance(image2, RGBImage):
            raise TypeError()

        # Check that both image sizes are equal
        if image1.num_rows != image2.num_rows or image1.num_cols != image2.num_cols:
            raise ValueError()

        # Calculate the sum of the squared differences
        euc_dist = (sum(
            ((image1.get_pixel(i, j)[x] - image2.get_pixel(i, j)[x]) ** 2)
            for i in range(image1.num_rows)
            for j in range(image1.num_cols)
            for x in range(3)))**(0.5)
       
        return euc_dist


    def vote(self, candidates): #passes terminal tests
        """
        Returns the most frequent label in the given list

        >>> knn = ImageKNNClassifier(3)
        >>> knn.vote(['label1', 'label2', 'label2', 'label2', 'label1'])
        'label2'
        """
        if not candidates:
            return None

        count = {}
        for label in candidates:
            if label in count:
                count[label] += 1
            else:
                count[label] = 1
        popular = max(count, key=lambda k: count[k])
        return popular


    def predict(self, image):
        """
        Predicts the label of the given image using the labels of
        the K closest neighbors to this image

        The test for this method is located in the knn_tests method below
        """
        if not self.data:
            raise ValueError()

        distance = [(self.distance(image, training), label) for training, label in self.data]
        distance.sort(key=lambda x: x[0])
        knn = [label for i, label in distance[:self.k_neighbors]]
        prediction = self.vote(knn)
        return prediction



def knn_tests(test_img_path):
    """
    Function to run knn tests

    >>> knn_tests('img/knn_test_img.png')
    'nighttime'
    """
    # Read all of the sub-folder names in the knn_data folder
    # These will be treated as labels
    path = 'knn_data'
    data = []
    for label in os.listdir(path):
        label_path = os.path.join(path, label)
        # Ignore non-folder items
        if not os.path.isdir(label_path):
            continue
        # Read in each image in the sub-folder
        for img_file in os.listdir(label_path):
            train_img_path = os.path.join(label_path, img_file)
            img = img_read_helper(train_img_path)
            # Add the image object and the label to the dataset
            data.append((img, label))

    # Create a KNN-classifier using the dataset
    knn = ImageKNNClassifier(5)

    # Train the classifier by providing the dataset
    knn.fit(data)

    # Create an RGBImage object of the tested image
    test_img = img_read_helper(test_img_path)

    # Return the KNN's prediction
    predicted_label = knn.predict(test_img)
    return predicted_label
"""

"""
