#ifndef MODEL_CONFIG_H
#define MODEL_CONFIG_H

#ifdef __cplusplus
extern "C" {
#endif

/* Model Configuration */
#define MODEL_NUM_CLASSES        (4)
#define MODEL_CONF_THRESHOLD     (0.5f)
#define MODEL_INPUT_SCALE        (0.0f)
#define MODEL_INPUT_ZERO_POINT   (0)
#define MODEL_OUTPUT_SCALE       (0.0f)
#define MODEL_OUTPUT_ZERO_POINT  (0)
#define MODEL_INPUT_IS_INT8      (0)
#define MODEL_INPUT_WIDTH        (224)
#define MODEL_INPUT_HEIGHT       (224)
#define MODEL_INPUT_CHANNELS     (3)

/* Class Labels */
static const char * const MODEL_LABELS[MODEL_NUM_CLASSES] =
{
    "PAPER",
    "ROCK",
    "SCISSORS",
    "UNKNOWN",
};

#ifdef __cplusplus
}
#endif

#endif /* MODEL_CONFIG_H */
 