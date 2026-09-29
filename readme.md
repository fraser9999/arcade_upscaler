
 Arcade Upscaler — README

# 🕹️ Arcade Upscaler

 **arcade\_upscaler** is a modular Python upscaler designed for small **retro graphics, arcade sprites, and pixel art**.

 The project is specifically designed for images where the **logical pixel/block size** should first be detected. The image can then be reduced to its actual low-resolution representation and subsequently upscaled to 4x or 8x using a neural **ESRGAN/RRDB model**.

 In addition, the project provides simple pixel-art scaling methods and optional post-processing for edge smoothing.

---

 ## ✨ Features

 - 🔍 **Automatic Pixel/Block Size Detection**
  - Analysis of connected image regions
  - Detection of a frequently occurring block size
  - Particularly useful for heavily upscaled retro sprites
- 🧩 **Reduction to Logical Resolution**
  - Reconstructs the smaller original structure from an upscaled sprite
  - Uses `PIL.Image.Resampling.BOX`
- 🤖 **ESRGAN 4x Upscaling**
  - Integrated RRDBNet architecture
  - No external ESRGAN Python implementation required
  - Pre-trained `.pth` weights can be loaded directly
- 🔗 **ESRGAN 8x Chaining**
  - First pass: 4x
  - Second pass: another 4x
  - The resulting 16x image is then reduced to exactly 8x using Lanczos
  - Provides a flexible 8x processing pipeline
- 🕹️ **HQx-Style Upscaling**
  - Fast integer scaling using OpenCV
  - Supports 2x, 3x, and 4x scaling factors
  - Currently uses `INTER_NEAREST` to preserve hard pixel structures
- 🧼 **Edge Smoothing**
  - Gaussian Blur
  - Median Filter
  - The Median Filter is particularly useful for pixel art and flat sprite graphics
- ⚡ **CUDA Support**
  - ESRGAN automatically detects an available NVIDIA CUDA GPU
  - Falls back to CPU when CUDA is unavailable
- 📦 **Modular Architecture**
  - Individual functions can be imported directly into other Python projects

---

 ## 🖼️ Typical Workflow

 The main strength of the project is working with already **upscaled retro sprites**.

 For example, a sprite with a visible block structure can first be analyzed:

```
Large Image
    │
    ▼
Block Size Analysis
    │
    ▼
Detected Logical Pixel Size
    │
    ▼
Reduction to Low Resolution
    │
    ▼
ESRGAN 4x / 8x
    │
    ▼
Median / Edge Smoothing
    │
    ▼
High-Resolution Arcade Sprite
```

 This means the image is not simply enlarged again from an already artificially upscaled version. Instead, the pipeline first attempts to reconstruct the underlying logical pixel structure.

---

 # 📁 Project Structure

```
arcade_upscaler/
│
├── aracde_upscaler.py       # Main program / interactive pipeline
│
├── blocksize.py             # Pixel/block size detection
├── distances.py             # Distance grouping and analysis
├── reduce.py                # Reduction to logical low resolution
├── hqx.py                   # Fast HQx-style upscaling
│
├── esrgan_x4.py             # RRDBNet / ESRGAN 4x upscaler
├── esrgan_x8_chain.py       # ESRGAN 8x chaining
├── smooth.py                # Gaussian and Median smoothing
│
├── RRDB_ESRGAN_x4.pth       # Required model weights (not included)
│
├── requirements.txt
└── README.md
```

 > **Note:** The file `aracde_upscaler.py` is written this way in the original package and contains a historical typo in the filename. For a new GitHub repository, it can be renamed to `arcade_upscaler.py` if desired.

---

 # 🛠️ Installation

 ## 1\. Clone the Repository

```
git clone https://github.com/YOUR-USERNAME/arcade_upscaler.git
cd arcade_upscaler
```

 ## 2\. Create a Virtual Environment

 ### Windows

```
python -m venv venv
venv\Scripts\activate
```

 ### Linux / macOS

```
python3 -m venv venv
source venv/bin/activate
```

 ## 3\. Install Dependencies

```
pip install -r requirements.txt
```

---

 # 🤖 ESRGAN Model

 The ESRGAN functionality requires a compatible **RRDB\_ESRGAN\_x4 `.pth` model**.

 The model architecture is already included in `esrgan_x4.py`. The weights are loaded when creating the upscaler:

```
upscaler = ESRGANUpscaler(
    model_path="RRDB_ESRGAN_x4.pth"
)
```

 For example, place the model file directly in the project directory:

```
arcade_upscaler/
├── RRDB_ESRGAN_x4.pth
├── esrgan_x4.py
├── ...
```

 **The model weights are not included in this repository.**

---

 # 🚀 Usage

 ## Interactive Main Program

 The main program can be started directly:

```
python aracde_upscaler.py
```

 You will first be asked for an image path:

```
Image >
```

 The program will then automatically attempt to determine the block size.

 After that, you can choose between:

```
4x or 8x Upscaling> (4/8)
```

 The result is then lightly smoothed using a Median Filter.

---

 # 🔬 Using Individual Modules

 ## Detect Block Size

```
from blocksize import find_block_size

block_size = find_block_size("sprite.png")

print(f"Block size: {block_size}x{block_size}")
```

---

 ## Reduce an Image to Its Logical Resolution

```
from reduce import process

small_sprite = process(
    "sprite.png",
    block_size=20
)

small_sprite.save("sprite_lowres.png")
```

 The `BOX` resampling mode is used to average the pixel blocks during reduction.

---

 # 🤖 ESRGAN 4x

```
from esrgan_x4 import ESRGANUpscaler

upscaler = ESRGANUpscaler(
    model_path="RRDB_ESRGAN_x4.pth"
)

upscaler.upscale_image(
    input_path="sprite_lowres.png",
    output_path="sprite_4x.png"
)
```

 The processing device is selected automatically:

```
CUDA available → NVIDIA GPU
CUDA unavailable → CPU
```

 Alternatively, the device can be specified explicitly:

```
upscaler = ESRGANUpscaler(
    model_path="RRDB_ESRGAN_x4.pth",
    device="cuda"
)
```

 or:

```
upscaler = ESRGANUpscaler(
    model_path="RRDB_ESRGAN_x4.pth",
    device="cpu"
)
```

---

 # 🔗 ESRGAN 8x

 The 8x function uses two consecutive 4x passes:

```
Original
   │
   ├── 4x ESRGAN
   │
   ▼
  4x
   │
   ├── 4x ESRGAN
   │
   ▼
 16x
   │
   ├── Lanczos Downsampling
   │
   ▼
  8x
```

 Usage:

```
from esrgan_x8_chain import upscale_8x_chaining

upscale_8x_chaining(
    input_path="sprite_lowres.png",
    output_path="sprite_8x.png",
    model_path="RRDB_ESRGAN_x4.pth"
)
```

---

 # 🕹️ Fast HQx-Style Upscaling

 For very fast scaling without a neural model:

```
from hqx import upscale_hqx

output = upscale_hqx(
    "sprite.png",
    factor=4
)

print(output)
```

 Supported factors:

```
2
3
4
```

 The current module uses OpenCV `INTER_NEAREST`. This preserves hard pixel edges.

---

 # 🧼 Post-Processing

 ## Median Filter

 For pixel art, the Median Filter can be particularly useful:

```
from smooth import smooth_edges_median

img = smooth_edges_median(
    "sprite_4x.png",
    size=3
)

img.save("sprite_4x_smooth.png")
```

 The filter size must be an odd number:

```
3
5
7
...
```

---

 ## Gaussian Blur

 Alternatively, a light Gaussian smoothing pass can be applied:

```
from smooth import smooth_edges_gaussian

img = smooth_edges_gaussian(
    "sprite_4x.png",
    radius=1.0
)

img.save("sprite_4x_gaussian.png")
```

 Small values produce subtle smoothing, while larger values result in a noticeably softer image.

---

 # 💻 Hardware

 ## NVIDIA GPU

 ESRGAN automatically uses CUDA when PyTorch detects a CUDA-capable GPU.

 Check CUDA availability with:

```
import torch

print(torch.cuda.is_available())
```

 If the result is:

```
True
```

 the GPU will be used by default.

 ## CPU

 The project can also be used without an NVIDIA GPU. ESRGAN inference will then run on the CPU.

 For larger images, however, CPU inference is significantly slower.

---

 # 📦 Dependencies

 The project primarily uses:

 | Package | Purpose |
| --- | --- |
| **PyTorch** | ESRGAN/RRDBNet and GPU inference |
| **NumPy** | Image/tensor conversion |
| **Pillow** | Image loading, saving, scaling, and filtering |
| **OpenCV-Python** | Image analysis and fast upscaling |
| **SciPy** | Connected-component analysis |

All required Python packages are listed in:

```
requirements.txt
```

---

 # ⚠️ Notes

 ### Memory Usage

 ESRGAN can generate very large intermediate images during upscaling. In particular, 8x chaining can require significantly more RAM and VRAM than a single 4x pass.

 For very large input images, it is therefore recommended to test with smaller images first.

 ### Pixel Art

 For classic pixel art, it is useful to determine the actual logical resolution first:

```
Upscaled Sprite
       ↓
Determine Block Size
       ↓
Low-Resolution Sprite
       ↓
ESRGAN
       ↓
Post-Processing
```

 Directly applying ESRGAN to an already heavily upscaled pixel-art image can cause the existing block structures to be interpreted as actual image details.

 ### Model Compatibility

 The ESRGAN class expects model weights that are compatible with the implemented `RRDBNet` architecture. Not every `.pth` model is automatically compatible.

---

 # 🧪 Example

 A typical complete workflow looks like this:

```
from blocksize import find_block_size
from reduce import process
from esrgan_x4 import ESRGANUpscaler
from smooth import smooth_edges_median

input_file = "arcade_sprite.png"

# 1. Detect pixel block size
block_size = find_block_size(input_file)

# 2. Reduce to logical resolution
lowres = process(
    input_file,
    block_size=block_size
)

lowres.save("sprite_lowres.png")

# 3. ESRGAN 4x
upscaler = ESRGANUpscaler(
    model_path="RRDB_ESRGAN_x4.pth"
)

upscaler.upscale_image(
    "sprite_lowres.png",
    "sprite_4x.png"
)

# 4. Apply light smoothing
result = smooth_edges_median(
    "sprite_4x.png",
    size=3
)

result.save("sprite_final.png")
```

---

 # 🎮 Target Audience

 The project is particularly useful for:

 - Retro game development
- Arcade remakes
- C64 / Amiga / Atari / arcade graphics
- Pixel art
- Sprite restoration
- Legacy game graphics
- Upscaled screenshots
- Preparing small sprites for modern game engines

---

 # 📜 Project Status

 **arcade\_upscaler – Version 0.1a**

 The project is currently in an early experimental stage.

 The current focus is on:

 - Automatic block-size detection
- Reconstruction of the logical sprite resolution
- ESRGAN 4x upscaling
- ESRGAN 8x chaining
- Pixel-art-oriented post-processing

---

 ## ⭐ The Idea Behind the Project

 Many old arcade and retro graphics are no longer available in their original pixel resolution. Instead, they often exist as already upscaled images or screenshots.

 **arcade\_upscaler** therefore attempts to partially reverse this process:

 > **Large sprite → detect pixel structure → reconstruct logical resolution → neural upscaling → modern sprite**

 The goal is not simply to create a larger image, but to provide a useful starting point for further use in modern retro remakes and arcade projects.