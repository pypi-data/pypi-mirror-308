import pytest

import torch.nn as nn
from torchvision.models import resnet18

from pytorch_rse.rse import RSE, AddGaussianNoise

def validate_modified_model(model):
    """
    Validates that all nn.Conv2d layers in the model (excluding skip connections)
    are wrapped in an nn.Sequential and preceded by an AddGaussianNoise layer.

    Args:
        model (nn.Module): The modified model to validate.
    
    Returns:
        bool: True if the model is correctly modified, False otherwise.
    """
    for name, module in model.named_modules():
        # Skip layers named 'downsample' or their submodules
        if "downsample" in name:
            continue

        if isinstance(module, nn.Conv2d):
            # Check the parent module for nn.Sequential wrapping
            parent_name = name.rsplit('.', 1)[0]  # Get parent module name
            parent = dict(model.named_modules()).get(parent_name, None)
            
            if not isinstance(parent, nn.Sequential):
                print(f"Error: {name} is not wrapped in an nn.Sequential.")
                return False
            
            # Check for AddGaussianNoise before the Conv2d layer
            seq_children = list(parent.children())
            if not isinstance(seq_children[0], AddGaussianNoise):
                print(f"Error: AddGaussianNoise is not present before {name}.")
                return False

    print("Model validation passed!")
    return True



import pytest
from torchvision import models
import torch.nn as nn

def test_rse_wrapping():
    """
    Test the RSE wrapping and validation on a set of PyTorch models.
    """

    # List of models to test
    models_to_test = [
    # ResNet Family
        models.resnet18(),
        models.resnet34(),
        models.resnet50(),
        models.resnet101(),
        models.resnet152(),
        
        # VGG Family
        models.vgg11(),
        models.vgg13(),
        models.vgg16(),
        models.vgg19(),
        
        # MobileNet
        models.mobilenet_v2(),
        models.mobilenet_v3_large(),
        models.mobilenet_v3_small(),
        
        # DenseNet Family
        models.densenet121(),
        
        # EfficientNet Family
        models.efficientnet_b0(),
        models.efficientnet_b1(),
        
        # SqueezeNet
        models.squeezenet1_0(),
        models.squeezenet1_1(),
        
        # ShuffleNet
        models.shufflenet_v2_x0_5(),
        
        # AlexNet
        models.alexnet(),
        
        # ConvNeXt Family
        models.convnext_tiny(),
        
        # Vision Transformer (ViT)
        models.vit_b_16(),
        
        # RegNet Family
        models.regnet_y_400mf(),
    ]

    for model in models_to_test:
        # Wrap the model with RSE
        wrapped_model = RSE(model, std_devs=(0.1, 0.1))

        # Validate the modified model
        assert validate_modified_model(wrapped_model), f"Model {model.__class__.__name__} failed validation."





if __name__ == "__main__":
    model = resnet18()
    
    rse_model = RSE(model)
    print(rse_model)

    validate_modified_model(rse_model)
