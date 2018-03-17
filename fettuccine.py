import sys
import argparse
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

class Fettuccine:
    def __init__(self, image_path, width=1, iterations=2):
        self.original_image_path = image_path
        self.width = width
        self.iterations = iterations
        self.merge_mode = 0

        self.original_image_array = np.empty(shape=[0, 0])
        self.final_image_array = np.empty(shape=[0, 0])
        self.even = np.empty(shape=[0, 0])
        self.odd = np.empty(shape=[0, 0])

        self.load_image()

    def load_image(self):
        self.original_image_array = np.array(Image.open(self.original_image_path))
        self.final_image_array = self.original_image_array

    def make_noodles(self):
        '''
        https://stackoverflow.com/questions/38347664/selecting-every-alternate-group-of-n-columns-numpy
        '''
        if self.merge_mode == 1:
            self.odd = self.final_image_array[:, np.mod(np.arange(self.final_image_array.shape[1]),
                                                        2 * self.width) < self.width]
            self.even = self.final_image_array[:, np.mod(np.arange(self.final_image_array.shape[1]),
                                                         2 * self.width) >= self.width]
        else:
            self.odd = self.final_image_array[np.mod(np.arange(self.final_image_array.shape[0]),
                                                     2 * self.width) < self.width, :]
            self.even = self.final_image_array[np.mod(np.arange(self.final_image_array.shape[0]),
                                                      2 * self.width) >= self.width, :]

    def merge_images(self):
        self.final_image_array = np.concatenate((self.odd, self.even), axis=self.merge_mode)
        self.update_merge_mode()

    def update_merge_mode(self):
        if self.merge_mode == 1:
            self.merge_mode = 0
        else:
            self.merge_mode = 1

    def run(self):
        print("Image: {0}".format(self.original_image_path))
        print("Width: {0}".format(self.width))
        print("Iterations: {0}".format(self.iterations))

        for i in range(self.iterations):
            self.make_noodles()
            self.merge_images()

        plt.imshow(self.final_image_array)
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Make image fettuccine. \
                    https://www.reddit.com/r/videos/comments/84whqs/didnt_knew_shredding_could_do_this/')
    parser.add_argument('-i', '--image', required=True,
                        help='Path of the image file. Required.')
    parser.add_argument('-w', '--width', type=int, default=1,
                        help='With of the fettuccine noodle. Default is 1.')
    parser.add_argument('-n', '--iterations', type=int, default=2,
                        help='How many images do you want to generate? Default is 2.')

    args = parser.parse_args()

    try:
        fettuccine = Fettuccine(image_path=args.image, width=args.width, iterations=args.iterations)
        fettuccine.run()
    except FileNotFoundError:
        print("File not found. {0}".format(args.image))
        sys.exit()
