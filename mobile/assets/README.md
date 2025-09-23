# Customising Expo Assets

This directory intentionally stores only documentation so that the repository avoids bundling binary image files, which are not supported by the target submission system.

To personalise the Expo application icon or splash screen:

1. Add your PNG assets (recommended square icon at 1024×1024 and splash image at 2048×2048) into this folder.
2. Update `app.json` to point to your filenames. For example:
   ```json
   {
     "expo": {
       "icon": "./assets/icon.png",
       "splash": {
         "image": "./assets/splash.png",
         "resizeMode": "contain",
         "backgroundColor": "#0f172a"
       }
     }
   }
   ```
3. Rebuild or restart the Expo development server so the new assets are picked up.

If you skip these steps, Expo will use its default icon and splash visuals, which is sufficient for development and automated testing.
