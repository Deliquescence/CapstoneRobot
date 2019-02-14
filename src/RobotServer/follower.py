from fastai.vision import *
import cv2


class Follower:
    def __init__(self):
        self.model = load_learner("models", fname="supervised.pkl")

    def get_action(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = PIL.Image.fromarray(img)
        img = pil2tensor(img, np.float32)
        img.div_(255)
        result = self.model.predict(Image(img))
        return result[0]


if __name__ == '__main__':
    follower = Follower()
    image = cv2.imread("C:/Code/Senior Project/train/mirrorB_2605.jpg")

    print(follower.get_action(image))
