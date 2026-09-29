import torch
import torch.nn as nn
import numpy as np
from PIL import Image

class ResidualDenseBlock_5C(nn.Module):
    def __init__(self, nf=64, gc=32, bias=True):
        super(ResidualDenseBlock_5C, self).__init__()
        self.conv1 = nn.Conv2d(nf, gc, 3, 1, 1, bias=bias)
        self.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1, bias=bias)
        self.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1, bias=bias)
        self.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1, bias=bias)
        self.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1, bias=bias)
        self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

    def forward(self, x):
        x1 = self.lrelu(self.conv1(x))
        x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
        x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
        x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
        x5 = self.conv5(torch.cat((x, x1, x2, x3, x4), 1))
        return x5 * 0.2 + x

class RRDB(nn.Module):
    def __init__(self, nf, gc=32):
        super(RRDB, self).__init__()
        self.RDB1 = ResidualDenseBlock_5C(nf, gc)
        self.RDB2 = ResidualDenseBlock_5C(nf, gc)
        self.RDB3 = ResidualDenseBlock_5C(nf, gc)

    def forward(self, x):
        out = self.RDB1(x)
        out = self.RDB2(out)
        out = self.RDB3(out)
        return out * 0.2 + x

class RRDBNet(nn.Module):
    def __init__(self, in_nc=3, out_nc=3, nf=64, nb=23, gc=32):
        super(RRDBNet, self).__init__()
        self.conv_first = nn.Conv2d(in_nc, nf, 3, 1, 1, bias=True)
        self.RRDB_trunk = nn.Sequential(*[RRDB(nf, gc) for _ in range(nb)])
        self.trunk_conv = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        self.upconv1 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        self.upconv2 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        self.HRconv = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        self.conv_last = nn.Conv2d(nf, out_nc, 3, 1, 1, bias=True)
        self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

    def forward(self, x):
        fea = self.conv_first(x)
        trunk = self.trunk_conv(self.RRDB_trunk(fea))
        fea = fea + trunk

        fea = self.lrelu(self.upconv1(nn.functional.interpolate(fea, scale_factor=2, mode='nearest')))
        fea = self.lrelu(self.upconv2(nn.functional.interpolate(fea, scale_factor=2, mode='nearest')))
        out = self.conv_last(self.lrelu(self.HRconv(fea)))
        return out

class ESRGANUpscaler:
    def __init__(self, model_path, device=None):
        """
        Initialisiert den ESRGAN 4x-Upscaler.
        :param model_path: Pfad zur .pth Datei mit den Modellgewichten.
        :param device: 'cuda', 'cpu' oder None (automatische Geräteerkennung).
        """
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
            
        # Initialisiere Netzwerkarchitektur für 4x-Modelle
        self.model = RRDBNet(in_nc=3, out_nc=3, nf=64, nb=23, gc=32)
        
        # Gewichte laden
        state_dict = torch.load(model_path, map_location=self.device)
        if 'params' in state_dict:
            state_dict = state_dict['params']
            
        self.model.load_state_dict(state_dict, strict=True)
        self.model.eval()
        self.model.to(self.device)

    def upscale_image(self, input_path, output_path):
        """
        Verarbeitet ein einzelnes Bild und skaliert es hoch.
        :param input_path: Pfad zum Ausgangsbild.
        :param output_path: Zielpfad für das hochskalierte Bild.
        """
        # Bild laden und normalisieren
        img = Image.open(input_path).convert('RGB')
        img_np = np.array(img, dtype=np.float32) / 255.0
        
        # Dimensionen anpassen: (H, W, C) -> (C, H, W) -> (1, C, H, W)
        img_tensor = torch.from_numpy(np.transpose(img_np, (2, 0, 1))).float().unsqueeze(0).to(self.device)
        
        # Inferenz ohne Gradientenberechnung
        with torch.no_grad():
            output_tensor = self.model(img_tensor).data.squeeze().float().cpu().clamp_(0, 1).numpy()
            
        # Zurückkonvertieren: (C, H, W) -> (H, W, C)
        output_np = np.transpose(output_tensor, (1, 2, 0))
        output_img = (output_np * 255.0).round().astype(np.uint8)
        
        # Speichern des hochaufgelösten Bildes
        Image.fromarray(output_img).save(output_path)
