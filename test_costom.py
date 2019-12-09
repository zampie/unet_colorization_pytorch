import argparse
import os
import random
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim as optim
import torch.utils.data
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torchvision.utils as vutils
import numpy as np
import matplotlib.pyplot as plt
import torch.functional as F
from unet_model import UNet
# from model_PaintsChainer import UNet
from data_loader import Img_tran_AB, SimpleImageFolder
from PIL import Image

if __name__ == '__main__':

    # image_size = 256  # All images will be resized to this size using a transformer.

    # Root directory for dataset
    # filename = './7.jpg'
    # filename = './derori_san.jpg'
    filename = './imomushi_san.jpg'


    ckpt_path = './samples_0/ckpt_200000.tar'

    img = Image.open(filename)
    img = img.convert('L')

    # device = torch.device("cpu")
    device = torch.device("cuda:0" if (torch.cuda.is_available()) else "cpu")

    transform = transforms.Compose([
        # transforms.Resize(image_size),
        # transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,)),
    ])

    img = transform(img)
    img = img.unsqueeze(0)


    def get_layer_param(model):
        return sum([torch.numel(param) for param in model.parameters()])


    net = UNet(1, 3).to(device)
    print(net)
    print('parameters:', get_layer_param(net))

    print("Loading checkpoint...")
    checkpoint = torch.load(ckpt_path)
    net.load_state_dict(checkpoint['net_state_dict'])
    net.eval()

    print("Starting Test...")
    # -----------------------------------------------------------
    # Initial batch
    data_A = img.to(device)
    # -----------------------------------------------------------
    # Generate fake img:
    fake_B = net(data_A)
    # -----------------------------------------------------------
    # Output training stats
    # vutils.save_image(data_A, os.path.join(samples_path, 'result', '%s_data_A.jpg' % str(i).zfill(6)),
    #                   padding=2, nrow=2, normalize=True)
    vutils.save_image(fake_B, os.path.join('./', '%s_fake_B_leaky.jpg' % filename[0:-4]),
                      padding=0, nrow=1, normalize=True)

    print("Finished")
