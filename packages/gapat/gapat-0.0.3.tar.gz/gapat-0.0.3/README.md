# A comprehensive framework of GPU-accelerated image reconstruction for photoacoustic computed tomography

The repository provides code of the paper with the same name as this repository.

> A comprehensive framework of GPU-accelerated image reconstruction for photoacoustic computed tomography.

## Abstract

**Significance**: Photoacoustic Computed Tomography (PACT) is a promising non-invasive imaging technique for both life science and clinical implementations. To achieve fast imaging speed, modern PACT systems have equipped arrays that have hundreds to thousands of ultrasound transducer (UST) elements, and the element number continues to increase. However, large number of UST elements with parallel data acquisition could generate a massive data size, making it very challenging to realize fast image reconstruction. Although several research groups have developed GPU-accelerated method for PACT, there lacks an explicit and feasible step-by-step description of GPU-based algorithms for various hardware platforms.

**Aim**: In this study, we propose a comprehensive framework for developing GPU-accelerated PACT image reconstruction (Gpu-Accelerated PhotoAcoustic computed Tomography, _**GAPAT**_), helping the research society to grasp this advanced image reconstruction method.

**Approach**: We leverage widely accessible open-source parallel computing tools, including Python multiprocessing-based parallelism, Taichi Lang for Python, CUDA, and possible other backends. We demonstrate that our framework promotes significant performance of PACT reconstruction, enabling faster analysis and real-time applications. Besides, we also described how to realize parallel computing on various hardware configurations, including multicore CPU, single GPU, and multiple GPUs platform.

**Results**: Notably, our framework can achieve an effective rate of approximately 871 times when reconstructing extremely large-scale 3D PACT images on a dual-GPU platform compared to a 24-core workstation CPU. Besides this manuscript, we shared example codes in the GitHub.

**Conclusions**: Our approach allows for easy adoption and adaptation by the research community, fostering implementations of PACT for both life science and medicine.

**Keywords**: photoacoustic computed tomography, large-scale data size, GPU-accelerated method, Taichi Lang for python, multiple GPU platform.

## Documentation

### gapat.algorithms

#### `gapat.algorithms.recon(signal_backproj, detector_location, detector_normal, x_range, y_range, z_range, res, vs, fs, delay=0, method="das", device="cpu", num_devices=1, block_dim=512)`

Reconstruction of photoacoustic computed tomography.

**Warning**: When using multi-device reconstruction, the function must be called on the main process.

**Parameters**

| Parameter           | Type         | Description                                                                                                                                    |
| ------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `signal_backproj`   | `np.ndarray` | The input signal. Each row is a signal of a detector.<br>Shape: (num_detectors, num_times). Dtype: np.float32.                                 |
| `detector_location` | `np.ndarray` | The location of the detectors. Each row is the coordinates of a detector.<br>Shape: (num_detectors, 3). Dtype: np.float32.                     |
| `detector_normal`   | `np.ndarray` | The normal of the detectors. Each row is the normal of a detector which points to the volume.<br>Shape: (num_detectors, 3). Dtype: np.float32. |
| `x_range`           | `list`       | The range of the reconstruction volume. The first is the start x and the second is the end x. Example: [0, 1].<br>Shape: (2,). Dtype: float.   |
| `y_range`           | `list`       | The range of the reconstruction volume. The first is the start y and the second is the end y. Example: [0, 1].<br>Shape: (2,). Dtype: float.   |
| `z_range`           | `list`       | The range of the reconstruction volume. The first is the start z and the second is the end z. Example: [0, 1].<br>Shape: (2,). Dtype: float.   |
| `res`               | `float`      | The resolution of the volume.                                                                                                                  |
| `vs`                | `float`      | The speed of sound in the volume.                                                                                                              |
| `fs`                | `float`      | The sampling frequency.                                                                                                                        |
| `delay`             | `int`        | The delay of the detectors. Default: 0.                                                                                                        |
| `method`            | `str`        | The method to use. Default: "das". Options: "das", "ubp".                                                                                      |
| `device`            | `str`        | The device to use. Default: "gpu". Options: "cpu", "gpu".                                                                                      |
| `num_devices`       | `int`        | The number of devices to use. Default: 1.                                                                                                      |
| `block_dim`         | `int`        | The block dimension. Default: 512.                                                                                                             |

**Returns**

| Parameter      | Type         | Description                                                                   |
| -------------- | ------------ | ----------------------------------------------------------------------------- |
| `signal_recon` | `np.ndarray` | The reconstructed signal.<br>Shape: (num_x, num_y, num_z). Dtype: np.float32. |

### gapat.processings

#### `gapat.processings.bandpass_filter(signal_matrix, fs, band_range, order=2, axis=0)`

Bandpass filter the signal matrix.

**Parameters**

| Parameter       | Type         | Description                                                                                                                                               |
| --------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `signal_matrix` | `np.ndarray` | The signal matrix to be filtered.<br>Shape: (num_detectors, num_times). Dtype: np.float32.                                                                |
| `fs`            | `float`      | The sampling frequency (Hz).                                                                                                                              |
| `band_range`    | `list`       | The band range to filter (Hz). The first is the low frequency and the second is the high frequency. Example: [10e6, 100e6].<br>Shape: (2,). Dtype: float. |
| `order`         | `int`        | The order of the filter. Default: 2.                                                                                                                      |
| `axis`          | `int`        | The axis to filter. Default: 0. (Which will be applied to each detector.)                                                                                 |

**Returns**

| Parameter                | Type         | Description                                                                          |
| ------------------------ | ------------ | ------------------------------------------------------------------------------------ |
| `filtered_signal_matrix` | `np.ndarray` | The filtered signal matrix.<br>Shape: (num_detectors, num_times). Dtype: np.float32. |

#### `gapat.processings.negetive_processing(signal_recon, method="zero", axis=0)`

Process the negative signal.

**Parameters**

| Parameter      | Type         | Description                                                                                                                                                                                                                                                                     |
| -------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `signal_recon` | `np.ndarray` | The reconstructed signal to be processed.<br>Shape: (num_x, num_y, num_z). Dtype: np.float32.                                                                                                                                                                                   |
| `method`       | `str`        | The method to process the negative signal. Default: "zero". Options: "zero", "abs", "hilbert".<br>"zero": Set the negative signal to zero.<br>"abs": Take the absolute value of the negative signal.<br>"hilbert": Use the hilbert transform to get the envelope of the signal. |
| `axis`         | `int`        | The axis to process when method is "hilbert". Default: 0.                                                                                                                                                                                                                       |

**Returns**

| Parameter                | Type         | Description                                                                              |
| ------------------------ | ------------ | ---------------------------------------------------------------------------------------- |
| `processed_signal_recon` | `np.ndarray` | The processed signal reconstruction.<br>Shape: (num_x, num_y, num_z). Dtype: np.float32. |

### gapat.utils

#### `gapat.utils.load_mat(filename)`

Load .mat file and return a dictionary with variable names as keys, and loaded matrices as values.

**Parameters**

| Parameter  | Type  | Description                |
| ---------- | ----- | -------------------------- |
| `filename` | `str` | The path to the .mat file. |

**Returns**

| Parameter | Type   | Description                                                              |
| --------- | ------ | ------------------------------------------------------------------------ |
| `data`    | `dict` | A dictionary with variable names as keys, and loaded matrices as values. |

#### `gapat.utils.save_mat(filename, varname, data)`

Save data to .mat file with the given variable name.

**Parameters**

| Parameter  | Type         | Description                            |
| ---------- | ------------ | -------------------------------------- |
| `filename` | `str`        | The path to the .mat file.             |
| `varname`  | `str`        | The variable name to save the data to. |
| `data`     | `np.ndarray` | The data to save.                      |
