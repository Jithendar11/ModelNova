# Common Inference Library (CIL)

## Overview

The **Common Inference Library (CIL)** provides a unified interface for
**pre-processing** and **post-processing** of AI models such as **Image
Classification** and **Object Detection**.

Instead of writing model-specific processing code in every application,
CIL exposes two common APIs:

- `preprocess()`
- `postprocess()`

Based on the configured model, these APIs automatically invoke the
required internal processing functions.

---

## Components

| File | Description |
|---|---|
| `cil_process.a` | Prebuilt static library implementing pre-processing (resize, normalize, quantize) and post-processing (decode, NMS, format). Configured at build time for the target model category. |
| `cil_helper.h` | Public C API header. Provides `preprocess()`, `postprocess()`, and data structures (`detection_t`, `postprocess_data_t`). |
| `model_config.h` | Auto-generated header with model parameters - input dimensions (`MODEL_INPUT_WIDTH/HEIGHT/CHANNELS`), quantization scale/zero point, number of classes, labels, confidence threshold, and model category (`OBJECT_DETECTION` / `IMAGE_CLASSIFICATION`). |

The AI Layer (runner code in the board's `algorithm/` folder) ties these together
by calling the CIL APIs and delivering results through the SDS framework.

---

## Examples

For a **Image Classification** model:

**Preprocess** - Resize image, ImageNet normalization, tensor formatting  
**Postprocess** - Softmax, argmax, confidence score

For an **Object Detection** model:

**Preprocess** - Resize / letterbox, quantization (if required)  
**Postprocess** - Bounding box decoding, Non-Maximum Suppression (NMS), detection result formatting

---

## Benefits

- Common API for multiple AI models
- Eliminates duplicate processing code
- Easy integration of new models
- Simplifies application development
- Modular and reusable design

---

## Typical Flow

```
Input Image
     │
     ▼
preprocess()
     │
Model Inference
     │
     ▼
postprocess()
     │
Application Result
```

The application only calls the common APIs, while CIL internally
performs the model-specific preprocessing and postprocessing steps.
 