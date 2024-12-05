
# Robust VMAF

Robust modification of Video Multimethod Assessment Fusion (VMAF)

## Installation
You should install ffmpeg with VMAF support (guide can be found here https://github.com/netflix/vmaf/blob/master/resource/doc/ffmpeg.md)

## Usage

Example code:
```
from robust_vmaf import RobustVMAF

if __name__ == "__main__":
    rvmaf = RobustVMAF()
    print(rvmaf.predict("example/reference.mp4", "example/DragoToneMap.mp4"))
    print(rvmaf.predict("example/reference.mp4", "example/DragoToneMap.mp4", return_vmaf=False, return_vmaf_neg=False))
```

Output:
```
{'model': np.float32(95.81248), 'vmaf': 112.4708638, 'vmaf_neg': 91.1492206}
95.81248
```

