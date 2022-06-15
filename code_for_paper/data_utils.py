import pandas as pd
import pyarrow
import pyarrow.parquet as parquet
import os
from scipy import interpolate,signal
import numpy as np

def butter_data_path():
    return os.getenv("DMP_BUTTER_DATA_DIR", "s3://oedi-data-lake/butter")

def get_s3_filesystem():
    import s3fs
    import botocore
    return s3fs.S3FileSystem(config_kwargs={"signature_version": botocore.UNSIGNED})

def read_pandas(sweep, filters, columns):
    # Get path from environment. Default is OEDI data lake.
    path = butter_data_path()
    
    # Clean up path (trim filesystem identifier) and create filesystem objects
    if path[:5]=="s3://":
        fs = get_s3_filesystem()
        path = path[5:] + "/" + sweep
        schema_fp = fs.open(f'{path}/_common_metadata')
    else:
        fs = None
        path = path+"/"+sweep
        schema_fp = open(f'{path}/_common_metadata', 'rb')
    
    # Read schema data from _common_metadata file
    schema = parquet.read_schema(schema_fp)
    schema_fp.close()

    # Read parquet table
    table = parquet.read_table(path, filesystem=fs, filters=filters, schema=schema, columns=columns)

    # Convert to pandas
    return table.to_pandas()

partition_cols = [
    'dataset',
    'learning_rate',
    'batch_size',
    'kernel_regularizer.type',
    'label_noise',
    'epochs',
    'shape',
    'depth',
]

def make_interpolator(x, y, kind='linear',  fill_value='extrapolate'):
    return interpolate.interp1d(
        x, y, kind=kind, fill_value=fill_value)

def resample_data(x, y, x_resampled, kind='linear', fill_value='extrapolate'):
    interpolator = make_interpolator(x, y, kind=kind, fill_value=fill_value)
    # x_resampled = np.linspace(np.min(x), np.max(x), num_points, endpoint=True) + x_offset
    return x_resampled, interpolator(x_resampled)

def filter_log_loss(log_epoch, log_loss, x_resampled, window=101, polyorder=1):
    x, y = resample_data(log_epoch, log_loss, x_resampled)
    smooth_log_epoch, smooth_log_val_loss = \
                signal.savgol_filter((x, y), window, polyorder)
    return smooth_log_epoch, smooth_log_val_loss

def equation_1(log_size,m,b):
    """
    This is just a linear function, but the output will be transformed using np.power(y,-3)
    """
    return m*log_size + b
    
def equation_2(log_size,c,p,sigma_0,phi):
    return c*np.power(log_size - sigma_0, -p) + phi

def equation_3(log_size,l,sigma_1,alpha_0):
    return -l*np.power(log_size - sigma_1, 2) + alpha_0