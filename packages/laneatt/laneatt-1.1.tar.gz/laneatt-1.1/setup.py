from distutils.core import setup
setup(
  name = 'laneatt',
  packages = ['laneatt', 'laneatt.utils'],
  version = '1.1',
  license='MIT',
  description = 'A package to detect lane lines in images and videos',
  author = 'Paolo Reyes',
  author_email = 'paolo.alfonso.reyes@gmail.com',
  url = 'https://github.com/PaoloReyes/RealTime-LaneATT',
  download_url = 'https://github.com/PaoloReyes/RealTime-LaneATT/archive/refs/tags/LaneATT-v1.0.tar.gz',
  keywords = ['lanes', 'AI', 'greenhouse', 'detection', 'machine', 'learning', 'laneatt', 'lane', 'lines', 'line'],
  install_requires=[
          'filelock',
          'fsspec',
          'Jinja2',
          'joblib',
          'MarkupSafe',
          'mpmath',
          'networkx',
          'numpy',
          'nvidia-cublas-cu12',
          'nvidia-cuda-cupti-cu12',
          'nvidia-cuda-nvrtc-cu12',
          'nvidia-cuda-runtime-cu12',
          'nvidia-cudnn-cu12',
          'nvidia-cufft-cu12',
          'nvidia-curand-cu12',
          'nvidia-cusolver-cu12',
          'nvidia-cusparse-cu12',
          'nvidia-nccl-cu12',
          'nvidia-nvjitlink-cu12',
          'nvidia-nvtx-cu12',
          'opencv-python',
          'pillow',
          'PyYAML',
          'scikit-learn',
          'scipy',
          'setuptools',
          'sympy',
          'threadpoolctl',
          'torch',
          'torchaudio',
          'torchvision',
          'tqdm',
          'triton',
          'typing_extensions',
          'wheel',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable', # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers', # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License', # License

    'Programming Language :: Python :: 3', # Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.12',
  ],
)