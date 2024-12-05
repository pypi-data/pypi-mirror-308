import argparse
import os

class Options():
    """This class defines options used during both training and prediction"""

    def __init__(self):
        self.initialized = False

    def initialize(self, parser):
        parser.add_argument('-m', '--mode', help='[pred |coreg |train] switch between training, prediction mode and corregistration (which includes prediction)',
                        required=True)
        # model parameters
        parser.add_argument('--netG', type=str, default='resnet', help='[resnet | Unet]')
        parser.add_argument('--netD', type=str, default='PatchGAN', help='[PatchGAN | PixelGAN]')
        parser.add_argument('--ndf', default=128, type=int, help='number of filters in discriminator')
        parser.add_argument('--ngf', default=64, type=int, help='number of filters in generator')
        parser.add_argument('--generatorLR', type=float, default=0.0002, help='learning rate for generator')
        parser.add_argument('--discriminatorLR', type=float, default=0.0002, help='learning rate for discriminator')
        parser.add_argument('--workers', default=32, type=int, help='number of data loading workers')
        parser.add_argument('--lamb', type=float, default=100, help='weight on L1 term in objective')
        parser.add_argument('--checkpoints_dir', type=str, default='./checkpoints', help='experiments are saved here')
        parser.add_argument('--run_dir', type=str, default='./experiment_AC_PET', help='each training outputs are saved here')
        # parser.add_argument('--generatorWeights', type=str, default='./checkpoints/g.pth', help="path to generator weights (to continue training)")
        # parser.add_argument('--discriminatorWeights', type=str, default='./checkpoints/d.pth', help="path to discriminator weights (to continue training)")

        # basic parameters
        parser.add_argument('--direction', type=str, default='image_to_label', help='image_to_label or label_to_image')
        parser.add_argument('--data_path', type=str, default='./data',help='Location of data for training')
        parser.add_argument('--min_pixel', default=1, help='Percentage of minimum non-zero pixels in the cropped label')
        parser.add_argument('--drop_ratio', default=0, help='Probability to drop a cropped area if the label is empty. All empty patches will be dropped for 0 and accept all cropped patches if set to 1')
        parser.add_argument('--increase_factor_data',  default=2, type=int, help='Increase the data number passed in each epoch')
        parser.add_argument('--output', type=str, default='./checkpoints', help='Training checkpoints save directory')
        parser.add_argument('--gpu_id', type=str, default='0', help='gpu id. Use -1 for CPU')
        parser.add_argument('--save_fre', type=int, default=5, help='model weights save frequency')
        parser.add_argument('--val_fre', type=int, default=5, help='execute validation per epoch frequency')

        # dataset parameters
        parser.add_argument('--resample', default=True, help='Decide or not to rescale the images to a new resolution during training')
        parser.add_argument('--new_resolution', default=(3.3, 3.3, 1.645), help='New resolution')
        #parser.add_argument('--min_pixel', default=1, help='Percentage of minimum non-zero pixels in the cropped label')
        #parser.add_argument('--drop_ratio', default=0, help='Probability to drop a cropped area if the label is empty. All empty patches will be dropped for 0 and accept all cropped patches if set to 1')
        parser.add_argument('--batch_size', type=int, default=2, help='batch size')
        parser.add_argument('--patch_size', default=[128, 128, 128], help='Size of the patches extracted from the image')
        parser.add_argument('--img_channel', default=1, type=int, help='Channels of the image')
        parser.add_argument("--stride_inplane", type=int, nargs=1, default=32, help="Stride size in 2D plane (during validation)")
        parser.add_argument("--stride_layer", type=int, nargs=1, default=32, help="Stride size in z direction (during validation)")

        # training parameters
        parser.add_argument('--epoch_count', type=int, default=1, help='the starting epoch count')
        parser.add_argument('--niter', type=int, default=700, help='# of iter at starting learning rate')
        parser.add_argument('--niter_decay', type=int, default=1450, help='# of iter to linearly decay learning rate to zero')
        parser.add_argument('--lr_policy', type=str, default='lambda', help='learning rate policy: lambda|step|plateau|cosine')
        parser.add_argument('--lr_decay_iters', type=int, default=50, help='multiply by a gamma every lr_decay_iters iterations')
        parser.add_argument('--resume', default=0, type=int, help='resume training or not default:0/not')

        # Inference
        # This is just a trick to make the predict script working
        parser.add_argument("-d", "--subject_directory", type=str,
                            help="Subject directory containing the different PET/CT images of the same subject",
                            required=True)


        self.initialized = True
        return parser

    def parse_options(self):
        if not self.initialized:
            parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                            description='ORCA (Optimized Registration through Conditional Adversarial networks) is a ')
            parser = self.initialize(parser)
        opt = parser.parse_args()
        
        # set gpu ids
        if opt.gpu_id != '-1':
            os.environ["CUDA_VISIBLE_DEVICES"] = opt.gpu_id
        return opt





