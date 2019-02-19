from fastai.vision import *
import cv2
import time

# From fastai
def conv_bn_lrelu(ni:int, nf:int, ks:int=3, stride:int=1)->nn.Sequential:
    "Create a seuence Conv2d->BatchNorm2d->LeakyReLu layer."
    return nn.Sequential(
        nn.Conv2d(ni, nf, kernel_size=ks, bias=False, stride=stride, padding=ks//2),
        nn.BatchNorm2d(nf),
        nn.LeakyReLU(negative_slope=0.1, inplace=True))

class ResLayer(nn.Module):
    "Resnet style layer with `ni` inputs."
    def __init__(self, ni:int):
        super().__init__()
        self.conv1=conv_bn_lrelu(ni, ni//2, ks=1)
        self.conv2=conv_bn_lrelu(ni//2, ni, ks=3)

    def forward(self, x): return x + self.conv2(self.conv1(x))

# From fastai, modified head
class CustomDarknet(nn.Module):
    "https://github.com/pjreddie/darknet"

    def make_group_layer(self, ch_in: int, num_blocks: int, stride: int = 1):
        "starts with conv layer - `ch_in` channels in - then has `num_blocks` `ResLayer`"
        return [conv_bn_lrelu(ch_in, ch_in * 2, stride=stride)
                ] + [(ResLayer(ch_in * 2)) for i in range(num_blocks)]

    def __init__(self, num_blocks: Collection[int], num_classes: int, nf=32):
        "create darknet with `nf` and `num_blocks` layers"
        super().__init__()
        layers = [conv_bn_lrelu(3, nf, ks=3, stride=1)]
        for i, nb in enumerate(num_blocks):
            layers += self.make_group_layer(nf, nb, stride=2 - (i == 1))
            nf *= 2
        layers += [nn.AdaptiveAvgPool2d(1), Flatten(), nn.Linear(nf, num_classes)]
        layers += [nn.Linear(num_classes, 2), SigmoidRange(-1, 1)]
        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        return self.layers(x)

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
    #image = cv2.imread("~/Pictures/mirrorB_2605.jpg")
    camera = cv2.VideoCapture(0)
    _, image = camera.read()
    action = follower.get_action(image)
    print(action[0].item())
    print(action[1].item())
