import os

import torch

from cats_classifier import load_model


model_cls_checkpoint = os.getenv('MODEL_ISCAT_ABS_PATH')
cls_model = load_model(model_cls_checkpoint)

epsilons = [0, .05, .1, .15, .2, .25, .3]


def fgsm_attack(image, epsilon, data_grad):
    # Collect the element-wise sign of the data gradient
    sign_data_grad = data_grad.sign()
    # Create the perturbed image by adjusting each pixel of the input image
    perturbed_image = image + epsilon*sign_data_grad
    # Adding clipping to maintain [0,1] range
    perturbed_image = torch.clamp(perturbed_image, 0, 1)
    # Return the perturbed image
    return perturbed_image

