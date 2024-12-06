# Angular Deviation Diffuser

## Overview

**Angular Deviation Diffuser** is a transformer-based diffusion model designed for efficiently generating conformational ensembles of protein backbones by using angular deviations as data flow. It aims to overcome the limitations of traditional molecular dynamics (MD) simulations by providing a fast and computationally efficient approach for sampling protein conformational landscapes. This model leverages the concepts of SE(3) symmetry, angular deviations, and diffusion processes to produce dynamic ensembles that closely match those generated through MD simulations, thereby offering a new way to study protein structure and function.

## Background

Protein dynamics are essential for understanding biological functionality, as proteins exist not only in a single static structure but also in multiple dynamic conformational states. MD simulations are the gold standard for studying these dynamics, but they are resource-intensive and limited in their ability to fully explore all possible conformational states. The Angular Deviation Diffuser addresses these limitations by utilizing advanced deep learning techniques, specifically a diffusion model integrated with SE(3) invariance, to efficiently generate accurate protein conformations.

## Features

- **Angular Deviation-Based Diffusion**: Uses angular deviations rather than absolute angles for data representation, improving stability and efficiency.
- **Transformer Backbone**: Utilizes a transformer architecture for learning protein dynamics from training data, capturing the conformational space effectively.
- **SE(3) Symmetry Integration**: Ensures the generated conformations respect the inherent rotational and translational symmetry of molecular systems.
- **Efficient Ensemble Generation**: Capable of generating diverse conformational ensembles in significantly less time compared to traditional MD simulations.

## Installation

To use Angular Deviation Diffuser, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Angular-Deviation-Diffuser.git
   cd Angular-Deviation-Diffuser
   ```
2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The following steps outline how to use the code to generate protein conformations:

1. **Data Preparation**: Extract the backbone angles (φ, ψ, ω) and bond angles (θ₁, θ₂, θ₃) from MD simulations. Calculate angular deviations relative to a reference structure.
2. **Training the Model**: Train the transformer-based diffusion model using the angular deviation data extracted in the previous step.
   
3. **Generating Conformations**: Generate a diverse ensemble of protein backbone conformations using the trained model.
   
4. **Adding Side Chains**: Use PyRosetta to add side chains to the generated backbone structures.
   


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to our research team for their contributions and support throughout the development of this model.

