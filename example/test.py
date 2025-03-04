import os
import torch
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from example.networks.config import parse_options
from example.networks.mlp import MLPNet
from DualMeshUDF import extract_mesh, write_obj
from example.neural_utils import udf_from_mlp, udf_and_grad_from_mlp


if __name__ == "__main__":

    ## load config
    args_parser = parse_options(True)
    args = args_parser.parse_args()

    ## load device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    ## load network
    net = MLPNet(args).to(device)

    if args.pretrained:
        net.load_state_dict(torch.load(args.pretrained))

    ## load functions
    udf_func = udf_from_mlp(net, device)
    udf_grad_func = udf_and_grad_from_mlp(net, device)

    ## get mesh
    mesh_v, mesh_f = extract_mesh(udf_func, udf_grad_func)
    exp_name = ((args.pretrained).split('/')[-1]).replace('.pth','')
    if not os.path.exists(args.mesh_prefix):
        os.makedirs(args.mesh_prefix)
    mesh_name = f'{args.mesh_prefix}{exp_name}.obj'
    write_obj(mesh_name, mesh_v, mesh_f)


    

        
