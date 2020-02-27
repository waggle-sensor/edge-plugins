import sys
import os

import torch
from torchvision.models.segmentation import fcn_resnet101

class FCN(torch.nn.Module):
    def __init__(self, n_class=2):
        super(FCN, self).__init__()
        self.fcn = fcn_resnet101(pretrained=False, num_classes=2)
    def forward(self, x, debug=False):
        return self.fcn(x)['out']
#checkpoint = torch.load('/storage/fcn/model_best.pth.tar')
#model = checkpoint['model']
#model.load_state_dict(checkpoint['model_state_dict'])
'''
model = torch.hub.load('pytorch/vision:v0.4.2', 'fcn_resnet101', pretrained=True)
#model.eval()    ### set in evaluation mode
model.train()    ### set in train mode
'''
#model.eval()
model = FCN()
checkpoint = torch.load('/storage/fcn/sp_fcn_pytorch/logs/MODEL-resnet101/model_best.pth.tar')
print(checkpoint['arch'])
model.load_state_dict(checkpoint['model_state_dict'])
#optimizer.load_state_dict(checkpoint['optimizer'])
#model.eval()

from PIL import Image
from torchvision import transforms

def run(file_path, model):
    print(os.path.dirname(file_path))
    output_base = os.path.dirname(file_path)
    output_name = os.path.basename(file_path) + "_out.jpg"
    output_path = os.path.join(output_base, output_name)
    input_image = Image.open(file_path)
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model
    # move the input and model to GPU for speed if available
    if torch.cuda.is_available():
       input_batch = input_batch.to('cuda')
       model.to('cuda')
    with torch.no_grad():
        output = model(input_batch)[0]

    print(output.shape)
    print(output[0].min())
    print(output[0].max())
    print(output[1].min())
    print(output[1].max())
    print(output.argmax(0).shape)
    print(output.argmax(0).min())

    output_predictions = output.argmax(0)


    count = 0
    for i in range(len(output_predictions)):
        for j in range(len(output_predictions[0])):
            if output_predictions[i][j] != 1:
                count += 1
    print(count)


    print(output_predictions)
    # create a color pallette, selecting a color for each class
    palette = torch.tensor([2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1])
    colors = torch.as_tensor([i for i in range(21)])[:, None] * palette
    colors = (colors % 255).numpy().astype("uint8")
    # plot the semantic segmentation predictions of 21 classes in each color
    r = Image.fromarray(output_predictions.byte().cpu().numpy()).resize(input_image.size)
    r.putpalette(colors)
    r.convert('RGB').save(output_path)

run(sys.argv[1], model)

