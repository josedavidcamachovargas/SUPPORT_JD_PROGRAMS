# Content Policy Violation Handling

## Overview

The Activity Selector now includes automatic handling for OpenAI content policy violations during image generation. When the AI detects that a prompt may violate safety guidelines, the application automatically retries with a sanitized, generic prompt.

## How It Works

### Normal Flow
1. **Get Description**: ChatGPT generates a family-friendly description of the activity
2. **Build Prompt**: Creates a detailed image prompt based on the description
3. **Generate Image**: DALL-E 3 generates the image
4. **Cache & Display**: Image is cached and displayed to the user

### Fallback Flow (Content Policy Violation)
1. **Policy Violation Detected**: DALL-E rejects the prompt due to safety concerns
2. **Automatic Retry**: System logs the issue and retries immediately
3. **Generic Prompt**: Uses a safe, generic prompt without specific content references
4. **Generate Image**: DALL-E generates a generic but thematically appropriate image
5. **Cache & Display**: Generic image is cached and displayed

## Example

### Original Prompt (Rejected)
```
A cinematic scene inspired by the film 'Terminator'. 
In "Terminator," a cyborg assassin from the future travels 
back in time to eliminate Sarah Connor...
```

### Fallback Prompt (Accepted)
```
A cinematic movie poster in vibrant digital art style. 
Professional illustration showing an exciting adventure scene 
with dramatic lighting. Family-friendly, artistic, colorful 
composition suitable for all ages.
```

## Benefits

- ✅ **No Manual Intervention**: Automatic retry without user interaction
- ✅ **Always Gets Image**: Even with policy violations, user gets a relevant image
- ✅ **Maintains Experience**: App continues smoothly without errors
- ✅ **Clear Logging**: Console shows when fallback is used

## Implementation Details

### Code Location
`services/image_service.py` → `_generate_dalle_image()` method

### Key Changes
1. **Try-Catch Block**: Wraps image generation call
2. **Error Detection**: Checks for `content_policy_violation` in error message
3. **Fallback Method**: `_build_safe_fallback_prompt()` creates generic prompts
4. **Logging**: Prints fallback usage to console

### Fallback Prompts by Category

**Movies**
- Generic cinematic scene
- Dramatic lighting
- Adventure theme
- Family-friendly

**TV Series**
- Promotional poster style
- Engaging characters
- Story-driven composition
- All-audience appropriate

**Video Games**
- Game cover art style
- Dynamic action scene
- Colorful design
- Family-friendly

**Other Activities**
- Generic artistic illustration
- Vibrant colors
- Professional quality

## Error Messages

### Before (Failed Generation)
```
Error generating image: OpenAI API error: Error code: 400 - 
{'error': {'message': 'Your request was rejected as a result 
of our safety system...', 'type': 'image_generation_user_error', 
'code': 'content_policy_violation'}}
```

### After (Successful Fallback)
```
Generated description: [original description]
Image prompt: [original prompt]
Content policy violation detected. Retrying with sanitized prompt...
Fallback prompt: [generic safe prompt]
[Image successfully generated and displayed]
```

## Configuration

No additional configuration needed. The system works automatically with your existing settings:

- Uses your configured `image_style` setting
- Maintains cache behavior
- Works with all activity categories

## Testing

To test the fallback mechanism:

1. Try activities with potentially sensitive content (action movies, etc.)
2. Check console output for "Content policy violation detected"
3. Verify a generic but appropriate image is still generated
4. Confirm image is cached for future use

## Future Improvements

Potential enhancements:
- [ ] More sophisticated fallback prompts per activity
- [ ] User notification when fallback is used
- [ ] Retry with slightly modified original prompt before full fallback
- [ ] Category-specific safety filters

## Related Files

- `services/image_service.py` - Main implementation
- `utils/constants.py` - Configuration constants
- `TROUBLESHOOTING.md` - General error handling guide

---

**Last Updated**: November 7, 2025  
**Version**: 2.0.0
