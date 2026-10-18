
# AstronomyWeather

An Android client prototype for displaying weather visualizations to support astrophotography planning.

The app is part of a small project ecosystem exploring how weather observations from the German Weather Service (DWD) can be retrieved by a backend and presented on a mobile device.

## Features

- Android UI built with Jetpack Compose and Material 3
- Background image fetching using Android WorkManager
- HTTP communication with a companion weather backend
- Local caching of downloaded weather plots

## Tech Stack

- **Language:** Kotlin
- **UI:** Jetpack Compose, Material 3
- **Background tasks:** Android WorkManager
- **Networking:** OkHttp
- **Backend:** Python, Flask
- **Weather data:** DWD via `wetterdienst`

## Related Projects

- [AstronomyWeatherBackend](https://github.com/crizzzly/AstronomyWeatherBackend) — retrieves weather observations and serves visualizations
- [CS-Warn](https://github.com/crizzzly/CS-Warn) — Python Telegram bot for astronomy weather monitoring

## Project Status

Prototype. The application and its integration with the backend have not been verified as a complete, reproducible setup.
