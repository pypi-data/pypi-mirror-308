import warnings


warnings.filterwarnings("ignore", category=FutureWarning)

import torch
import math
from tqdm import tqdm
from model import FoldingDiff
from util import wrap
import numpy as np
import os


DEFAULT_MU = [
    -0.0056, -0.0255, 0.1337, 0.0090, -0.0026, 0.0020
]






def generate_conformations(ckpt='model_para.ckpt',timepoints=1000,num_residues=147,batch_size=10,mu=DEFAULT_MU,output='sample_trajectory.npy',total_samples=10,reference='reference_confor.npy'):



    T = timepoints
    mu = torch.tensor(mu).float()
    if not os.path.exists(reference):
        raise FileNotFoundError(f"No reference file found at {reference}")
    reference_ = torch.from_numpy(np.load(reference)).float()
    reference_.nan_to_num_(0.0)

    # Load model
    model = FoldingDiff()

    state_dict = torch.load(ckpt, map_location=torch.device('cpu'))['state_dict']
    model.load_state_dict(state_dict)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    s = 8e-3
    t = torch.arange(T + 1)
    f_t = torch.cos((t / T + s) / (1 + s) * math.pi / 2.0).square()
    alpha_bar = f_t / f_t[0]
    beta = torch.cat([torch.tensor([0.0]), torch.clip(1 - alpha_bar[1:] / alpha_bar[:-1], min=1e-5, max=1 - 1e-5)])

    alpha = 1 - beta

    total_batches = math.ceil(total_samples / batch_size)

    trajectory = []
    with torch.no_grad():
        for batch_idx in tqdm(range(total_batches), desc='sampling batches',leave=False):

            current_batch_size = batch_size if batch_idx < total_batches - 1 else total_samples % batch_size or batch_size

            if current_batch_size == 0:
                break

            random_init = torch.randn(current_batch_size, num_residues, 6).to(device)
            x = wrap(random_init)

            for t in tqdm(range(T, 0, -1), desc='sampling', leave=False):

                sigma_t = math.sqrt((1 - alpha_bar[t - 1]) / (1 - alpha_bar[t]) * beta[t])

                # Sample from N(0, sigma_t^2)
                if t > 1:
                    z = torch.randn(current_batch_size, num_residues, 6).to(device) * sigma_t * 0.0015


                else:
                    z = torch.zeros(current_batch_size, num_residues, 6).to(device)

                # Update x
                t_tensor = torch.tensor([t]).long().unsqueeze(0).to(device)
                out = model(x, t_tensor).cpu()
                out_ = 1 / math.sqrt(alpha[t]) * (x - beta[t] / math.sqrt(1 - alpha_bar[t]) * out) + z
                x = wrap(out_.to(device))
                x_ = out_ + reference_.to(device)

                if t == 1:
                    trajectory.append(x_.unsqueeze(1))
    trajectory = wrap(torch.cat(trajectory, dim=1) + mu)
    np.save(output, trajectory.numpy())

