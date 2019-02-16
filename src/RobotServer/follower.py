from fastai.vision import *
import cv2
import time


class Follower:
    def __init__(self):
        self.model = load_learner("models", fname="supervised.pkl")

    def get_action(self, frame):
        start_time = time.time()

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = PIL.Image.fromarray(img)
        img = pil2tensor(img, np.float32)
        img.div_(255)
        result = self.model.predict(Image(img))

        duration = time.time() - start_time
        #print(f"Prediction took {duration}")
        return result[1]


if __name__ == '__main__':
    follower = Follower()
    image = cv2.imread("C:/Code/Senior Project/train/mirrorB_2605.jpg")
    action = follower.get_action(image)
    print(action[0].item())
    print(action[1].item())
