#ifndef CIL_H
#define CIL_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdlib.h>
#include <stdint.h>

/** @brief Supported input image color formats. */
typedef enum {
    IMAGE_COLOR_RGB,
    IMAGE_COLOR_BGR,
    IMAGE_COLOR_GRAYSCALE,
    IMAGE_COLOR_YUV
} image_color_format_t;

/** @brief Supported tensor layout formats. */
typedef enum {
    NHWC,
    NCHW
} image_input_format_t;

/** @brief Status codes returned by preprocessing and postprocessing. */
typedef enum {
    STATUS_OK = 0,
    STATUS_ERROR = -1,
    STATUS_NO_MEMORY = -2,
    STATUS_INVALID_ARG = -3
} status_t;

/** @brief Data type for model inputs or outputs. */
typedef enum {
    DATATYPE_FLOAT32,
    DATATYPE_INT8
}datatype_t;

/** @brief Single detection with bounding box, score, and class id. */
typedef struct {
    uint16_t class_id;
    float score;
    uint16_t x1, y1, x2, y2;
} detection_t;

/** @brief Output data structure for postprocess results. */
typedef struct {
    float max_confidence;
    int   detected_class_index;
    
    detection_t* detections;
    int detection_count;

    int max_detections;

    float score_threshold;
    float iou_threshold;
    
    float scale;
    int zero_point;
    
    int original_width;   
    int original_height;
} postprocess_data_t;

/**
 * @brief Preprocess raw image data for model input.
 *
 * @param image_data Pointer to input image bytes.
 * @param image_width Width of the input image in pixels.
 * @param image_height Height of the input image in pixels.
 * @param preprocessed_data Output buffer for model input tensor.
 * @param preprocess_arena Working memory buffer used by preprocessing.
 * @param input_image_color_format Color format of the input image.
 * @param image_format Tensor layout format expected by the model (NHWC or NCHW).
 * @return status_t Status code indicating success or failure.
 */
status_t preprocess(const uint8_t *image_data,
                uint32_t image_width,
                uint32_t image_height,
                void *preprocessed_data,
                uint8_t* preprocess_arena,
                image_color_format_t input_image_color_format,
                image_input_format_t image_format);

/**
 * @brief Compute arena size required for preprocessing.
 *
 * @param image_width Width of the input image in pixels.
 * @param image_height Height of the input image in pixels.
 * @param model_input_width Model input width in pixels.
 * @param model_input_height Model input height in pixels.
 * @param input_image_color_format Color format of the input image.
 * @return int Required arena size in bytes.
 */
int preprocess_arena_space(int image_width, int image_height,
                           int model_input_width, int model_input_height,
                           image_color_format_t input_image_color_format);

/**
 * @brief Postprocess inference output into structured results.
 *
 * @param inference_result Pointer to raw model output.
 * @param result Output structure populated with postprocess data.
 * @return status_t Status code indicating success or failure.
 */
status_t postprocess(void *inference_result,
                postprocess_data_t* result);

#ifdef __cplusplus
}
#endif

#endif
