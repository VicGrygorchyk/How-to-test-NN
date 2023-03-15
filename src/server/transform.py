import torchvision.transforms as transforms

NORMALIZE_COEF = 0.5

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(256),
    transforms.ToTensor(),
    transforms.Normalize(mean=[NORMALIZE_COEF, NORMALIZE_COEF, NORMALIZE_COEF],
                         std=[NORMALIZE_COEF, NORMALIZE_COEF, NORMALIZE_COEF] )
])
