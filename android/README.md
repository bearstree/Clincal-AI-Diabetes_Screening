# Android client

Open this folder in current Android Studio and use JDK 17 / Android SDK 37. The debug build calls `http://10.0.2.2:8000` from the emulator; only the debug manifest permits cleartext traffic. For a release build, provide the deployed HTTPS URL:

```powershell
gradle :app:assembleRelease -PclinicalApiBaseUrl=https://YOUR-SPACE.hf.space
```

The app requests only Internet access, stores no health inputs or predictions, and sends the same four fields shown on screen.
