![Orca-logo](ORCA_graph.jpg)

## ORCA: Optimized Registration through Conditional Adversarial networks

[![Recommended Version](https://img.shields.io/badge/Recommended-pip%20install%20orcaz%3D%3D0.1.0-9400D3.svg)](https://pypi.org/project/orcaz/0.1.0/) 
[![Monthly Downloads](https://img.shields.io/pypi/dm/orcaz?label=Downloads%20(Monthly)&color=9400D3&style=flat-square&logo=python)](https://pypi.org/project/orcaz/) 
[![Daily Downloads](https://img.shields.io/pypi/dd/orcaz?label=Downloads%20(Daily)&color=9400D3&style=flat-square&logo=python)](https://pypi.org/project/orcaz/)


## **Requirements** ✅

For an optimal experience with ORCA, ensure the following:

- **Operating System**: ORCA runs smoothly on Windows, Mac, or Linux.
- **Memory**: At least 32GB of RAM ensures ORCA operates without a hitch.
- **GPU**: For blazing-fast predictions, an NVIDIA GPU comes highly recommended. But if you don't have one, fret not! ORCA will still get the job done, just at a more leisurely pace.
For training new models, you must have a GPU!
- **Python**: Version 3.9.2 or above. We like to stay updated!

---

## **Installation Guide** 🛠️

Navigating the installation process is a breeze. Just follow the steps below:

**For Linux and MacOS** 🐧🍏
1. Create a Python environment, for example, 'orca-env'.
```bash
python3 -m venv orca-env
```
2. Activate your environment.
```bash
source orca-env/bin/activate  # for Linux
source orca-env/bin/activate  # for MacOS
```
3. Install ORCA.
```bash
pip install orcaz
```

## Usage Guide 📚

### Command-line tool for data folder processing :computer: 

```bash
orcaz -d <path_to_patient_dir> -m <mode>
```

Here `<path_to_patient_dir>` refers to the directory containing your subject's PET and CT images. 
Where `<mode>` is the name of the mode for which we want to use the tool, from the available options. 

`train`: Yes we can !! Orca can be used to train your own models as a generic cGAN paltform. More instructions for that to follow !

`pred `: This option will use orca only to generate a synthetic CT from your PET data. 

`coreg`: Option to generate synethic CT and perform the coregistration pipeline with an output of the co-registered CT. ORCA in its full glory !!

Using ORCA requires your data to be structured according to specific conventions. ORCA supports both DICOM and NIFTI formats. 

### Required Directory Structure 🌳
Please structure your dataset as follows for coregistration:

```
EXAMPLE_Data_folder/
├── S1
│   ├── S1_CT
│   │   ├── xyz_1.dcm
│   │   ├── xyz_2.dcm
│   │   ├── .
│   │   ├── .
│   │   ├── .
│   │   └── xyz_532.dcm
│   └── S1_FDG_NAC_PT
│       ├── xyz_1.dcm
│       ├── xyz_2.dcm
│       ├── .
│       ├── .
│       ├── .
│       └── xyz_532.dcm
├── S2
│   ├── S2_CT
│   │   ├── xyz_1.dcm
│   │   ├── xyz_2.dcm
│   │   ├── .
│   │   ├── .
│   │   ├── .
│   │   └── xyz_532.dcm
│   └── S2_FDG_NAC_PT
│       ├── xyz_1.dcm
│       ├── xyz_2.dcm
│       ├── .
│       ├── .
│       ├── .
│       └── xyz_532.dcm
├── S3
│   ├── S3_CT.nii
│   └── S3_FDG_NAC_PT.nii
├── S4
│   ├── S4_CT.nii.gz
│   └── S4_FDG_NAC_PT.nii.gz
```

In all these cases, ORCA can be executed on the directories one by one

```bash
orcaz -d S1 -m coreg
orcaz -d S2 -m coreg
orcaz -d S3 -m coreg  
```

**Note:** If the necessary naming conventions are not followed, ORCA will not process the data in the directory.


### Naming Conventions for files 📝
There is none! Currently orca requires the naming of the subject subfoders inlcude particular names.
The patient identifier can be placed in the start of each subfolder

For instance, `S1_CT` and `S1_FDG_NAC_PT`, or  `S1_CT` and `S1_FDG_AC_PT`.  
`S2_CT` and `S2_PSMA_NAC_PT`.  
`S3_CT` and `S3_FACBC_NAC_PT`.  
`S4_CT` and `S4_DOTA_NAC_PT`.  
`S5_CT` and `S5_AGNOSTIC_NAC_PT`.  

### Output
After successful completion, the co-registered CT is saved as dicom data in `ORCA_CT_DICOM`.

Intermediate images and warp files are stored within the `ORCA-VXX-YYYY-MM-DD-HH-MM-SS` folder
```
S1
├── CT
├── NAC_FDG_PET
├── ORCA_CT_DICOM
├── ORCA-V01-2023-09-28-00-02-52
```


### Directory Structure for sCT prediction only
The above dataset structure will also work in prediction mode, but the CT directory is not necessary:

For prediction the following is sufficient.
```
EXAMPLE_Data_folder/
├── S1
│   └── S1_FDG_NAC_PT
│       ├── xyz_1.dcm
│       ├── xyz_2.dcm
│       ├── .
│       ├── .
│       ├── .
│       └── xyz_532.dcm
├── S2
│   └── S2_FDG_NAC_PT
│       ├── xyz_1.dcm
│       ├── xyz_2.dcm
│       ├── .
│       ├── .
│       ├── .
│       └── xyz_532.dcm
├── S3
│   └── S3_FDG_NAC_PT.nii
```

In all these cases, ORCA can be executed to generate sCT on the directories one by one

```bash
orcaz -d S1 -m pred
orcaz -d S2 -m pred
orcaz -d S3 -m pred  
```

