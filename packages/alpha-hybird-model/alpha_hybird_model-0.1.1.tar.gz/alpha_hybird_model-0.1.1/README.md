
# Alpha Hybrid Model

[![PyPI Version](https://img.shields.io/pypi/v/alpha_hybird_model.svg)](https://pypi.org/project/alpha_hybird_model/)
[![Python Versions](https://img.shields.io/pypi/pyversions/alpha_hybird_model.svg)](https://pypi.org/project/alpha_hybird_model/)
[![License](https://img.shields.io/pypi/l/alpha_hybird_model.svg)](https://github.com/yourusername/alpha_hybird_model/blob/main/LICENSE)

A Python package for training a multi-branch Convolutional Neural Network (CNN) model that combines **ResNet50V2** and **DenseNet169** architectures for image classification tasks.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Installation via Pip](#installation-via-pip)
- [Usage](#usage)
  - [Command-Line Interface](#command-line-interface)
    - [Basic Usage](#basic-usage)
    - [Options](#options)
    - [Help](#help)
  - [Examples](#examples)
  - [Data Preparation](#data-preparation)
- [Programmatic Usage](#programmatic-usage)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Contributing](#contributing)
  - [Reporting Issues](#reporting-issues)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

---

## Introduction

**Alpha Hybrid Model** is a Python package designed for image classification tasks using a hybrid approach that combines the strengths of ResNet50V2 and DenseNet169 architectures. By integrating these two powerful models, the Alpha Hybrid Model aims to improve classification performance through enhanced feature extraction.

---

## Features

- **Hybrid Architecture**: Combines ResNet50V2 and DenseNet169 for superior feature extraction.
- **Data Augmentation**: Implements various augmentation techniques to improve model generalization.
- **Early Stopping & Learning Rate Reduction**: Includes callbacks for early stopping and learning rate reduction on plateau.
- **Command-Line Interface**: Easy-to-use CLI for training and evaluation.
- **Customizable Hyperparameters**: Adjust learning rate, batch size, epochs, and more.
- **Training History Plotting**: Option to visualize training and validation accuracy and loss.

---

## Installation

### Prerequisites

- **Python**: Version 3.6 or higher.
- **TensorFlow**: Version 2.x.
- **pip**: Latest version recommended.

### Installation via Pip

Install the package directly from PyPI:

```bash
pip install alpha_hybird_model
```

**Note**: It's recommended to use a virtual environment to avoid dependency conflicts.

---

## Usage

### Command-Line Interface

After installation, the `alpha_hybird_train` command becomes available.

#### Basic Usage

```bash
alpha_hybird_train --train_dir PATH_TO_TRAIN_DIR --val_dir PATH_TO_VAL_DIR [OPTIONS]
```

#### Options

- `--train_dir`: **(Required)** Path to the training data directory.
- `--val_dir`: **(Required)** Path to the validation data directory.
- `--epochs`: Number of epochs to train (default: 50).
- `--batch_size`: Batch size for training (default: 8).
- `--initial_lr`: Initial learning rate (default: 1e-4).
- `--output_dir`: Directory to save model weights and outputs (default: `./`).
- `--plot`: Include this flag to plot training history after training.

#### Help

For detailed usage instructions:

```bash
alpha_hybird_train --help
```

### Examples

#### Example 1: Basic Training

```bash
alpha_hybird_train   --train_dir ./data/train   --val_dir ./data/val   --epochs 25   --batch_size 16
```

#### Example 2: Training with Custom Learning Rate and Output Directory

```bash
alpha_hybird_train   --train_dir ./data/train   --val_dir ./data/val   --epochs 30   --batch_size 32   --initial_lr 5e-5   --output_dir ./model_outputs   --plot
```

### Data Preparation

Organize your dataset as follows:

```
dataset/
├── train/
│   ├── class1/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── class2/
│       ├── image1.jpg
│       ├── image2.jpg
│       └── ...
└── val/
    ├── class1/
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    └── class2/
        ├── image1.jpg
        ├── image2.jpg
        └── ...
```

- **Classes**: Each class should have its own subdirectory.
- **Training and Validation Data**: Separate directories for training and validation datasets.

---

## Programmatic Usage

You can also use the package within your Python scripts:

```python
from alpha_hybird_model import build_model, plot_training_history
import tensorflow as tf

# Build the model
model = build_model(input_shape=(224, 224, 3), num_classes=2)

# Compile the model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Proceed with custom training loop or other tasks
```

---

## Project Structure

```
alpha_hybird_model/
├── alpha_hybird_model/
│   ├── __init__.py
│   ├── model.py
│   └── utils.py
├── scripts/
│   └── train_model.py
├── setup.py
├── README.md
├── LICENSE
└── requirements.txt
```

- **alpha_hybird_model/**: Core package containing the model and utility functions.
- **scripts/**: Contains the command-line script `train_model.py`.
- **setup.py**: Configuration file for packaging.
- **README.md**: Comprehensive documentation.
- **LICENSE**: License information.
- **requirements.txt**: List of package dependencies.

---


##Benfits of Alpha_Hybird_Model 

Benefits of the Alpha Hybrid Model Over Traditional CNNs
The Alpha Hybrid Model is a multi-branch CNN that combines ResNet50V2 and DenseNet169 architectures. By leveraging the unique strengths of these architectures, the Alpha Hybrid Model provides several advantages over traditional CNNs:

Enhanced Feature Extraction:

ResNet50V2 and DenseNet169 are state-of-the-art architectures that use different methodologies for feature extraction. ResNet50V2 utilizes skip connections to avoid the vanishing gradient problem, allowing deeper layers without performance loss. DenseNet169, on the other hand, promotes feature reuse through dense connections, enabling efficient learning of both high- and low-level features.
By combining these models, Alpha Hybrid Model achieves richer feature extraction, capturing a wide range of patterns and enhancing model performance in complex classification tasks.
Improved Generalization with Multi-Branch Architecture:

The hybrid approach in the Alpha Hybrid Model merges the outputs of both architectures. This fusion acts as a built-in ensemble, increasing the model's robustness and reducing overfitting. This is especially advantageous in datasets with high variability, as the model learns diverse representations from both ResNet and DenseNet branches.
The model's design also enables better handling of minor variations in input data, improving accuracy and generalization across unseen samples.
Moderate Regularization for Stability:

The Alpha Hybrid Model employs L2 regularization and dropout to reduce overfitting, leading to a more stable and reliable model. Dropout layers encourage the model to be resilient to small feature variations, and L2 regularization helps prevent excessively high weights, which can improve generalization.
Efficient Training with Adaptive Learning Rate:

The model includes callbacks for early stopping and learning rate reduction on plateau, allowing adaptive learning throughout training. This setup helps prevent overtraining and optimizes the model's training time, focusing on valuable epochs for learning and stopping once minimal improvements are detected.
Higher Accuracy and Faster Convergence:

Combining ResNet50V2 and DenseNet169 has shown improvements in classification accuracy compared to using either architecture alone. The model also converges faster due to its dual-branch structure and adaptive learning approach, making it suitable for scenarios requiring efficient training and high performance.
Versatility for Real-World Applications:

The Alpha Hybrid Model’s ability to capture detailed features makes it well-suited for various applications, including medical imaging, object detection, and other fields requiring high precision and adaptability.
By utilizing this hybrid approach, the Alpha Hybrid Model outperforms traditional CNNs and single-architecture models, particularly in complex classification tasks where both low-level and high-level features are crucial. This unique architecture allows users to achieve robust performance with reduced risk of overfitting, making it a powerful choice for image classification tasks.

## Documentation

For more detailed information, please refer to the [GitHub repository](https://github.com/ihtesham-jahangir/alpha_hybird_model).

---

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the Repository**: Create your own fork of the project on GitHub.

2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/ihtesham-jahangir/alpha_hybird_model.git
   ```

3. **Create a Feature Branch**:

   ```bash
   git checkout -b feature/YourFeature
   ```

4. **Commit Your Changes**:

   ```bash
   git commit -am 'Add a new feature'
   ```

5. **Push to Your Fork**:

   ```bash
   git push origin feature/YourFeature
   ```

6. **Submit a Pull Request**: Open a pull request to the main repository.

### Reporting Issues

If you encounter any problems, please [open an issue](https://github.com/ihtesham-jahangir/alpha_hybird_model/issues).

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Contact

- **Author**: ihtesham jahangir
- **Email**: [ihteshamjahangir21@gmail.com](mailto:ihteshamjahangir21@gmail.com)
- **GitHub**: [ihtesham-jahangir](https://github.com/ihtesham-jahangir)

---

## Acknowledgments

- **TensorFlow Community**: For providing a powerful deep learning framework.
- **Keras Team**: For simplifying deep learning model development.
- **Researchers and Contributors**: Behind ResNet and DenseNet architectures.
- **Open Source Community**: For fostering collaboration and innovation.

---

*This README provides comprehensive information about the Alpha Hybrid Model package, ensuring users have all the necessary details to install, use, and contribute to the project.*

---


